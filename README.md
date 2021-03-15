# Django Message REST API

REST API for message managing.

Project based on Django, Postgres, Celery and RabbitMQ.


## Build and run the container

1. Install Docker.

2. Download this repository.

3. In env.env and DjangoTaskEnjoyPro/settings.py you can change database and celery settings.
    
    env.env
    ```
    # Environment settings for docker development.

    RABBITMQ_DEFAULT_USER=user
    RABBITMQ_DEFAULT_PASS=pass
    CELERY_BROKER=amqp://user:pass@rabbitmq:5672
    POSTGRES_DB=rest_messaging
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=pass
    POSTGRES_HOST_AUTH_METHOD=trust
   
    ```

4. On the command line, within this directory, do this to build the image and
   start the container:

        docker-compose build

5. If that's successful you can then start it up. This will start up the database and web server:

        docker-compose up

6. (Also you can use docker-compose up --build to quickly build and run container

6. Open http://localhost:8000 in your browser.


## Description

Api functions:

'rest_messaging/':
* 'posts/' - GET. List of messages.
* 'posts/create' - POST, data example = {'title': 'new message'}. Create message.
* 'posts/<int:pk>' - PUT, data example = {'description': 'some'}. Change message.
* 'posts/<int:pk>' - DELETE. Delete message.
* 'posts/<int:message_id>/read' - POST. Imitate message read.
* 'posts/download' - GET. Download csv file with messages.


### Accessing the database

To access the PostgreSQL database just connect it through pgAdmin. Just set: host name - localhost, port - 5432 and password - pass.
