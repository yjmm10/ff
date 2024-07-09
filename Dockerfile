FROM python:3.10

LABEL name="FF"
LABEL version="0.1.0"
LABEL description="About python common file handling functions for all your needs."

WORKDIR /app

ADD . ./

# CMD ["python"]