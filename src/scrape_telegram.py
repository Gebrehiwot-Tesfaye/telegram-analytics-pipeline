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

def get_last_message_id(channel_name):
    last_id_path = os.path.join("data", "last_scraped", f"{channel_name}.json")
    if os.path.exists(last_id_path):
        with open(last_id_path, "r") as f:
            return json.load(f).get("last_id")
    return None

def set_last_message_id(channel_name, last_id):
    os.makedirs(os.path.join("data", "last_scraped"), exist_ok=True)
    last_id_path = os.path.join("data", "last_scraped", f"{channel_name}.json")
    with open(last_id_path, "w") as f:
        json.dump({"last_id": last_id}, f)

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

    # Load previous messages if exist
    prev_messages = []
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            prev_messages = json.load(f)
        prev_ids = {m["id"] for m in prev_messages}
    else:
        prev_ids = set()

    last_id = get_last_message_id(channel_name)

    with TelegramClient('anon', API_ID, API_HASH) as client:
        messages = []
        image_msgs = []
        for message in client.iter_messages(channel_url, limit=500, min_id=last_id or 0):
            if message.id in prev_ids:
                continue
            msg = {
                "id": message.id,
                "date": str(message.date),
                "text": message.text,
                "media": bool(message.media),
                "channel_name": channel_name,
                "channel_url": channel_url,
                "sender_id": message.sender_id,
                "is_reply": message.is_reply,
            }
            messages.append(msg)
            if message.media and isinstance(message.media, MessageMediaPhoto):
                image_msgs.append(message)
        # Combine previous and new messages, sort by id
        all_messages = prev_messages + messages
        all_messages = {m["id"]: m for m in all_messages}.values()  # deduplicate by id
        all_messages = sorted(all_messages, key=lambda x: x["id"], reverse=True)
        # Save as JSON (raw)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(list(all_messages), f, ensure_ascii=False, indent=2)
        # Preprocess: filter out messages with null/empty text or media==False
        preprocessed = [m for m in all_messages if m["text"] not in (None, "") and m["media"] is True]
        with open(preprocessed_path, "w", encoding="utf-8") as f:
            json.dump(preprocessed, f, ensure_ascii=False, indent=2)
        # Download only top 100 new images
        download_images(client, image_msgs, img_out_dir, max_images=100)
        # Update last scraped id
        if all_messages:
            set_last_message_id(channel_name, max(m["id"] for m in all_messages))
    logging.info(f"Scraped {len(messages)} new messages, {len(preprocessed)} preprocessed, and {min(len(image_msgs), 100)} images from {channel_url}")

if __name__ == "__main__":
    for channel in CHANNELS:
        try:
            scrape_channel(channel)
            print(f"Scraped {channel} successfully.")
        except Exception as e:
            logging.error(f"Error scraping {channel}: {e}")
            print(f"Error scraping {channel}: {e}")
