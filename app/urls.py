from django.urls import path
from . import views

urlpatterns = [
    path('query_fw/', views.query_fw),
    path('query_td/', views.query_td),
    path('query_sjwz/', views.query_sjwz),
    path('query_sjwz_e/', views.query_sjwz_e),
    path('query_cdwz/', views.query_cdwz),
    path('query_cdwz_e/', views.query_cdwz_e),
    path('insert_sj/', views.insert_sj),
    path('insert_wz/', views.insert_wz),
    path('insert_wz/xianlu/', views.insert_wz_xianlu),
    path('insert_sj/xianlu/', views.insert_sj_xianlu),
    path('insert_wz/zhandian/', views.insert_wz_zhandian),
    path('insert_qc/', views.insert_qc),
]