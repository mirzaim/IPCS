FROM python:3.9 

WORKDIR /ipcs
COPY ./src .

RUN pip install -r requirements.txt

RUN mkdir -p output
CMD ["python", "./main.py", "configs/docker.ini"]
