FROM ubuntu:latest
WORKDIR /app
RUN apt update && apt install -y python3  &&  apt install -y python3.14-venv && python3 -m venv /app/venv 
RUN /app/venv/bin/pip install --upgrade pip
COPY . /app
RUN /app/venv/bin/pip install -r requirements.txt
CMD ["/app/venv/bin/python", "/app/app.py"]
