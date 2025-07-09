select
    channel_id,
    channel_name
from {{ source('public', 'channels') }}
