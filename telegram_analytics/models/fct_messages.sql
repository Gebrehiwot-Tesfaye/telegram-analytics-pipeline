select
    id as message_id,
    date,
    text,
    media,
    media_path,
    channel_id
from {{ source('public', 'raw_telegram_messages') }}
