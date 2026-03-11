# Mapeamento de Dados Atrixcore

Este documento mapeia as tabelas e campos do banco de dados `atrixcore` utilizados no projeto.

| Tabela                            | Campo Banco          | Observação                                        |
| :-------------------------------- | :------------------- | :------------------------------------------------ |
| **tbltickets**                    | id                   | ID interno do ticket                              |
|                                   | date                 | Data de abertura do ticket                        |
|                                   | dateclosed           | Data de encerramento do ticket                    |
|                                   | tid                  | Protocolo/TID do ticket                           |
|                                   | userid               | ID do cliente associado                           |
|                                   | serviceid            | ID do serviço/hosting associado                   |
|                                   | did                  | ID do departamento atual                          |
|                                   | deptrequester        | ID do departamento que abriu o ticket             |
|                                   | status               | Status do ticket (Open, Closed, etc)              |
|                                   | substatusid          | ID do substatus do ticket                         |
|                                   | title                | Título/Assunto do ticket                          |
|                                   | flag                 | Analista designado (ID)                           |
|                                   | useropen             | Analista que abriu o ticket (ID)                  |
|                                   | forecast             | Previsão de entrega/forecast                      |
|                                   | partnerid            | ID do parceiro associado                          |
|                                   | normalization_date   | Data de normalização (campo customizado)          |
|                                   | merged_ticket_id     | IDs de tickets mesclados                          |
|                                   | bdeskprotocol        | Protocolo do BDesk                                |
|                                   | type                 | Tipo de log/alteração                             |
| **tblclients**                    | id                   | ID do cliente                                     |
|                                   | companyname          | Nome da empresa/Nome fantasia                     |
|                                   | firstname            | Primeiro nome do contato                          |
|                                   | lastname             | Sobrenome do contato                              |
|                                   | document             | CPF ou CNPJ (usado na busca)                      |
|                                   | segmentid            | ID do segmento do cliente                         |
|                                   | address1             | Endereço (Logradouro)                             |
|                                   | address2             | Bairro                                            |
|                                   | number               | Número do endereço                                |
|                                   | complement           | Complemento do endereço                           |
|                                   | city                 | Cidade                                            |
|                                   | state                | Estado (UF)                                       |
|                                   | postcode             | CEP                                               |
|                                   | country              | País                                              |
|                                   | phonenumber          | Número de telefone                                |
|                                   | email                | E-mail de contato                                 |
|                                   | manageraccount       | Gerente de contas (ID do admin)                   |
|                                   | priority             | Criticidade/Prioridade do cliente                 |
| **tblhosting**                    | id                   | ID do serviço contratado                          |
|                                   | userid               | ID do cliente dono do serviço                     |
|                                   | packageid            | ID do pacote/produto (tblproducts)                |
|                                   | domain               | Domínio ou identificador do serviço               |
|                                   | amount               | Valor mensal/recorrente                           |
|                                   | firstpaymentamount   | Valor do primeiro pagamento                       |
|                                   | billingcycle         | Ciclo de faturamento (Monthly, Annually, etc)     |
|                                   | domainstatus         | Status do serviço (Active, Suspended, etc)        |
|                                   | regdate              | Data do registro                                  |
|                                   | nextduedate          | Próximo vencimento                                |
|                                   | nextinvoicedate      | Próxima data de fatura                            |
|                                   | termination_date     | Data de cancelamento/término                      |
|                                   | paymentmethod        | Forma de pagamento                                |
|                                   | promoid              | ID da promoção aplicada                           |
|                                   | server               | ID do servidor associado                          |
|                                   | numplan              | Número do plano                                   |
|                                   | designator           | Designador do serviço/circuito                    |
|                                   | designator_old       | Designador antigo                                 |
|                                   | notes                | Observações fiscais                               |
|                                   | dateactivate         | Data de ativação                                  |
|                                   | datecontract         | Data do contrato                                  |
|                                   | datecancellation     | Data de cancelamento                              |
|                                   | bitrixbusinessnumber | Número do negócio no Bitrix                       |
|                                   | migratedfrom         | Origem do cadastro (Atrix, etc)                   |
|                                   | obs                  | Observações gerais                                |
| **tbladdress**                    | id                   | ID do registro de endereço                        |
|                                   | relid                | ID relacionado (geralmente tblhosting.id)         |
|                                   | subtype              | Tipo de endereço (ex: 'INSTALACAO')               |
|                                   | address              | Logradouro completo                               |
|                                   | neighborhood         | Bairro                                            |
|                                   | number               | Número                                            |
|                                   | complement           | Complemento                                       |
|                                   | city                 | ID da cidade (relaciona com tblcities)            |
|                                   | citydesc             | Descrição/Nome da cidade                          |
|                                   | state                | Estado (UF)                                       |
|                                   | postcode             | CEP                                               |
|                                   | latitude             | Coordenada latitude                               |
|                                   | longitude            | Coordenada longitude                              |
| **tblticketdepartments**          | id                   | ID do departamento                                |
|                                   | name                 | Nome do departamento                              |
| **tblclientsegment**              | id                   | ID do segmento                                    |
|                                   | name                 | Nome do segmento (ex: Gold, Platinum)             |
| **tblhostingprojects**            | id                   | ID do projeto                                     |
|                                   | name                 | Nome do projeto associado ao serviço              |
| **tblproducts**                   | id                   | ID do produto                                     |
|                                   | name                 | Nome do produto                                   |
|                                   | cnl_service          | Código/Identificador do serviço CNL               |
| **tbltickettyperequest**          | id                   | ID do tipo de solicitação                         |
|                                   | title                | Descrição do tipo de solicitação                  |
| **tblticketsubstatus**            | id                   | ID do substatus                                   |
|                                   | name                 | Nome do substatus                                 |
| **tblticketlogs**                 | id                   | ID do log                                         |
|                                   | ticketid             | ID do ticket relacionado                          |
|                                   | adminid              | ID do administrador que gerou o log               |
|                                   | created_at           | Data e hora do log                                |
|                                   | type                 | Tipo de alteração (status, did, substatusid, etc) |
|                                   | oldvalue             | Valor anterior                                    |
|                                   | newvalue             | Novo valor                                        |
|                                   | description          | Descrição da alteração                            |
| **tblticketnotes**                | id                   | ID da nota                                        |
|                                   | ticketid             | ID do ticket                                      |
|                                   | message              | Conteúdo da nota/comentário                       |
| **tbladmins**                     | id                   | ID do administrador                               |
|                                   | username             | Login do administrador                            |
|                                   | firstname            | Nome do admin                                     |
|                                   | lastname             | Sobrenome do admin                                |
| **tblpartners**                   | id                   | ID do parceiro                                    |
|                                   | name                 | Nome do parceiro                                  |
| **tblhostingnetworkconfig**       | hosting_id           | ID do serviço (relacionado ao tblhosting)         |
|                                   | technology_id        | ID da tecnologia (relaciona tblnetworktechnology) |
|                                   | provider_id          | ID do fornecedor (relaciona tblnetworkprovider)   |
|                                   | partnerid            | ID do parceiro técnico                            |
|                                   | serial               | Serial do equipamento                             |
|                                   | serial_code          | Código serial (S/N)                               |
|                                   | mac                  | Endereço MAC                                      |
|                                   | pop                  | Ponto de presença                                 |
|                                   | gateway              | Gateway de rede                                   |
|                                   | interface_1          | Interface 1                                       |
|                                   | interface_2          | Interface 2                                       |
|                                   | access_point         | Ponto de acesso                                   |
|                                   | cpe                  | Equipamento CPE                                   |
|                                   | ip_management        | IP de gerência                                    |
|                                   | ip_telephony         | IP de telefonia                                   |
|                                   | ip_block             | Bloco de IPs                                      |
|                                   | vlan                 | VLAN ID                                           |
|                                   | login_pppoe          | Login PPPoE                                       |
|                                   | asn                  | ASN                                               |
|                                   | prefixes             | Prefixos de rede                                  |
|                                   | onu_id               | ID da ONU                                         |
|                                   | pon_port             | Porta PON                                         |
|                                   | model_onu            | Modelo da ONU                                     |
|                                   | slot                 | Slot do chassi                                    |
|                                   | wifi_ssid            | Nome da rede Wi-Fi                                |
|                                   | wifi_passcode        | Senha da rede Wi-Fi                               |
|                                   | circuitpartner       | Circuito do parceiro                              |
|                                   | obs                  | Observações técnicas                              |
| **tblnetworktechnology**          | id                   | ID da tecnologia                                  |
|                                   | name                 | Nome da tecnologia (ex: FTTH, Radio)              |
| **tblnetworkprovider**            | id                   | ID do provedor/fornecedor                         |
|                                   | name                 | Nome do fornecedor de rede                        |
| **tblcities**                     | id                   | ID da cidade                                      |
|                                   | name                 | Nome da cidade                                    |
| **tblhostingconfigoptions**       | relid                | ID do serviço relacionado (tblhosting)            |
|                                   | configid             | ID da configuração (tblproductconfigoptions)      |
|                                   | optionid             | ID da opção (tblproductconfigoptionssub)          |
| **tblproductconfigoptions**       | id                   | ID da categoria de configuração                   |
|                                   | optionname           | Nome da categoria (TECNOLOGIA, VELOCIDADES, etc)  |
| **tblproductconfigoptionssub**    | id                   | ID da sub-opção                                   |
|                                   | optionname           | Valor da opção (ex: 100MB, Fibra)                 |
| **tblchannels**                   | id                   | ID do canal de atendimento                        |
|                                   | name                 | Nome do canal (Telefone, Whatsapp, etc)           |
| **tblticketcloseclassifications** | id                   | ID da classificação de fechamento                 |
|                                   | name                 | Nome da classificação                             |
| **tblpromotions**                 | id                   | ID da promoção                                    |
|                                   | code                 | Código promocional                                |
| **tblservers**                    | id                   | ID do servidor                                    |
|                                   | name                 | Nome do servidor                                  |
| **tblticketemaillogs**            | ticketid             | ID do ticket relacionado ao e-mail                |
|                                   | created_at           | Data do log de e-mail                             |
|                                   | acaoOrigem           | Origem (ex: 'recebida')                           |
| **tblprocessingqueue**            | elementid            | ID do elemento (ex: protocolo do ticket)          |
|                                   | operationType        | Tipo de operação (ex: ticket-update-status)       |
|                                   | jsonData             | Dados da operação em formato JSON                 |
