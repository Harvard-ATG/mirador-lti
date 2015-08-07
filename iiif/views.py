from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
import json
from manifest import Manifest
from mirador.models import IsiteImages, LTICourseImages

def _manifest(request, manifest_id):
    manifest = Manifest(request, manifest_id, label='', description='')
    manifest.create(images=_get_images(request, manifest_id))
    return manifest

def _get_images(request, manifest_id):
    isite_images = IsiteImages.objects.all()
    print isite_images
    manifest_images = []

    for img in isite_images:
        manifest_img = {
            'id': img.id,
            'is_link': img.isite_file_type == 'link'
        }

        if img.isite_file_type == 'file':
            manifest_img['url'] = settings.IIIF_IMAGE_SERVER_URL + img.s3_key
        else:
            manifest_img['url'] = img.isite_file_url

        manifest_images.append(manifest_img)

    return manifest_images

def manifest(request, *args):
    result = ''
    if len(args) == 1:
        manifest_id = args[0]
        manifest = _manifest(request, manifest_id)
        result = manifest.to_json()
    else:
        raise Http404
    
    return HttpResponse(result, content_type="application/json")
