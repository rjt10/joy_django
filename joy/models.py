from django.db import models

class User(models.Model):
    joined = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=100, blank=True, default='')
    fb_userid = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('joined',)
