# API para Generación de Gráficos desde Dataset de Kaggle

Esta API utiliza un dataset de Kaggle para generar gráficos relacionados con los precios de vuelos y su distribución entre aerolíneas. Puedes acceder a las rutas disponibles para descargar estos gráficos.

## Requisitos

- Python 3.12+
- Flask
- pandas
- matplotlib
- seaborn
- kaggle

## Instalación

1. Clona el repositorio en tu máquina local:
   ```bash
   git clone https://github.com/Pokerk999/EntregaETL.git
   cd EntregaETL


Use sudo docker compose build para construir la imagen y sudo docker compose up para ejecutarla.
 
curl http://127.0.0.1:5000/download --output histograma.png
curl http://127.0.0.1:5000/aerolineas --output aerolineas.png

