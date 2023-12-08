FROM python:3.10
WORKDIR /app
RUN apt-get update && apt-get install -y cmake
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./main.py ./
CMD ["python", "main.py"]
EXPOSE 8000
