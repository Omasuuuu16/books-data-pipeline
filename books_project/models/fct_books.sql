with staged as (
    select * from {{ ref('stg_books') }}
)

select
    title,
    rating_number,
    CAST(REGEXP_REPLACE(REPLACE(price, '£', ''), '[^0-9.]', '', 'g') AS DOUBLE) as price_clean
from staged
order by rating_number desc