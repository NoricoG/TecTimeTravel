FROM python:3.7.4

WORKDIR /usr/src/app

COPY load/opensky/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

ENV PYTHONUNBUFFERED 1

CMD [ "python", "./load/opensky/schedule.py"]