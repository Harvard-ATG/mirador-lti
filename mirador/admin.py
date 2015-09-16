from django.contrib import admin
from .models import IsiteImage, ImageSource, ImageCollection, LTIResourceImages

class IsiteImageAdmin(admin.ModelAdmin):
    search_fields = ['isite_keyword', 'isite_topic_id', 'isite_file_url', 'isite_file_title']
    list_display = ('id', 'isite_keyword', 'isite_topic_id','isite_site_title', 'isite_topic_title','isite_file_name', 'isite_file_url', 'isite_file_title', 'isite_file_description', 'iiif_file_id', 'created')

class ImageSourceAdmin(admin.ModelAdmin):
    search_fields = ['title', 'iiif_file_id']
    list_display = ('id', 'source_type', 'file_name', 'file_url', 'iiif_file_id', 'title', 'created')
    
class ImageCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description', 'sort_order', 'created')

class LTIResourceImagesAdmin(admin.ModelAdmin):
    search_fields = ['resource__id', 'collection__label', 'image__title', 'image__iiif_file_id']
    list_display = ('id', 'resource', 'collection', 'image', 'created')

admin.site.register(IsiteImage, IsiteImageAdmin)
admin.site.register(ImageSource, ImageSourceAdmin)
admin.site.register(LTIResourceImages, LTIResourceImagesAdmin)
admin.site.register(ImageCollection, ImageCollectionAdmin)
