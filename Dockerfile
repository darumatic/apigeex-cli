FROM python:3-slim
COPY . /app
RUN pip3 install -r /app/requirements.txt
WORKDIR /app
