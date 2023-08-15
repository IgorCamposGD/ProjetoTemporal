FROM python:3.8
WORKDIR /py
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt 
