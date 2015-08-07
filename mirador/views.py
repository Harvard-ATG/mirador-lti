from django.shortcuts import render
from django.core.urlresolvers import reverse
import json

def index(request, course_id):
    '''Renders the page with Mirador, which loads the images specified by the IIIF manifest.'''

    manifest_url = reverse("iiif:manifest", args=[course_id])
    manifest_data = [{
        "manifestUri": request.build_absolute_uri(manifest_url),
        "location": "Harvard University",
    }]
    context = {"manifest_data_json": json.dumps(manifest_data)}

    return render(request, 'mirador.html', context)
