from django.db import models
# Create your models here.

class Utterance(models.Model):
    code = models.CharField(max_length=32, blank=True, null=True, unique=True)
    text = models.TextField(max_length=2048, blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True, default=0)
    active = models.BooleanField(blank=True, null=True, default=True)
    def __str__(self): return self.code

class Age(models.Model):
    code = models.CharField(max_length=32, blank=True, null=True, unique=True)
    category = models.CharField(max_length=32, blank=True, null=True, unique=True)
    detail = models.CharField(max_length=1024, blank=True, null=True, unique=True)
    count = models.BigIntegerField(blank=True, null=True, default=0)
    def __str__(self): return self.category

class Ethnic(models.Model):
    code = models.CharField(max_length=32, blank=True, null=True, unique=True)
    category = models.CharField(max_length=32, blank=True, null=True, unique=True)
    detail = models.CharField(max_length=1024, blank=True, null=True, unique=True)
    count = models.BigIntegerField(blank=True, null=True, default=0)
    def __str__(self): return self.category

class Dialect(models.Model):
    code = models.CharField(max_length=32, blank=True, null=True, unique=True)
    category = models.CharField(max_length=32, blank=True, null=True, unique=True)
    detail = models.CharField(max_length=1024, blank=True, null=True, unique=True)
    count = models.BigIntegerField(blank=True, null=True, default=0)
    def __str__(self): return self.category

class Gender(models.Model):
    code = models.CharField(max_length=32, blank=True, null=True, unique=True)
    category = models.CharField(max_length=1024, blank=True, null=True, unique=True)
    count = models.BigIntegerField(blank=True, null=True, default=0)
    def __str__(self): return self.category
