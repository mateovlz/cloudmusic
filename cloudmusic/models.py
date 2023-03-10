from django.db import models
import datetime
import pytz


# Create your models here.

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    public = models.BooleanField()
    created_by = models.IntegerField()
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_timestamp']

    def save(self, *args, **kwargs):
        self.created_timestamp = datetime.datetime.now(pytz.utc)
        super(Song, self).save(*args, **kwargs)


class UserAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'password']

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def save(self, *args, **kwargs):
        self.created_timestamp = datetime.datetime.now(pytz.utc)
        super(UserAccounts, self).save(*args, **kwargs)