with RECURSIVE date_vals AS (    
select i::timestamp as metric_date     
from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i
),
earlier_starts AS    
(
	select account_id, metric_date, min(start_date) as start_date    
	from subscription inner join date_vals
		on start_date <= metric_date    
		and (end_date > metric_date or end_date is null)
	group by account_id, metric_date

	UNION

	select s.account_id, metric_date, s.start_date    
	from subscription s inner join earlier_starts e
		on s.account_id=e.account_id
		and s.start_date < e.start_date
		and s.end_date >= (e.start_date-31)

)
/* insert into metric (account_id,metric_time,metric_name_id,metric_name,metric_value)  UNCOMMENT TO ACTUALLY INSERT */
SELECT account_id, metric_date, 0 as metric_name_id, metric_date-min(start_date) as account_tenure
FROM earlier_starts
group by account_id, metric_date
order by account_id, metric_date
