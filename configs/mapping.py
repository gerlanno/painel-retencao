from datetime import datetime, date

def format_currency(value):
    if value is None:
        return "R$ 0,00"
    try:
        val_float = float(value)
        return f"R$ {val_float:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        return str(value)

def format_date(dt, include_time=False):
    """
    Converte um objeto de data/hora (ou string ISO) para o padrão brasileiro.
    Padrão: DD/MM/AAAA ou DD/MM/AAAA HH:MM:SS
    """
    if dt is None:
        return "-"
    
    # Se for string (ex: do Atrix em alguns casos), tenta converter
    if isinstance(dt, str):
        try:
            # Tenta formatos comuns
            if " " in dt:
                dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            else:
                dt = datetime.strptime(dt, "%Y-%m-%d")
        except:
            return dt

    if include_time and isinstance(dt, (datetime)):
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    
    return dt.strftime("%d/%m/%Y")

def formatar_cnpj(cnpj_input):
    """
    Recebe uma string de CNPJ. Se contiver apenas números e tiver 14 dígitos, 
    aplica a máscara (XX.XXX.XXX/XXXX-XX). 
    Caso contrário, devolve a própria string.
    """
    apenas_numeros = "".join(filter(str.isdigit, str(cnpj_input)))
    if len(apenas_numeros) == 14:
        return f"{apenas_numeros[:2]}.{apenas_numeros[2:5]}.{apenas_numeros[5:8]}/{apenas_numeros[8:12]}-{apenas_numeros[12:]}"
    return cnpj_input

# Mapeamento de Status (Tradução Inglês -> Português)

STATUS_SERVICO = {
    "Active": "Ativo",
    "Cancelled": "Cancelado",
    "Pending": "Pendente",
    "Suspended": "Suspenso",
    "Terminated": "Terminado",
    "Completed": "Concluído"
}

STATUS_TICKET = {
    "Open": "Aberto",
    "Closed": "Fechado",
    "Cancelled": "Cancelado",
    "In Progress": "Em Andamento",
    "Answered": "Respondido",
    "Customer-Reply": "Resposta do Cliente",
    "On Hold": "Em Espera",
    "Awaiting-Reply": "Aguardando Resposta"
}

def traduzir_status(status, mapeamento):
    """
    Traduz um status utilizando um dos dicionários de mapeamento.
    Caso o status não seja encontrado, retorna o original.
    """
    if not status:
        return "-"
    return mapeamento.get(status, status)

# Mapeamento de Clusters de Motivos de Ticket por Palavras-Chave (Substrings)
MOTIVO_KEYWORDS = {
    "Técnicos": [
        "INDISPONIBILIDADE", "LENTIDÃO", "LENTIDAO", "OSCILAÇÃO", "OSCILACAO", "CONFIGURAÇÃO", "CONFIGURACAO",
        "FALHA", "ROTEAMENTO", "WIFI", "WI-FI", "EQUIPAMENTO", "REPARO", "PERFORMANCE", "QUEDA", 
        "ROTEADOR", "ONU", "GPON", "FIBRA", "ROMPIMENTO", "LUZ VERMELHA", "LOS", "PING", "LATÊNCIA", "LATENCIA",
        "JITTER", "PERDA", "ACESSO", "IP", "PORTA", "SENHA", "MODEM", "SINAL"
    ],
    "Administrativos": [
        "DESCONTO", "ANÁLISE DE DESCONTO", "VENCIMENTO", "CANCELAMENTO", "CANCELA",
        "ENDEREÇO", "ENDERECO", "MUDANÇA", "MUDANCA", "TRANSFERÊNCIA", "TRANSFERENCIA", "TITULARIDADE", "CADASTRO",
        "CONTRATO", "ASSINATURA", "VISITA", "REAGENDAMENTO"
    ],
    "Financeiros": [
        "BOLETO", "FATURA", "PAGAMENTO", "BLOQUEIO", "DESBLOQUEIO", "CONFIANÇA", "CONFIANCA",
        "NEGOCIAÇÃO", "NEGOCIACAO", "MENSALIDADE", "COBRANÇA", "COBRANCA", "ISENÇÃO", "ISENCAO", "ACORDO",
        "PIX", "CARTÃO", "CARTAO", "PROMESSA", "RETENÇÃO", "JUROS", "MULTA", "ESTORNO"
    ],
    "Comerciais": [
        "UPGRADE", "DOWNGRADE", "NOVO PONTO", "PLANO", "VELOCIDADE", "PONTO EXTRA", "VENDA", "RENOVAÇÃO", "RENOVACAO", "ADESÃO"
    ]
}

def classificar_motivo(motivo_texto):
    """
    Classifica um motivo de ticket aberto (ex: LENTIDÃO NA REDE DE DADOS) para 
    um cluster estratégico maior (ex: Técnicos) analisando substrings textuais.
    Ignora case e espaços durante a checagem.
    """
    if not motivo_texto:
        return "Outros"
    
    texto = str(motivo_texto).strip().upper()
    
    # Busca por correspondência parcial (substring)
    for cluster, keywords in MOTIVO_KEYWORDS.items():
        for keyword in keywords:
            if keyword in texto:
                return cluster
                
    return "Outros"

def format_sla(minutes):
    """
    Converte minutos em uma string formatada (Ex: 1d 4h 30m, 2h 15m ou 45m).
    """
    if minutes is None or minutes == "-":
        return "-"
    
    try:
        total_min = int(float(minutes))
    except (ValueError, TypeError):
        return str(minutes)

    if total_min < 0:
        return "0m"

    days = total_min // 1440
    remaining_min = total_min % 1440
    hours = remaining_min // 60
    mins = remaining_min % 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if mins > 0 or (days == 0 and hours == 0):
        parts.append(f"{mins}m")

    return " ".join(parts)
