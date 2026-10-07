FROM python:3.12-slim

# pull the distribution's security patches so the image scan has nothing
# fixable to complain about; the base image lags behind debian's updates
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd --no-create-home --uid 1000 appuser
USER appuser

EXPOSE 5000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.lending:app"]
