from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class Event:
    x: float
    point: Point
    arc: 'Arc'
    is_valid: bool = True


@dataclass
class Arc:
    point: Point
    prev: Optional['Arc'] = None
    next: Optional['Arc'] = None
    event: Optional[Event] = None
    first_segment: Optional['Segment'] = None
    second_segment: Optional['Segment'] = None


@dataclass
class Segment:
    start: Point
    end: Optional[Point] = None
