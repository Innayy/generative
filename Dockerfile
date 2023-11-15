# Dockerfile

# pull the official docker image
FROM python:3.11-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy project
COPY ./ /app/

# run project
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
