from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
import json
from manifest import Manifest
from mirador.models import IsiteImages, LTIResourceImages, LTIResourceCollections

def manifest(request, **kwargs):
    '''
    Returns JSON output to render a IIIF manifest of images that belong to a resource.
    
    This is intended to work with Mirador.
    
    Example request: http://localhost:8000/1/manifest.json
    
    See also: http://iiif.io/api/presentation/2.0/
    See also: https://github.com/IIIF/mirador
    '''
    manifest_id = kwargs.get('manifest_id', None)
    object_type = kwargs.get('object_type', None)
    object_id = kwargs.get('object_id', None)

    if manifest_id is None or object_type is None:
        raise Http404

    manifest = _manifest(request, manifest_id)

    if object_type == 'manifest':
        return HttpResponse(manifest.to_json(), content_type="application/json")
    else:
        if object_id is not None:
            result = manifest.find_object(object_type, object_id)
            if result is not None:
                return HttpResponse(result.to_json(), content_type="application/json")

    raise Http404

def _manifest(request, manifest_id):
    '''Returns a Manifest object that has been instantiated and populated with images.'''
    ids = manifest_id.split(':', 2)
    resource_id = ids[0]
    collection_id = None
    manifest_label = 'Manifest'
    manifest_description = 'Manifest of resource images'
    if len(ids) == 2:
        collection_id = ids[1]
        collection = LTIResourceCollections.objects.get(pk=collection_id)
        manifest_label = collection.label
        manifest_description = "Manifest of images for collection %s" % collection.label

    images = _get_images(request, resource_id, collection_id)
    #print "manifest_id=%s resource_id=%s collection_id=%s images=%s" % (manifest_id, resource_id, collection_id, len(images))

    manifest = Manifest(request, manifest_id, label=manifest_label, description=manifest_description)
    manifest.create(images=images)

    return manifest

def _get_images(request, resource_id, collection_id):
    '''Returns a list of images [(id, is_link, label), ...] that belong to a manifest.'''
    lti_resource = LTIResourceImages.get_lti_resource(resource_id)

    filter_by = {'resource':lti_resource}
    if collection_id is not None:
        filter_by['collection__id'] = collection_id

    lti_resource_images = LTIResourceImages.objects.select_related().filter(**filter_by)
    manifest_images = []

    for c in lti_resource_images:
        manifest_img = {
            'id': c.isite_image.id,
            'is_link': c.isite_image.isite_file_type == 'link',
            'label': c.isite_image.isite_file_title,
            'url': '',
        }
 
        if c.isite_image.isite_file_type == 'file':
            manifest_img['url'] = settings.IIIF_IMAGE_SERVER_URL + c.isite_image.s3_key
        elif c.isite_image.isite_file_type == 'link':
            manifest_img['url'] = c.isite_image.isite_file_url
        else:
            raise Exception("unknown image file type: %s" % c.isite_image.isite_file_type)

        manifest_images.append(manifest_img)

    return manifest_images

