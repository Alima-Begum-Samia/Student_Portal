from ..models import *
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..externalModuleApis import financeModuleApis
from datetime import datetime, timedelta


def all_courses(request):
  courses = OfferedCourses.objects.all()
  params = {
    'title':"All Courses",
    'tab_name':"all_courses",
    'courses':courses,
  }
  return render(request, "home/coursesList.html", params)


@login_required
def courseView(request, id):
    try:
        course = OfferedCourses.objects.get(course_id=id)
        existing_enrollment = CourseEnrollment.objects.filter(enrolledCourse=course, enrolledBy=request.user).first()
        params = {
            'course': course,
            'enrollment': existing_enrollment
        }
        return render(request, "home/singleCourseView.html", params)
    except OfferedCourses.DoesNotExist:
        messages.error(request, "Course not found.")
    except CourseEnrollment.DoesNotExist:
        params = {
            'course': course,            
        }
        return render(request, "home/singleCourseView.html", params)


@login_required
def enroll_course(request, id):
  try:
    course = OfferedCourses.objects.get(course_id=id)
    enrollmentReference = None
    if request.user in course.enrolled_students.all():
        messages.info(request, "You've already enrolled this Course.")
        return redirect('course-view', id=id)
    try:
       courseInvoice = financeModuleApis.create_new_invoice(float(course.course_amount), get_due_date(), "TUITION_FEES", request.user.user_id)
       if not courseInvoice["is_created"]:
          messages.error(request, "Failed to enroll course. Please ensure finance module is running")
          return redirect('course-view', id=id)
       enrollmentReference = courseInvoice["reference"]
    except Exception as e:
       print(e)
       return redirect('course-view', id=id)
    newEnrollment = CourseEnrollment.objects.create(enrolledCourse = course, enrolledBy = request.user, invoiceReference=enrollmentReference)
    if not newEnrollment is None:
        course.enrolled_students.add(request.user)
        course.save()
        messages.success(request, f"You've successfully enrolled this course. Invoice Reference is: {enrollmentReference}")
    else:
        messages.error(request, "Something Went wrong. Can't Enroll right now")
  except Exception as e:
    print(e)
  return redirect('course-view', id=id)


def cancel_enrollment(request, id):
    course = OfferedCourses.objects.get(course_id=id)
    try:
      enrollment = CourseEnrollment.objects.get(enrolledCourse = course, enrolledBy=request.user)
      if not enrollment is None:
        invoiceCanceled = financeModuleApis.cancel_invoice(enrollment.invoiceReference)
        if not invoiceCanceled['status'] == 200:
          messages.warning(request, "Can't Cancel Enrollment")
          return redirect("course-view", id=id)
        print(invoiceCanceled)
        enrollment.delete()
        course.enrolled_students.remove(request.user)
        course.save()
        messages.warning(request, "You've successfully cancelled the enrollment.")    
    except Exception as e:
      print(e)
      messages.error(request, "Something Went Wrong")
    return redirect('course-view', id=id)


@login_required
def my_enrollments(request):    
    courses = OfferedCourses.objects.filter(enrolled_students=request.user)
    params = {
       "title": "My Enrollments",
        "courses": courses,
        'tab_name':"enrolled_courses",
    }
    return render(request, 'home/coursesList.html', params)

@login_required
def search_course(request):
    if request.method == 'POST':
      if request.POST.get('query', '') == '':
        messages.error(request, "Please enter a valid search query.")
        return redirect('home')
      query = request.POST.get('query')
      courses = OfferedCourses.objects.filter(course_title__icontains=query)
      context = {
      'courses': courses,
      'title':"Search Results"
      }
      return render(request, 'home/coursesList.html', context)
    

def get_due_date():
    return (datetime.now().date() + timedelta(days=5)).strftime("%Y-%m-%d")
