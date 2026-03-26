SELECT
    c.name AS classificacao,
    COUNT(*) AS total
FROM
    tbltickets t
    JOIN tblticketcloseclassifications c ON c.id = t.closeclassificationid
WHERE
    t.serviceid = %s
    AND t.date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY
    c.name
ORDER BY
    total DESC
LIMIT
    5