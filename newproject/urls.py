from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from newapp import views  # your app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('room/', views.room_view, name='room_view'),
   # path('api/messages/<str:room_name>/', views.messages_api, name='messages_api'),
    path("chartwithuser/<int:id>/",views.chartwithuser,name="chartwithuser"),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
