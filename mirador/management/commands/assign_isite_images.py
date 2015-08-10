from django.core.management.base import BaseCommand, CommandError
from mirador.models import IsiteImages, LTICourseImages

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('course_id', help="LTI Course ID") 
        parser.add_argument('keyword', help="iSite keyword")
        parser.add_argument('--topic_id', help="iSite topic_id")

    def handle(self, *args, **options):
        course_id = options['course_id']
        keyword = options['keyword']
        topic_id = options['topic_id']

        filter_by = {'isite_keyword': options['keyword']}
        if options['topic_id'] is not None:
            filter_by['isite_topic_id'] = options['topic_id']

        isite_images = IsiteImages.objects.filter(**filter_by)
        self.stdout.write('Number of images to assign: %s' % len(isite_images))

        lti_course = LTICourseImages.get_lti_course(options['course_id'])
        LTICourseImages.objects.filter(course=lti_course).delete()
        self.stdout.write('Deleted all images assigned to course %s' % lti_course)

        course_image_records = [LTICourseImages(course=lti_course, isite_image=isite_image) for isite_image in isite_images]
        LTICourseImages.objects.bulk_create(course_image_records)
        self.stdout.write('Assigned %s images to course %s' % (len(course_image_records), lti_course))

