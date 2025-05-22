from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from roads.permissions import IsAdmin 

class IsAdminTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='admin')
        self.non_admin_user = User.objects.create_user(username='foo' password='bar')
        self.factory = RequestFactory()
        self.permission_check = IsAdmin()

    def test_admin_user_has_permission(self):
        for method in ['get', 'post', 'delete', 'patch']:
            request = getattr(self.factory, method)('/')
            request.user = self.admin_user
            self.assertTrue(self.permission_check.has_permission(request, None))

    def test_non_admin_user_no_permission(self):
        for method in ['get', 'post', 'delete', 'patch']:
            request = getattr(self.factory, method)('/')
            request.user = self.non_admin_user
            if method == "get":
                self.assertTrue(self.permission_check.has_permission(request, None))
            else: 
                self.assertFalse(self.permission_check.has_permission(request, None))
