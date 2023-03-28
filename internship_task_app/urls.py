from django.urls import path,include
from internship_task_app import views
from rest_framework import routers
from django.conf import settings
router = routers.DefaultRouter()
from internship_task_app import google_sheets
from django.conf.urls.static import static

urlpatterns = [
    # Form urls
    path('new_form', views.FormsMethods.NewForm, name='new_form'),
    path('get_form', views.FormsMethods.GetForm, name='get_form'),
    path('update_form', views.FormsMethods.UpdateForm, name='update_form'),
    path('delete_form', views.FormsMethods.DeleteForm, name='delete_form'),

    # User urls
    path('new_user', views.UserMethods.NewUser, name='new_form'),
    path('get_user', views.UserMethods.GetUser, name='get_user'),
    path('update_user', views.UserMethods.UpdateUser, name='update_user'),
    path('delete_user', views.UserMethods.DeleteUser, name='delete_user'),

    # Response urls
    path('new_response', views.ResponsesMethods.NewResponse, name='new_form'),
    path('get_response', views.ResponsesMethods.GetResponse, name='get_response'),
    path('update_response', views.ResponsesMethods.UpdateResponse, name='update_response'),

    # Google sheet urls
    path('get_sheet', google_sheets.FormToGoogleSheet.getSheet, name='get_sheet'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
