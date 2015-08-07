from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
import json
from manifest import Manifest
from mirador.models import IsiteImages, LTICourseImages

def manifest(request, *args):
    '''
    Returns JSON output to render a IIIF manifest of images that belong to a course.
    
    This is intended to work with Mirador.
    
    Example request: http://localhost:8000/1/manifest.json
    
    See also: http://iiif.io/api/presentation/2.0/
    See also: https://github.com/IIIF/mirador
    '''
    
    if len(args) == 0:
        raise Http404

    manifest_id = args[0]
    manifest = _manifest(request, manifest_id)

    if len(args) == 1:
        return HttpResponse(manifest.to_json(), content_type="application/json")

    elif len(args) == 3:
        object_type = args[1]
        object_id = int(args[2])
        print object_type, object_id
        
        if object_type == "sequence":
            sequences = manifest.sequences
            for s in sequences:
                if s.sequence_id == object_id:
                    return HttpResponse(s.to_json(), content_type="application/json") 
            raise Http404

        elif object_type == "canvas":
            canvases = manifest.sequences[0].canvases
            for c in canvases:
                if c.canvas_id == object_id:
                    return HttpResponse(c.to_json(), content_type="application/json")
        
        elif object_type == "resource":
            canvases = manifest.sequences[0].canvases
            for c in canvases:
                if c.resource.resource_id == object_id:
                    return HttpResponse(c.resource.to_json(), content_type="application/json")

    raise Http404


def _manifest(request, manifest_id):
    '''Returns a Manifest object that has been instantiated and populated with images.'''
    images = _get_images(request, manifest_id)
    manifest = Manifest(request, manifest_id, label='Manifest', description='Manifest of course images')
    manifest.create(images=images)
    return manifest

def _get_images(request, manifest_id):
    '''Returns a list of images [(id, is_link, label), ...] that belong to a manifest.'''
    isite_images = IsiteImages.objects.all()
    manifest_images = []

    for img in isite_images:
        manifest_img = {
            'id': img.id,
            'is_link': img.isite_file_type == 'link',
            'label': img.isite_file_title
        }

        if img.isite_file_type == 'file':
            manifest_img['url'] = settings.IIIF_IMAGE_SERVER_URL + img.s3_key
        else:
            manifest_img['url'] = img.isite_file_url

        manifest_images.append(manifest_img)

    return manifest_images

