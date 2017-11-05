from typing import NewType

TargetTypeId = NewType("TargetTypeId", int)
SpawnPriorityId = NewType("SpawnPriorityId", int)

TopLevelMemoryId = NewType("TopLevelMemoryId", str)
SecondLevelMemoryKey = NewType("SecondLevelMemoryKey", str)

InnerProcessMemKey = NewType("InnerProcessMemKey", str)

ProcessTypeId = NewType("ProcessTypeId", int)
ProcessId = NewType("ProcessId", str)
