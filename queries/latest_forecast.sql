SELECT forecast_date, :parameter
FROM(
SELECT city, :parameter, forecast_date, ROW_NUMBER() OVER(PARTITION BY city, CAST(forecast_date AS date ) ORDER BY forecast_date DESC ) AS RN
FROM forecasts
) t
WHERE RN = 1 AND city = ':name'
ORDER BY forecast_date ASC
;