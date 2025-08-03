from .base_downloader import BaseDownloader
from telethon import TelegramClient

import os
import asyncio
from datetime import datetime
from typing import List, Union, Optional, Callable
from telethon import TelegramClient, events
from telethon.tl.types import User, Chat, Channel, MessageMediaDocument

class TelegramDownloader(BaseDownloader):
    #api_id: str
    #api_hash: str

    def __init__(self, download_destination: str, journals_to_download: List[str], api_id: str, api_hash: str, phone_number: str, channel_name: str):
        super().__init__(download_destination, journals_to_download)
        self.api_id = api_id
        self.api_hash = api_hash

        self.phone_number = phone_number
        
        self.client = TelegramClient('anon', api_id, api_hash)

        self.channel_name = channel_name

        self.is_running = False
    

    async def message_handler(self, event):
        print(f"Received: {event.message.text}")
    

    async def start(self) -> None:
        """
        Start the client and begin monitoring the channel.
        """
        
        try:
            await self.client.start(phone=self.phone_number)
            print(f"Client started successfully!")

            # Register event handler for the specified channel entity
            self.client.add_event_handler(
                self.message_handler,
                events.NewMessage(chats=self.channel_name)
            )

            #TODO get last 50 messages and check the date. If it is the current day download
            
            self.is_running = True
            print("Listening for messages... (Press Ctrl+C to stop)")
            
            # Keep the client running
            await self.client.run_until_disconnected()
            
        except KeyboardInterrupt:
            print("\nStopping message handler...")
            await self.stop()
        except Exception as e:
            print(f"Error starting client: {e}")
            await self.stop()
    
    async def stop(self) -> None:
        """
        Stop the client and cleanup.
        """
        if self.is_running:
            self.is_running = False
            await self.client.disconnect()
            print("Client stopped successfully!")
    
    def run(self) -> None:
        """
        Convenience method to run the handler using asyncio.
        """
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            pass
    
    # ---------------------------------------------
    def _download_journal(self):
        pass

    def download_journals(self):
        pass

    # async def list_channels(self):
    #     """
    #     List all available channels to help find the correct ID
    #     """
    #     try:
    #         await self.client.start(phone=self.phone_number)
    #         print("Available channels and chats:")
    #         print("-" * 60)
            
    #         async for dialog in self.client.iter_dialogs():
    #             entity = dialog.entity
    #             if hasattr(entity, 'megagroup') or hasattr(entity, 'broadcast'):
    #                 print(f"Title: {dialog.title}")
    #                 print(f"ID: {entity.id}")
    #                 print(f"Username: @{getattr(entity, 'username', 'No username')}")
    #                 print(f"Type: {'Channel' if getattr(entity, 'broadcast', False) else 'Group'}")
    #                 print("-" * 30)
            
    #         await self.client.disconnect()
            
    #     except Exception as e:
    #         print(f"Error listing channels: {e}")

    async def message_handler(self, event):
        """Handle incoming messages and download PDF files"""
        try:
            message = event.message
            print(f"New message received:")
            print(f"   Text: {message.text or '[No text]'}")
            
            # Check if message has media
            if message.media:
                await self.handle_media_message(message)
            else:
                print("No media attached")
            
        except Exception as e:
            print(f"Error in message handler: {e}")
    
    async def handle_media_message(self, message):
        """Handle messages with media attachments"""
        try:
            media = message.media
            
            # Check if it's a document (files are usually documents in Telegram)
            if isinstance(media, MessageMediaDocument):
                document = media.document
                
                # Get file information
                file_name = None
                file_size = document.size
                mime_type = document.mime_type
                
                # Extract filename from document attributes
                for attribute in document.attributes:
                    if hasattr(attribute, 'file_name') and attribute.file_name:
                        file_name = attribute.file_name
                        break
                print(f"Name: {file_name or 'Unknown'}")
                
                # Check if it's a PDF file
                if self.is_pdf_file(file_name, mime_type):
                    #check if the pdf is of interest

                    if self._is_interesting(file_name):
                        await self.download_pdf(message, file_name or f"document_{message.id}.pdf")
                    else:
                        print("PDF not interesting")
                else:
                    print(f"Not a PDF file, skipping")
            else:
                print(f"Media type: {type(media).__name__} (not a document)")
                
        except Exception as e:
            print(f"Error handling media: {e}")
    
    def is_pdf_file(self, file_name: str, mime_type: str) -> bool:
        """Check if the file is a PDF based on filename and MIME type"""
        # Check MIME type first (most reliable)
        if mime_type and mime_type.lower() == 'application/pdf':
            return True
        
        # Check file extension as fallback
        if file_name and file_name.lower().endswith('.pdf'):
            return True
        
        return False
    
    async def download_pdf(self, message, file_name: str):
        """Download PDF file from message"""
        try:
            # Ensure download directory exists
            os.makedirs(self.download_destination, exist_ok=True)
            
            # Create filename with timestamp to avoid conflicts
            downloaded_file_name = f"{datetime.today().strftime('%d_%m_%Y')}___{file_name}"
            file_path = os.path.join(self.download_destination, downloaded_file_name)
            
            print(f"Downloading to: {file_path}")
            
            # Download the file
            await message.download_media(file=file_path)
            
            # Verify download
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"Download successful!")
            else:
                print(f"Download failed - file not found")
                
        except Exception as e:
            print(f"Download error: {e}")

    def _is_interesting(self, file_name: str):
        for token_list in self.journals_tokens:
            if all(token in file_name.lower() for token in token_list):
                return True
        return False
