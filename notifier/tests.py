###############################################################################
## Imports
###############################################################################
# Django
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.core import mail

# User
import notifier
from notifier import _get_permission_queryset
from notifier import models


###############################################################################
## Tests
###############################################################################
class PreferencesTests(TestCase):
    def setUp(self):
        self.email_backend = models.Backend.objects.get(name='email')

        self.sms_backend = models.Backend.objects.create(
            display_name='SMS',
            name='sms',
            enabled=True,
            description='SMS delivery method',
            klass='notifier.methods.Delivery')

        self.test1_notification = models.Notification.objects.create(
            display_name='Test Notification 1',
            name='test-not-1',
            public=True,
        )
        self.test1_notification.backends.add(
            self.email_backend, self.sms_backend)

        self.test2_notification = models.Notification.objects.create(
            display_name='Test Notification 2',
            name='test-not-2',
            public=False,
        )
        self.test2_notification.backends.add(
            self.email_backend)

        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com'
        )

        self.group1 = Group.objects.create(
            name='group1'
        )

        self.user1.groups.add(self.group1)

        models.GroupPrefs.objects.create(
            group=self.group1,
            notification=self.test1_notification,
            backend=self.email_backend,
            notify=True
        )

    def test1GroupPreference(self):
        """Test if group preference applies to user"""
        method_dict = self.test1_notification.get_user_prefs(user=self.user1)

        # print models.Backend.objects.values_list(
        #     'display_name', 'name', 'id')
        # print method_dict

        self.assertEqual(method_dict[self.email_backend], True,
            msg='Group notification preference failed.')

    def test2UserPreference(self):
        """Test if User preference supercedes group preference"""
        models.UserPrefs.objects.create(
            user=self.user1,
            notification=self.test1_notification,
            backend=self.email_backend,
            notify=False
        )

        method_dict = self.test1_notification.get_user_prefs(user=self.user1)

        # print models.Backend.objects.values_list(
        #     'display_name', 'name', 'id')
        # print method_dict

        self.assertEqual(method_dict[self.email_backend], False,
            msg='User notification preference failed.')


class PermissionTests(TestCase):
    """Tests related to permission checking for notifications."""

    def setUp(self):
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com'
        )

        self.permission1 = Permission.objects.create(
            codename='test-permission',
            name='Test Permission',
            content_type=ContentType.objects.get_for_model(User)
        )

        self.permission2 = Permission.objects.create(
            codename='test-permission-2',
            name='Test Permission 2',
            content_type=ContentType.objects.get_for_model(User)
        )

        self.test1_notification = models.Notification.objects.create(
            display_name='Test Notification 1',
            name='test-not-1',
            public=True,
        )
        self.test1_notification.permissions.add(self.permission1,
            self.permission2)

    def test1PermissionFunction(self):
        """Test the Notification.check_perms function."""
        self.assertEqual(self.test1_notification.check_perms(self.user1),
            False, msg='Permission check Failed')

        self.user1.user_permissions.add(self.permission1)
        # Django caches permissions on user, so refetch user from the database
        self.user1 = User.objects.get(pk=self.user1.pk)
        self.assertEqual(self.test1_notification.check_perms(self.user1),
            False, msg='Permission check Failed')

        self.user1.user_permissions.add(self.permission2)
        # Django caches permissions on user, so refetch user from the database
        self.user1 = User.objects.get(pk=self.user1.pk)
        self.assertEqual(self.test1_notification.check_perms(self.user1),
            True, msg='Permission check Failed')


class UtilityFunctionTests(TestCase):
    def test1GetPermissionQueryset(self):
        """Test the notifier._get_permission_queryset function."""
        permissions = Permission.objects.filter(id__in=[1, 2])

        # Compare querysets after converting to lists, becuase different
        # instance of same queryset will not test as equal.
        resp = _get_permission_queryset(permissions)
        # print resp
        self.assertEqual(list(resp), list(permissions),
            msg='Queryset input failed')

        resp = _get_permission_queryset(permissions[0])
        # print resp
        self.assertEqual(resp, [permissions.get(id=1)],
            msg='Single object input failed')

        resp = _get_permission_queryset(
            list(permissions.values_list('codename', flat=True)))
        # print resp
        self.assertEqual(list(resp), list(permissions),
            msg='Permission codename list input failed')

        resp = _get_permission_queryset(permissions[0].codename)
        # print resp
        self.assertEqual(list(resp), list(permissions.filter(id=1)),
            msg='Permission codename input failed')


class EmailTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com'
        )

        self.email_backend = models.Backend.objects.get(name='email')

        self.test_notification = notifier.create_notification(
            'test-notification',
            display_name='Test',
            permissions=None,  # No permissions required
            backends=None,  # All backend will be added ('email')
            public=True
        )

        models.UserPrefs.objects.create(
            user=self.user1,
            notification=self.test_notification,
            backend=self.email_backend,
            notify=True
        )

    def test_send_notification(self):
        notifier.send('test-notification', self.user1)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'django-notify test email')
