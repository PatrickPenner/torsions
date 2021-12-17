"""torsion_analyzer models"""
import csv
import logging
import os
from django.db import models, transaction
from .torsion_analyzer_wrapper import TorsionAnalyzerWrapper
from .settings import BINARY, TORLIB, STATIC_TORLIB_URL


class Status:
    """Class wrapping a status enum"""
    PENDING = 'p'
    RUNNING = 'r'
    SUCCESS = 's'
    FAILURE = 'f'

    choices = [
        (PENDING, 'pending'),
        (RUNNING, 'running'),
        (SUCCESS, 'success'),
        (FAILURE, 'failure'),
    ]

    @staticmethod
    def to_string(status):
        """Convert status to a readable string"""
        if status == 'p':
            return 'pending'
        if status == 'r':
            return 'running'
        if status == 's':
            return 'success'
        if status == 'f':
            return 'failure'
        return None


class TorsionPattern(models.Model):
    """Torsion pattern model with SMARTS and path to its plot"""
    smarts = models.TextField()
    csd_plot_path = models.TextField()
    pdb_plot_path = models.TextField()

    def dict(self):
        """To dict"""
        return {'id': self.id, 'smarts': self.smarts, 'csdPlotPath': self.csd_plot_path, 'pdbPlotPath': self.pdb_plot_path}

    @staticmethod
    def read_static_torsion_patterns(mapping_path):
        """Read torsion patterns from a mapping file in a torlib directory"""
        with open(mapping_path) as mapping_file:
            reader = csv.reader(mapping_file, delimiter='\t')
            for line in reader:
                torsion_pattern_id = int(line[0])
                smarts = line[1]
                csd_plot_path = os.path.join(
                    STATIC_TORLIB_URL,
                    'csd',
                    str(torsion_pattern_id) + '.svg'
                )
                pdb_plot_path = os.path.join(
                    STATIC_TORLIB_URL,
                    'pdb',
                    str(torsion_pattern_id) + '.svg'
                )
                torsion_pattern = TorsionPattern(
                    id=torsion_pattern_id,
                    smarts=smarts,
                    csd_plot_path=csd_plot_path,
                    pdb_plot_path=pdb_plot_path
                )
                torsion_pattern.save()


class TorsionAnalysis(models.Model):
    """Torsion analysis model that initially holds the input and then the analysed molecules"""
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    mol_string = models.TextField()
    result_string = models.TextField()
    file_type = models.CharField(max_length=5)
    accessed = models.DateField(auto_now=True)

    def dict(self, detail=False):
        """To dict"""
        torsion_analysis_dict = {'id': self.id, 'status': Status.to_string(self.status)}
        if detail:
            torsion_analysis_dict['molecules'] = [m.dict(detail) for m in self.molecule_set.all()]
        else:
            torsion_analysis_dict['molecules'] = [m.id for m in self.molecule_set.all()]
        return torsion_analysis_dict

    def analyze(self):
        """Perform the actual analysis"""
        self.status = Status.RUNNING
        self.save()
        try:
            with transaction.atomic():
                mols = Molecule.from_torsion_analysis(self)
                analyzer = TorsionAnalyzerWrapper(BINARY, self.mol_string, self.file_type, TORLIB)
                self.result_string = analyzer.raw_result
                TorsionResult.from_analyzer_results(mols, analyzer.result)
                self.status = Status.SUCCESS
                self.save()
        except Exception as error:
            logging.error(error)
            self.status = Status.FAILURE
            self.save()


