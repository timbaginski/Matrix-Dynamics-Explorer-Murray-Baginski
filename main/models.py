from django.db import models
from django_random_id_model import RandomIDModel

# Create your models here.

class Iteration(RandomIDModel):
    polynomial = models.CharField(max_length=100, default='')
    currentIteration = models.IntegerField(default=0)
    maxIteration = models.IntegerField(default=0)
    startValue = models.CharField(default='', max_length=10000)
    threshold = models.FloatField(default=0.0)
    converged = models.BooleanField(default=False)


class IterationStep(models.Model):
    iterationID = models.ForeignKey(to=Iteration, on_delete=models.CASCADE)
    value = models.CharField(max_length=10000)
    step = models.IntegerField(default=0)

