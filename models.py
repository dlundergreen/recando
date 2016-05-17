from django.db import models

class Signup(models.Model):
    email = models.CharField(max_length=200)
    signup_date = models.DateTimeField('date published')

class Post(models.Model):
    title = models.CharField(max_length=200)
    question_text = models.TextField()
    username = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    club = models.ForeignKey('Clubs')

class Clubs(models.Model):
    name = models.CharField(max_length=40, unique=True)
    tagline = models.CharField(max_length=200)
    password = models.CharField(max_length=40)
    admin = models.CharField(max_length=300)

class Mac(models.Model):
    username = models.CharField(max_length=200)
    club = models.ForeignKey('Clubs')

class Comment(models.Model):
    comment = models.TextField()
    sentence = models.IntegerField()
    username = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    post = models.ForeignKey('Post')

class Notification(models.Model):
    user_rec = models.CharField(max_length=100)
    user_sent = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    notification = models.CharField(max_length=300)
    seen = models.IntegerField()
    post = models.ForeignKey('Post')
