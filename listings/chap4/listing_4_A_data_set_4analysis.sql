with observation_params as     
(
    select  interval 'MET_INTERVAL' as metric_period,
    'FRYR-MM-DD'::timestamp as obs_start,    
    'TOYR-MM-DD'::timestamp as obs_end    
)
select m.account_id, o.observation_date, is_churn FLAT_METRIC_SELECT
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn    
