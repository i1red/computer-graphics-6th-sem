from typing import List

from data_types import Point, Event, Arc, Segment
from priority_queue import PriorityQueue
from utils import get_circle, get_intersection, get_arc_intersection, get_bounding_box


def voronoi(points: List[Point]) -> List[Segment]:
    return FortuneAlgorithm(points).find_voronoi_diagram()


class FortuneAlgorithm:
    def __init__(self, points: List[Point]) -> None:
        self._voronoi_diagram = []
        self._arc = None

        self._points = PriorityQueue()
        self._events = PriorityQueue()

        for point in points:
            self._points.push(point, point.x)

        min_x, max_x, min_y, max_y = get_bounding_box(points)
        self._min_x = min_x
        self._max_x = max_x
        self._min_y = min_y
        self._max_y = max_y

    def find_voronoi_diagram(self) -> List[Segment]:
        while self._points:
            if self._events and self._events.top().x <= self._points.top().x:
                self._process_event()
            else:
                self._process_point()

        while self._events:
            self._process_event()

        self._close_segments()
        return self._voronoi_diagram

    def _process_point(self) -> None:
        self._insert_arc(self._points.pop())

    def _process_event(self) -> None:
        # get next event from circle pq
        event = self._events.pop()

        if event.is_valid:
            # start new edge
            segment = Segment(event.point)
            self._voronoi_diagram.append(segment)

            # remove associated arc (parabola)
            arc = event.arc
            if arc.prev is not None:
                arc.prev.next, arc.prev.second_segment = arc.next, segment
            if arc.next is not None:
                arc.next.prev, arc.next.first_segment = arc.prev, segment

            # finish the edges before and after arc
            if arc.first_segment is not None:
                arc.first_segment.end = event.point
            if arc.second_segment is not None:
                arc.second_segment.end = event.point

            # recheck circle events on either side of p
            if arc.prev is not None:
                self._check_circle_event(arc.prev)
            if arc.next is not None:
                self._check_circle_event(arc.next)

    def _insert_arc(self, point: Point) -> None:
        if self._arc is None:
            self._arc = Arc(point)
        else:
            # find the current arcs at p.y
            arc = self._arc
            while arc is not None:
                intersection_point = get_arc_intersection(point, arc)
                if intersection_point is not None:
                    intersection_point_next = get_arc_intersection(point, arc.next)
                    if arc.next is not None and intersection_point_next is None:
                        arc.next.prev = Arc(arc.point, arc, arc.next)
                        arc.next = arc.next.prev
                    else:
                        arc.next = Arc(arc.point, arc)
                    arc.next.second_segment = arc.second_segment

                    arc.next.prev = Arc(point, arc, arc.next)
                    arc.next = arc.next.prev

                    arc = arc.next

                    # add new half-edges connected to arc's endpoints
                    segment = Segment(intersection_point)
                    self._voronoi_diagram.append(segment)
                    arc.prev.second_segment = arc.first_segment = segment

                    segment = Segment(intersection_point)
                    self._voronoi_diagram.append(segment)
                    arc.next.first_segment = arc.second_segment = segment

                    # check for new circle events around the new arc
                    self._check_circle_event(arc)
                    self._check_circle_event(arc.prev)
                    self._check_circle_event(arc.next)

                    return
                        
                arc = arc.next

            arc = self._arc
            while arc.next is not None:
                arc = arc.next
            arc.next = Arc(point, arc)

            x, y = self._min_x, (arc.next.point.y + arc.point.y) / 2
            start = Point(x, y)

            segment = Segment(start)
            arc.second_segment = arc.next.first_segment = segment
            self._voronoi_diagram.append(segment)

    def _check_circle_event(self, arc: Arc) -> None:
        # look for a new circle event for arc
        if arc.event is not None and arc.event.x != self._min_x:
            arc.event.is_valid = False
        arc.event = None

        if arc.prev is not None and arc.next is not None:
            max_x, center = get_circle(arc.prev.point, arc.point, arc.next.point)
            if max_x is not None and max_x > self._min_x:
                arc.event = Event(max_x, center, arc)
                self._events.push(arc.event, arc.event.x)

    def _close_segments(self) -> None:
        l = 2 * (self._max_x + (self._max_x - self._min_x) + (self._max_y - self._min_y))
        arc = self._arc
        while arc.next is not None:
            if arc.second_segment is not None:
                arc.second_segment.end = get_intersection(arc.point, arc.next.point, l)
            arc = arc.next
