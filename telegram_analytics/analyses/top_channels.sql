select channel_id, count(*) as message_count
from {{ ref('fct_messages') }}
group by channel_id
order by message_count desc