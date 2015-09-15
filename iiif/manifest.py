from django.core.urlresolvers import reverse
from django.conf import settings
import json

class IIIFObject:
    '''
    IIIF Object is the base object for IIIF presentation classes.
    
    This class contains shared behaviors and methods that should be implemented.
    
    See also: http://iiif.io/api/presentation/2.0/
    '''
    def build_url(self):
        '''Returns an absolute URL to the object.'''
        raise Exception("not implemented yet")

    def to_dict(self):
        '''Returns itself as a dictionary.'''
        raise Exception("not implemented yet")

    def to_json(self):
        '''Returns itself as JSON.'''
        obj = self.to_dict()
        if settings.DEBUG:
            return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
        return json.dumps(obj)

    def __unicode__(self):
        '''Returns a string representation.'''
        return self.to_json()    

class Manifest(IIIFObject):
    '''
    IIIF Manifest represents a collection of images and defines the overall structure
    of the collection.

    A Manifest object is composed of Sequence, Canvas, and ImageResource objects:
    
    Manifest
        Sequence
            Canvas
                ImageResource
            Canvas
                ImageResource
            Canvas
                ImageResource
    
    Each object must have a unique ID that can be mapped to a URL. For this implementation:
    
        -the Manifest may be uniquely identified by the resource ID.
        -the Sequence may be uniquely identified by "1" because there is only
         one Sequence in this implementation.
        -the Canvas may be uniquely identified by the image ID because
         Canvas:ImageResource is 1:1 in this implementation.
        -the ImageResource may be uniquely identified by the image ID.

    This is intended to be a minimal implementation of the IIIF 2.0 Presentation specification,
    so not all features are supported. 
    
    Usage:
    
    manifest = Manifest(request, 1)
    manifest.create(images=[
        {'id': 1, 'is_link': False, 'url': 'http://localhost:8000/loris/foo.jpg'},
        {'id': 2, 'is_link': False, 'url': 'http://localhost:8000/loris/bar.jpg'}
    ])
    output = manifest.to_json()
    print output
    '''
    def __init__(self, request, manifest_id, **kwargs):
        self.request = request
        self.id = manifest_id
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
    
    def find_object(self, object_type, object_id):
        if object_type == "manifest":
            if object_id == self.id:
                return self
        elif object_type == "sequence":
            for s in self.sequences:
                if object_id == s.id:
                    return s
        elif object_type == "canvas":
            for c in self.sequences[0].canvases:
                if object_id == c.id:
                    return c
        elif object_type == "resource":
            for c in self.sequences[0].canvases:
                if object_id == c.resource.id:
                    return c.resource
        return None
    
    def build_absolute_uri(self, url_name, url_args):
        reversed_url = reverse(url_name, kwargs=url_args)
        return self.request.build_absolute_uri(reversed_url)

    def build_url(self):
        return self.build_absolute_uri('iiif:manifest', {
            'manifest_id': self.id,
            'object_type': 'manifest',
        })

    def to_dict(self):
        manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@type": "sc:Manifest",
            "@id": self.build_url(),
            "label": self.label,
            "description": self.description,
            "sequences": [sequence.to_dict() for sequence in self.sequences]
        }
        return manifest

class Sequence(IIIFObject):
    def __init__(self, manifest, sequence_id):
        self.manifest = manifest
        self.id = sequence_id
        self.canvases = []

    def add_canvas(self, canvas_id):
        canvas = Canvas(self.manifest, canvas_id)
        self.canvases.append(canvas)
        return canvas
    
    def build_url(self):
        return self.manifest.build_absolute_uri('iiif:sequence', {
            'manifest_id': self.manifest.id,
            'object_type': 'sequence',
            'object_id': self.id
        })

    def to_dict(self):
        sequence = {
            "@id": self.build_url(),
            "@type": "sc:Sequence",
            "label": "Default order",
            "canvases": [canvas.to_dict() for canvas in self.canvases],
        }
        return sequence

class Canvas(IIIFObject):
    def __init__(self, manifest, canvas_id):
        self.manifest = manifest
        self.id = canvas_id
        self.label = 'Image'
        self.resource = None

    def add_image(self, image_id, image_url, is_link):
        self.resource = ImageResource(self.manifest, image_id, image_url, is_link)
        return self
    
    def set_label(self, label):
        self.label = label
        
    def build_url(self):
        return self.manifest.build_absolute_uri('iiif:canvas', {
            'manifest_id': self.manifest.id,
            'object_type': 'canvas',
            'object_id': self.id
        })

    def to_dict(self):
        canvas = {
            "@id": self.build_url(),
            "@type": "sc:Canvas",
            "label": self.label,
            "images": [{
                "@type": "oa:Annotation",
                "resource": self.resource.to_dict(),
                "on": self.build_url(),
            }],
            "width": 100, # TODO: get real width
            "height": 100, # TODO: get real height
        }
        return canvas

class ImageResource(IIIFObject):
    def __init__(self, manifest, resource_id, image_url, is_link=False):
        self.manifest = manifest
        self.id = resource_id
        self.image_url = image_url
        self.is_link = is_link
        
    def build_url(self):
        return self.manifest.build_absolute_uri('iiif:resource', {
            'manifest_id': self.manifest.id,
            'object_type': 'resource',
            'object_id': self.id
        })

    def to_dict(self):
        if self.is_link:
            resource = {
                "@id": self.image_url,
                "@type": "dctypes:Image",
            }
        else:
            resource = {
                "@id": self.build_url(),
                "@type": "dctypes:Image",
                "service": {
                    "@id": self.image_url,
                    "profile": "http://iiif.io/api/image/2/level1.json", 
                }
            }
        return resource
