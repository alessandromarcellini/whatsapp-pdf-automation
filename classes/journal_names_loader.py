#Author: Alessandro Marcellini, alessandromarcellini49@gmail.com
from typing import List

class JournalNamesLoader:
    # file_path: str
    # journal_names: List[str]

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.journal_names = []
    
    def get_names(self) -> List[str]:
        return self.journal_names
    
    def load_names(self) -> None:
        with open(self.file_path) as f:
            for line in f:
                self.journal_names.append(line.strip())

    def reset_names(self) -> None:
        self.journal_names = []