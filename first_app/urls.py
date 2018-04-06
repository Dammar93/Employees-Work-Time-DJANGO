from django.conf.urls import url
from first_app import views

#TEMPLATE TAGGING
app_name = 'first_app'


urlpatterns = [
    url(r'^zestaw2/$',views.z2, name='zestaw2'),
    url(r'^zestaw3/$',views.z3, name='zestaw3'),
]
