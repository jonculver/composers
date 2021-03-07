from __future__ import annotations
from datetime import datetime,timedelta
import dateutil.parser as date_parser

class Event():

    def __init__(self,
                 name:str,
                 start:str,
                 end:str) -> None:
        self.name = name
        self.start = date_parser.parse(start)
        try:
            self.end = date_parser.parse(end)
        except:
            self.end = None

    def dates(self) -> str:
        """
        Return a string 'start_year' - 'end_year'
        """
        return f"{self.start.strftime('%Y')} - {self.end.strftime('%Y') if self.end is not None else ''}"
    
    def after(self, comparison:Event) -> bool:
        """
        Return true if this event was started after the comparison ended
        """
        return comparison.end is not None and comparison.end < self.start

    def __str__(self) -> str:
        """
        Pretty-print composer
        """
        return f"{self.name} ({self.dates()})"