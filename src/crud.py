from sqlalchemy import text
from .database import engine

def get_top_products(limit: int):
    sql = """
        SELECT product, COUNT(*) AS mentions
        FROM products_mentions
        GROUP BY product
        ORDER BY mentions DESC
        LIMIT :limit
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), {"limit": limit})
        return [{"product": row.product, "mentions": row.mentions} for row in result]

def get_channel_activity(channel_name: str):
    sql = """
        SELECT
            channel_name,
            COUNT(*) AS post_count,
            MAX(date) AS last_post_date,
            COUNT(CASE WHEN media THEN 1 END) AS image_count,
            COUNT(CASE WHEN is_reply THEN 1 END) AS reply_count
        FROM raw_telegram_messages
        WHERE channel_name = :channel_name
        GROUP BY channel_name
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), {"channel_name": channel_name}).fetchone()
        if result:
            return {
                "channel_name": result.channel_name,
                "post_count": result.post_count,
                "last_post_date": result.last_post_date,
                "image_count": result.image_count,
                "reply_count": result.reply_count
            }
        return {
            "channel_name": channel_name,
            "post_count": 0,
            "last_post_date": None,
            "image_count": 0,
            "reply_count": 0
        }

def search_messages(query: str):
    sql = """
        SELECT id AS message_id, channel_name, text AS content
        FROM raw_telegram_messages
        WHERE text ILIKE :query
        LIMIT 50
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), {"query": f"%{query}%"}).fetchall()
        return [
            {
                "message_id": str(row.message_id) if row.message_id is not None else "",
                "channel_name": str(row.channel_name) if row.channel_name is not None else "",
                "content": row.content if row.content is not None else ""
            }
            for row in result
        ]

def get_top_media(limit: int):
    sql = """
        SELECT media_path, COUNT(*) AS mentions
        FROM image_detections
        GROUP BY media_path
        ORDER BY mentions DESC
        LIMIT :limit
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), {"limit": limit})
        return [{"media_path": row.media_path, "mentions": row.mentions} for row in result]

def list_channels():
    sql = """
        SELECT DISTINCT channel_name
        FROM raw_telegram_messages
        WHERE channel_name IS NOT NULL
        ORDER BY channel_name
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql)).fetchall()
        return [row.channel_name for row in result]

def get_top_questions(limit: int):
    sql = """
        SELECT text, COUNT(*) AS count
        FROM raw_telegram_messages
        WHERE text IS NOT NULL AND TRIM(text) <> ''
        GROUP BY text
        ORDER BY count DESC
        LIMIT :limit
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), {"limit": limit})
        return [{"text": row.text, "count": row.count} for row in result]

def get_channel_overview():
    sql = """
        SELECT
            channel_name,
            COUNT(*) AS message_count,
            COUNT(CASE WHEN media = TRUE THEN 1 END) AS media_post_count,
            COUNT(CASE WHEN is_reply = TRUE THEN 1 END) AS reply_count
        FROM raw_telegram_messages
        WHERE channel_name IS NOT NULL
        GROUP BY channel_name
        ORDER BY message_count DESC
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql)).fetchall()
        return [
            {
                "channel_name": str(row.channel_name) if row.channel_name is not None else "",
                "message_count": row.message_count,
                "media_post_count": row.media_post_count,
                "reply_count": row.reply_count
            }
            for row in result
        ]

def get_all_messages():
    sql = """
        SELECT
            id,
            date,
            text,
            media,
            channel_name,
            channel_url,
            sender_id,
            is_reply
        FROM raw_telegram_messages
        LIMIT 1000
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql)).mappings().fetchall()
        return [
            {
                "id": row["id"],
                "date": str(row["date"]) if row["date"] is not None else "",
                "text": row["text"] if row["text"] is not None else "",
                "media": bool(row["media"]) if row["media"] is not None else False,
                "channel_name": row["channel_name"] if row["channel_name"] is not None else "",
                "channel_url": row["channel_url"] if row["channel_url"] is not None else "",
                "sender_id": row["sender_id"] if row["sender_id"] is not None else None,
                "is_reply": bool(row["is_reply"]) if row["is_reply"] is not None else False
            }
            for row in result
        ]