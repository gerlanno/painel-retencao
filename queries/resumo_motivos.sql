SELECT
    tr.title AS motivo,
    COUNT(*) AS total
FROM
    tbltickets t
    JOIN tbltickettyperequest tr ON tr.id = t.typerequestcurrent
WHERE
    t.serviceid = %s
    AND t.date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY
    tr.title
ORDER BY
    total DESC
LIMIT
    5