class Molecule(models.Model):
    """Molecule model in a torsion analysis"""
    entry_id = models.IntegerField()
    name = models.CharField(max_length=80)
    mol_string = models.TextField()
    file_type = models.CharField(max_length=5)
    torsion_analysis = models.ForeignKey(TorsionAnalysis, on_delete=models.CASCADE)

    def dict(self, detail=False):
        """To dict"""
        molecule_dict = {
            'id': self.id,
            'entryId': self.entry_id,
            'name': self.name,
            'molString': self.mol_string,
            'fileType': self.file_type
        }
        if detail:
            molecule_dict['torsionResults'] = [r.dict(detail) for r in self.torsionresult_set.all()]
        else:
            molecule_dict['torsionResults'] = [r.id for r in self.torsionresult_set.all()]
        return molecule_dict

    @staticmethod
    def from_torsion_analysis(torsion_analysis):
        """Generate molecule models from torsion analysis input"""
        mols = []
        split_mol_strings = [s for s in torsion_analysis.mol_string.split('$$$$\n') if s.strip()]
        entry = 1
        for split_mol_string in split_mol_strings:
            # better to correctly terminate even if it may not be necessary
            split_mol_string += '$$$$\n'
            name = split_mol_string.split('\n')[0]
            mol = Molecule(
                entry_id=entry,
                name=name,
                mol_string=split_mol_string,
                file_type=torsion_analysis.file_type,
                torsion_analysis=torsion_analysis
            )
            mol.save()
            mols.append(mol)
            entry += 1
        return mols


class TorsionResult(models.Model):
    """Torsion result model associated with a molecule and a torsion pattern"""
    atom_id_1 = models.IntegerField()
    atom_id_2 = models.IntegerField()
    atom_id_3 = models.IntegerField()
    atom_id_4 = models.IntegerField()
    angle = models.FloatField()
    quality = models.CharField(max_length=10)
    pattern_hierarchy = models.TextField()
    molecule = models.ForeignKey(Molecule, on_delete=models.CASCADE)
    torsion_pattern = models.ForeignKey(TorsionPattern, on_delete=models.CASCADE)

    def dict(self, detail=False):
        """To dict"""
        torsion_result_dict = {
            'id': self.id,
            'atomId1': self.atom_id_1,
            'atomId2': self.atom_id_2,
            'atomId3': self.atom_id_3,
            'atomId4': self.atom_id_4,
            'angle': round(self.angle, 2),
            'quality': self.quality,
            'patternHierarchy': self.pattern_hierarchy
        }
        if detail and self.torsion_pattern_id:
            torsion_result_dict['torsionPattern'] = self.torsion_pattern.dict()
        elif self.torsion_pattern_id:
            torsion_result_dict['torsionPattern'] = self.torsion_pattern.id
        return torsion_result_dict

    @staticmethod
    def from_analyzer_results(mols, results):
        """Generate torsion result models from analyzer results"""
        torsion_pattern_cache = {}
        torsion_results = []
        for entry in results.keys():
            for result in results[entry]:
                torsion_pattern_smarts = result['patternHierarchy'][0]
                torsion_pattern_model = None
                if torsion_pattern_smarts in torsion_pattern_cache:
                    torsion_pattern_model = torsion_pattern_cache[torsion_pattern_smarts]
                else:
                    torsion_pattern_models = \
                        TorsionPattern.objects.filter(smarts=torsion_pattern_smarts)
                    if torsion_pattern_models.count() != 0:
                        torsion_pattern_model = torsion_pattern_models[0]
                        # cache pattern because database queries are expensive
                        torsion_pattern_cache[torsion_pattern_smarts] = torsion_pattern_model
                    else:
                        logging.warning(
                            'Could not find torsion pattern: %s', torsion_pattern_smarts)
                torsion_result = TorsionResult(
                    atom_id_1=result['atomId1'],
                    atom_id_2=result['atomId2'],
                    atom_id_3=result['atomId3'],
                    atom_id_4=result['atomId4'],
                    angle=result['angle'],
                    quality=result['quality'],
                    pattern_hierarchy='|'.join(result['patternHierarchy']),
                    torsion_pattern=torsion_pattern_model,
                    molecule=mols[entry]
                )
                torsion_result.save()
                torsion_results.append(torsion_result)
        return torsion_results
