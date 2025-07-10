select
    id as message_id,
    date,
    text,
    media,
    media_path,
    channel_id,
    message_length,
    has_image
from {{ ref('stg_telegram_messages') }}