from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
import json
from manifest import Manifest

def _manifest(request, manifest_id):
    manifest = Manifest(request, manifest_id, label='', description='')
    manifest.create()
    return manifest

def manifest(request, *args):
    result = ''
    if len(args) == 1:
        manifest_id = args[0]
        manifest = _manifest(request, manifest_id)
        result = manifest.to_json()
    else:
        raise Http404
    
    return HttpResponse(result, content_type="application/json")
