from django import forms
from CSS.models import *
from django.forms import EmailField, ModelChoiceField, ModelMultipleChoiceField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)  # create, but don't save
        user.set_password(self.cleaned_data['password1'])  # use set_password instead of (.password) to hash.
        user.is_active = False  # is_active: to control whether or not the user can log in.
        if commit:
            user.save()
        return user


class UserTypeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('type',)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('type', 'user')
        widgets = {'image': forms.FileInput()}


class MenuForm(forms.ModelForm):
    locations = ModelMultipleChoiceField(queryset=Location.objects.all())

    def __init__(self, *args, **kwargs):
        """
         Help pass user_id into clean function
        """
        initial_data = kwargs.pop('initial', None)
        print("initial data: ", initial_data)
        if initial_data:
            self.user_id = initial_data.pop('user_id', None)
            self.from_edit = initial_data.pop('from_edit', False)
            self.previous_is_lunch = initial_data.pop('previous_is_lunch', None)
        super(MenuForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Menu
        fields = ("image", "food_name", "is_lunch", "price")
        widgets = {'image': forms.FileInput()}

    def clean_is_lunch(self):
        """
        If lunch or dinner's menu for today has already been created, extra create is not allowed
        """
        data = self.cleaned_data['is_lunch']
        today_menus_status = [menu.is_lunch for menu in Menu.get_today_menu().filter(merchant_id=self.user_id)]
        # form for create menu
        if not self.from_edit:
            if data in today_menus_status:
                raise forms.ValidationError(
                    _("You have already created a menu for today's %s." % ('lunch' if data else 'dinner')))
        # form for edit menu
        else:
            if len(today_menus_status) == 2 and data != self.previous_is_lunch:
                    raise forms.ValidationError(
                        _("You have already created a menu for today's %s." % ('lunch' if data else 'dinner')))
        return data




class OrderQuantityForm(forms.ModelForm):
    location = ModelChoiceField(queryset=Location.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        """
        Guarantee students can only choose available location to pick their food.
        """
        menu_id = None
        initial_data = kwargs.pop('initial', None)
        if initial_data:
            menu_id = initial_data.pop('menu_id', None)
        super(OrderQuantityForm, self).__init__(*args, **kwargs)
        if menu_id:
            self.fields['location'].queryset = Menu.objects.filter(id=menu_id)[0].location_set.all()

    class Meta:
        model = Order
        fields = ('quantity',)

    def save(self, commit=True):
        new_order = super(OrderQuantityForm, self).save(commit=False)  # create, but don't save
        new_order.location = self.cleaned_data['location']
        if commit:
            new_order.save()
        return new_order


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('rating',)


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ('menu', 'is_seller', 'quantity',)


class AddLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('menus',)
