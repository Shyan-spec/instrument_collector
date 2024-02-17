# Django catcollector heroku deployment

#Hello
# REMINDER: FORK AND CLONE IF NEEDED
The backend for catcollector is here, if you fork this repo be sure to check the checkbox off so that you can get all branches, this will be useful if you want to retrace your steps or redo any section of the build again for practice:

You can just go there and fork this repo then go through the steps to set everything up in heroku including updating the config vars as described above.

[heroku-deployment](https://github.com/Gregorio-Moreta/django-cat-collector/tree/heroku-deployment)

There are also branches throughout the build there so you can check out the branch that left off at django-authentication if you want to actually go through the process and add all of these changes yourself.

[django-authentication](https://github.com/Gregorio-Moreta/django-cat-collector/tree/django-authentication)

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
pipenv install django-environ dj-database-url django-heroku whitenoise gunicorn

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

## .gitignore
Add a `.gitignore` file to the root of your project. Add these two lines, this should hide your .env file for sure and also hide the gitignore file if you don't want to push your gitignore up to git either.

```python
cacollector/.env
.gitignore
```

### WARNING
Do not skip this step. Safeguard your credentials so they don't get accidentally exposed when you push your code to github.


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

# These are required
DATABASE_URL=''

SECRET_KEY=''

# These are not required.
# If you want to connect locally to the database you may need them
# Something to be aware of, nothing more.

# PGDATABASE=''

# PGHOST=''

# PGPASSWORD=''

# PGPORT='5432'

# PGUSER=''

```

# catollector/settings.py

All of the following changes will be made in the `catcollector/settings.py` 

We will: 

- Add our imports up at the top of our file
```python
import environ  
import dj_database_url
import django_heroku

```

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

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
```

- Add environment variables ( django-environ )

```python
# catcollector/settings.py

# These are required
DATABASE_URL=env('DATABASE_URL')
SECRET_KEY=env('SECRET_KEY')

# These are not required.
# If you want to connect locally to the database you may need them
# Something to be aware of, nothing more.

# PGDATABASE=env('PGDATABASE')
# PGHOST=env('PGHOST')
# PGPASSWORD=env('PGPASSWORD')
# PGPORT=env('PGPORT')
# PGUSER=env('PGUSER')
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

#### Step 1: 

Go to [heroku](https://dashboard.heroku.com/apps) and create a new project, call it something like this: django-catcollector.

#### Step 2: 
Go to the deploy tab, next select github as your method of connecting the git repo that you want to deploy. `django-catcollector`

#### Step 3: 
Once you have connected the repo, select the branch that you want to deploy. In this case we are deploying the `heroku-deployment` branch.

#### Step 4: 
Go to the resources tab and in the search bar for addons, search `heroku postgres`. 
![resource tab heroku](/Assets/Screen%20Shot%202024-02-07%20at%2010.30.07%20PM.png)

### WARNING
Make sure that you select the `mini` option for the Plan name. This has a maximum charge of $5 dollars on it, it's the cheapest option and best choice for our purposes. If you select an expensive plan and your database credentials are leaked you could be held liable for any charges. 

You will be prompted to submit an order form to add the heroku postgres addon to your catcollector project you are deploying on heroku.
![resource tab heroku select the mini plan when signing up for the heroku postgres resource](/Assets/Screen%20Shot%202024-02-07%20at%2010.34.38%20PM.png)


You will then have a new database addon resource available in the resources tab. Which you can then click on to access the database addon.
![resource tab in heroku project](/Assets/Screen%20Shot%202024-02-07%20at%2010.37.02%20PM.png)

#### Step 5: 
After clicking on the new resource addon, you will be taken to a new page that looks like the one below. 

Make sure that you click onto the settings tab, there you should be able to click on the view credentials button and get back all of the information you will need to plug into your environmental variables. 

![PSQL resource settings tab heroku](/Assets/Screen%20Shot%202024-02-07%20at%2010.36.19%20PM.png)

We will add those environment variables into our projects settings in the reveal config vars and it will act like our connection string in mongo, except that there are 7 env variables for PSQL. 

These are variables used to configure the connection to the server. They should look very familiar since they are the same as we declared in the project. You can add these to your env if you want to connect your project on your local machine to the heroku server.

![PSQL resource settings tab in heroku, has database credentials blocked out](/Assets/Screen%20Shot%202024-02-07%20at%2010.42.39%20PM.png)


#### Step 6: 
##### Heroku config vars
Now you can configure your Heroku project settings. Click on the button to reveal config vars and you should already have a `DATABASE_URL` variable in your configuration already from the addon. Don't change that, it should be the correct value.

You do however need to add another env variable just for deployment purposes.
```python
# add this env variable to your settings config vars on heroku.
DISABLE_COLLECTSTATIC=1
```

Failure to do this will lead to an error like this:

![error in deployment due to not include DISABLE_COLLECTSTATIC=1
 in config vars](/Assets/Screen%20Shot%202024-02-07%20at%2011.19.36%20PM.png)

##### This is how your config vars should look like
![update config cars in the heroku project settings](/Assets/Screen%20Shot%202024-02-07%20at%2011.35.07%20PM.png)


### Step 7: 
##### Deployment
You should be able to deploy the `heroku-deployment` branch from your catcollector project. Just go to the deployment tab and deploy like normal.
![resource tab heroku](/Assets/Screen%20Shot%202024-02-07%20at%2011.44.16%20PM.png)

##### Cry tears of joy, your django app is deployed!!!
![home page for deployed catcollector app](/Assets/Screen%20Shot%202024-02-07%20at%2011.37.01%20PM.png)


### Step 8
Go test all your routes in postman or with the frontend repo for the catcollector project!

Do both for extra experience that will be useful during the project and beyond!

[catcollector-frontend](https://git.generalassemb.ly/seb-beherenow/catcollector-frontend)

