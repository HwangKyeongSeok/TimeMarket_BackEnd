from django.urls import path
from . import views

urlpatterns = [
    path('', views.NearbyTimePostList.as_view(), name="timepost-nearby-list"),     # GET (근처 시간 판매/구인)
    path('create/', views.TimePostCreate.as_view(), name="timepost-create"),       # POST (글 등록)
    path('<int:pk>/', views.TimePostDetail.as_view(), name="timepost-detail"),     # GET, PATCH, DELETE
    path('board/', views.BoardTimePostList.as_view(), name="timepost-board"),      # GET (게시판형)
]
