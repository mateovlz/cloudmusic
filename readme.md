
# MyCloudMusic API
This API REST application was made with **[Django REST Framework](https://www.django-rest-framework.org/ "Django REST Framework")** using the JWT Authentication.

## Installation Environment
1. First we're going to create and start our python env to install the lastest version of Django
     - Create the env `python3 -m venv env`

     - Start the env Linux `source env/bin/activate`   On Windows use `env\Scripts\activate`

2. We install all what we need
      - Django `pip install django`

      - Django REST `pip install djangorestframework`

      - Django REST JWT `pip install djangorestframework-simplejwt`

3. We initialize our models and start the migrate 
     - We make migrations `python manage.py makemigrations`
     - We migrate our models `python manage.py migrate`

4. We prefill our tables with pre-establish data
     - We initialize our data with the fixtures for users `python manage.py loaddata fixtures/user_accounts.json --app cloudmusic.UserAccounts`

     - We initialize our songs list `python manage.py loaddata fixtures/song.json --app cloudmusic.Song`

5. Finally we have everyting to go we initialize our server
    - `python manage.py runserver`

## APIs
In the following section, we are going show all the endpoints **mycloudmusic** with the current version that is running on PRD.
> Please remember that all the endpoints are procteted wiht JWT except `signUp` and `random-number`.

>For access to the application first you should create an account with your email and password that full fill this conditions `password should contain at least 10 characters, one lowercase letter, one uppercase letter and one of the following characters: !, @, #, ? or ] `.

> Once you have created your account Login if everything match you'll receive an `access_token`, that you should utilize in the Autorizathion Headers as Bearer Token to access the endpoints correctly 

| METHOD | API  | DESCRIPTION  |
| :------------ | :------------ | :------------: |
| POST  |  http://copierking.com.co:40/signUp | Creates an account into the application using the JSON Body  `{ "email": "mateo@cloudmusic.co", "password": "Kgmkh12312]"}`  |
| POST |  http://copierking.com.co:40/login | Login into the application an retrieve the token for indentify yourself in the next endpoints otherwise you can't access the others endpoints using JSON Body `{ "email": "mateo@cloudmusic.co", "password": "Kgmkh12312]"}` this user is already in the PRD environment |
| POST  |  http://copierking.com.co:40/song | Create a song with the JSON Body you passed `{"id": 1, "name": "Papatoi", "duration": "25","public":  "Y"}` |
| PUT |  http://copierking.com.co:40/song | Update the song you pass as JSON Body `{"id": 1, "name": "Papatoi", "duration": "25","public":  "Y"}` |
| GET |  http://copierking.com.co:40/song/(pk) | Retrieve the song correspond the (pk) you passed, if you didn't created it but is public will show otherwise will appear a message of not found  |
| DELETE |  http://copierking.com.co:40/song/(pk) | Deletes the song with the `(pk)` you passed   |
| GET |  http://copierking.com.co:40/song/list/(type) |  Retrieve a list of songs with pagination of 20 songs per page with the following page in the JSON response replace ~ `(type)` with `private` or `public`, the `private` will show you the songs that you created in private |
| GET  |  http://copierking.com.co:40/random-number | Retrieve a random number without authentication **public endpoint**  |  |

## Help
If during your installation or testing you have any corcern or issue, please contact me.

## Production Environment
The PRD environment app is running in [DigitalOcean](https://www.digitalocean.com/ "DigitalOcean") powered by [Gunicorn](https://gunicorn.org/ "Gunicorn") and [Apache Server](https://httpd.apache.org/ "Apache Server")
