FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app/

COPY Pipfile .
COPY Pipfile.lock .


RUN pip install -U pipenv

RUN pipenv install --system

COPY ./app .

# expose the port
EXPOSE 8000

# Command to run
CMD ["./scripts/entrypoint.sh"]