from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 
# Simple todo:
# - it has an owner who has created it and can manage it
# - it has a person who it is assigned to (and can mark it done!)
# - it has description - text that tells what to do
# - it has state that tells if it's completed or not

class Todo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_to', null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    done = models.BooleanField()