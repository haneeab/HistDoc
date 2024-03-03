from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.messages.storage import session
from django.test import TestCase,tag
from django.urls import reverse,resolve
from django.test import Client
from ourproject.views import homepage_admin, conactus, add_product_admin, logoutcustomer,workers,worker_view_feedback,add_worker,add_worker2
from ourproject.views import logincustomer,loginAdmin,loginWorker,singup,products_worker,add_product_worker,update_product_worker,review_my_order,work_schedule,best_sales,customer,Admin_Reviewproduct_list,view_order
from ourproject.views import logincustomer,loginAdmin,loginWorker,singup,products_worker,add_product_worker,update_product_worker,review_my_order,work_schedule,best_sales,homepage_admin,conactus,homepage_worker
from ourproject.views import logincustomer,loginAdmin,loginWorker,singup,products_worker,add_product_worker,update_product_worker,review_my_order,work_schedule,best_sales,login,logoutcustomer,logoutadmin,logoutworker
import unittest
import requests
import json
from ourproject.forms import FeedbackForm
from django.shortcuts import render,get_object_or_404,redirect
from ourproject.models import *
from django.test import RequestFactory, TestCase
from django.urls import reverse
from ourproject.models import User, Order
from requests import Session


class Login_customerTest(TestCase):
    def testCustomerLoginUsedTemplate(self):
        response =self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/login_customer.html')
    def testCustomerLoginNotUsedTemplate(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/singup.html')
    def testLoginAccessUrl(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    def testloginaccessUrlNegetve(self):
        response = self.client.get('/login/')
        self.assertNotEqual(response.status_code, 300)
    def testloginUrlIsResolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func,logincustomer)
    def testloginAccessName(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    def testLoginAccessNameNegative(self):
        response = self.client.get(reverse('login'))
        self.assertNotEqual(response.status_code, 300)
class Login_adminTest(TestCase):
    def testAdminLoginUsedTemplate(self):
        response =self.client.get(reverse('loginadmin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/log_in_admin.html')
    def testAdminLoginNotUsedTemplate(self):
        response = self.client.get(reverse('loginadmin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/singup.html')
    def testLoginAccessUrl(self):
        response = self.client.get('/loginAdmin/')
        self.assertEqual(response.status_code, 200)
    def testloginaccessUrlNegetve(self):
        response = self.client.get('/loginAdmin/')
        self.assertNotEqual(response.status_code, 300)
    def testloginUrlIsResolved(self):
        url = reverse('loginadmin')
        self.assertEquals(resolve(url).func,loginAdmin)
    def testloginAccessName(self):
        response = self.client.get(reverse('loginadmin'))
        self.assertEqual(response.status_code, 200)
    def testLoginAccessNameNegative(self):
        response = self.client.get(reverse('loginadmin'))
        self.assertNotEqual(response.status_code, 300)
class Login_WorkerTest(TestCase):
    def testWorkerLoginUsedTemplate(self):
        response =self.client.get(reverse('loginWorker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/log_in_worker.html')
    def testWorkerLoginNotUsedTemplate(self):
        response = self.client.get(reverse('loginWorker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/singup.html')
    def testLoginAccessUrl(self):
        response = self.client.get('/loginWorker/')
        self.assertEqual(response.status_code, 200)
    def testloginaccessUrlNegetve(self):
        response = self.client.get('/loginWorker/')
        self.assertNotEqual(response.status_code, 300)
    def testloginUrlIsResolved(self):
        url = reverse('loginWorker')
        self.assertEquals(resolve(url).func,loginWorker)
    def testloginAccessName(self):
        response = self.client.get(reverse('loginWorker'))
        self.assertEqual(response.status_code, 200)
    def testLoginAccessNameNegative(self):
        response = self.client.get(reverse('loginWorker'))
        self.assertNotEqual(response.status_code, 300)
class singupTest(TestCase):
    def testsingupUsedTemplate(self):
        response =self.client.get(reverse('sigup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/singup.html')
    def testsingupNotUsedTemplate(self):
        response = self.client.get(reverse('sigup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testsingupAccessUrl(self):
        response = self.client.get('/singup/')
        self.assertEqual(response.status_code, 200)
    def testsingupaccessUrlNegetve(self):
        response = self.client.get('/singup/')
        self.assertNotEqual(response.status_code, 300)
    def testsingupUrlIsResolved(self):
        url = reverse('sigup')
        self.assertEquals(resolve(url).func,singup)
    def testsingupAccessName(self):
        response = self.client.get(reverse('sigup'))
        self.assertEqual(response.status_code, 200)
    def testsingupAccessNameNegative(self):
        response = self.client.get(reverse('sigup'))
        self.assertNotEqual(response.status_code, 300)
class review_worker_productTest(TestCase):
    def testreview_worker_productUsedTemplate(self):
        response =self.client.get(reverse('poducts_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/product_for_worker.html')
    def testreview_worker_productNotUsedTemplate(self):
        response = self.client.get(reverse('poducts_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testreview_worker_productAccessUrl(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
    def testreview_worker_productpaccessUrlNegetve(self):
        response = self.client.get('/products/')
        self.assertNotEqual(response.status_code, 300)
    def testreview_worker_productUrlIsResolved(self):
        url = reverse('poducts_worker')
        self.assertEquals(resolve(url).func,products_worker)
    def testreview_worker_productAccessName(self):
        response = self.client.get(reverse('poducts_worker'))
        self.assertEqual(response.status_code, 200)
    def testreview_worker_productAccessNameNegative(self):
        response = self.client.get(reverse('poducts_worker'))
        self.assertNotEqual(response.status_code, 300)
class add_product_workerTest(TestCase):
    def testadd_product_workerUsedTemplate(self):
        response =self.client.get(reverse('add_product_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/add_product_worker.html')
    def testadd_product_workerNotUsedTemplate(self):
        response = self.client.get(reverse('add_product_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testadd_product_workerAccessUrl(self):
        response = self.client.get('/add_product_worker/')
        self.assertEqual(response.status_code, 200)
    def testadd_product_workerpaccessUrlNegetve(self):
        response = self.client.get('/add_product_worker/')
        self.assertNotEqual(response.status_code, 300)
    def testadd_product_workerUrlIsResolved(self):
        url = reverse('add_product_worker')
        self.assertEquals(resolve(url).func,add_product_worker)
    def testadd_product_workerAccessName(self):
        response = self.client.get(reverse('add_product_worker'))
        self.assertEqual(response.status_code, 200)
    def testadd_product_workerAccessNameNegative(self):
        response = self.client.get(reverse('add_product_worker'))
        self.assertNotEqual(response.status_code, 300)
##########################################################################################################

# class customer_review_hisorderTest(TestCase):
#     def testcustomer_review_hisorderUsedTemplate(self):
#         response =self.client.get(reverse('review_my_order'))
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateNotUsed(response,'ourproject/review_myorder_customer.html')
#     def testcustomer_review_hisorderNotUsedTemplate(self):
#         response = self.client.get(reverse('review_my_order'))
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
#     def testcustomer_review_hisorderAccessUrl(self):
#         response = self.client.get('/review_my_order/')
#         self.assertEqual(response.status_code, 404)
#     def testcustomer_review_hisorderpaccessUrlNegetve(self):
#         response = self.client.get('/review_my_order/')
#         self.assertNotEqual(response.status_code, 300)
#     def testcustomer_review_hisorderUrlIsResolved(self):
#         url = reverse('review_my_order')
#         self.assertEquals(resolve(url).func,add_product_worker)
#     def testcustomer_review_hisorderAccessName(self):
#         response = self.client.get(reverse('review_my_order'))
#         self.assertEqual(response.status_code, 200)
#     def testacustomer_review_hisorderAccessNameNegative(self):
#         response = self.client.get(reverse('review_my_order'))
#         self.assertNotEqual(response.status_code, 300)
class work_scheduleTest(TestCase):
# class work_scheduleTest(TestCase):
    def testwork_scheduleUsedTemplate(self):
        response =self.client.get(reverse('work_schedule'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/buildschedule_forAdmin.html')
    def testcwork_scheduleNotUsedTemplate(self):
        response = self.client.get(reverse('work_schedule'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testwork_scheduleAccessUrl(self):
        response = self.client.get('/work_schedule/')
        self.assertEqual(response.status_code, 200)
    def testwork_schedulepaccessUrlNegetve(self):
        response = self.client.get('/work_schedule/')
        self.assertNotEqual(response.status_code, 300)
    def testwork_scheduleUrlIsResolved(self):
        url = reverse('work_schedule')
        self.assertEquals(resolve(url).func,work_schedule)
    def testwork_scheduleAccessName(self):
        response = self.client.get(reverse('work_schedule'))
        self.assertEqual(response.status_code, 200)
    def testwork_scheduleAccessNameNegative(self):
        response = self.client.get(reverse('work_schedule'))
        self.assertNotEqual(response.status_code, 300)
class best_salesTest(TestCase):
    def testbest_salesUrlIsResolved(self):
        url = reverse('best_sales')
        self.assertEquals(resolve(url).func,best_sales)
class homepage_adminTest(TestCase):
    def testhomepage_adminUsedTemplate(self):
        response =self.client.get(reverse('homepage_admin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/homepage_admin.html')
    def testhomepage_adminNotUsedTemplate(self):
        response = self.client.get(reverse('homepage_admin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testhomepage_adminAccessUrl(self):
        response = self.client.get('/homepageadmin/')
        self.assertEqual(response.status_code, 200)
    def testhomepage_adminpaccessUrlNegetve(self):
        response = self.client.get('/homepageadmin/')
        self.assertNotEqual(response.status_code, 300)
    def testhomepage_adminUrlIsResolved(self):
        url = reverse('homepage_admin')
        self.assertEquals(resolve(url).func,homepage_admin)
    def testhomepage_adminAccessName(self):
        response = self.client.get(reverse('homepage_admin'))
        self.assertEqual(response.status_code, 200)
    def testhomepage_admineAccessNameNegative(self):
        response = self.client.get(reverse('homepage_admin'))
        self.assertNotEqual(response.status_code, 300)
# class ReviewMyOrderTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.product = Product.objects.create(
#             bar_code='123',
#             name='Test Product',
#             price=10,
#             amount=10,
#             category='Drawing media',description='rrrrrrrr')
#         self.user = User.objects.create(username='testuser',first_name='firdt',last_name='lkm',email='jjj',password='123')
#         self.order = Order.objects.create(customer=self.user, order_number=888,price=6,amount=8,name_of_product='bbb',customer_name='hhh',product=self.product)
#     def test_review_my_order(self):
#         request = self.factory.get(reverse('review_my_order', kwargs={'pk': 'testuser'}))
#         request.user = self.user
#         response = review_my_order(request, 'testuser')
#         self.assertTemplateUsed(response, 'ourproject/review_myorder_customrt.html')
#         self.assertEqual(response.context_data['item'], 'testuser')
#         self.assertEqual(list(response.context_data['order']), [self.order])
#         self.assertEqual(response.status_code, 200)
class UpdateProductWorkerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            bar_code='123',
            name='Test Product',
            price=10,
            amount=10,
            category='Drawing media',
            description='rrrrrrrr',
        )
        self.url = reverse('update_product_worker', args=[self.product.bar_code])
        self.data = {
            'bar_code': '123',
            'name': 'Test Product Updated',
            'price': 12,
            'amount': 10,
            'category':'Drawing media',
            'description' : 'rrrrrrrr'
        }
    def test_update_product_worker(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Test Product Updated')
        self.assertEqual(self.product.price, 12)

# class ContactUsViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create(username='John Doe',first_name='firdt',last_name='lkm',email='jjj',password='123')
#     def test_form_submission(self):
#         data = {'customer': 'John Doe','feedback': 'Test message'}
#         request = self.factory.post(reverse('conactus'), data)
#         response = conactus(request)
#         self.assertEqual(response.status_code, 302)  # Expects a redirect
#         self.assertRedirects(response, reverse('homepage'))
#         self.assertEqual(FeedbackForm.objects.count(), 1)
#         feedback = FeedbackForm.objects.first()
#         self.assertEqual(feedback.customer, 'John Doe')
#         self.assertEqual(feedback.feedback, 'Test message')
#     def test_form_invalid(self):
#         data = {'customer': 'John Doe','feedback': 'Test message'}
#         request = self.factory.post(reverse('conactus'), data)
#         response = conactus(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(FeedbackForm.objects.count(), 0)
class homepage_workerTest(TestCase):
    def testhomepage_workerUsedTemplate(self):
        response =self.client.get(reverse('homepage_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/homepage_worker.html')
    def testhomepage_workerNotUsedTemplate(self):
        response = self.client.get(reverse('homepage_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testhomepage_workerAccessUrl(self):
        response = self.client.get('/homepageworker/')
        self.assertEqual(response.status_code, 200)
    def testhomepage_workerpaccessUrlNegetve(self):
        response = self.client.get('/homepageworker/')
        self.assertNotEqual(response.status_code, 300)
    def testhomepage_workerUrlIsResolved(self):
        url = reverse('homepage_worker')
        self.assertEquals(resolve(url).func,homepage_worker)
    def testhomepage_workerAccessName(self):
        response = self.client.get(reverse('homepage_worker'))
        self.assertEqual(response.status_code, 200)
    def testhomepage_workerAccessNameNegative(self):
        response = self.client.get(reverse('homepage_worker'))
        self.assertNotEqual(response.status_code, 300)


class review_admin_workersTest(TestCase):
    def testreview_admin_workersUsedTemplate(self):
        response =self.client.get(reverse('workers'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/workers.html')
    def testreview_admin_workersNotUsedTemplate(self):
        response = self.client.get(reverse('workers'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/homepage_admin.html')
    def testreview_admin_workersAccessUrl(self):
        response = self.client.get('/workers/')
        self.assertEqual(response.status_code, 200)
    def testreview_admin_workerspaccessUrlNegetve(self):
        response = self.client.get('/workers/')
        self.assertNotEqual(response.status_code, 300)
    def testreview_admin_workersUrlIsResolved(self):
        url = reverse('workers')
        self.assertEquals(resolve(url).func,workers)
    def testreview_admin_workersAccessName(self):
        response = self.client.get(reverse('workers'))
        self.assertEqual(response.status_code, 200)
    def testreview_admin_workersAccessNameNegative(self):
        response = self.client.get(reverse('workers'))
        self.assertNotEqual(response.status_code, 300)


class add_worker_adminTest(TestCase):
    def testadd_worker_adminUsedTemplate(self):
        response =self.client.get(reverse('add_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/add_worker.html')
    def testadd_worker_adminNotUsedTemplate(self):
        response = self.client.get(reverse('add_worker'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/workers.html')
    def testadd_worker_adminAccessUrl(self):
        response = self.client.get('/addworker/')
        self.assertEqual(response.status_code, 200)
    def testadd_worker_adminpaccessUrlNegetve(self):
        response = self.client.get('/addworker/')
        self.assertNotEqual(response.status_code, 300)
    def testadd_worker_adminUrlIsResolved(self):
        url = reverse('add_worker')
        self.assertEquals(resolve(url).func,add_worker)
    def testadd_worker_adminAccessName(self):
        response = self.client.get(reverse('add_worker'))
        self.assertEqual(response.status_code, 200)
    def testadd_worker_adminAccessNameNegative(self):
        response = self.client.get(reverse('add_worker'))
        self.assertNotEqual(response.status_code, 300)


class add_worker2_adminTest(TestCase):
    def testadd_worker2_adminUsedTemplate(self):
        response =self.client.get(reverse('add_worker2'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/add_worker2.html')
    def testadd_worker2_adminNotUsedTemplate(self):
        response = self.client.get(reverse('add_worker2'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/workers.html')
    def testadd_worker2_adminAccessUrl(self):
        response = self.client.get('/addworker2/')
        self.assertEqual(response.status_code, 200)
    def testadd_worker2_adminpaccessUrlNegetve(self):
        response = self.client.get('/addworker2/')
        self.assertNotEqual(response.status_code, 300)
    def testadd_worker2_adminUrlIsResolved(self):
        url = reverse('add_worker2')
        self.assertEquals(resolve(url).func,add_worker2)
    def testadd_worker2_adminAccessName(self):
        response = self.client.get(reverse('add_worker2'))
        self.assertEqual(response.status_code, 200)
    def testadd_worker2_adminAccessNameNegative(self):
        response = self.client.get(reverse('add_worker2'))
        self.assertNotEqual(response.status_code, 300)

class review_worker_feedbackTest(TestCase):
    def testreview_worker_feedbackUsedTemplate(self):
        response =self.client.get(reverse('worker_view_feedback'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ourproject/worker_view_feedback.html')
    def testreview_worker_feedbackNotUsedTemplate(self):
        response = self.client.get(reverse('worker_view_feedback'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/homepage_worker.html')
    def testreview_worker_feedbackAccessUrl(self):
        response = self.client.get('/worker_view_feedback/')
        self.assertEqual(response.status_code, 200)
    def testreview_worker_feedbackpaccessUrlNegetve(self):
        response = self.client.get('/worker_view_feedback/')
        self.assertNotEqual(response.status_code, 300)
    def testreview_worker_feedbackUrlIsResolved(self):
        url = reverse('worker_view_feedback')
        self.assertEquals(resolve(url).func,worker_view_feedback)
    def testreview_worker_feedbackAccessName(self):
        response = self.client.get(reverse('worker_view_feedback'))
        self.assertEqual(response.status_code, 200)
    def testreview_worker_feedbackAccessNameNegative(self):
        response = self.client.get(reverse('worker_view_feedback'))
        self.assertNotEqual(response.status_code, 300)

# class LogoutWorkerTest(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#     def test_logout_worker(self):
#         # Create a request and log in a user
#         request = self.factory.get(reverse('login'))
#         request.user = User.objects.create_user(username='testuser', password='testpassword',first_name='fff',last_name='ffff',email='ffff@gmail.com')
#         request.new_group = Group.objects.get_or_create(name='Worker')
#         request.user.groups.add(Group.objects.get(name='Worker'))
#         request.user.save()
#         login(request, request.user)
#         response = logoutworker(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/login/')
#         self.assertFalse(request.user.is_authenticated)
# class LogoutAdminTest(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#     def test_logout_admin(self):
#         # Create a request and log in a user
#         request = self.factory.get(reverse('login'))
#         request.user = User.objects.create_user(username='testuser', password='testpassword',first_name='fff',last_name='ffff',email='ffff@gmail.com')
#         request.new_group = Group.objects.get_or_create(name='Admin')
#         request.user.groups.add(Group.objects.get(name='Admin'))
#         request.user.save()
#         login(request, request.user)
#         response = logoutadmin(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/login/')
#         self.assertFalse(request.user.is_authenticated)
# class customer_listTest(TestCase):
#     def testcustomer_listUsedTemplate(self):
#        response =self.client.get(reverse('customer_list'))
#        self.assertEquals(response.status_code, 200)
#        self.assertTemplateUsed(response,'ourproject/customer_list.html')
#     def testcustomer_listNotUsedTemplate(self):
#         response = self.client.get(reverse('customer_list'))
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateNotUsed(response, 'ourproject/singup.html')
#     def tescustomer_listAccessUrl(self):
#         response = self.client.get('/customers/')
#         self.assertEqual(response.status_code, 200)
#     def testcustomer_listaccessUrlNegetve(self):
#         response = self.client.get('/customers/')
#         self.assertNotEqual(response.status_code, 300)
#     def testcustomer_listUrlIsResolved(self):
#         url = reverse('customer_list')
#         self.assertEquals(resolve(url).func,customer)
#     def testcustomer_listAccessName(self):
#         response = self.client.get(reverse('customer_list'))
#         self.assertEqual(response.status_code, 200)
#     def testcustomer_listAccessNameNegative(self):
#         response = self.client.get(reverse('customer_list'))
#         self.assertNotEqual(response.status_code, 300)
class review_admin_productTest(TestCase):
    def testreview_admin_productUsedTemplate(self):
        response = self.client.get(reverse('Admin_Reviewproduct_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ourproject/Admin_Reviewproduct_list.html')

    def testreview_admin_productNotUsedTemplate(self):
        response = self.client.get(reverse('Admin_Reviewproduct_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')
    def testreview_admin_productAccessUrl(self):
        response = self.client.get('/Admin_Reviewproduct_list/')
        self.assertEqual(response.status_code, 200)

    def testreview_admin_productpaccessUrlNegetve(self):
        response = self.client.get('/Admin_Reviewproduct_list/')
        self.assertNotEqual(response.status_code, 300)

    def testreview_admin_productUrlIsResolved(self):
        url = reverse('Admin_Reviewproduct_list')
        self.assertEquals(resolve(url).func, Admin_Reviewproduct_list)

    def testreview_admin_productAccessName(self):
        response = self.client.get(reverse('Admin_Reviewproduct_list'))
        self.assertEqual(response.status_code, 200)

    def testreview_admin_productAccessNameNegative(self):
        response = self.client.get(reverse('Admin_Reviewproduct_list'))
        self.assertNotEqual(response.status_code, 300)

class add_product_adminTest(TestCase):
    def testadd_product_workerUsedTemplate(self):
        response = self.client.get(reverse('add_product_admin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ourproject/add_product_admin.html')

    def testadd_product_adminNotUsedTemplate(self):
        response = self.client.get(reverse('add_product_admin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')

    def testadd_product_adminAccessUrl(self):
        response = self.client.get('/add_product_admin/')
        self.assertEqual(response.status_code, 200)

    def testadd_product_adminpaccessUrlNegetve(self):
        response = self.client.get('/add_product_admin/')
        self.assertNotEqual(response.status_code, 300)

    def testadd_product_adminUrlIsResolved(self):
        url = reverse('add_product_admin')
        self.assertEquals(resolve(url).func, add_product_admin)

    def testadd_product_adminAccessName(self):
        response = self.client.get(reverse('add_product_admin'))
        self.assertEqual(response.status_code, 200)

    def testadd_product_adminAccessNameNegative(self):
        response = self.client.get(reverse('add_product_admin'))
        self.assertNotEqual(response.status_code, 300)
class UpdateProductadminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            bar_code='123',
            name='Test Product',
            price=10,
            amount=10,
            category='Drawing media',
            description='rrrrrrrr',
        )
        self.url = reverse('update_product_admin', args=[self.product.bar_code])
        self.data = {
            'bar_code': '123',
            'name': 'Test Product Updated',
            'price': 12,
            'amount': 10,
            'category':'Drawing media',
            'description' : 'rrrrrrrr'
        }
    def test_update_product_admin(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Test Product Updated')
        self.assertEqual(self.product.price, 12)
class order_listTest(TestCase):
    def testorder_listUsedTemplate(self):
        response = self.client.get(reverse('view_order'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ourproject/order_list.html')

    def testorder_listNotUsedTemplate(self):
        response = self.client.get(reverse('view_order'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'ourproject/dashboard.html')

    def testorder_listAccessUrl(self):
        response = self.client.get('/view_order/')
        self.assertEqual(response.status_code, 200)

    def testorder_listpaccessUrlNegetve(self):
        response = self.client.get('/view_order/')
        self.assertNotEqual(response.status_code, 300)

    def testorder_listUrlIsResolved(self):
        url = reverse('view_order')
        self.assertEquals(resolve(url).func, view_order)

    def testorder_listAccessName(self):
        response = self.client.get(reverse('view_order'))
        self.assertEqual(response.status_code, 200)

    def testorder_listAccessNameNegative(self):
        response = self.client.get(reverse('view_order'))
        self.assertNotEqual(response.status_code, 300)

# class LogoutCustomerTest(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#     def test_logout_customer(self):
#         # Create a request and log in a user
#         request = self.factory.get(reverse('login'))
#         request.user = User.objects.create_user(username='testuser', password='testpassword',first_name='fff'
#                                                 ,last_name='ffff',email='ffff@gmail.com')
#         request.new_group = Group.objects.get_or_create(name='Customer')
#         request.user.groups.add(Group.objects.get(name='Customer'))
#         request.user.save()
#         login(request, request.user)
#         response = logoutcustomer(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/login/')
#         self.assertFalse(request.user.is_authenticated)

