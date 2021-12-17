"""torsion_analyzer urls"""
from django.urls import path

from . import views

urlpatterns = [
    path(
        'torsion_analysis',
        views.torsion_analysis_perform,
        name='torsion_analysis_perform'
    ),
    path(
        'torsion_analysis/<int:torsion_analysis_id>',
        views.torsion_analysis_detail,
        name='torsion_analysis_detail'
    ),
    path(
        'torsion_analysis/<int:torsion_analysis_id>/download',
        views.torsion_analysis_download,
        name='torsion_analysis_download'
    )
]
