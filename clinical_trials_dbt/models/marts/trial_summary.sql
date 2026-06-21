with staged as (
    select * from {{ ref('stg_clinical_trials') }}
),

summary as (
    select
        overall_status,
        count(*) as trial_count,
        count(distinct sponsor_name) as unique_sponsors,
        min(start_date) as earliest_trial,
        max(start_date) as latest_trial
    from staged
    where overall_status is not null
    group by overall_status
)

select * from summary