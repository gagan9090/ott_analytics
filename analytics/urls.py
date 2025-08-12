from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path("", views.user_dashboard_template, name="user_dashboard"),
    path("video/", views.video_dashboard_template, name="video_dashboard"),
    path('general/', views.general_dashboard_template, name='general_dashboard_template'),

    # API data
    path('api/user/', views.user_dashboard_data, name='user_dashboard_data'),
    path('api/video/', views.video_dashboard_data, name='video_dashboard_data'),
    path('api/general/', views.general_dashboard_api, name='general_dashboard_api'),
    # APIs with Id
    path('api/user/<int:user_id>/', views.user_analytics_api, name='user_analytics_api'),
    path('api/video/<int:video_id>/', views.video_analytics_api, name='video_analytics_api'),
    

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
settings.DEBUG = True
