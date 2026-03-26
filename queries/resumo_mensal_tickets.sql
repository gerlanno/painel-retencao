SELECT
  DATE_FORMAT(date, '%Y-%m') AS mes_ordem,
  DATE_FORMAT(date, '%m/%Y') AS mes_nome,
  COUNT(*) AS total
FROM
  tbltickets
WHERE
  serviceid = %s
  AND date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY
  mes_ordem,
  mes_nome
ORDER BY
  mes_ordem ASC;