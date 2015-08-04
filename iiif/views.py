from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json

def manifest(request, identifier):
    manifest_id = request.build_absolute_uri(reverse('iiif:manifest', args=[identifier])) 
    manifest = {
        '@context': 'http://www.shared-canvas.org/ns/context.json',
        "@id": manifest_id,

    }
    return HttpResponse(json.dumps(manifest), content_type="application/json")
