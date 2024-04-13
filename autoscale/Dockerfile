FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir kubernetes
CMD ["python", "./auto_scale_service.py"]
