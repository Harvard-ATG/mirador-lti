from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test

from .isite import IsiteImageDataLoader, iSiteImageDataSource, IsiteImageAssigner
from .manifests import ManifestLinks

import logging
import StringIO

def index(request, resource_id):
    '''
    Loads Mirador with a set of links to IIIF manifests.
    Each manifest link corresponds to a collection of images associated with the tool. 
    '''
    manifest_links = ManifestLinks(request, resource_id)
    context = {
        "manifests_json": manifest_links.get_links_json(),
    }
    return render(request, 'mirador.html', context)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def import_api_assign(request):
    logger = logging.getLogger(__file__)
    log_capture_string = StringIO.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    
    resource_id = request.GET.get('resource_id', None)
    keyword = request.GET.get('keyword', None)
    topic_id = None
    if topic_id in request.GET:
        topic_id = request.GET.get('topic_id', None)

    isite_image_assigner = IsiteImageAssigner(resource_id, keyword, topic_id=topic_id, logger=logger)
    isite_image_assigner.assign()

    log_contents = log_capture_string.getvalue()
    log_capture_string.close()

    return HttpResponse(log_contents, content_type="text/plain")
