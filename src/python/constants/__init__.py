from typing import NewType

RoleId = NewType("RoleId", int)
TargetTypeId = NewType("TargetTypeId", int)
SpawnPriorityId = NewType("SpawnPriorityId", int)

BodyTypeId = NewType("BodyTypeId", int)

SpawnIdeaKey = NewType("SpawnIdeaKey", str)

TopLevelMemoryId = NewType("TopLevelMemoryId", str)
SecondLevelMemoryKey = NewType("SecondLevelMemoryKey", str)

InnerProcessMemKey = NewType("InnerProcessMemKey", str)

TaskId = NewType("TaskId", int)
ProcessTypeId = NewType("ProcessTypeId", int)
MessageTypeId = NewType("MessageTypeId", int)
ProcessId = NewType("ProcessId", str)
