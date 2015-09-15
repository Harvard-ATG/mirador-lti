from django.contrib import admin
from .models import IsiteImages, LTIResourceImages, LTIResourceCollections

class IsiteImagesAdmin(admin.ModelAdmin):
    search_fields = ['isite_keyword', 'isite_topic_id', 'isite_file_url']
    list_display = ('id', 'isite_keyword', 'isite_topic_id','isite_site_title', 'isite_topic_title','isite_file_name', 'isite_file_url', 'isite_file_title', 'isite_file_description', 's3_bucket', 's3_key', 'created')

class LTIResourceImagesAdmin(admin.ModelAdmin):
    search_fields = ['resource__id', 'collection__label', 'isite_image__isite_file_url']
    list_display = ('id', 'resource', 'collection', 'isite_image', 'created')
    
class LTIResourceCollectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'sort_order', 'created')

admin.site.register(IsiteImages, IsiteImagesAdmin)
admin.site.register(LTIResourceImages, LTIResourceImagesAdmin)
admin.site.register(LTIResourceCollections, LTIResourceCollectionsAdmin)
