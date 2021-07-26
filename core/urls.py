from django.urls import path
from rooms import views as room_views

app_name = "core"  # config.urls.py의 urlpatterns에 사용되는 namespace와 동일해야 함

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
