
with source as (
    select * from {{ source('clinical_trials', 'raw_studies') }}
),

staged as (
    select
        nct_id,
        brief_title,
        overall_status,
        sponsor_name,
        conditions,
        -- fixing date type and null handling
        case
            when start_date = '' or start_date is null then null
            when length(start_date) = 7 then cast(concat(start_date, '-01') as date)
            else cast(start_date as date)
        end as start_date,
        -- adds another column for ingestion time
        current_timestamp() as ingested_at
    from source
)

select * from staged