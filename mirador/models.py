from django.db import models
from django_app_lti.models import LTICourse

class IsiteImages(models.Model):
    isite_file_type = models.CharField(max_length=64)
    isite_file_name = models.CharField(max_length=2048)
    isite_file_url = models.CharField(max_length=4096)
    isite_file_title = models.CharField(max_length=2048, null=True, blank=True)
    isite_file_description = models.TextField(null=True, blank=True)
    isite_topic_id = models.CharField(max_length=128)
    isite_keyword = models.CharField(max_length=128)
    s3_key = models.CharField(max_length=4096)
    s3_bucket = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['isite_keyword', 'isite_topic_id', 'isite_file_type', 'isite_file_name']
        verbose_name = 'Isite Image'
        verbose_name_plural = 'Isite Images'
        
class LTICourseImages(models.Model):
    course = models.ForeignKey(LTICourse)
    isite_image = models.ForeignKey(IsiteImages)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'LTI Course Images'
        verbose_name_plural = 'LTI Course Images'