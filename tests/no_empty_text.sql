select *
from {{ ref('fct_messages') }}
where text is null or text = ''