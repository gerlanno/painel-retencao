SELECT
    AVG(TIMESTAMPDIFF(HOUR, date, dateclosed)) AS sla_medio_horas,
    MAX(TIMESTAMPDIFF(HOUR, date, dateclosed)) AS sla_max_horas,
    COUNT(*) AS total_resolvidos_90d,
    SUM(CASE WHEN TIMESTAMPDIFF(HOUR, date, dateclosed) <= 24 THEN 1 ELSE 0 END) AS resolvidos_24h_90d
FROM tbltickets
WHERE serviceid = %s
AND status = 'Closed'
AND date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
