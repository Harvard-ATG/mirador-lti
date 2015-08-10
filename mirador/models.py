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
    s3_key = models.CharField(max_length=4096, null=True)
    s3_bucket = models.CharField(max_length=128, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s/%s/%s" % (self.isite_keyword, self.isite_topic_id, self.isite_file_name)

    class Meta:
        ordering = ['id']
        verbose_name = 'Isite Image'
        verbose_name_plural = 'Isite Images'

class LTICourseCollections(models.Model):
    label = models.CharField(max_length=128)
    sort_order = models.IntegerField(null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.id, self.label)

    class Meta:
        ordering = ['id']
        verbose_name = 'LTI Course Collection'
        verbose_name_plural = 'LTI Course Collections'

class LTICourseImages(models.Model):
    course = models.ForeignKey(LTICourse)
    collection = models.ForeignKey(LTICourseCollections, null=True)
    isite_image = models.ForeignKey(IsiteImages)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.collection, self.isite_image)

    @classmethod
    def get_lti_course(self, course_id):
        return LTICourse.objects.get(pk=course_id)

    class Meta:
        verbose_name = 'LTI Course Images'
        verbose_name_plural = 'LTI Course Images'
