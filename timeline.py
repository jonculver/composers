from __future__ import annotations
import csv
from datetime import datetime,timedelta
import dateutil.parser as date_parser


COMPOSERS_FILE = "composers.csv"
PLAYLIST_COMPOSERS_FILE = "playlist_composers.csv"

DOB="dob"
DOD="dod"
SURNAME="surname"
NAMES="names"

HIDDEN="hidden"

class Composer():

    def __init__(self,
                 surname:str,
                 names:str,
                 dob:str,
                 dod:str):
        self.surname = surname
        self.names = names
        self.dob = date_parser.parse(dob) #datetime.strptime(dob, "%m/%d/%Y")
        if dod == "__":
            self.dod = None
        else:
            self.dod = date_parser.parse(dod) #datetime.strptime(dob, "%m/%d/%Y")

    def name(self) -> str:
        """
        Return the full name of this composer
        """
        return f"{self.names} {self.surname}"

    def dates(self) -> str:
        """
        Return a string 'year of birth' - 'year of death'
        """
        return f"{self.dob.strftime('%Y')} - {self.dod.strftime('%Y') if self.dod is not None else ''}"
    
    def after(self, comparison:Composer) -> bool:
        """
        Return true if this composer was born after the comparison died
        """
        return comparison.dod is not None and comparison.dod < self.dob

    def __str__(self) -> str:
        """
        Pretty-print composer
        """
        return f"{self.name()} ({self.dates()})"



def create_composer_dict() -> dict[str:Composer]:
    """
    Read data from CSV files and populate dictionary of composers, indexed by SURNAME,Names
    """
    result = {}
    with open(COMPOSERS_FILE, newline='') as csvfile:
        filereader = csv.DictReader(csvfile)
        for row in filereader:
            entry = Composer(row[SURNAME], row[NAMES], row[DOB], row[DOD])
            result[entry.name()] = entry
    return result

def create_playlist_names() -> list:
    """
    Read data from playlist CSV and create a list of composer names
    """
    result = []
    with open(PLAYLIST_COMPOSERS_FILE, newline='') as csvfile:
        filereader = csv.DictReader(csvfile)
        for row in filereader:
            if not row[HIDDEN]:
                result.append(f"{row[NAMES]} {row[SURNAME]}")
    return result


def filter_composer_dict(composer_dict:dict[str:Composer],
                         playlist:list) -> dict[str:Composer]:
    """
    Return a filtered dictionary with only the entries present on the playlist
    """
    result = {}
    for entry in playlist:
        if entry in composer_dict:
            result[entry] = composer_dict[entry]
        else:
            print(f"Unknown composer: '{entry}'")
    return result

def create_cycles(composer_dict:dict[str:Composer]) -> list[list[Composer]]:
    """
    Return a list of lists of composers with non-overlapping lifetimes
    """
    result = []
    for entry in sorted(composer_dict.values(), key=lambda item: item.dob):
        done = False
        for cycle in result:
            if entry.after(cycle[-1]):
                cycle.append(entry)
                done = True
                break
        if not done:
            result.append([entry]) 
    return result




if __name__ == "__main__":
    composer_dict = create_composer_dict()
    playlist = create_playlist_names()
    composer_dict = filter_composer_dict(composer_dict, playlist)

    cycles = create_cycles(composer_dict)
    for i, entry in enumerate(cycles):
        print(f"{i+1}. -----")
        for composer in entry:
            print(composer)
        
    

