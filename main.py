import os
from dotenv import load_dotenv

from typing import List


from classes.journal_names_loader import JournalNamesLoader
from classes.journal_downloader import JournalDownloader

#LOADING ENV VARIABLES
load_dotenv()
JOURNAL_NAMES_FILE = os.getenv('JOURNAL_NAMES_FILE')
PDFS_DOWNLOAD_URL = os.getenv('PDFS_DOWNLOAD_URL')
PDFS_DESTINATION = os.getenv('PDFS_DESTINATION')

def get_journal_names() -> List[str]:
    names_loder = JournalNamesLoader(JOURNAL_NAMES_FILE)
    names_loder.load_names()
    return names_loder.get_names()





# ------------------------------------------------------------------------------------
def main():
    #GET JOURNALS TO DOWNLOAD
    journal_names: List[str] = get_journal_names()






if __name__ == '__main__':
    main()