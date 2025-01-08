# URL

```path('auth/', include('simple.urls')),```


# Setting

* INSTALLED_APPS = [
    ...
    ```'simple'```
]

* TEMPLATES = [
    {
        ...
        ```'APP_DIRS': True,``` # make sure app dirs is set to true 
     ...
     }
],

```AUTH_USER_MODEL = 'simple.UserModels'```

<!-- if you get an error the first time try-->
```python manage.py makemigration simple```

# Optional
* defaults is home

* LOGIN_REDIRECT 
* LOGOUT_REDIRECT
* RESET_TIME # in minutes default is 10
* RESET_REDIRECT

* you can add email and set the reset password on your own

