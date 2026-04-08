with source as (
    select * from {{ ref('books') }}
),

staged as (
    select
        title,
        price,
        rating,
        case rating
            when 'One'   then 1
            when 'Two'   then 2
            when 'Three' then 3
            when 'Four'  then 4
            when 'Five'  then 5
        end as rating_number
    from source
)

select * from staged