with raw as (
    select
        *,
        row_number() over (partition by id order by date desc) as rn
    from {{ source('public', 'raw_telegram_messages') }}
)
select
    id::bigint,
    date::timestamp,
    text,
    media,
    media_path,
    channel_id,
    channel_name,
    channel_url,

    length(text) as message_length,
    case when media then 1 else 0 end as has_image
from raw
where text is not null
  and text != ''
  and channel_id is not null
  and rn = 1