"""Loads the celery app any time torsions is imported"""
from .celery import app as celery_app

__all__ = ('celery_app',)
