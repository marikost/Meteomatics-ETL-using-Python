SELECT city, max(:parameter) as maximum
FROM forecasts
GROUP BY city
ORDER BY max(:parameter) DESC
LIMIT :n
;