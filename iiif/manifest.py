from django.core.urlresolvers import reverse
from django.conf import settings
import json

DEBUG = settings.DEBUG

class Manifest:
    def __init__(self, request, manifest_id, **kwargs):
        self.request = request
        self.manifest_id = manifest_id
        self.label = kwargs.get('label', '')
        self.description = kwargs.get('description', '')
        self.sequences = []

    def create(self, images=None):
        if images is None:
            images = []
        seq = self.add_sequence(1)
        for n, img in enumerate(images, start=1):
            if not img['is_link']:
                can = seq.add_canvas(img['id'])
                can.set_label(img['label'])
                can.add_image(img['id'], img['url'], img['is_link'])
        return self
 
    def add_sequence(self, sequence_id):
        sequence = Sequence(self, sequence_id)
        self.sequences.append(sequence)
        return sequence

    def to_dict(self):
        manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@type": "sc:Manifest",
            "@id": self.build_url('iiif:manifest', [self.manifest_id]),
            "label": self.label,
            "description": self.description,
            "sequences": [sequence.to_dict() for sequence in self.sequences]
        }
        return manifest
    
    def build_url(self, url_name, url_args):
        return self.request.build_absolute_uri(reverse(url_name, args=url_args))

    def to_json(self):
        return dump_to_json(self.to_dict())
    
    def __str__(self):
        return self.to_json()

class Sequence:
    def __init__(self, manifest, sequence_id):
        self.manifest = manifest
        self.sequence_id = sequence_id
        self.canvases = []

    def add_canvas(self, canvas_id):
        canvas = Canvas(self.manifest, canvas_id)
        self.canvases.append(canvas)
        return canvas

    def to_dict(self):
        sequence = {
            "@id": self.manifest.build_url('iiif:sequence', [self.manifest.manifest_id, 'sequence', self.sequence_id]),
            "@type": "sc:Sequence",
            "label": "Default order",
            "canvases": [canvas.to_dict() for canvas in self.canvases],
        }
        return sequence

    def to_json(self):
        return dump_to_json(self.to_dict())

class Canvas:
    def __init__(self, manifest, canvas_id):
        self.manifest = manifest
        self.canvas_id = canvas_id
        self.label = 'Image'
        self.resource = None

    def add_image(self, image_id, image_url, is_link):
        self.resource = ImageResource(self.manifest, image_id, image_url, is_link)
        return self
    
    def set_label(self, label):
        self.label = label

    def to_dict(self):
        canvas_uri = self.manifest.build_url('iiif:canvas', [self.manifest.manifest_id, 'canvas', self.canvas_id])
        canvas = {
            "@id": canvas_uri,
            "@type": "sc:Canvas",
            "label": self.label,
            "images": [{
                "@id": "",
                "@type": "oa:Annotation",
                "resource": self.resource.to_dict(),
                "on": canvas_uri,
            }],
            "width": 100, # TODO: get real width
            "height": 100, # TODO: get real height
        }
        return canvas

    def to_json(self):
        return dump_to_json(self.to_dict())

class ImageResource:
    def __init__(self, manifest, resource_id, image_url, is_link=False):
        self.manifest = manifest
        self.resource_id = resource_id
        self.image_url = image_url
        self.is_link = is_link
    
    def to_dict(self):
        if self.is_link:
            resource = {
                "@id": self.image_url,
                "@type": "dctypes:Image",
            }
        else:
            resource = {
                "@id": self.manifest.build_url('iiif:resource', [self.manifest.manifest_id, 'resource', self.resource_id]),
                "@type": "dctypes:Image",
                "service": {
                    "@id": self.image_url,
                    "profile": "http://iiif.io/api/image/2/level1.json", 
                }
            }
        return resource
        
    def to_json(self):
        return dump_to_json(self.to_dict())    

def dump_to_json(obj):
    if DEBUG:
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    return json.dumps(obj)
