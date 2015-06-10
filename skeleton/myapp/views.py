from django.http import HttpResponse

def index(request, course_id=None):
    content = 'Welcome to my app. Course ID: %s User: %s' % (course_id, request.user.email)
    return HttpResponse(content)

