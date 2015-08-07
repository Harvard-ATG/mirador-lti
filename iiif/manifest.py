from django.core.urlresolvers import reverse

import json

class Manifest:
    def __init__(self, request, manifest_id, **kwargs): 
        self.label = kwargs.get('label', '')
        self.description = kwargs.get('description', '')
        self.manifest_id = manifest_id
        self.sequences = []
        self.request = request

    def create(self, **kwargs):
        images = kwargs.get('images', [])
        images = [
            {'id':123, 'url': 'http://localhost:8000/images/1.jpg'},
            {'id':456, 'url':'http://localhost:8000/images/2.jpg'},
        ]
        seq = self.add_sequence(1)
        for n, img in enumerate(images, start=1):
            can = seq.add_canvas(n)
            can.set_label('Image %d' % n)
            can.add_image(img['id'], img['url'])
        return self
 
    def add_sequence(self, sequence_id):
        sequence = Sequence(self, sequence_id)
        self.sequences.append(sequence)
        return sequence

    def to_dict(self):
        manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@type": "sc:Manifest",
            "@id": self.request.build_absolute_uri(reverse('iiif:manifest', args=[self.manifest_id])),
            "label": self.label,
            "description": self.description,
            "sequences": [sequence.to_dict() for sequence in self.sequences]
        }
        return manifest

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
            "@id": self.manifest.request.build_absolute_uri(reverse('iiif:sequence', args=[self.manifest.manifest_id, 'sequence', self.sequence_id])),
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
        self.resources = []

    def add_image(self, image_id, image_url):
        self.resource = ImageResource(self.manifest, image_id, image_url)
        return self
    
    def set_label(self, label):
        self.label = label

    def to_dict(self):
        canvas = {
            "@id": self.manifest.request.build_absolute_uri(reverse('iiif:canvas', args=[self.manifest.manifest_id, 'canvas', self.canvas_id])),
            "@type": "sc:Canvas",
            "label": self.label,
            "images": [{
                "@id": "",
                "@type": "oa:Annotation",
                "resource": self.resource.to_dict(),
                "on": self.canvas_id,
            }]
        }
        return canvas

    def to_json(self):
        return dump_to_json(self.to_dict())

class ImageResource:
    def __init__(self, manifest, resource_id, image_url):
        self.manifest = manifest
        self.resource_id = resource_id
        self.image_url = image_url
    
    def to_dict(self):
        resource = {
            "@id": self.manifest.request.build_absolute_uri(reverse('iiif:resource', args=[self.manifest.manifest_id, 'resource', self.resource_id])),
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
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
