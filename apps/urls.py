from django.urls import include, path
from django.contrib import admin

from theme import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books_crud/', include('books_crud.urls', namespace='books_crud')),
    path('', views.home),
]
