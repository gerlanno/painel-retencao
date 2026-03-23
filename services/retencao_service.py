from repositories.cliente_repository import ClienteRepository
from repositories.servicos_cliente import ServicoRepository
from repositories.tickets_repository import TicketRepository
from repositories.financeiro_repository import FinanceiroRepository
from repositories.diagnostico_repository import DiagnosticoRepository
from configs.mapping import STATUS_SERVICO, STATUS_TICKET, traduzir_status, format_date, classificar_motivo


class RetencaoService:

    @staticmethod
    def _gerar_mini_diagnostico(diagnostico, financeiro):
        t30 = diagnostico.get("tickets_30d") if diagnostico else 0
        if t30 is None:
            t30 = 0
            
        motivos = diagnostico.get("motivos_90d", [])
        if motivos and len(motivos) > 0:
            principal_motivo = motivos[0]["motivo"]
        else:
            principal_motivo = "Não especificado"
            
        # 📈 Score Multidimensional
        score = 0
        
        # 1. Volume vs Recência
        if t30 >= 5: score += 40
        elif t30 >= 2: score += 20
        
        # 2. Motivo (Indisponibilidade é crítico)
        if "INDISPONIBILIDADE" in principal_motivo.upper() or "QUEDA" in principal_motivo.upper():
            score += 30
            
        # 3. SLA (Se tem muito histórico demorado)
        sla = diagnostico.get("sla_90d", {})
        sla_medio_str = str(sla.get("sla_medio_horas", "-")).replace("h", "")
        if sla_medio_str.isdigit() and int(sla_medio_str) > 24:
            score += 20
            
        # 4. Financeiro
        if financeiro and financeiro.get("faturas_abertas", 0) > 0:
            score += 10
            
        if score == 0:
            return None # Nenhum risco
            
        if score >= 50:
            severidade = "Crítico"
            alerta = "alto risco de churn"
        else:
            severidade = "Atenção"
            alerta = "instabilidade ou atrito detectado"

        return f"🚨 **{severidade}:** {alerta.capitalize()} (Score Churn: {score}/100). Cliente abriu {t30} tickets curtos. Dor principal: '{principal_motivo}'."

    @staticmethod
    def get_painel_cliente(cnpj, servico_id=None):

        # 1️⃣ Buscar cliente
        cliente = ClienteRepository.get_by_cnpj(cnpj)

        if not cliente:
            return None

        cliente_id = cliente["id"]

        # 2️⃣ Buscar serviços
        servicos = ServicoRepository.listar_por_cliente(cliente_id)

        if not servicos:
            return {
                "cliente": cliente,
                "servicos": [],
                "servico_selecionado": None,
                "diagnostico": None,
                "tickets": [],
                "financeiro": None
            }

        # 3️⃣ Determinar serviço selecionado
        servicos_ativos = [s for s in servicos if s["domainstatus"] == "Active"]

        if servico_id:
            servico_selecionado = next(
                (s for s in servicos if s["servico_id"] == servico_id),
                servicos_ativos[0] if servicos_ativos else servicos[0]
            )

        else:
            servico_selecionado = servicos_ativos[0] if servicos_ativos else servicos[0]

        servico_id = servico_selecionado["servico_id"]

        # 4️⃣ Diagnóstico
        diagnostico = DiagnosticoRepository.get_diagnostico(servico_id)

        # 5️⃣ Tickets
        tickets = TicketRepository.listar_por_servico(servico_id)

        # 6️⃣ Financeiro e Descontos        
        financeiro = FinanceiroRepository.get_resumo(cliente_id)
        descontos = FinanceiroRepository.get_descontos_servico(servico_id)
        
        # Consolidação de total de descontos
        total_desconto = sum(d.get("value", 0) for d in descontos) if descontos else 0
        servico_selecionado["descontos"] = descontos
        servico_selecionado["total_desconto"] = total_desconto

        # 💲 Faturas do Serviço (API Atrix)
        from datetime import datetime
        hoje = datetime.now().date()
        faturas_brutas = FinanceiroRepository.get_faturas_servico(servico_id)
        
        faturas_servico_abertas = 0
        valor_servico_aberto = 0.0
        dias_max_atraso = 0
        datas_faturas = []
        faturas_tratadas = []
        
        for f in faturas_brutas:
            status_fatura = f.get("status", "")
            
            # Tratamento de valores para garantir formato correto
            valor_float = 0.0
            try:
                valor_float = float(f.get("total", 0))
            except ValueError:
                pass
                
            duedate_str = f.get("duedate", "")
            atraso_view = 0
            
            if status_fatura == "Unpaid":
                faturas_servico_abertas += 1
                valor_servico_aberto += valor_float
                if duedate_str:
                    try:
                        duedate_dt = datetime.strptime(duedate_str, "%Y-%m-%d").date()
                        atraso = (hoje - duedate_dt).days
                        if atraso > dias_max_atraso:
                            dias_max_atraso = atraso
                        if atraso > 0:
                            atraso_view = atraso
                    except Exception:
                        pass
                        
            # Guardar datas para descobrir a última fatura
            date_str = f.get("date") or duedate_str
            if date_str:
                try:
                    datas_faturas.append(datetime.strptime(date_str, "%Y-%m-%d").date())
                except Exception:
                    pass
            
            # Formatar itens da visualização (DETALHE tabela)
            status_traduzido = "Paga" if status_fatura == "Paid" else ("Aberta" if status_fatura == "Unpaid" else ("Cancelada" if status_fatura == "Cancelled" else status_fatura))
            
            vencimento_view = ""
            if duedate_str:
                try:
                    vencimento_view = datetime.strptime(duedate_str, "%Y-%m-%d").strftime("%d/%m")
                except:
                    vencimento_view = duedate_str
                    
            faturas_tratadas.append({
                "vencimento_sort": duedate_str,
                "Vencimento": vencimento_view,
                "Valor": valor_float,
                "Status": status_traduzido,
                "Dias atraso": atraso_view
            })
            
        # Ordenar decrescente pelo vencimento (para mostrar últimas no topo da tabela)
        faturas_tratadas = sorted(faturas_tratadas, key=lambda x: str(x.get("vencimento_sort", "")), reverse=True)
        # Remover a chave de ordenação
        for f in faturas_tratadas:
            if "vencimento_sort" in f:
                del f["vencimento_sort"]

        ultima_fatura_dt = max(datas_faturas) if datas_faturas else None
        ultima_fatura_view = ultima_fatura_dt.strftime("%d/%m") if ultima_fatura_dt else "-"
        
        financeiro_servico = {
            "faturas": faturas_tratadas,
            "faturas_abertas": faturas_servico_abertas,
            "valor_aberto": valor_servico_aberto,
            "dias_atraso": dias_max_atraso,
            "ultima_fatura": ultima_fatura_view
        }

        # 🔄 Traduções e Formatações
        for s in servicos:
            s["domainstatus"] = traduzir_status(s["domainstatus"], STATUS_SERVICO)
            s["regdate"] = format_date(s["regdate"])
            
            # 🚦 Lógica de Saúde
            t90 = s.get("tickets_90d")
            if t90 is None:
                t90 = 0
                
            if s["domainstatus"] == "Cancelado":
                s["saude"] = "-"
            elif t90 == 0:
                s["saude"] = "🟢"
            elif t90 <= 5:
                s["saude"] = "🟡"
            else:
                s["saude"] = "🔴"
        
        for t in tickets:
            t["status"] = traduzir_status(t["status"], STATUS_TICKET)
            t["date"] = format_date(t["date"], include_time=True)
            t["dateclosed"] = format_date(t["dateclosed"], include_time=True)
            
            # Formatar SLA do ticket individual
            if t.get("sla_horas") is not None:
                t["sla_horas"] = f"{int(t['sla_horas'])}h"
            else:
                t["sla_horas"] = "-"
                
            # Tratar nulidades nos campos de apoio e classificar motivo
            motivo_sujo = t.get("motivo") or "Não especificado"
            t["motivo"] = " ".join(str(motivo_sujo).upper().replace("-", "").strip().split())
            t["classificacao"] = t.get("classificacao") or "Não especificado"
            t["departamento"] = t.get("departamento") or "Não especificado"
            t["cluster"] = classificar_motivo(t["motivo"])

        if diagnostico:
            diagnostico["ultimo_ticket"] = format_date(diagnostico["ultimo_ticket"], include_time=True)
            
            # 📊 Clusterização de Motivos
            clusters_count = {}
            for m in diagnostico.get("motivos_90d", []):
                motivo_sujo = m.get("motivo") or "Não especificado"
                motivo_limpo = " ".join(str(motivo_sujo).upper().replace("-", "").strip().split())
                m["motivo"] = motivo_limpo
                
                total = m["total"]
                cluster_nome = classificar_motivo(motivo_limpo)
                clusters_count[cluster_nome] = clusters_count.get(cluster_nome, 0) + total
            
            # Formatar para lista ordenada
            diagnostico["clusters_90d"] = [{"cluster": k, "total": v} for k, v in sorted(clusters_count.items(), key=lambda item: item[1], reverse=True)]
            
            # ⏱️ Formatação do SLA
            sla = diagnostico.get("sla_90d")
            if sla and sla.get("sla_medio_horas") is not None:
                sla["sla_medio_horas"] = f"{int(sla['sla_medio_horas'])}h"
                sla["sla_max_horas"] = f"{int(sla['sla_max_horas'])}h"
                
                # Calcular porcentagem < 24h
                total_resolvidos = sla.get("total_resolvidos_90d", 0)
                resolvidos_24h = sla.get("resolvidos_24h_90d", 0)
                if total_resolvidos > 0:
                    pct = (resolvidos_24h / total_resolvidos) * 100
                    sla["resolvidos_24h_pct"] = f"{pct:.1f}%"
                else:
                    sla["resolvidos_24h_pct"] = "0%"
            else:
                diagnostico["sla_90d"] = {"sla_medio_horas": "-", "sla_max_horas": "-", "resolvidos_24h_pct": "-"}
            
            # 🚨 Mini Diagnóstico
            diagnostico["mini_diagnostico"] = RetencaoService._gerar_mini_diagnostico(diagnostico, financeiro)
        
        if financeiro:
            financeiro["ultima_fatura"] = format_date(financeiro["ultima_fatura"])

        # 7️⃣ Montar objeto final
        painel = {
            "cliente": cliente,
            "servicos": servicos,
            "servico_selecionado": servico_selecionado,
            "diagnostico": diagnostico,
            "tickets": tickets,
            "financeiro": financeiro,
            "financeiro_servico": financeiro_servico
        }

        return painel