SELECT
    c.id,
    c.companyname,
    c.firstname,
    c.segmentid,
    s.name AS segmento_nome
FROM
    tblclients c
    LEFT JOIN tblclientsegment s ON s.id = c.segmentid
WHERE
    c.document = %s