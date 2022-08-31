from django.urls import path

from morphers.views import MorpherDetailView, exportExcel, generateDocs, morpherListView


app_name = 'morphers'

urlpatterns = [
    path('', morpherListView, name='list'),
    path('<int:pk>/', MorpherDetailView.as_view(), name='detail'),
    path('export/', generateDocs, name='export'),
    path('export/excel/', exportExcel, name='export-excel'),
]