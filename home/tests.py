from django.test import TestCase
from home.models import User
from django.urls import reverse
from django.test import Client
from django.contrib.messages import get_messages
from .models import OfferedCourses, CourseEnrollment
from unittest.mock import patch


# user registration test cases
class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_success(self):
        # Ensure registration succeeds with valid data
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'test_user',
            'password': 'test_password',
            'password2': 'test_password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='test_user').exists())  
        self.assertRedirects(response, reverse('home'))   

    def test_registration_missing_fields(self):
        # Ensure registration fails if any field is missing
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': '',   
            'password': 'test_password',
            'password2': 'test_password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(User.objects.filter(email='test@example.com').exists())  
        self.assertRedirects(response, reverse('home'))   

    def test_registration_password_mismatch(self):
        # Ensure registration fails if passwords do not match
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'test_user',
            'password': 'test_password',
            'password2': 'mismatched_password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(User.objects.filter(username='test_user').exists())   
        self.assertRedirects(response, reverse('home'))  

    def test_registration_existing_username(self):
        # Ensure registration fails if username already exists
        User.objects.create_user(username='existing_user', email='existing@example.com', password='existing_password')
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'existing_user',  
            'password': 'test_password',
            'password2': 'test_password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(User.objects.filter(email='test@example.com').exists())  
        self.assertRedirects(response, reverse('home'))  

    def test_registration_existing_email(self):
        # Ensure registration fails if email already exists
        User.objects.create_user(username='existing_user', email='existing@example.com', password='existing_password')
        response = self.client.post(reverse('register'), {
            'email': 'existing@example.com',   
            'username': 'test_user',
            'password': 'test_password',
            'password2': 'test_password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(User.objects.filter(username='test_user').exists()) 
        self.assertRedirects(response, reverse('home')) 

    def test_registration_get_request(self):
        # Ensure registration fails with GET request
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  


# user login/authentication test cases
class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')

    def test_login_success(self):
        # Ensure login succeeds with valid credentials
        response = self.client.post(reverse('login'), {
            'username': 'test_user',
            'password': 'test_password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertIn('_auth_user_id', self.client.session)  
        self.assertRedirects(response, reverse('home')) 

    def test_login_missing_credentials(self):
        # Ensure login fails if username or password is missing
        response = self.client.post(reverse('login'), {
            'username': '',   
            'password': 'test_password'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertNotIn('_auth_user_id', self.client.session) 
        self.assertRedirects(response, reverse('home'))   

        response = self.client.post(reverse('login'), {
            'username': 'test_user',
            'password': ''  # Missing password
        })
        self.assertEqual(response.status_code, 302)  
        self.assertNotIn('_auth_user_id', self.client.session)  
        self.assertRedirects(response, reverse('home'))  

    def test_login_invalid_credentials(self):
        # Ensure login fails with invalid credentials
        response = self.client.post(reverse('login'), {
            'username': 'test_user',
            'password': 'invalid_password'
        })
        self.assertEqual(response.status_code, 302)   
        self.assertNotIn('_auth_user_id', self.client.session)  
        self.assertRedirects(response, reverse('home')) 

    def test_login_get_request(self):
        # Ensure login fails with GET request
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('home')) 


# enroll course test cases
class EnrollCourseViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.course = OfferedCourses.objects.create(course_title='Test Course', course_description='Description of Test Course', course_amount=100.00)
        self.course_id = self.course.course_id

    @patch('home.externalModuleApis.financeModuleApis.create_new_invoice')
    def test_enroll_course_success(self, mock_create_new_invoice):
        mock_create_new_invoice.return_value = {"is_created": True, "reference": "INVOICE123"}
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('enroll-course', args=[self.course_id]))
        
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(self.user in self.course.enrolled_students.all()) 
        self.assertTrue(CourseEnrollment.objects.filter(enrolledCourse=self.course, enrolledBy=self.user).exists()) 
        self.assertRedirects(response, reverse('course-view', args=[self.course_id])) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  
        self.assertEqual(str(messages[0]), f"You've successfully enrolled this course. Invoice Reference is: INVOICE123")

    @patch('home.externalModuleApis.financeModuleApis.create_new_invoice')
    def test_enroll_course_already_enrolled(self, mock_create_new_invoice):
        self.course.enrolled_students.add(self.user)

        self.client.force_login(self.user)
        response = self.client.get(reverse('enroll-course', args=[self.course_id]))

        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('course-view', args=[self.course_id])) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  
        self.assertEqual(str(messages[0]), "You've already enrolled this Course.") 

    @patch('home.externalModuleApis.financeModuleApis.create_new_invoice')
    def test_enroll_course_finance_failure(self, mock_create_new_invoice):
        mock_create_new_invoice.return_value = {"is_created": False}
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('enroll-course', args=[self.course_id]))

        self.assertEqual(response.status_code, 302) 
        self.assertFalse(self.user in self.course.enrolled_students.all()) 
        self.assertFalse(CourseEnrollment.objects.filter(enrolledCourse=self.course, enrolledBy=self.user).exists()) 
        self.assertRedirects(response, reverse('course-view', args=[self.course_id]))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  
        self.assertEqual(str(messages[0]), "Failed to enroll course. Please ensure finance module is running")  


    @patch('home.externalModuleApis.financeModuleApis.create_new_invoice')
    def test_enroll_course_exception(self, mock_create_new_invoice):
        mock_create_new_invoice.side_effect = Exception("Test exception")
        self.client.force_login(self.user)
        response = self.client.get(reverse('enroll-course', args=[self.course_id]))

        self.assertEqual(response.status_code, 302) 
        self.assertFalse(self.user in self.course.enrolled_students.all())  
        self.assertFalse(CourseEnrollment.objects.filter(enrolledCourse=self.course, enrolledBy=self.user).exists())
        self.assertRedirects(response, reverse('course-view', args=[self.course_id])) 


#