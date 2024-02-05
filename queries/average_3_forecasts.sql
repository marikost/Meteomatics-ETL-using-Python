SELECT CAST(forecast_date AS date), :avg_parameter
FROM(
SELECT city, forecast_date, :parameter, ROW_NUMBER() OVER(PARTITION BY city, CAST(forecast_date AS date ) ORDER BY forecast_date DESC ) AS RN
FROM forecasts
) t
WHERE RN <= 3 AND city = ':name'
GROUP BY CAST(forecast_date AS date)
ORDER BY CAST(forecast_date AS date) ASC
;