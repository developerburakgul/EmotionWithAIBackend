from dataclasses import dataclass
from typing import List

from Models.TimeGroup import TimeGroup


@dataclass
class SenderGroup:
    sender: str
    time_groups: List[TimeGroup]