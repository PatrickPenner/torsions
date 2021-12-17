"""Tester for database models"""
import os
from django.test import TestCase
from torsions.settings import BASE_DIR
from ..models import TorsionAnalysis, TorsionPattern, Status
from ..settings import MAPPING


class ModelTester(TestCase):
    """Tester for database models"""

    def test_torsion_analysis_from_mol_string(self):
        """Test generating a torsion analysis from a string"""
        TorsionPattern.read_static_torsion_patterns(MAPPING)
        with open(os.path.join(BASE_DIR, 'torsion_analyzer', 'test', '5j1r_hits.sdf')) as mol_file:
            mol_string = mol_file.read()
        file_type = '.sdf'
        torsion_analysis = TorsionAnalysis(mol_string=mol_string, file_type=file_type)
        torsion_analysis.save()

        # simulate doing this asynchronously
        torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis.id)
        self.assertEqual(Status.PENDING, torsion_analysis.status)
        torsion_analysis.analyze()

        torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis.id)
        self.assertEqual(Status.SUCCESS, torsion_analysis.status)
        self.assertIsNotNone(torsion_analysis)
        self.assertIsNotNone(torsion_analysis.result_string)
        self.assertIsNotNone(torsion_analysis.accessed)
        self.assertIsNotNone(torsion_analysis.molecule_set)
        self.assertEqual(20, torsion_analysis.molecule_set.count())
        for molecule in torsion_analysis.molecule_set.all():
            if molecule.torsionresult_set:
                for torsion_result in molecule.torsionresult_set.all():
                    self.assertIsNotNone(torsion_result)
