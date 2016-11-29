from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login, password_reset_confirm
import CSS.views

urlpatterns = [

    url(r'^login$', login, {'template_name': 'CSS/login.html'}, name='login'),
    url(r'^logout$', logout_then_login, name='logout'),

    url(r'^register$', CSS.views.register, name='register'),
    url(r'^confirm-email/(?P<username>.*)/(?P<token>.*)', CSS.views.confirm_registration, name='confirm_email'),

    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', CSS.views.reset_confirm, name='reset_confirm'),
    url(r'^reset/$', CSS.views.reset, name='reset'),

    url(r'^$', CSS.views.home, name='home'),

    url(r'^browse-profile/(?P<profile_id>\d+)$', CSS.views.browse_profile, name='browse_profile'),
    url(r'^edit-profile/(?P<profile_id>\d+)$', CSS.views.edit_profile, name='edit_profile'),

    url(r'^create-menu/$', CSS.views.create_menu, name='create_menu'),
    url(r'^browse-menu/(?P<merchant_id>\d+)$', CSS.views.browse_menu, name='browse_menu'),
    url(r'^edit-menu/(?P<menu_id>\d+)$', CSS.views.edit_menu, name='edit_menu'),
    url(r'^delete-menu/(?P<menu_id>\d+)$', CSS.views.delete_menu, name='delete_menu'),

    url(r'^create-order/$', CSS.views.create_order, name='create_order'),
    url(r'^browse-order/(?P<customer_id>\d+)$', CSS.views.browse_order, name='browse_order'),
    url(r'^edit-order/(?P<order_id>\d+)$', CSS.views.edit_order, name='edit_order'),
    url(r'^delete-order/(?P<order_id>\d+)$', CSS.views.delete_order, name='delete_order'),

    url(r'^pickup-notification/(?P<menu_id>\d+)$', CSS.views.pickup_notification, name='pickup_notification'),
    url(r'^exchange/$', CSS.views.exchange, name='exchange'),
    url(r'^order-review/$', CSS.views.order_review, name='order_review'),
    url(r'^dashboard/$', CSS.views.dashboard, name='dashboard'),

    url(r'^pickup-order/(?P<order_id>\d+)$', CSS.views.pickup_order, name='pickup_order'),

    # Recommendation System
    # url(r'^CF/$', CSS.views.CF, name='CF'),
    # url(r'^daily/$', CSS.views.daily, name='daily'),
]
