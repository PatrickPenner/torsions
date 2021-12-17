"""Seed command to read static torsion patterns"""
from django.core.management.base import BaseCommand
from torsion_analyzer.models import TorsionPattern
from torsion_analyzer.settings import MAPPING


class Command(BaseCommand):
    """Seed command to read static torsion patterns"""
    help = 'Seeds database with static torsion patterns'

    def handle(self, *_args, **_options):
        TorsionPattern.read_static_torsion_patterns(MAPPING)
