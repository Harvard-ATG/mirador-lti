from django.contrib import admin
from .models import IsiteImages, LTICourseImages

class IsiteImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'isite_keyword', 'isite_topic_id','isite_file_name', 'isite_file_url', 'isite_file_title', 'isite_file_description', 's3_bucket', 's3_key', 'created')

class LTICourseImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(IsiteImages, IsiteImagesAdmin)
admin.site.register(LTICourseImages, LTICourseImagesAdmin)
