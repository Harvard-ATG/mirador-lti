from django.db import models
from django_app_lti.models import LTIResource

class IsiteImage(models.Model):
    isite_file_type = models.CharField(max_length=64)
    isite_file_name = models.CharField(max_length=2048)
    isite_file_url = models.CharField(max_length=4096)
    isite_file_title = models.CharField(max_length=2048, null=True, blank=True)
    isite_file_description = models.TextField(null=True, blank=True)
    isite_site_title = models.CharField(max_length=4096)
    isite_topic_title = models.CharField(max_length=4096)
    isite_topic_id = models.CharField(max_length=128)
    isite_keyword = models.CharField(max_length=128)
    iiif_file_id = models.CharField(max_length=4096, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s/%s/%s" % (self.isite_keyword, self.isite_topic_id, self.isite_file_name)

    class Meta:
        ordering = ['id']
        verbose_name = 'Isite Image'
        verbose_name_plural = 'Isite Images'

class ImageSource(models.Model):
    FILE_TYPE = 'FILE'
    LINK_TYPE = 'LINK'
    SOURCE_TYPE_CHOICES = (
        (FILE_TYPE, 'File'),
        (LINK_TYPE, 'URL to File'),
    )
    source_type = models.CharField(max_length=4, choices=SOURCE_TYPE_CHOICES, default=FILE_TYPE)
    file_name = models.CharField(max_length=2048, null=True, blank=True)
    file_url = models.CharField(max_length=4096, null=True, blank=True)
    title = models.CharField(max_length=2048, null=False)
    description = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    iiif_file_id = models.CharField(max_length=4096, null=True, blank=True)
    is_iiif_compatible = models.BooleanField(default=True)
    is_isite_image = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s" % (self.id, self.title)

    class Meta:
        ordering = ['id']
        verbose_name = 'Image Source'
        verbose_name_plural = 'Image Sources'

class ImageCollection(models.Model):
    label = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    sort_order = models.IntegerField(null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s" % (self.id, self.label)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Image Collection'
        verbose_name_plural = 'Image Collections'

class LTIResourceImages(models.Model):
    resource = models.ForeignKey(LTIResource)
    collection = models.ForeignKey(ImageCollection, null=True)
    image = models.ForeignKey(ImageSource)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.collection, self.image)

    @classmethod
    def get_lti_resource(self, resource_id):
        return LTIResource.objects.get(pk=resource_id)

    class Meta:
        verbose_name = 'LTI Resource Images'
        verbose_name_plural = 'LTI Resource Images'
