"""Settings (constants) for the torsion analyzer"""
import os
from torsions.settings import BASE_DIR

BINARY = os.path.join(BASE_DIR, 'bin', 'TorsionAnalyzer')
TORLIB = '/local/torsions/static/torsion_lib/tor_lib.xml'
MAPPING = '/local/torsions/static/torsion_lib/mapping.tsv'
STATIC_TORLIB_URL = '/static/torsion_lib/'
KEEP_ANALYSIS = 7  # days
