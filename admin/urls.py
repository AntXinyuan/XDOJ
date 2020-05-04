from django.urls import path, include

urlpatterns = [
    path('account/', include('account.urls.admin')),
    path('announcement/', include('announcement.urls.admin')),
    path('problem/', include('problem.urls.admin')),
    path('submission/', include('submission.urls.admin'))
]