# 0x02. AirBnB clone - MySQL

## Background Context

Environment variables will be your best friend for this project!

* HBNB_ENV: running environment. It can be “dev” or “test” for the moment (“production” soon!)
* HBNB_MYSQL_USER: the username of your MySQL
* HBNB_MYSQL_PWD: the password of your MySQL
* HBNB_MYSQL_HOST: the hostname of your MySQL
* HBNB_MYSQL_DB: the database name of your MySQL
* HBNB_TYPE_STORAGE: the type of storage used. It can be “file” (using FileStorage) or db (using DBStorage)

## General

* What is Unit testing and how to implement it in a large project
* What is *args and how to use it
* What is **kwargs and how to use it
* How to handle named arguments in a function
* How to create a MySQL database
* How to create a MySQL user and grant it privileges
* What ORM means
* How to map a Python Class to a MySQL table
* How to handle 2 different storage engines with the same codebase
* How to use environment variables

## How to test with MySQL?

First, you create a specific database for it (next tasks). After, you have to remember what the purpose of an unittest?

“Assert a current state (objects/data/database), do an action, and validate this action changed (or not) the state of your objects/data/database”

For example, “you want to validate that the create State name="California" command in the console will add a new record in your table states in your database”, here steps for your unittest:

* get the number of current records in the table states (my using a MySQLdb for example - but not SQLAlchemy (remember, you want to test if it works, so it’s better to isolate from the system))
* execute the console command
* get (again) the number of current records in the table states (same method, with MySQLdb)
if the difference is +1 => test passed

## What’s a Many-to-Many relationship?

In our system, we don’t want to duplicate amenities (for example, having 10000 time the amenity Wifi), so they will be unique. But, at least 2 places can have the same amenity (like Wifi for example). We are in the case of:

* an amenity can be linked to multiple places
* a place can have multiple amenities

= Many-To-Many

To make this link working, we will create a third table called place_amenity that will create these links.

And you are good, you have a new engine

