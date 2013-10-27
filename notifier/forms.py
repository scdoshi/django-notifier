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
class NotifierForm(forms.Form):
    def __init__(self, user=None, notification=None, *args, **kwargs):
        if not user:
            # Use try/except?
            user = kwargs['initial'].pop('user')
        if not notification:
            # Use try/except?
            notification = kwargs['initial'].pop('notification')

        super(NotifierForm, self).__init__(*args, **kwargs)

        self.user = user
        self.notification = notification
        self.prefs_dict = notification.get_user_prefs(user)
        self.backends_included = set()
        self.title = notification.display_name

        for backend, value in self.prefs_dict.items():
            self.backends_included.add(backend)
            self.fields[backend.name] = forms.BooleanField(
                required=False
            )
            self.fields[backend.name].initial = value

    def save(self, *args, **kwargs):
        for backend, value in self.prefs_dict.items():
            self.prefs_dict[backend] = self.cleaned_data[backend.name]
        return self.notification.update_user_prefs(self.user, self.prefs_dict)


###############################################################################
## Formset
###############################################################################
class NotifierFormSet(BaseFormSet):
    def __init__(self, user, data=None, files=None, **kwargs):
        notifications = Notification.objects.get_user_notifications(user)
        kwargs['initial'] = []

        for notification in notifications:
            kwargs['initial'].append(
                {'notification': notification, 'user': user})

        self.form = NotifierForm
        self.extra = 0
        self.can_order = False
        self.can_delete = False
        self.max_num = 100  # Required for >=Dj1.4.5
        self.absolute_max = 100  # Required for >=Dj1.4.5

        super(NotifierFormSet, self).__init__(data, files, **kwargs)

        # This is a list of backends used in the form for use in the template.
        self.backends_included = set()
        for form in self.forms:
            self.backends_included = self.backends_included.union(form.backends_included)
        self.dm = self.backends_included  # aliased for backwards compatibility

    def save(self, *args, **kwargs):
        for form in self.forms:
            form.save()
