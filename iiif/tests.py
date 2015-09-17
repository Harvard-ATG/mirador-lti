import unittest
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from .manifest import IIIFManifest

class ManifestLinksTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def create_manifest(self, manifest_id, **kwargs):
        request = self.factory.get(reverse('iiif:manifest', kwargs={"manifest_id":manifest_id, "object_type": "manifest"}))
        manifest = IIIFManifest(request, manifest_id, **kwargs)
        return (request, manifest)

    def create_images_list(self):
        images = [
            {'id': 1, 'is_link': False, 'url': 'http://localhost:8000/loris/foo.jpg', 'label': 'foo.jpg'},
            {'id': 2, 'is_link': False, 'url': 'http://localhost:8000/loris/bar.jpg', 'label': 'bar.jpg'},
            {'id': 3, 'is_link': True, 'url': 'http://my.link/image.jpg', 'label': 'image.jpg'},
        ]
        return images

    def test_create_manifest(self):
        manifest_id = 1
        request, manifest = self.create_manifest(manifest_id)
        manifest.create(images=self.create_images_list())
        manifest_dict = manifest.to_dict()
        self.assertTrue(manifest_dict)
