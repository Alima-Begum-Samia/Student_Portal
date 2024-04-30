
from django.urls import path
from .views import homeViews, authenticationViews, courseViews, profileViews, libraryAndFinanceViews
urlpatterns = [
    # Home urls
    path("", homeViews.home, name="home"),
    path('not-logged-in', homeViews.notLoggedIn, name='not-logged-in'),

    # Authentication urls 
    path('login', authenticationViews.login_view, name="login"),
    path('logout', authenticationViews.logout_view, name="logout"),
    path('register', authenticationViews.register_view, name="register"),
    path('update-password',authenticationViews.update_password , name='update-password'),

    # profile url
    path("profile", profileViews.showProfile, name="profile"),
    path("update-profile", profileViews.update_profile, name="update-profile"),
    
    # Course url 
    path("all-courses", courseViews.all_courses, name="all-courses"),
    path("course-view/<int:id>", courseViews.courseView, name="course-view"),
    path('enroll-course/<int:id>', courseViews.enroll_course, name="enroll-course"),
    path('cancel-enrollment/<int:id>', courseViews.cancel_enrollment, name="cancel-enrollment"),
    path('my-enrollments', courseViews.my_enrollments, name="my-enrollments"),
    path('search-course', courseViews.search_course, name="search-course"),

    # Finance & Library url
    path("invoices", libraryAndFinanceViews.all_invoices, name="invoices"),
    path('library-info', libraryAndFinanceViews.libraryAccountInfo, name="library-info"),
    path("graduation-status", libraryAndFinanceViews.graduation_status, name="graduation-status"),
]