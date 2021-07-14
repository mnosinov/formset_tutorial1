from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('collection/<int:pk>', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('collection_create', views.CollectionCreateView.as_view(), name='collection_create'),
    path('collection/update/<int:pk>', views.CollectionUpdateView.as_view(), name='collection_update'),
    path('collection/delete/<int:pk>', views.CollectionDeleteView.as_view(), name='collection_delete'),
]
