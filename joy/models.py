from django.db import models

class User(models.Model):
    """
    An app user.
    """
    id = models.AutoField(primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    fb_userid = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return '%s:%s' % (self.name, self.fb_userid)

    class Meta:
        ordering = ('date_joined',)


class Group(models.Model):
    """
    A group of users. A user could be in multiple groups.
    """
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, default='tic tac')
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_created',)


class Membership(models.Model):
    """
    Models the many-to-many user-group relationship.
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '%s:%s' % (self.user, self.group)

    class Meta:
        ordering = ('date_joined',)