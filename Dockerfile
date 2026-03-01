FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY flask.py .
COPY quickdraw_crab_fish_model.keras .
COPY templates/ templates/
COPY static/ static/

EXPOSE 5002

CMD ["python", "flask.py"]
