# acme_project/urls.py
# Импортируем настройки проекта.
from django.conf import settings
# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

    
class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]

    
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
    path("auth/logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        'auth/registration/', 
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
    # Подключаем urls.py приложения для работы с пользователями.
    path('auth/', include('django.contrib.auth.urls')),
    # В конце добавляем к списку вызов функции static.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
