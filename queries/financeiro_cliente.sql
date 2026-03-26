SELECT
    COUNT(*) AS faturas_abertas,
    SUM(total) AS valor_aberto,
    MAX(duedate) AS ultima_fatura
FROM
    tblinvoices
WHERE
    userid = %s
    AND STATUS = 'Unpaid'