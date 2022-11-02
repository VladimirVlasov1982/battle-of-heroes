FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./

CMD flask run -h 0.0.0.0 -p 80