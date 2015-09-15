from django.core.urlresolvers import reverse
from .models import LTIResourceImages, LTIResourceCollections

import json

class ManifestLinks:
    '''
    This class is responsible for generating the set of IIIF manifest URLs
    that Mirador will consume. Each manifest URL corresponds to a collection
    of images.
    '''
    def __init__(self, request, resource_id):
        self.request = request
        self.resource_id = resource_id
        self.location = "Harvard University"
        self.has_all_link = True

    def build_manifest_uri(self, collection_id=None):
        '''
        Builds a fully qualified URL to the manifest.
        '''
        if collection_id is None:
            manifest_id = self.resource_id
        else:
            manifest_id = "%s:%s" % (self.resource_id, collection_id)

        return self.request.build_absolute_uri(reverse("iiif:manifest", kwargs={
            'manifest_id': manifest_id,
            'object_type': 'manifest',
        }))

    def get_links(self):
        '''
        Returns links for each collection's manifest as well as an "all" manifest.
        '''
        return self.get_all_link() + self.get_collection_links()

    def get_links_json(self):
        '''
        Returns the links formatted as JSON.
        '''
        return json.dumps(self.get_links())

    def get_all_link(self):
        '''
        Returns a link to a manifest that will contain *all* images of the resource.
        '''
        if not self.has_all_link:
            return []
        return [{
            "manifestUri": self.build_manifest_uri(),
            "location": self.location,
        }]
    
    def get_collection_links(self):
        '''
        Returns links to each collection's manifest.
        '''
        collections = self.get_collections()
        return [{
            "location": self.location,
            "manifestUri": self.build_manifest_uri(collection.id), 
        } for collection in collections]

    def get_collections(self):
        collections = []
        collection_ids = LTIResourceImages.objects.filter(resource__id=self.resource_id).distinct().values_list('collection', flat=True)
        if len(collection_ids) > 0:
            collections = LTIResourceCollections.objects.filter(id__in=collection_ids).order_by('sort_order', 'label')
        return collections

