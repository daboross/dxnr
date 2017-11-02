from typing import Any, Callable, Dict, TYPE_CHECKING

from constants import MessageTypeId, ProcessId, ProcessTypeId
from meta.tasks import Schedule
from utilities import warnings

if TYPE_CHECKING:
    # TODO: make Transcrypt ignore type-only imports
    from core.kernel import Kernel


class ProcessType:
    def __init__(self,
                 process_type_id: ProcessTypeId,
                 run: Callable[[ProcessId, Kernel], None]) -> None:
        self.process_type_id = process_type_id
        self.run = run
        self.schedule = Schedule.always()
        self.message_handlers = {}  # type: Dict[MessageTypeId, Callable[[ProcessId, Kernel, ProcessId, Any], None]]

    def set_schedule(self, schedule: Schedule) -> 'ProcessType':
        self.schedule = schedule
        return self

    def message(self,
                mtid: MessageTypeId,
                handler: Callable[[ProcessId, Kernel, ProcessId, Any], None]) -> 'ProcessType':
        if mtid in self.message_handlers:
            warnings.repeated_registration("message handler in ptid '{}'".format(self.process_type_id), mtid)
        self.message_handlers[mtid] = handler
        return self
