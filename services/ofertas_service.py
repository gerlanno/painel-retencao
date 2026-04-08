import pandas as pd
from repositories.ofertas_repository import OfertasRepository
from configs.mapping import format_currency

class OfertasService:

    @staticmethod
    def get_tabelas_booking():
        """
        Retorna as tabelas de ofertas processadas, prontas para exibição na UI.
        Retorno: dicionário com chaves sendo o tipo de oferta e os valores 
        sendo DataFrames formatados ou dicionários complementares.
        """
        data = OfertasRepository.get_booking_data()
        produtos = data.get("connection_products", {})
        
        tabelas = {}
        
        # IP Connect GPON
        gpon_data = produtos.get("ip_connect_gpon", {})
        df_gpon = pd.DataFrame.from_dict(gpon_data.get("pricing", {}), orient="index").reset_index()
        if not df_gpon.empty:
            df_gpon = df_gpon.rename(columns={"index": "Banda", "12m": "12 Meses", "24m": "24 Meses", "36m": "36 Meses"})
            for col in ["12 Meses", "24 Meses", "36 Meses"]:
                if col in df_gpon.columns:
                    df_gpon[col] = df_gpon[col].apply(format_currency)
        tabelas["gpon"] = {
            "unidade": gpon_data.get("unit", "Mbps"),
            "df": df_gpon
        }
        
        # IP Connect Metro
        metro_data = produtos.get("ip_connect_metro", {})
        df_metro = pd.DataFrame.from_dict(metro_data.get("pricing", {}), orient="index").reset_index()
        if not df_metro.empty:
            df_metro = df_metro.rename(columns={"index": "Banda", "12m": "12 Meses", "24m": "24 Meses", "36m": "36 Meses"})
            for col in ["12 Meses", "24 Meses", "36 Meses"]:
                if col in df_metro.columns:
                    df_metro[col] = df_metro[col].apply(format_currency)
        tabelas["metro"] = {
            "unidade": metro_data.get("unit", "Mbps"),
            "df": df_metro
        }
        
        # Lan to Lan
        lan_data = produtos.get("lan_to_lan", {})
        df_lan = pd.DataFrame.from_dict(lan_data.get("pricing", {}), orient="index").reset_index()
        if not df_lan.empty:
            df_lan = df_lan.rename(columns={"index": "Banda", "local": "Local", "intermunicipal": "Intermunicipal", "interestadual": "Interestadual"})
            for col in ["Local", "Intermunicipal", "Interestadual"]:
                if col in df_lan.columns:
                    df_lan[col] = df_lan[col].apply(format_currency)
        tabelas["lan_to_lan"] = {
            "unidade": lan_data.get("unit", "Mbps"),
            "df": df_lan
        }
        
        # Banda Larga IP Fixo
        fixo_data = produtos.get("banda_larga_ip_fixo", {})
        df_fixo = pd.DataFrame.from_dict(fixo_data.get("pricing", {}), orient="index").reset_index()
        if not df_fixo.empty:
            df_fixo = df_fixo.rename(columns={"index": "Banda", "download": "Download", "upload": "Upload", "price": "Preço", "phone_addon": "Adicional Telefone"})
            if "Preço" in df_fixo.columns:
                df_fixo["Preço"] = df_fixo["Preço"].apply(format_currency)
            if "Adicional Telefone" in df_fixo.columns:
                df_fixo["Adicional Telefone"] = df_fixo["Adicional Telefone"].apply(format_currency)
        tabelas["ip_fixo"] = {
            "unidade": fixo_data.get("unit", "Mbps"),
            "df": df_fixo
        }
        
        return tabelas

    @staticmethod
    def get_tabelas_retencao():
        """
        Retorna as tabelas de retenção processadas, prontas para exibição na UI.
        """
        data = OfertasRepository.get_booking_retencao_data()
        produtos = data.get("connection_products_retention", {})
        
        tabelas = {}
        
        # IP Connect GPON
        gpon_data = produtos.get("ip_connect_gpon", {})
        df_gpon = pd.DataFrame.from_dict(gpon_data.get("pricing", {}), orient="index").reset_index()
        if not df_gpon.empty:
            df_gpon = df_gpon.rename(columns={"index": "Banda", "fidelized": "Fidelizado", "12m": "12 Meses", "24m": "24 Meses"})
            for col in ["Fidelizado", "12 Meses", "24 Meses"]:
                if col in df_gpon.columns:
                    df_gpon[col] = df_gpon[col].apply(format_currency)
        tabelas["gpon"] = {
            "unidade": gpon_data.get("unit", "Mbps"),
            "df": df_gpon
        }
        
        # IP Connect Metro
        metro_data = produtos.get("ip_connect_metro", {})
        df_metro = pd.DataFrame.from_dict(metro_data.get("pricing", {}), orient="index").reset_index()
        if not df_metro.empty:
            df_metro = df_metro.rename(columns={"index": "Banda", "fidelized": "Fidelizado", "12m": "12 Meses", "24m": "24 Meses"})
            for col in ["Fidelizado", "12 Meses", "24 Meses"]:
                if col in df_metro.columns:
                    df_metro[col] = df_metro[col].apply(format_currency)
        tabelas["metro"] = {
            "unidade": metro_data.get("unit", "Mbps"),
            "df": df_metro
        }
        
        # Banda Larga IP Fixo
        fixo_data = produtos.get("banda_larga_ip_fixo", {})
        df_fixo = pd.DataFrame.from_dict(fixo_data.get("pricing", {}), orient="index").reset_index()
        if not df_fixo.empty:
            df_fixo = df_fixo.rename(columns={"index": "Banda", "download": "Download", "upload": "Upload", "price": "Preço", "phone_addon": "Adicional Telefone"})
            if "Preço" in df_fixo.columns:
                df_fixo["Preço"] = df_fixo["Preço"].apply(format_currency)
            if "Adicional Telefone" in df_fixo.columns:
                df_fixo["Adicional Telefone"] = df_fixo["Adicional Telefone"].apply(format_currency)
        tabelas["ip_fixo"] = {
            "unidade": fixo_data.get("unit", "Mbps"),
            "df": df_fixo
        }
        
        return tabelas
