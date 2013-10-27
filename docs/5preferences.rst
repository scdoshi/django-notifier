***********
Preferences
***********

Preferences about notifications can be set per user and per group. 


Group Preferences
=================

Per group preferences can be set so that if a user belongs to any group that has the the preference set to True, then a notification is sent, unless it is overridden by user preference.

Group preferences are stored in the ``GroupPrefs`` model.

::
    
    notifier.models.GroupPrefs


User Preferences
================

Per user preferences override per group preferences. The user preference for a notification can only be set if the user has all the permissions required for that notification.

User preferences are stored in the ``UserPrefs`` model.

::
    
    notifier.models.UserPrefs


Form
----

django-notifier has a formset that includes a form for every notification along with checkboxes for every backend for that notification. This can be used in a view to allow the users to set notification preferences.

::

    notifier.forms.NotifierFormSet


There is a shortcut method to clear all user preferences (set preferences back to default)

::
    
    from notifier.shortcuts import clear_preferences
    clear_preferences([user1, user2])


.. autofunction:: notifier.shortcuts.clear_preferences


An example of customizing the formset in django templates:

::

    {% load attribute %}

    {% if formset.forms %}
    <form id="notification_form" name="input" method="post" autocomplete="off" class="form">
        {% csrf_token %}
        {{ formset.management_form }}
        <div class="form_item table"><table>
            <tr>
                <th>Notification</th>
                {% for method in formset.dm %}
                    <th>{{ method.display_name }}</th>
                {% endfor %}
            </tr>
            {% for form in formset %}
                <tr>
                    <td>
                        <div class="form_label">{{ form.title }}</div>
                    </td>
                    {% for method in formset.dm %}
                        <td>
                            {% with field=form|attr:method.name %}
                                {% if field %} {{ field }} {% endif %}
                            {% endwith %}
                        </td>  
                    {% endfor %}
                </tr>
            {% endfor %}
        </table></div>

        <div class="form_item">
            <div class="two-button">
                <input type="submit" value="Save">
            </div>
        </div>
    </form>
    {% else %}
    <p>There are no notifications that can be configured.</p>
    {% endif %}

