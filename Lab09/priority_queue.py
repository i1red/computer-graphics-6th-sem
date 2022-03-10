import heapq


class PriorityQueue:
    def __init__(self):
        self._data = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._data, (priority, self._index, item))
        self._index += 1

    def pop(self):
        _, _, item = heapq.heappop(self._data)
        return item

    def top(self):
        _, _, item = self._data[0]
        return item

    def __bool__(self):
        return bool(self._data)
