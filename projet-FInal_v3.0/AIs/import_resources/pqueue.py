import heapq
import itertools


class PriorityQueue(object):
    _REMOVED = "<REMOVED>"

    def __init__(self):
        self.heap = []
        self.entries = {}
        self.counter = itertools.count()
        self.size = 0

    def add(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        if task in self.entries:
            self.remove(task)

        count = next(self.counter)
        # weight = priority since heap is a min-heap
        entry = [priority, count, task]
        self.entries[task] = entry
        heapq.heappush(self.heap, entry)
        self.size += 1

    def remove(self, task):
        """ Mark the given task as REMOVED.

        Do this to avoid breaking heap-invariance of the internal heap.
        """
        entry = self.entries[task]
        entry[-1] = PriorityQueue._REMOVED

    def pop(self):
        """ Get task with highest priority.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, count, task = heapq.heappop(self.heap)
            if task is not PriorityQueue._REMOVED:
                del self.entries[task]
                return weight, task
        raise KeyError("The priority queue is empty")

    def peek(self):
        """ Check task with highest priority, without removing.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, count, task = self.heap[0]
            if task is PriorityQueue._REMOVED:
                heapq.heappop(self.heap)
            else:
                return weight, task

        return None

    def is_empty(self):
        """
        Check if the queue is empty
        :return:
        """
        return len(self.entries) == 0

    def __str__(self):
        temp = [str(e) for e in self.heap if e[-1] is not PriorityQueue._REMOVED]
        return "[%s]" % ", ".join(temp)
