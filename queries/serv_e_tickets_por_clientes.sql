SELECT
	u.firstname AS "CLIENTE",
	h.numplan AS "Nº PLANO",
	h.regdate AS "DATA DO CADASTRO",
	h.id AS "SERVIÇO",
    (
        SELECT GROUP_CONCAT(CONCAT(pco.optionname, ' : ', sub_velo.optionname) SEPARATOR ' | ')
        FROM tblhostingconfigoptions hco
        INNER JOIN tblproductconfigoptions pco ON hco.configid = pco.id AND pco.optionname IN ('TECNOLOGIA', 'VELOCIDADES', 'TIPO DE ENTREGA')
        INNER JOIN tblproductconfigoptionssub sub_velo ON hco.optionid = sub_velo.id
        WHERE hco.relid = h.id
    ) AS "VELOCIDADE_TECNOLOGIA",
	h.amount AS "VALOR",
	h.validitycontract AS "VIGENCIA DO CONTRATO",
	NULL AS "MOTIVO DO CANCELAMENTO", -- Não mapeado no documento
	h.bitrixbusinessnumber AS "NEGOCIO BITRIX",
	h.datecontract AS "DATA DO CONTRATO",
	h.serviceprimary AS "SERVIÇO PRIMARIO", -- Não há mapeamento direto
	pt.name AS "PARCEIRO TÉCNICO RESPONSÁVEL",
	pj.name AS "NOME DO PROJETO",
	a.address AS "ENDEREÇO",
	a.number AS "NUMERO",
	a.complement AS "COMPLEMENTO",
	a.postcode AS "CEP",
	NULL AS "INSTALADO POR", -- Requer mapeamento do técnico
	nc.model_onu AS "MODELO",
	nc.serial AS "SERIAL",
	h.domainstatus AS "STATUS",
	p.name AS "PRODUTO",
	h.designator AS "DESIGNADOR",
	h.dateactivate AS "DATA DA ATIVAÇÃO",
	a.neighborhood AS "BAIRRO",
	c.name AS "CIDADE",
	a.state AS "ESTADO",
	tickets_filtrados.tickets AS "TICKETS"
FROM
	tblhosting h
LEFT JOIN (
    SELECT 
        t.serviceid,
        GROUP_CONCAT(t.id SEPARATOR ', ') AS tickets
    FROM tbltickets t
    WHERE t.typerequest IN (57,1309,505,1785,2999,3019,3001,3021,3003,3023,1935,487,489,493,491,1695,2175,3143,3281,495,2669,2683,2201,2209,2005,1945,2173,623,1849,633,639,1705,697,699,2163,2181,2179,2169,1693,71,129,3015,3035,3371,3431,3113,405,1559,391,1469,63,475,1645,317,2977,1535,1539,3007,3027,685,1851,477,479,483,481,485,693,691)
    GROUP BY t.serviceid
) tickets_filtrados 
    ON tickets_filtrados.serviceid = h.id
LEFT JOIN tblproducts p ON
	h.packageid = p.id
LEFT JOIN tbladdress a ON
	h.id = a.relid
	AND a.subtype = 'INSTALACAO'
LEFT JOIN tblcities c ON
	a.city = c.id
LEFT JOIN tblhostingnetworkconfig nc ON
	h.id = nc.hosting_id
LEFT JOIN tblpartners pt ON
	nc.partnerid = pt.id
LEFT JOIN tblhostingprojects pj ON
	h.hostingprojectid = pj.id
LEFT JOIN tblclients u ON
	h.userid = u.id
WHERE
	h.userid = %s AND h.domainstatus <> 'Cancelled'
