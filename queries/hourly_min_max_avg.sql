SELECT EXTRACT(HOUR FROM forecast_date) AS hour_of_the_day, :min_max_avg_parameter
FROM forecasts
WHERE city = ':name'
GROUP BY EXTRACT(HOUR FROM forecast_date)
ORDER BY EXTRACT(HOUR FROM forecast_date) ASC
;