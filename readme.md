# Django real time private messaging

## Setup:
- Migrate the database
    ```
    $ docker-compose up migration
    ```
- Create User models & relationships

    ```
    $ docker-compose run --rm web bash

    Python 3.6.3 (default, Dec 12 2017, 16:40:53)
    ...
    ...
    (InteractiveConsole)
    >>> # Create three users
    >>> alex = User.objects.create_user('alex', password='test')
    >>> jake = User.objects.create_user('jake', password='test')
    >>> bob = User.objects.create_user('bob', password='test')

    >>> # Make alex friends with jake and bob
    >>> alex.friends.add(jake, bob)
    >>> jake.friends.add(alex)
    >>> bob.friends.add(alex)
    ```
- Run redis and the web application
    ```
    $ docker-compose up
    ```

- Navigate to http://localhost:8000 on two web browsers (incognito + normal) and
log in using the credentials created above



## 

