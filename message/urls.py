from django.urls import path

from message import views

app_name = 'message'

urlpatterns = [
    path('list/', views.ListMessageView.as_view(), name='list'),
    path('create/', views.CreateMessageView.as_view(), name='create'),
    path('details/<pk>', views.DetailsMessageView.as_view(), name='details'),
    path('update/<pk>', views.UpdateMessageView.as_view(), name='update'),
    path('delete/<pk>', views.DeleteMessageView.as_view(), name='delete'),
]
