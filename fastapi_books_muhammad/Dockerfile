FROM python:3.9

WORKDIR /fastapi_books_muhammad

COPY ./app /fastapi_books_muhammad/app
COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]