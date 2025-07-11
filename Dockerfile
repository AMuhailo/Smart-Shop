FROM python:3.12.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["gunicorn", "myshop.wsgi", "--bind", "0.0.0.0:8000"]