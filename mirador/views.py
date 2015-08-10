from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import LTICourseImages, LTICourseCollections
import json

def _build_manifest_uri(request, manifest_id):
    return request.build_absolute_uri(reverse("iiif:manifest", kwargs={
        'manifest_id': manifest_id,
        'object_type': 'manifest',
    }))

def index(request, course_id):
    '''Renders the page with Mirador, which loads the images specified by the IIIF manifest.'''

    # Add manifest of images for the whole course (across collections)
    manifests = [{
        "manifestUri": _build_manifest_uri(request, course_id),
        "location": "Harvard University",
    }]

    # Add manifest for each collection of images
    collection_ids = LTICourseImages.objects.filter(course__id=course_id).distinct().values_list('collection', flat=True)
    collections = []
    if len(collection_ids) > 0:
        collections = LTICourseCollections.objects.filter(id__in=collection_ids).order_by('sort_order', 'label')

    for collection in collections:
        manifest_id = "%s:%s" % (course_id, collection.id)
        manifests.append({
            "manifestUri": _build_manifest_uri(request, manifest_id),
            "location": "Harvard University",
        })

    return render(request, 'mirador.html', {"manifests_json": json.dumps(manifests)})
