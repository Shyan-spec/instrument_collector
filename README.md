# Django catcollector heroku deployment

# Dependencies

### Open catcollector app in VScode
Find your catcollector application and open it in VScode and make the following changes to your project so configure it for heroku deployment.

### Activate your virtual environment

```python
pipenv shell
```

```python
# Here is a list of all the packages required in order to deploy your django application to heroku.

# Install the following packages:
pipenv install django-environ django-environ dj-database-url django-heroku whitenoise gunicorn

# Go into the documentation and ask GPT for more clarification on these packages as the need arises during the deployment process. 
# I will try to include comments where relevant for documentation purposes. 
#Look for hints in the code blocks below.

# https://pypi.org/project/django-environ/
pipenv install django-environ

# https://pypi.org/project/dj-database-url/
pipenv install dj-database-url

# https://pypi.org/project/django-heroku/
pipenv install django-heroku

# https://pypi.org/project/whitenoise/
pipenv install whitenoise

# https://pypi.org/project/gunicorn/
pipenv install gunicorn
```
Once you have installed all of the packages above you can actually begin to modify your code in preparation of deployment.

## Procfile ( gunicorn )
Add a `Procfile` to the root of your project.

```python
# Procfile in the root of your project with this code inside
# The migrate command is to migrate the app models/ tables to the database hosted in heroku servers.
release: python3 manage.py migrate
# The project folder is named catcollector, that's why we used it here. 
# gunicorn will allow us to deploy to heroku 
# It will act as a middleman between our application and the internet.
web: gunicorn catcollector.wsgi 
```
This link contains details about how gunicorn works when deploying a django application.

- https://chat.openai.com/share/c28a8ad4-5248-45c9-815c-335e9096a672


## env ( django-environ )

Add an env file to the root of your project folder. `catcollector/.env `

```python
# catcollector/.env 

# Create the .env folder on the root of the project folder ( aka catcollector )

# env example 
# You will need all of these variables when deploying the application. 
# You will get the information for these variables when you create the SQL resource in heroku.
# These variables will be used to configure the database config in settings.py, as you will see further below.

SECRET_KEY=''

PGDATABASE=''

PGHOST=''

PGPASSWORD=''

PGPORT='5432'

PGUSER=''

DATABASE_URL=''

```

# catollector/settings.py

All of the following changes will be made in the `catcollector/settings.py` 

We will: 

### No package required


- Add allowed hosts to accept requests from a heroku origin 

```python
# catcollector/settings.py

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
```

### Package required
- Set up our application to accept/ use env variables ( django-environ )

```python
# catcollector/settings.py

import environ  
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
```

- Add environment variables ( django-environ )

```python
# catcollector/settings.py

SECRET_KEY=env('SECRET_KEY')
PGDATABASE=env('PGDATABASE')
PGHOST=env('PGHOST')
PGPASSWORD=env('PGPASSWORD')
PGPORT=env('PGPORT')
PGUSER=env('PGUSER')
DATABASE_URL=env('DATABASE_URL')
```

- Add middleware ( whitenoise )
  
```python
# catcollector/settings.py
# Be certain that you placed the whitenoise middleware as indicated below
# If you fail to do so you app will potentially not deploy
# If it does deploy, it will not have any styling on the DRF dashboard
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

- Update the database configs ( dj-database-url ) 

```python
# catcollector/settings.py

DATABASES = {
    'default': 
        dj_database_url.config('DATABASE_URL')
}
```

- Configure our application to interface with heroku ( django-heroku
 )

```python
# catcollector/settings.py

# Add this to the very bottom of your settings.py file
# If you don't your app will not deploy properly
django_heroku.settings(locals())

```





# Heroku

Step 1: Go to https://dashboard.heroku.com/apps and create a new project, call it something like this: django-catcollector.

Step 2: Go to the deploy tab, next select github as your method of connecting the git repo that you want to deploy. `django-catcollector`

Step 3: Once you have connected the repo, select the branch that you want to deploy. In this case we are deploying the `heroku-deployment` branch.










