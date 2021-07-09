# Quickstart Webhooks

## Requirements

Simple requirements render happy developers! The only requirements for this quickstart to run are `Docker` and `Compose`! 🐳

## Implemented endpoints

This quickstart implements two basic endpoints:

### `POST /webhook`

This endpoint receives an [Event](https://docs.fintoc.com/reference#eventos) object as the JSON request body. This is the endpoint that should be passed to Fintoc as the Webhook Endpoint. On this quickstart, the events are just being saved to a database, but you could send a push notification to a mobile application or interact with other parts of your application data. The sky is the limit!

### `GET /events`

This endpoint serves just as a validation endpoint for you to confirm that the events are being saved idempotently on the database.

## Local Usage

This quickstart doesn't need to be deployed to a remote server for the webhooks to work. Instead, it starts the server locally, and tunnels it to a public URL using `ngrok`. Let's start!

To try the application, first migrate the database inside the Docker container:

```sh
docker-compose run web flask db upgrade
```

Now, start the development server:

```sh
docker-compose up
```

Because of the usage of `ngrok` to expose the local application to the internet, the last line of the `docker-compose up` command logs should look something like this:

```
ngrok_1  | t=2021-07-09T15:47:35+0000 lvl=info msg="started tunnel" obj=tunnels name=command_line addr=http://web:5000 url=https://4bc029a5ef40.ngrok.io
```

Notice how the last attribute of the log states that `url=https://4bc029a5ef40.ngrok.io` (the random string before `ngrok.io` should change every time that you start the server). This means that the running application can be found at `https://4bc029a5ef40.ngrok.io`, so you would need to create the Webhook Endpoint pointing at `https://4bc029a5ef40.ngrok.io/webhook`.

Once the server is running, go to the [Fintoc Webhooks Dashboard](https://app.fintoc.com/webhooks) and create a new test Webhook Endpoint. This Webhook Endpoint should be pointing to `https://<your-random-string>.ngrok.io/webhook` (remember that this URL will appear on your console after running `docker-compose up`). Now, you can send a test webhook to that Webhook Endpoint, and you console should log the request. Moreover, you should now be able to `GET https://<your-random-string>.ngrok.io/events`, and the test event sent on the test webhook should now be part of the returned array! 🎉

## Deployment to Heroku

You can also run this from Heroku instead of using `ngrok` and your local machine! To run from Heroku, you can follow these steps:

First, create a new Heroku app:

```sh
heroku create
```

This should show on the console the name of the newly created application. From now on, `<app-name>` should be replaced with that name.

Then, add the `heroku-postgresql` addon to the Heroku app:

```sh
heroku addons:create -a <app-name> heroku-postgresql:hobby-dev
```

This command will add the **free** basic `heroku-postgresql` addon to your app (you can upgrade this later if you desire).

Next, build the image and push it to Container Registry:

```sh
heroku container:push -a <app-name> web
```

Now, release the image to your app:

```sh
heroku container:release -a <app-name> web
```

Finally, run the database migrations:

```sh
heroku run -a <app-name> flask db upgrade
```

Remember to add a secret key on the Heroku environment, using the `SQLALCHEMY_SECRET_KEY` key.

You should now be able to use `<app-name>.herokuapp.com/webhook` as the Webhook Endpoint from the [Fintoc Webhooks Dashboard](https://app.fintoc.com/webhooks)!
