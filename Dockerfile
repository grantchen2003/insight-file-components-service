FROM python:3.12

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "file_components_service.main"]