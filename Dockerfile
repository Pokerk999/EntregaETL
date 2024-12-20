FROM python:3.12-slim

WORKDIR /app

COPY ./app /app

COPY ./app/kaggle.json /root/.config/kaggle/kaggle.json

RUN chmod 600 /root/.config/kaggle/kaggle.json

RUN pip install --no-cache-dir flask pandas kaggle seaborn

CMD ["python", "app.py"]
