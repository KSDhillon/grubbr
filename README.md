# grubbr.io

CS 4501 Project
Group Members: Aadil Abbas, Karan Dhillon

#TODO
-Ask TA about links on docker-compose
-Don’t store plaintext passwords in the database. In your create_user() function, you should hash the input password before storing it.
-No input validation for create() functions.
-Provide default values for your request.POST accesses. Use request.POST.get(‘key’, ‘default_val’) to achieve this.
-You created your own User model, which is fine (and will be necessary), but I would recommend subclassing it off of the Django AbstractBaseUser class so that things like authentication, sessions, and passing the user to each page in a template are taken care of for you).
