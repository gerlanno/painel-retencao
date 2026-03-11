SELECT
COUNT(*) AS total_tickets,

CAST(SUM(
    CASE WHEN date >= NOW() - INTERVAL 30 DAY
    THEN 1 ELSE 0 END
) AS UNSIGNED) AS tickets_30d,

CAST(SUM(
    CASE WHEN date >= NOW() - INTERVAL 90 DAY
    THEN 1 ELSE 0 END
) AS UNSIGNED) AS tickets_90d,

MAX(date) AS ultimo_ticket

FROM tbltickets
WHERE serviceid = %s