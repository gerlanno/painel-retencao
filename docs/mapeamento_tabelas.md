# Mapeamento de Tabelas do Banco de Dados

Este documento mantém o registro das tabelas referenciadas pelo Painel de Retenção para facilitar manutenções futuras.

## Tabela: `tbldiscount`

Utilizada para calcular e exibir o histórico de descontos e isenções dados a um serviço específico (relid).

```sql
CREATE TABLE `tbldiscount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `relid` int(11) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `qtd` int(1) DEFAULT NULL,
  `qtd_rest` int(1) DEFAULT NULL,
  `type` enum('quantity','recurrent') DEFAULT NULL,
  `value` decimal(10,2) DEFAULT NULL,
  `adminid` int(11) DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `category` enum('discount','addition') DEFAULT 'discount',
  `typevalue` enum('nominal','percent') DEFAULT 'nominal',
  `typerecord` varchar(50) DEFAULT NULL,
  `datebegin` date DEFAULT NULL,
  `dateend` date DEFAULT NULL,
  `skipNextInvoice` tinyint(1) NOT NULL DEFAULT '0',
  `nextInvoiceSkipped` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `idx_relid` (`relid`)
) ENGINE=InnoDB AUTO_INCREMENT=402678 DEFAULT CHARSET=latin1;
```
