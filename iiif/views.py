from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
import json
from manifest import IIIFManifest
from mirador.models import ImageSource, ImageCollection, LTIResourceImages

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
    '''Returns a IIIFManifest object that has been instantiated and populated with images.'''
    ids = manifest_id.split(':', 2)
    resource_id = ids[0]
    collection_id = None
    manifest_label = 'Manifest'
    manifest_description = 'Manifest of resource images'
    if len(ids) == 2:
        collection_id = ids[1]
        collection = get_object_or_404(ImageCollection, pk=collection_id)
        manifest_label = collection.label
        manifest_description = collection.description

    images = _get_images(request, resource_id, collection_id)
    #print "manifest_id=%s resource_id=%s collection_id=%s images=%s" % (manifest_id, resource_id, collection_id, len(images))

    manifest = IIIFManifest(request, manifest_id, label=manifest_label, description=manifest_description)
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
        is_image_link = c.image.source_type == ImageSource.LINK_TYPE
        manifest_img = {
            'id': c.image.id,
            'is_link': is_image_link,
            'label': c.image.title,
            'url': '',
        }
 
        if c.image.is_iiif_compatible: 
            manifest_img['url'] = settings.IIIF_IMAGE_SERVER_URL + c.image.iiif_file_id
        else:
            if is_image_link:
                manifest_img['url'] = c.image.file_url
            else:
                raise Exception("unknown image source type: %s" % c.image.source_type)

        manifest_images.append(manifest_img)

    return manifest_images

