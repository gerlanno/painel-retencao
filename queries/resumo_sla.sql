SELECT
    AVG(TIMESTAMPDIFF(MINUTE, date, dateclosed)) AS sla_medio_minutos,
    MAX(TIMESTAMPDIFF(MINUTE, date, dateclosed)) AS sla_max_minutos,
    COUNT(*) AS total_resolvidos_90d,
    SUM(
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, date, dateclosed) <= 1440 THEN 1
            ELSE 0
        END
    ) AS resolvidos_1440m_90d
FROM
    tbltickets
WHERE
    serviceid = %s
    AND STATUS = 'Closed'
    AND date >= DATE_SUB(NOW(), INTERVAL 90 DAY)