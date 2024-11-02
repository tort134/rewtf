from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = ([
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('create-request/', create_request, name='create_request'),
    path('delete_request/<int:request_id>/', delete_request, name='delete_request'),
    path('update-district/', update_district, name='update_district'),
    path('change-password/', change_password, name='change_password'),
    path('update_request_status/<int:request_id>/', update_request_status, name='update_request_status'),
    path('manage-categories/', manage_categories, name='manage_categories'),
    path('add-category/', add_category, name='add_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
