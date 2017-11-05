from typing import Any, Dict, List, Optional, Tuple, Type, cast

from constants import InnerProcessMemKey, ProcessId, ProcessTypeId, SecondLevelMemoryKey
from constants.memkeys import key_memory_core, key_memory_process
from constants.processes import ptid_bootup
from defs import *
from meta.process_base import Process
from providers import exp_memory, registry
from utilities import errors, names, warnings
from utilities.infos import Log

key_kernel_process_table = SecondLevelMemoryKey('p')
key_kernel_child_table = SecondLevelMemoryKey('t')

__pragma__('skip')
_ProcessTable = Dict[ProcessId, Tuple[ProcessTypeId, Optional[ProcessId], List[ProcessId]]]
_InstanceTable = Dict[ProcessId, Process]
__pragma__('noskip')

log = Log("kernel")


class Kernel:
    def __init__(self) -> None:
        self._known_processes = registry.get().process_types
        self._core_memory = exp_memory.top_level_mem(key_memory_core)
        self._process_table = self._core_memory[key_kernel_process_table]  # type: _ProcessTable
        self._instantiated_processes = {}  # type: _InstanceTable
        if not self._process_table:
            self._process_table = {}  # type: _ProcessTable
            self._core_memory[key_kernel_process_table] = self._process_table
        self._process_memory = cast(Dict[ProcessId, Dict[InnerProcessMemKey, _MemoryValue]],
                                    exp_memory.top_level_mem(key_memory_process))

    def _add_child(self, from_pid: ProcessId, pid: ProcessId) -> None:
        process_info = self._process_table[from_pid]
        process_info[2].append(pid)

    def _remove_child(self, from_pid: ProcessId, pid: ProcessId) -> None:
        process_info = self._process_table[from_pid]
        process_children = process_info[2]
        if not process_children:
            raise ValueError("_remove_child(): {} has no children.".format(from_pid))
        process_children.remove(pid)

    def _get_children(self, from_pid: ProcessId) -> List[ProcessId]:
        return self._process_table[from_pid][2]

    def get_process_definition(self, ptid: ProcessTypeId) -> Type[Process]:
        process_type = self._known_processes[ptid]
        if not process_type:
            raise ValueError("get_process_definition(): invalid process type id: '{}'.".format(ptid))
        return process_type

    def process_memory(self, pid: ProcessId) -> Dict[InnerProcessMemKey, _MemoryValue]:
        memory = self._process_memory[pid]
        if not memory:
            memory = {}
            self._process_memory[pid] = memory
        return memory

    def spawn(self, from_pid: ProcessId, ptid: ProcessTypeId, *parameters: Any) -> ProcessId:
        """
        Spawns a new process!

        :param from_pid: The parent of this process
        :param ptid: The type of this process
        :param parameters: Any additional parameters.
        :return: The newly spawned process's process id.
        """
        log.trace("spawning child: (from_pid: {}, ptid: {}, *parameters: {})", from_pid, ptid, parameters)
        if not ptid:
            raise ValueError("spawn(): invalid process type: '{}'.".format(ptid))
        pid = ProcessId(names.create_name_excluding_keys_to(self._process_table))
        self._process_table[pid] = (ptid, from_pid, [])

        if from_pid is not None:
            self._add_child(from_pid, pid)

        instance = self.get_process_definition(ptid)(pid, self)
        self._instantiated_processes[pid] = instance
        instance.init(*parameters)

        return pid

    def kill(self, pid: ProcessId) -> None:
        """
        Removes the given process and all its children from the process tree.
        """
        log.trace("killing process: (pid: {})", pid)
        process_info = self._process_table[pid]
        if not process_info:
            raise ValueError("kill(): invalid process id: '{}'.".format(pid))

        for child_pid in process_info[2]:
            self.kill(child_pid)

        if pid in self._instantiated_processes:
            self._instantiated_processes[pid].died()

        del self._process_memory[pid]

        del self._process_table[pid]

    def is_process_alive(self, pid: ProcessId) -> bool:
        return pid in self._process_table

    def get_parent_of(self, pid: ProcessId) -> Optional[ProcessId]:
        return self._process_table[pid][1]

    def get_children_of(self, pid: ProcessId) -> List[ProcessId]:
        return self._get_children(pid)

    def get_instance(self, pid: ProcessId) -> Optional[Process]:
        return self._instantiated_processes[pid]

    def _run_process(self, pid: ProcessId) -> None:
        instance = self._instantiated_processes[pid]
        log.trace("running process: (pid: {}, instance: {})", pid, instance.__class__.__name__)
        if not instance:
            return

        def run() -> None:
            instance.run()

        errors.execute_catching(run,
                                lambda: "error running process (type: '{}', id: '{}')".format(instance.ptid, pid),
                                pid, self)

    def instantiate_processes(self) -> None:
        for pid in Object.keys(self._process_table):
            if pid not in self._process_table:
                log.debug("skipping process instantiation: (pid: {}, reason: no longer alive)", pid)
                continue
            ptid = self._process_table[pid][0]

            definition = self.get_process_definition(ptid)
            if not definition:
                warnings.warn("run_process(): invalid process type: '{}'. Killing '{}'.".format(ptid, pid))
                self.kill(pid)
            self._instantiated_processes[pid] = definition(pid, self)

    def run(self) -> None:
        pids_to_run = Object.keys(self._process_table)

        if not len(self._process_table):
            log.info("no processes: starting bootup")
            self.spawn(None, ptid_bootup)

        for pid in pids_to_run:
            self._run_process(pid)
