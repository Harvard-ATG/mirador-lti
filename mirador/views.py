from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse
from .models import LTICourseImages, LTICourseCollections
from mirador.isite import IsiteImageDataLoader, iSiteImageDataSource, assign_images
import json
import logging
import StringIO

def _build_manifest_uri(request, manifest_id):
    return request.build_absolute_uri(reverse("iiif:manifest", kwargs={
        'manifest_id': manifest_id,
        'object_type': 'manifest',
    }))

def index(request, course_id):
    '''Renders the page with Mirador, which loads the images specified by the IIIF manifest.'''

    # Add manifest of images for the whole course (across collections)
    manifests = [{
        "manifestUri": _build_manifest_uri(request, course_id),
        "location": "Harvard University",
    }]

    # Add manifest for each collection of images
    collection_ids = LTICourseImages.objects.filter(course__id=course_id).distinct().values_list('collection', flat=True)
    collections = []
    if len(collection_ids) > 0:
        collections = LTICourseCollections.objects.filter(id__in=collection_ids).order_by('sort_order', 'label')

    for collection in collections:
        manifest_id = "%s:%s" % (course_id, collection.id)
        manifests.append({
            "manifestUri": _build_manifest_uri(request, manifest_id),
            "location": "Harvard University",
        })

    return render(request, 'mirador.html', {"manifests_json": json.dumps(manifests)})

def import_api_load(request):
    logger = logging.getLogger(__file__)
    log_capture_string = StringIO.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    loader = IsiteImageDataLoader({
        'key': settings.AWS_KEY,
        'secret': settings.AWS_SECRET,
        'bucket': settings.S3_BUCKET, 
    }, logger)

    if "reload" in request.GET:
        loader.delete_all()

    dry_run = False
    if "dryrun" in request.GET:
        dry_run = True

    loader.load_all(dry_run=dry_run)

    log_contents = log_capture_string.getvalue()
    log_capture_string.close()   

    return HttpResponse(log_contents, content_type="text/plain")

def import_api_assign(request):
    logger = logging.getLogger(__file__)
    log_capture_string = StringIO.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    
    course_id = request.GET.get('course_id', None)
    keyword = request.GET.get('keyword', None)
    topic_id = None
    if topic_id in request.GET:
        topic_id = request.GET.get('topic_id', None)

    assign_images(course_id, keyword, topic_id=topic_id, logger=logger)

    log_contents = log_capture_string.getvalue()
    log_capture_string.close()

    return HttpResponse(log_contents, content_type="text/plain")
