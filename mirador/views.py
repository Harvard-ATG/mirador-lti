from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import LTICourseImages
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
    collections = LTICourseImages.objects.values('collection').distinct()
    for collection in collections:
        collection_id = collection['collection']
        manifest_id = "%s:%s" % (course_id, collection_id)
        manifests.append({
            "manifestUri": _build_manifest_uri(request, manifest_id),
            "location": "Harvard University",
        })

    return render(request, 'mirador.html', {"manifests_json": json.dumps(manifests)})
