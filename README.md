# Homework 2 Louis Durand

This is my submission for Homework 2


## Description of what I've done

I have implemented a Web application that listens on localhost:5000 and renders an authentication form.
The user can create a username and password and it redirect user to profile page at http://localhost:5000/profile.
If you try to access this page while being not logged in, you will be redirected to login page. And if you try to get to login page while being connected, you will be auto reconnected to your session.
The user and password are stored in Mongodb in `louisdurandhw2` and `users` collection.
Once on the profile page, a user can decide to logout, or change password. He is also greeted with custom message with his username. And as said previously can't go back to login without pressing disconnect.
The password is also hashed when stored in the database.

## Checklist

Basic part: Implement authentication feature
- [x] Listen on localhost:5000
- [x] Render authentication form at http://localhost:5000/
- [x] Redirect user to profile page if successfully authenticated
- [x] Show profile page for authenticated user only at http://localhost:5000/profile
- [x] User name and password are stored in Mongodb
--------
Advanced part:
- [x] Implement feature that allows users to create new account, profile will be shown with data respected to each account.
- [x] Implement password hashing, logout and password change features
- [ ] Allow users to update profile picture (new user will have a default profile picture)
- [ ] Allow users to update profile information
--------
Challenging part:
- [ ] Implement notification, an active user will receive notification when a new account is created.


## How to run the Web Application

`python app.py`
or 
`flask run`