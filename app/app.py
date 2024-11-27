import os,io
from flask import Flask, send_file
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


app = Flask(__name__)

api = KaggleApi()

@app.route("/")
def home():
    return "Bienvenido a la API. Usa la ruta /download para descargar una grafico de uno de los dataset de Kaggle."

@app.route("/download", methods=["GET"] )
def download_dataset():

    api.authenticate()
    api.dataset_download_files('shubhambathwal/flight-price-prediction', path='.', unzip=True)
    dataset_path = './'
    file_name = 'economy.csv'
    file_path = os.path.join(dataset_path, file_name)
    if not os.path.exists(file_path):
        return "El archivo CSV no fue encontrado tras la descarga.", 404
    
    df = pd.read_csv(file_path)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], kde=True, bins=30)
    plt.title('Distribución de Precios')
    plt.xlabel('Precio')
    plt.ylabel('Frecuencia')
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png', as_attachment=False, download_name="histograma.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
