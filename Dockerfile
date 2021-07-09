FROM python:3.8
RUN apt-get update -qq && apt-get install -y postgresql-client
RUN mkdir /quickstart-webhooks
WORKDIR /quickstart-webhooks
COPY requirements.txt /quickstart-webhooks/requirements.txt
RUN pip install -r requirements.txt
COPY . /quickstart-webhooks

# Add a script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--reload"]
