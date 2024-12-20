from contextlib import contextmanager
import os,io
from flask import Flask, send_file
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


app = Flask(__name__)

api = KaggleApi()

@contextmanager
def open_csv(file_path: str):
    try:
        df = pd.read_csv(file_path)
        yield df  
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        yield None  
    finally:
        print("Proceso de lectura de archivo completado.")

@app.route("/")
def home():
    return "Bienvenido a la API. Usa la ruta /download para descargar una grafico de uno de los dataset de Kaggle."

@app.route("/download", methods=["GET"])
def download_dataset():
    api.authenticate()
    api.dataset_download_files('shubhambathwal/flight-price-prediction', path='.', unzip=True)
    
    dataset_path: str = './'
    file_name: str = 'economy.csv'
    file_path: str = os.path.join(dataset_path, file_name)

    if not os.path.exists(file_path):
        return "El archivo CSV no fue encontrado tras la descarga.", 404
    
    with open_csv(file_path) as df:
        if df is None:
            return "No se pudo leer el archivo CSV.", 500

        plt.figure(figsize=(10, 6))
        sns.histplot(df['price'], kde=True, bins=30)
        plt.title('Distribución de Precios')
        plt.xlabel('Precio')
        plt.ylabel('Frecuencia')

        img_bytes: io.BytesIO = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png', as_attachment=False, download_name="histograma.png")


@app.route("/aerolineas", methods=["GET"])
def download_companies_dataset():
    api.authenticate()
    api.dataset_download_files('shubhambathwal/flight-price-prediction', path='.', unzip=True)
    
    dataset_path: str = './'
    file_name: str = 'economy.csv'
    file_path: str = os.path.join(dataset_path, file_name)

    if not os.path.exists(file_path):
        return "El archivo CSV no fue encontrado tras la descarga.", 404
    
    with open_csv(file_path) as df:
        if df is None:
            return "No se pudo leer el archivo CSV.", 500

        if "price" not in df.columns:
            return "La columna 'price' no existe en el archivo CSV.", 404

        com_counts = df['airline'].value_counts()
        com_counts_table = pd.DataFrame(com_counts)
        
        plt.figure(figsize=(10, 6))
        fig, ax = plt.subplots()
        ax.pie(com_counts_table.values.squeeze(), labels=com_counts_table.index, autopct='%1.1f%%', shadow=True)
        plt.title('Distribución de Aerolíneas')
        
        img_bytes: io.BytesIO = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png', as_attachment=False, download_name="aerolineas.png")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
