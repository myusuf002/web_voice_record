from django.db import models

# Create your models here.
class Language(models.Model):
    code = models.CharField(max_length=512, blank=True, null=True, unique=True)    
    name = models.CharField(max_length=512, blank=True, null=True)    
    model = models.FileField(upload_to='model/', blank=True, null=True)
    beam_width = models.IntegerField(blank=True, null=True)
    lm = models.FileField(upload_to='lm/', blank=True, null=True)
    trie = models.FileField(upload_to='trie/', blank=True, null=True)
    lm_alpha = models.FloatField(blank=True, null=True)
    lm_beta = models.FloatField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True, default=True)
    