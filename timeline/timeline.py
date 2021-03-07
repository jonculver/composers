from __future__ import annotations
from timeline.event import Event

class Timeline():

    def __init__(self,
                 events:list[Event]) -> None:
        """
        Create new timeline object from a list of events
        """
        self.events = sorted(events, key=lambda item: item.start)

    def __iter__(self) -> Timeline:
        """
        Set the current event to the first one and return this object
        """
        self.next = 0
        return self

    def __next__(self) -> Event:
        """
        Return the next object in the (sorted) list of events
        """
        if self.next < len(self.events):
            result = self.events[self.next]
            self.next += 1
            return result
        else:
            raise StopIteration
    
    def _create_cycles(self) -> list[list[Event]]:
        """
        Return a list of lists of events with non-overlapping dates
        """
        result = []
        for entry in sorted(self.events, key=lambda item: item.start):
            done = False
            for cycle in result:
                if entry.after(cycle[-1]):
                    cycle.append(entry)
                    done = True
                    break
            if not done:
                result.append([entry]) 
        return result
