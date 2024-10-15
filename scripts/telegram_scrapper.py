from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import logging

# Ensure the scrapped_data directory exists
scrapped_data_dir = '../data/scrapped_data'
if not os.path.exists(scrapped_data_dir):
    os.makedirs(scrapped_data_dir)


# Set up logging configuration
logging.basicConfig(
    filename='../data/scrapped_data/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Function to scrape photos from specific channels
async def scrape_photos(client, channel_username, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title 
        logging.info(f"Scraping photos from channel: {channel_title}")
        
        async for message in client.iter_messages(entity):
            if message.media and hasattr(message.media, 'photo'):
                # Create a unique filename for the photo
                photo_filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, photo_filename)

                # Download the media to the specified directory if it's a photo
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media: {photo_filename}")

        logging.info(f"Photo scraping complete for channel: {channel_title}")

    except Exception as e:
        logging.error(f"Error scraping photos from channel {channel_username}: {str(e)}")

# Function to scrape messages from channels (no media)
async def scrape_messages(client, channel_username, scrapped_data_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title 
        logging.info(f"Scraping messages from channel: {channel_title}")
        
        # Create a CSV file for each channel
        filename = f"{scrapped_data_dir}/{channel_username}_data.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Views', 'Message Link'])

            async for message in client.iter_messages(entity, limit=4000):
                message_link = f'https://t.me/{channel_username}/{message.id}' if channel_username else None
                writer.writerow([channel_title, channel_username, message.id, message.message, message.date, message.views, message_link])

        logging.info(f"Message scraping complete for channel: {channel_title}")

    except Exception as e:
        logging.error(f"Error scraping messages from channel {channel_username}: {str(e)}")

# Initialize the client
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    try:
        await client.start()
        logging.info("Telegram client started")
        
        # Create directories for media files and scrapped data
        media_dir = '../data/photos'

        os.makedirs(media_dir, exist_ok=True)
        logging.info("Created required directories")

        # Channels to scrape photos from
        photo_channels = [
            '@CheMed123',
            '@lobelia4cosmetics'
        ]

        # Channels to scrape messages from
        message_channels = [
            "@DoctorsET", 
            "@CheMed123", 
            "@lobelia4cosmetics", 
            "@yetenaweg", 
            "@EAHCI"
        ]

        # Scrape photos from the specified channels
        #for channel in photo_channels:
            #await scrape_photos(client, channel, media_dir)
            #print(f"Scraped photos from {channel}")

        # Scrape messages from the other channels
        for channel in message_channels:
            await scrape_messages(client, channel, scrapped_data_dir)
            print(f"Scraped messages from {channel}")

    except Exception as e:
        logging.error(f"Error in the main function: {str(e)}")

with client:
    client.loop.run_until_complete(main())