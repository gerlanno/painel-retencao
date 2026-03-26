SELECT
    t.id,
    t.tid,
    t.title,
    t.status,
    t.date,
    t.dateclosed,
    tr.title AS motivo,
    c.name AS classificacao,
    d.name AS departamento,
    TIMESTAMPDIFF(MINUTE, t.date, t.dateclosed) AS sla_minutos
FROM
    tbltickets t
    LEFT JOIN tbltickettyperequest tr ON tr.id = t.typerequestcurrent
    LEFT JOIN tblticketcloseclassifications c ON c.id = t.closeclassificationid
    LEFT JOIN tblticketdepartments d ON d.id = t.did
WHERE
    t.serviceid = %s
ORDER BY
    t.date DESC
LIMIT
    50