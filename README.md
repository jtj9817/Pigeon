# Pigeon

### Pigeon - Pigeon

This is the root of the project. Apps such as pigeon_messaging, pigeon_posts, and account are added to this root.

This application is meant to run locally and as such, the links for the API endpoints are local URL addresses.

### Pigeon - Account

This is an application that handles user authentication (i.e. registration & log-in) using REST API architecture.

For registration & log-in, it uses dj-rest-auth to simplify the process as the package provides registration, login, and logout functionalities.
A token is generated using django-rest-knox in order to maintain authentication details during a user's session.

The following routes available from this web application are:

- http://127.0.0.1:8000/api/account/
- http://127.0.0.1:8000/api/account/<account.pk>
- http://127.0.0.1:8000/api/account/<account.pk>/update
- http://127.0.0.1:8000/api/account/<userid>/delete

i.e. http://127.0.0.1:8000/api/account/<5>/update
For account registration & login

- http://127.0.0.1:8000/api/account/register
- http://127.0.0.1:8000/api/account/login

A test suite is included on 'tests.py'. It can be ran by invoking the "python manage.py test" command while on the 'pigeon' directory.

**NOTE**:

To register an account:

Go to http://127.0.0.1:8000/api/account/register and copy+paste the following data format to ensure that the registration request will be processed:
`{ "username": "[insert username here]", "email": "[insert email here]", "password": "[insert password here]", "password_verify": "[insert password here again]" }`

As an example:
`{ "username": "pidgeonuserone", "email": "pidgeonuserone@gmail.com", "password": "coolpidgeons123", "password_verify": "coolpidgeons123" }`

### Pigeon - Messaging

This is an application that handles the one-to-one instant messaging feature of the Pigeon application.

This solution will be the simplest one - a 'Message' is considered as an object that has a Sender, Receiver, and Message.

Real-time messaging is complicated and available solutions for Django can vary depending on the complexity as solutions can be asynchronous or synchronous. Furthermore,
the setup for such real-time systems require Django Channels which require Redis and a message queue solution (i.e. RabbitMQ, Celery).

Routes Available:

- http://127.0.0.1:8000/api/messages/messages-list
- http://127.0.0.1:8000/api/messages/message/<message.pk>
- http://127.0.0.1:8000/api/messages/message/<message.pk>/delete/

Example:
http://127.0.0.1:8000/api/messages/message/<message.pk>

### Pigeon - Posts

This is an application that handles the creation of Pidgeon Posts (aka Tweets). It supports CRUD functionality while adhering to REST API architecture principles

Routes available:

- http://127.0.0.1:8000/api/posts/
- http://127.0.0.1:8000/api/posts/post/<post.pk>/
- http://127.0.0.1:8000/api/posts/post/<post.pk>/delete/

Example:

- http://127.0.0.1:8000/api/posts/post/1/

## Unit Testing

Unit tests for each functionality (account, messaging, post) are available under their respective folders.

Tests can be run in 2 ways:

- By invoking the "python manage.py test" command in Powershell/Commandline while under the Pigeon/pigeon directory. This would run all the tests.
- By invoking the "python manage.py [specific test suite]" command. For example - to run the test suite for the 'account' web application component, the command "python manage.py test account.tests" is invoked.

Tests directory:

- account/tests.py
- pigeon_messaging/tests.py
- pigeon_posts/tests.py

## Installation

To install:

1. Clone the repository
2. Once the repository has been completely cloned, create a Python virtual environment in the root directory of the repository.
   To create a Python virtualenv(venv), have python3 installed in your system and run the following command in the commandline while in the root of the Pigeon repository:
   `python3 -m venv [virtual environment name]` without the square brackets - i.e.: `python3 -m venv pigeonvenv`
3. Now run `[virtual environment name]\Scripts\activate` without the square brackets. For example: `pigeonvenv\Scripts\activate`
4. Once the virtual environment has been loaded, run the command `pip install -r requirements.txt` to install all the required software packages for the web application
5. Create a file called ".env" (yes, without any file name) and set your own configuration for the environment variables.
6. Once all packages has been successfully installed, go to 'pigeon' subdirectory and run `python manage.py runserver`
