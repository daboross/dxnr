from typing import Any, Dict, List, cast

from constants import InnerProcessMemKey, MessageTypeId, ProcessId, ProcessTypeId, SecondLevelMemoryKey
from constants.memkeys import key_memory_core, key_memory_process
from constants.processes import ptid_bootup
from core.process_type import ProcessType
from defs import *
from providers import exp_memory, registry
from utilities import errors, infos, names, warnings

key_kernel_process_table = SecondLevelMemoryKey('p')
key_kernel_child_table = SecondLevelMemoryKey('t')

section = "kernel"

_ProcessTable = Dict[ProcessId, ProcessTypeId]
_ChildTable = Dict[ProcessId, Dict[ProcessTypeId, List[ProcessId]]]
_ParentTable = Dict[ProcessId, ProcessId]

class Kernel:
    def __init__(self) -> None:
        self._known_processes = registry.get().process_types
        self._core_memory = exp_memory.top_level_mem(key_memory_core)
        self._process_table = self._core_memory[key_kernel_process_table]  # type: _ProcessTable
        self._child_table = self._core_memory[key_kernel_child_table]  # type: _ChildTable
        if not self._process_table:
            self._process_table = {}  # type: _ProcessTable
            self._core_memory[key_kernel_process_table] = self._process_table
        if not self._child_table:
            self._child_table = {}  # type: _ChildTable
            self._core_memory[key_kernel_child_table] = self._child_table
        self._process_memory = cast(Dict[ProcessId, Dict[InnerProcessMemKey, _MemoryValue]],
                                    exp_memory.top_level_mem(key_memory_process))

    def _add_child(self, from_pid: ProcessId, ptid: ProcessTypeId, pid: ProcessId) -> None:
        process_children = self._child_table[from_pid]
        if not process_children:
            self._child_table[from_pid] = process_children = {}
        process_children_categorized = process_children[ptid]
        if not process_children_categorized:
            process_children_categorized = process_children[ptid] = []

        process_children_categorized.append(pid)

    def _remove_child(self, from_pid: ProcessId, ptid: ProcessTypeId, pid: ProcessId) -> None:
        process_children = self._child_table[from_pid]
        if not process_children:
            raise ValueError("_remove_child(): {} has no children.".format(from_pid))
        process_children_categorized = process_children[ptid]
        if not process_children_categorized:
            raise ValueError("_remove_child(): {} has no children of type {}.".format(from_pid, ptid))

        process_children_categorized.remove(pid)
        if not len(process_children_categorized):
            del process_children[ptid]
        if not len(process_children):
            del self._child_table[from_pid]

    def _get_ro_children(self, from_pid: ProcessId, ptid: ProcessTypeId) -> List[ProcessId]:
        process_children = self._child_table[from_pid]
        if not process_children:
            return []
        process_children_categorized = process_children[ptid]
        if process_children_categorized:
            return process_children_categorized
        else:
            return []

    def get_process_definition(self, ptid: ProcessTypeId) -> ProcessType:
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

    def spawn(self, from_pid: ProcessId, ptid: ProcessTypeId) -> ProcessId:
        if not ptid:
            raise ValueError("spawn(): invalid process type: '{}'.".format(ptid))
        pid = ProcessId(names.create_name_excluding_keys_to(self._process_table))
        self._process_table[pid] = ptid

        self._add_child(from_pid, ptid, pid)

        return pid

    def get_or_spawn_child(self, from_pid: ProcessId, ptid: ProcessTypeId):
        children = self._get_ro_children(from_pid, ptid)
        if len(children):
            return _.sample(children)
        else:
            return self.spawn(from_pid, ptid)


    def kill(self, pid: ProcessId) -> None:
        process_type = self._process_table[pid]
        if not process_type:
            raise ValueError("kill(): invalid process id: '{}'.".format(pid))

        # TODO: kill hooks

        del self._process_table[pid]

    def message(self, from_pid: ProcessId, message_type: MessageTypeId, target_pid: ProcessId, contents: Any) -> None:
        target_ptid = self._process_table[target_pid]
        target_process = self.get_process_definition(target_ptid)

        handler = target_process.message_handlers[message_type]
        if not handler:
            raise ValueError("message(): ptid not prepared to handle type {} messages: {}."
                             .format(message_type, target_ptid))

        handler(target_pid, self, from_pid, contents)

    # TODO:
    # def message_any(self, from_pid: ProcessId, message_type: MessageTypeId, contents: Any) -> None:
    #     all_handles = self._known_message_handler_types[message_type]
    #     if not all_handles or not len(all_handles):
    #         raise ValueError("message_any(): no handlers prepared to handle mtid: '{}'.".format(message_type))
    #
    #     self.message(from_pid, message_type, _.sample(all_handles), contents)
    #
    # def message_all(self, from_pid: ProcessId, message_type: MessageTypeId, contents: Any) -> None:
    #     all_handles = self._known_message_handler_types[message_type]
    #     if not all_handles or not len(all_handles):
    #         return
    #
    #     for ptid in all_handles:
    #         self.message(from_pid, message_type, ptid, contents)

    def _run_process(self, pid: ProcessId) -> None:
        ptid = self._process_table[pid]

        definition = self.get_process_definition(ptid)
        if not definition:
            warnings.warn("run_process(): invalid process type: '{}'. Killing '{}'.".format(ptid, pid))
            self.kill(pid)

        errors.execute_catching(definition.run,
                                lambda: "error running process (type: '{}', id: '{}')".format(ptid, pid),
                                pid, self)

    def run(self) -> None:
        pids_to_run = Object.keys(self._process_table)

        if not len(self._process_table):
            infos.log(section, "no processes: starting bootup")
            self.spawn(ptid_bootup)

        for pid in pids_to_run:
            self._run_process(pid)
