"""torsion_analyzer tasks"""
from celery import shared_task
from .models import TorsionAnalysis


@shared_task
def calculate_torsion_analysis(torsion_analysis_id):
    """Perform a torsion analysis as a job"""
    torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis_id)
    torsion_analysis.analyze()
