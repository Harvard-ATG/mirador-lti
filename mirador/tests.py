import unittest
from mock import MagicMock
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from .manifests import ManifestLinks

class ManifestLinksTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def create_manifest_links(self, resource_id):
        request = self.factory.get(reverse('mirador:index', kwargs={"resource_id":resource_id}))
        manifest_links = ManifestLinks(request, resource_id)
        return (request, manifest_links)

    def test_build_manifest_uri(self):
        for tup in [(1,None,"1"), (1,123,"1:123"), (2,987,"2:987")]:
            resource_id, collection_id, manifest_id = tup
            request, manifest_links = self.create_manifest_links(resource_id)
            expected_link = request.build_absolute_uri(reverse('iiif:manifest', kwargs={
                "manifest_id": manifest_id, 
                "object_type": "manifest"
            }))
            given_link = manifest_links.build_manifest_uri(collection_id)
            self.assertEqual(given_link, expected_link)

    def create_mock_collections(self):
        class DummyCollection:
            def __init__(self, id):
                self.id = id
        collections = [DummyCollection(n) for n in range(10)]
        return collections
 
    def test_get_collections(self):
        resource_id = 1
        request, manifest_links = self.create_manifest_links(resource_id)
        collections = self.create_mock_collections()

        manifest_links.get_collections = MagicMock(manifest_links, return_value=collections)
        self.assertEqual(manifest_links.get_collections(), collections)

    def test_get_links(self):
        resource_id = 1
        request, manifest_links = self.create_manifest_links(resource_id)
        collections = self.create_mock_collections()

        manifest_links.get_collections = MagicMock(manifest_links, return_value=collections)
        self.assertEqual(manifest_links.get_collections(), collections)
        
        for has_all_link in [True, False]:
            manifest_links.has_all_link = has_all_link

            expected_num_links = len(collections)
            if manifest_links.has_all_link:
                expected_num_links += 1

            given_links = manifest_links.get_links()
            self.assertEqual(len(given_links), expected_num_links)

            for link in given_links:
                self.assertIn('location', link)
                self.assertEqual(link['location'], manifest_links.location)
                self.assertIn('manifestUri', link)
                self.assertTrue(link['manifestUri'].startswith('http'))
