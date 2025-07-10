select distinct
    date::date as date_id,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day
from {{ ref('stg_telegram_messages') }}