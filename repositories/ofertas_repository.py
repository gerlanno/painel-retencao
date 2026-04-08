import json
import os

class OfertasRepository:
    
    @staticmethod
    def get_booking_data():
        try:
            file_path = os.path.join("data", "booking_price_table.json")
            if not os.path.exists(file_path):
                return {}
                
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")
            return {}

    @staticmethod
    def get_booking_retencao_data():
        try:
            file_path = os.path.join("data", "booking_retencao_price_table.json")
            if not os.path.exists(file_path):
                return {}
                
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")
            return {}
