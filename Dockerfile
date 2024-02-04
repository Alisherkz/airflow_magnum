FROM apache/airflow:latest
RUN echo -e "AIRFLOW_UID=$(id -u)" > .env
COPY requirements.txt .

USER root
RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl
USER airflow

RUN pip install --no-cache-dir -r requirements.txt