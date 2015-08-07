from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
import json

def index(request, course_id):
    manifest_data = [{
        "manifestUri": request.build_absolute_uri(reverse("iiif:manifest", args=[course_id])),
        "location": "Harvard University",
    }]
    manifest_data_json = json.dumps(manifest_data)

    return render(request, 'mirador.html', {"manifest_data_json": manifest_data_json})
