###############################################################################
## Imports
###############################################################################
# Django
from django import forms
from django.forms.formsets import BaseFormSet

# User
from notifier.models import Notification


###############################################################################
## Forms
###############################################################################
class NotificationForm(forms.Form):
    def __init__(self, user=None, notification=None, *args, **kwargs):
        if not user:
            # Use try/except?
            user = kwargs['initial'].pop('user')
        if not notification:
            # Use try/except?
            notification = kwargs['initial'].pop('notification')

        super(NotificationForm, self).__init__(*args, **kwargs)

        self.user = user
        self.notification = notification
        self.prefs_dict = notification.get_user_prefs(user)
        self.dm = set()
        self.title = notification.display_name

        for deliverymethod, value in self.prefs_dict.items():
            self.dm.add(deliverymethod)
            self.fields[deliverymethod.name] = forms.BooleanField(
                required=False)
            self.fields[deliverymethod.name].initial = value

    def save(self, *args, **kwargs):
        for deliverymethod, value in self.prefs_dict.items():
            self.prefs_dict[deliverymethod] = self.cleaned_data[deliverymethod.name]
        return self.notification.update_user_prefs(self.user, self.prefs_dict)


###############################################################################
## Formset
###############################################################################
class NotificationFormSet(BaseFormSet):
    def __init__(self, user, data=None, files=None, **kwargs):
        notifications = Notification.objects.get_user_notifications(user)
        kwargs['initial'] = []

        for notification in notifications:
            kwargs['initial'].append(
                {'notification': notification, 'user': user})

        self.form = NotificationForm
        self.extra = 0
        self.can_order = False
        self.can_delete = False
        self.max_num = 100  # Required for >=Dj1.4.5
        self.absolute_max = 100  # Required for >=Dj1.4.5

        super(NotificationFormSet, self).__init__(data, files, **kwargs)

        self.dm = set()
        for form in self.forms:
            self.dm = self.dm.union(form.dm)

    def save(self, *args, **kwargs):
        for form in self.forms:
            form.save()
