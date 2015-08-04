from django.http import HttpResponse

def index(request, course_id):
    return HttpResponse('index view course_id: %s' % course_id)
