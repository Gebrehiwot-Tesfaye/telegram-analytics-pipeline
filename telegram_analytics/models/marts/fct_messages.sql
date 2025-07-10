select
    id as message_id,
    date,
    text,
    media,
    media_path,
    channel_id,
    channel_name,
    channel_url,
    message_length,
    has_image
from {{ ref('stg_telegram_messages') }}