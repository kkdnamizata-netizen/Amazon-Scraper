import os
import pandas as pd

class Saver:
    @staticmethod
    def save_products(products, subfolder, name):
        if not products:
            return
        os.makedirs(subfolder, exist_ok=True)
        data = [p.to_dict() for p in products]
        df = pd.DataFrame(data)

        csv_path = os.path.join(subfolder, f"{name}.csv")
        excel_path = os.path.join(subfolder, f"{name}.xlsx")

        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        try:
            df.to_excel(excel_path, index=False)
        except Exception as e:
            print(f"Erreur lors de l'export Excel: {e}")
