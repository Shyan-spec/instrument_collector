# Django catcollector heroku deployment

# Dependencies

### Open catcollector app in VScode
Find your catcollector application and open it in VScode and make the following changes to your project so configure it for heroku deployment.

### Activate your virtual environment

```python
pipenv shell
```

``` python
# Here is a list of all the packages required in order to deploy your django application to heroku.

# Install the following packages:
pipenv install django-environ django-environ dj-database-url django-heroku whitenoise gunicorn

# Go into the documentation and ask GPT for more clarification on these packages as the need arises during the deployment process. 

# I will try to include comments where relevant for documentation purposes. Look for hints in the code blocks below.

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
Once you have installed all of the packages above 

Step 4: Add a `Procfile` to the root of your project.

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














# Heroku

Step 1: Go to https://dashboard.heroku.com/apps and create a new project, call it something like this: django-catcollector.

Step 2: Go to the deploy tab, next select github as your method of connecting the git repo that you want to deploy. `django-catcollector`

Step 3: Once you have connected the repo, select the branch that you want to deploy. In this case we are deploying the `heroku-deployment` branch.










