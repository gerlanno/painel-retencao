SELECT
    id,
    description,
    CASE LOWER(TRIM(category))
        WHEN 'discount'       THEN 'Desconto'
        WHEN 'addition'     THEN 'Adicional'
        ELSE category
    END AS Categoria,
    value,
    typevalue,
    datebegin,
    dateend
FROM tbldiscount
WHERE relid = %s
ORDER BY id DESC
