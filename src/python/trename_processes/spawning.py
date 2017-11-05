from typing import Optional, Tuple

from constants import InnerProcessMemKey
from constants.processes import ptid_spawning
from defs import *
from meta.process_base import CreepSpawnInfo, HasCreeps, HasHome, HasMemory, Process
from meta.registry_exports import Exports
from providers import ordered_structures
from trename_processes.economy import Econ
from utilities import names, warnings
from utilities.infos import Log

key_cached_next_spawn = InnerProcessMemKey("n")
key_cache_expiry = InnerProcessMemKey("e")

log = Log("process: spawning")


class RoomSpawning(HasHome, HasMemory):
    ptid = ptid_spawning

    energy = 0

    def run(self) -> None:
        spawns = ordered_structures.spawns_in(self.room_name())

        self.energy = self.room().energyAvailable
        log.trace("spawning with (energy: {}, spawns: {})", self.energy, spawns)
        for spawn in spawns:
            self.run_spawn(spawn)

    def run_spawn(self, spawn: StructureSpawn) -> None:
        if spawn.spawning:
            log.trace("skipping spawn {}: spawning", spawn.name)
            return

        needed = self.get_next_needed_role()
        log.trace("found needed: {}", needed)
        if not needed:
            return
        cost = _.sum(needed.base, lambda p: BODYPART_COST[p])
        if cost <= self.energy:
            process = self.kernel.get_instance(needed.pid)
            if not process or not isinstance(process, HasCreeps):
                log.warning("canceling spawn for process {}: process no longer exists.".format(needed.pid))
                del self.memory()[key_cached_next_spawn]
                return
            name = names.create_name_excluding_keys_to(Game.creeps)
            result = spawn.spawnCreep(needed.base, name)
            if result == OK:
                process.claim_spawned_creep(name)
                del self.memory()[key_cached_next_spawn]
                self.energy -= cost
            else:
                log.warning("got non-OK result from (spawn {}).spawnCreep({}, {}): {}"
                            .format(spawn, needed.base, name, warnings.transform_error_code(result)))

        return None

    def get_next_needed_role(self) -> Optional[CreepSpawnInfo]:
        mem = self.memory()
        if key_cached_next_spawn in mem and mem[key_cache_expiry] > Game.time:
            log.trace("using cached needed role")
            serialized = mem[key_cached_next_spawn]
            if serialized is None:
                return None
            else:
                return CreepSpawnInfo.deserialize(serialized)
        else:
            expire, info = self.find_new_role_needed()
            mem[key_cached_next_spawn] = info
            mem[key_cache_expiry] = expire
            return None

    def find_new_role_needed(self) -> Tuple[int, Optional[CreepSpawnInfo]]:
        log.trace("finding new role needed")
        room = self  # type: Process
        while not isinstance(room, Econ):
            next_pid = self.kernel.get_parent_of(room.pid)
            if next_pid is None:
                raise ValueError("spawning process isn't a child of an econ process...")
            room = self.kernel.get_instance(next_pid)

        log.trace("found room pid: {}", room.pid)

        next_expire = Game.time + CREEP_LIFE_TIME
        # TODO: sorted order here...
        info = None

        def walk_tree_from(process: Process) -> None:
            nonlocal info, next_expire
            if info is not None:
                return
            if isinstance(process, HasCreeps):
                log.info("asking {} for info", process.pid)
                info = process.get_needed_creep()
                next_expire = min(next_expire, process.get_next_expire())
            for pid in self.kernel.get_children_of(process.pid):
                walk_tree_from(self.kernel.get_instance(pid))

        walk_tree_from(room)

        return next_expire, info


exports = Exports().process(RoomSpawning)
