from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('embedding/all', views.all_camping_to_embedding_json),
    path('patch/camping/embedding', views.patch_campings_embedding),
    path('recommend', views.recommend),
    path('idx', views.save_idxAndcontentId),
]