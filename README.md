# Short Messages API

## https://short-messages-api.herokuapp.com/

## General info

A web application made using Python 3, Django 2, Django Rest Framework and PostgreSQL.  
<br/>Application allows creating users, generating tokens and performing CRUD operations on Message model.

## Main functions

* creating users
* generating tokens
* creating, updating, displaying and deleting messages

## Technologies

* Python 3.7
* Django 2.2
* Django Rest Framework
* PostgreSQL

## Setup

To run this project locally:

1. In docker-compose.yaml replace `temporary_secret_key` with your own secret
   key (https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/#secret-key)
2. Start containers with

```
docker-compose up
```

3. Application will be available at `http://0.0.0.0:8000/`

## Endpoints

* Create user </br>
  POST </br>
  https://short-messages-api.herokuapp.com/api/v1/user/create/

![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/create_user.png)

* Request token </br>
  POST </br>
  https://short-messages-api.herokuapp.com/api/v1/user/token/

![alt text](https://raw.githubusercontentcom/dawidbudzynski/short-messages-api/main/demo_image/request_token.png)

* Message list </br>
  GET </br>
  https://short-messages-api.herokuapp.com/api/v1/message/list/

![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/list_messages.png)

* Message details </br>
  GET </br>
  https://short-messages-api.herokuapp.com/api/v1/message/details/4 <message_id>

![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/details_message.png)

* Create message (require authorizations) </br>
  POST </br>
  https://short-messages-api.herokuapp.com/api/v1/message/create/

![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/create_message.png)

* Update message (require authorizations) </br>
  PUT </br>
  https://short-messages-api.herokuapp.com/api/v1/message/update/4 <message_id>

![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/update_message.png)

* Delete message (require authorizations) </br>
  DELETE </br>
  https://short-messages-api.herokuapp.com/api/v1/message/delete/4 <message_id>

![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/delete_message.png)

## Authorization

To use endpoints which require authorization, token must be added to request header. To do that:

1. Create new user https://short-messages-api.herokuapp.com/api/v1/user/create/
2. Request token https://short-messages-api.herokuapp.com/api/v1/user/token/
3. Add `Token <generated_token>` as 'Authorization' header
   
![alt text](https://raw.githubusercontent.com/dawidbudzynski/short-messages-api/main/demo_images/add_token_header.png)

## Heroku deployment

To deploy application to Heroku:

1. Sign up to Heroku account and install Heroku CLI https://devcenter.heroku.com/articles/heroku-cli
2. In Heroku dashboard create new application
3. In CLI connect to remote of your application

```
heroku git:remote -a <your-application-name>
```

4. Log in to Container Registry

```
heroku container:login
```

5. Build a local image with correct tag

```
docker build -t registry.heroku.com/<your-application-name>/web .
```

6. Push your secret key

```
heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a <your-application-name>
```

7. Create and connect PostgreSQL

```
heroku addons:create heroku-postgresql:hobby-dev -a <your-application-name>
```

8. Push local image to Heroku registry

```
docker push registry.heroku.com/<your-application-name>/web
```

9. Release changes

```
heroku container:release -a <your-application-name> web
```

10. Run `manage.py migrate` on Heroku

```
heroku run python manage.py migrate
```