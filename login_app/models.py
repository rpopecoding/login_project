from django.db import models
import re	# the regex module


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    pwdhash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f"{self.first_name}"

class TweetManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['text']) < 2 or len(postData['text']) > 280:
            errors["length"] = "Post must be between 2 and 280 characters."
            return errors
        return errors

class Tweet(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(User, related_name="tweets", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TweetManager()


class Comment(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
