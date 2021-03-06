with
date_range as (    
	select i::timestamp as calc_date 
from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '1 day'::interval) i
)
select event_time::date as event_date,   
	count(*) as n_event,
  	sum(SUM_FIELD) as total_EVENT_NAME_SUM_FIELD
from date_range left outer join event e on calc_date=event_time::date
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='EVENT_NAME'
group by event_date    
order by event_date
