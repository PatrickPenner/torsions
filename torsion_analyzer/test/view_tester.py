"""torsion_analyzer view tester"""
import os
from django.test import TestCase
from torsions import celery_app
from torsions.settings import BASE_DIR
from ..models import TorsionAnalysis, TorsionPattern, Status
from ..settings import MAPPING

TEST_MOLS = os.path.join(BASE_DIR, 'torsion_analyzer', 'test', '5j1r_hits.sdf')


class ViewTester(TestCase):
    """torsion_analyzer view tester"""

    def setUp(self):
        TorsionPattern.read_static_torsion_patterns(MAPPING)
        # stop the views from actually creating jobs
        celery_app.conf.update(CELERY_ALWAYS_EAGER=True)

    def test_torsion_analysis_perform(self):
        """Test starting a torsion analysis with a mol string"""
        with open(TEST_MOLS) as mol_file:
            mol_string = mol_file.read()
        file_type = '.sdf'
        data = {
            'molString': mol_string,
            'fileType': file_type
        }
        response = self.client.post('/torsion_analysis', data=data)
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertIn('id', response_json)
        self.assertIn('status', response_json)
        self.assertEqual('pending', response_json['status'])

    def test_torsion_analysis_perform_file(self):
        """Test starting a torsion analysis with a file"""
        with open(TEST_MOLS) as mol_file:
            response = self.client.post('/torsion_analysis', data={'molFile': mol_file})
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertIn('id', response_json)
        self.assertIn('status', response_json)
        self.assertEqual('pending', response_json['status'])

    def test_torsion_analysis_detail(self):
        """Test retrieving a successful torsion analysis from the database"""
        with open(TEST_MOLS) as mol_file:
            mol_string = mol_file.read()
        file_type = '.sdf'
        torsion_analysis = TorsionAnalysis(mol_string=mol_string, file_type=file_type)
        torsion_analysis.save()

        # simulate doing this asynchronously
        torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis.id)
        self.assertEqual(Status.PENDING, torsion_analysis.status)
        torsion_analysis.analyze()
        torsion_analysis.save()

        response = self.client.get('/torsion_analysis/{}'.format(torsion_analysis.id))
        response_json = response.json()
        self.assertIn('status', response_json)
        self.assertEqual('success', response_json['status'])
        self.assertIn('molecules', response_json)
        molecules_json = response_json['molecules']
        for molecule in molecules_json:
            self.assertIn('torsionResults', molecule)

    def test_torsion_analysis_download(self):
        """Test downloading a TSV file of a torsion analysis"""
        with open(TEST_MOLS) as mol_file:
            mol_string = mol_file.read()
        file_type = '.sdf'
        torsion_analysis = TorsionAnalysis(mol_string=mol_string, file_type=file_type)
        torsion_analysis.save()

        # simulate doing this asynchronously
        torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis.id)
        self.assertEqual(Status.PENDING, torsion_analysis.status)
        torsion_analysis.analyze()
        torsion_analysis.save()

        response = self.client.get('/torsion_analysis/{}/download'.format(torsion_analysis.id))
        downloaded_content = response.content.decode('utf8')
        self.assertEqual(downloaded_content, torsion_analysis.result_string)
