#Author: Alessandro Marcellini, alessandromarcellini49@gmail.com
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

class BaseDownloader(ABC):
    # download_destination: str
    # journals_tokens: List[List[str]]

    
    def __init__(self, download_destination: str, journals_to_download: List[str]):
        self.download_destination = Path(download_destination)
        self.journals_tokens: List[List[str]] = [[token for token in journal.split(" ")] for journal in journals_to_download]

        if not self.download_destination.is_dir():
            raise Exception("Destination Must be a directory")
        print(self.download_destination)
    
    @classmethod
    @abstractmethod
    def _download_journal(self):
        pass

    @classmethod
    @abstractmethod
    def download_journals(self):
        pass
    
    # def destination_cleanup(self):
    #     for file in self.download_destination.iterdir():
    #         file.unlink()