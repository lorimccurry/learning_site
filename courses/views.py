from django.shortcuts import render
from django.http import HttpResponse

from .models import Course

def course_list(request):
    courses = Course.objects.all()
    output = ', '.join(courses)
    return HttpResponse(output)
