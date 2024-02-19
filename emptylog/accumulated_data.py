from dataclasses import dataclass, field
from typing import List

from emptylog.call_data import LoggerCallData


@dataclass
class LoggerAccumulatedData:
    debug: List[LoggerCallData] = field(default_factory=list)
    info: List[LoggerCallData] = field(default_factory=list)
    warning: List[LoggerCallData] = field(default_factory=list)
    error: List[LoggerCallData] = field(default_factory=list)
    exception: List[LoggerCallData] = field(default_factory=list)
    critical: List[LoggerCallData] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.debug) + len(self.info) + len(self.warning) + len(self.error) + len(self.exception) + len(self.critical)
