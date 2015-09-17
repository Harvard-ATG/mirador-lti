import unittest
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from .manifest import IIIFManifest

class IIIFManifestTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def create_manifest(self, manifest_id, **kwargs):
        request = self.factory.get(reverse('iiif:manifest', kwargs={"manifest_id":manifest_id, "object_type": "manifest"}))
        return (request, IIIFManifest(request, manifest_id, **kwargs))

    def create_images_list(self):
        images = [
            {'id': 1, 'is_link': False, 'url': 'http://localhost:8000/loris/foo.jpg', 'label': 'foo.jpg'},
            {'id': 2, 'is_link': False, 'url': 'http://localhost:8000/loris/bar.jpg', 'label': 'bar.jpg'},
            {'id': 3, 'is_link': True, 'url': 'http://my.link/image.jpg', 'label': 'image.jpg'},
        ]
        return images

    def test_create_manifest_with_images(self):
        request, manifest = self.create_manifest(1)
        images = self.create_images_list()
        manifest.create(images=images)
        md = manifest.to_dict()
        
        non_link_images = [img for img in images if img['is_link'] is False]

        self.assertEqual(len(md['sequences']), 1, "should have one default sequence")
        self.assertEqual(len(md['sequences'][0]['canvases']), len(non_link_images), "one canvas per image")
        for idx, canvas in enumerate(md['sequences'][0]['canvases']): 
            self.assertEqual(canvas['label'], non_link_images[idx]['label'], "canvas label should match image label")

    def test_manifest_attributes(self):
        label = 'test label'
        description = 'test description'
        request, manifest = self.create_manifest(1, label=label, description=description)
        md = manifest.to_dict()
        
        expected_attr = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@type": "sc:Manifest",
            "@id": request.build_absolute_uri(),
            "label": label,
            "description": description,
            "sequences": []
        }
        
        for key in expected_attr.keys():
            self.assertTrue(key in md, "manifest should have a %s attribute" % key)
            self.assertEqual(md[key], expected_attr[key])