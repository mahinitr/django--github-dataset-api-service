# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=200)

class Repo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=50)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date published')
    
