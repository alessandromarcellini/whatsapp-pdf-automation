import os
from dotenv import load_dotenv

from typing import List

from classes.journal_names_loader import JournalNamesLoader
from classes.downloaders.telegram_downloader import TelegramDownloader

# import asyncio

#LOADING ENV VARIABLES
load_dotenv()
JOURNAL_NAMES_FILE = os.getenv('JOURNAL_NAMES_FILE')
PDFS_DESTINATION = os.getenv('PDFS_DESTINATION')

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_CHANNEL_NAME = os.getenv('TELEGRAM_CHANNEL_NAME')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

def get_journal_names() -> List[str]:
    names_loder = JournalNamesLoader(JOURNAL_NAMES_FILE)
    names_loder.load_names()
    return names_loder.get_names()

def download_journals(journal_names) -> dict[str, bool]:
    downloader = TelegramDownloader(PDFS_DESTINATION, journal_names, TELEGRAM_API_ID, TELEGRAM_API_HASH, PHONE_NUMBER, TELEGRAM_CHANNEL_NAME)
    
    #preventively cleanup destination folder
    # downloader.destination_cleanup()
    # Start monitoring
    downloader.run()

    # asyncio.run(downloader.list_channels())



# ------------------------------------------------------------------------------------
def main():
    #GET JOURNALS TO DOWNLOAD
    journal_names: List[str] = get_journal_names()

    #DOWNLOAD JOURNALS DEAMON
    download_journals(journal_names)

    



if __name__ == '__main__':
    main()