High-level structure
====================


`dxnr` is Screeps AI - and as all Screeps AIs do, it controls many different things. `dxnr` _almost_ fits the 
"Operating System" model, but it has a few key differences.

### Processes

In `dxnr`, each thing running is a **process**. Each process has a **process id**, a **parent** and a number of 
**children**.

The **kernel** keeps track of all different processes. In general, it does three things:

- Runs each process once each tick
- Allows spawning a process from a given parent
- Allows killing a process and all children
- Allows "walking" the process tree starting at a given process id, seeing all children of that process

Each process runs once per tick, has a memory dedicated to it, and not much beyond that.

Spawning of creeps is handled by a spawn process knowing the room that it's responsible for, and walking the room's
process tree looking for all spawns needed by processes.

While some screeps AIs choose to mirror operating system structures as accurately as possible, `dxnr` makes this a
specific non-goal. This may not be maintainable, but it also may be more maintainable. Only way to know for sure is to
try! 

The main difference from a classic OS architecture is how inter-process communication works. In a classic OS, system
services such as shared memory or delayed message passing handle communication. In dxnr, a process can directly walk the
process tree and call methods on the processes it finds.

### Providers

While processes are great, they aren't the only thing we need. Processes handle storing state, making decisions, and
doing actions. Processes are retained and smart.

Providers, on the other hand, provide information. They're re-instantiated each tick, store no state, and make no
decisions. Instead, they just do raw processing on game information and make the results available to any processes
which need it.

Providers are _not lazy_. That is to say, they will _always_ do their processing, whether or not any process needs it
during a given tick. I'm not sure whether this is good or bad, we'll have to see as `dxnr` advances.

### Utilities

The last section of code is utilities. Like providers, these don't make decisions, and only provide information.

Unlike utilities, they have no state, not even during a tick. Instead, utilities just provide one-off functions to
do calculations.

They may interact with the game state, and may take information from the game state - but the key idea is that they
don't ever cache any state.