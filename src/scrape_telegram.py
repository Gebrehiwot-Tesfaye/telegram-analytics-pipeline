# This script scrapes messages and images from public Telegram channels related to Ethiopian medical businesses.
# It saves raw data in a partitioned directory structure for easy incremental processing and future loading into a database.
# Environment variables are loaded securely from .env using python-dotenv.

import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

CHANNELS = [
    "https://t.me/CheMed123",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

RAW_DATA_DIR = "data/raw/telegram_messages"

# Set up logging
logging.basicConfig(
    filename="data/raw/telegram_messages/scraping.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s"
)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def download_images(client, messages, img_out_dir, max_images=100):
    os.makedirs(img_out_dir, exist_ok=True)
    count = 0
    for msg in messages:
        if count >= max_images:
            break
        if msg.media and isinstance(msg.media, MessageMediaPhoto):
            try:
                client.download_media(msg, file=img_out_dir)
                count += 1
            except Exception as e:
                logging.error(f"Failed to download image {msg.id}: {e}")

def scrape_channel(channel_url):
    channel_name = channel_url.split('/')[-1]
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = os.path.join(RAW_DATA_DIR, date_str)
    img_out_dir = os.path.join("media", date_str, channel_name)
    pre_dir = os.path.join("data", "preprocessed", date_str)
    ensure_dir(out_dir)
    ensure_dir(img_out_dir)
    ensure_dir(pre_dir)
    out_path = os.path.join(out_dir, f"{channel_name}.json")
    preprocessed_path = os.path.join(pre_dir, f"{channel_name}_preprocessed.json")

    with TelegramClient('anon', API_ID, API_HASH) as client:
        messages = []
        image_msgs = []
        for message in client.iter_messages(channel_url, limit=500):
            msg = {
                "id": message.id,
                "date": str(message.date),
                "text": message.text,
                "media": bool(message.media),
                # Add more fields as needed
            }
            messages.append(msg)
            if message.media and isinstance(message.media, MessageMediaPhoto):
                image_msgs.append(message)
        # Save as JSON (raw)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        # Preprocess: filter out messages with null/empty text or media==False
        preprocessed = [m for m in messages if m["text"] not in (None, "") and m["media"] is True]
        with open(preprocessed_path, "w", encoding="utf-8") as f:
            json.dump(preprocessed, f, ensure_ascii=False, indent=2)
        # Download only top 100 images
        download_images(client, image_msgs, img_out_dir, max_images=100)
    logging.info(f"Scraped {len(messages)} messages, {len(preprocessed)} preprocessed, and {min(len(image_msgs), 100)} images from {channel_url}")

if __name__ == "__main__":
    for channel in CHANNELS:
        try:
            scrape_channel(channel)
            print(f"Scraped {channel} successfully.")
        except Exception as e:
            logging.error(f"Error scraping {channel}: {e}")
            print(f"Error scraping {channel}: {e}")
