SELECT
    h.id AS servico_id,
    h.designator AS designador,
    p.name AS plano,
    h.amount AS valor,
    h.billingcycle,
    h.domainstatus,
    h.regdate,
    a.citydesc AS cidade,
    t.name AS tecnologia,
    (SELECT s.optionname 
     FROM tblhostingconfigoptions co
     JOIN tblproductconfigoptions o ON o.id = co.configid
     JOIN tblproductconfigoptionssub s ON s.id = co.optionid
     WHERE co.relid = h.id 
     AND (o.optionname LIKE '%%VELOCIDADE%%' OR o.optionname LIKE '%%BANDWIDTH%%')
     LIMIT 1) AS velocidade,
    (SELECT COUNT(*) FROM tbltickets WHERE serviceid = h.id AND date >= DATE_SUB(NOW(), INTERVAL 90 DAY)) AS tickets_90d
FROM tblhosting h
JOIN tblproducts p
    ON p.id = h.packageid
LEFT JOIN tbladdress a
    ON a.relid = h.id AND a.subtype = 'INSTALACAO'
LEFT JOIN tblhostingnetworkconfig nc
    ON nc.hosting_id = h.id
LEFT JOIN tblnetworktechnology t
    ON t.id = nc.technology_id
WHERE h.userid = %s