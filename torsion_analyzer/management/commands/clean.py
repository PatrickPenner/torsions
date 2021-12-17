"""clean command to delete older torsion analyses"""
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from torsion_analyzer.models import TorsionAnalysis
from torsion_analyzer.settings import KEEP_ANALYSIS


class Command(BaseCommand):
    """clean command to delete older torsion analyses"""
    help = 'deletes all torsion analyses older than {} days'.format(KEEP_ANALYSIS)

    def handle(self, *_args, **_options):
        deletion_date = datetime.today() - timedelta(days=KEEP_ANALYSIS)
        analyses_to_delete = TorsionAnalysis.objects.filter(accessed__lte=deletion_date)
        for analysis in analyses_to_delete:
            analysis.delete()
