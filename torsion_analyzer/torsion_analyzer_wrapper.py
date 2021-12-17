"""Wrapper around the TorsionAnalyzer binary"""
import csv
import logging
import subprocess
import traceback
from tempfile import NamedTemporaryFile


class TorsionAnalyzerWrapper:
    """Wrapper around the TorsionAnalyzer binary"""
    def __init__(self, torsion_analyzer_binary, mol_string, file_type, torlib):
        self.binary = torsion_analyzer_binary
        self.torlib = torlib
        self.mol_string = mol_string
        self.file_type = file_type
        self.raw_result = None
        self.result = {}
        self.analyze()

    def analyze(self):
        """Perform a torsion analysis"""
        temp_mol_file = NamedTemporaryFile('w', suffix=self.file_type)
        temp_mol_file.write(self.mol_string)
        temp_mol_file.flush()
        out_tsv_file = NamedTemporaryFile('r', suffix='.tsv')
        args = [
            self.binary,
            '--input', temp_mol_file.name,
            '--out', out_tsv_file.name,
            '--torlib', self.torlib
        ]
        logging.debug('running: %s', ' '.join(args))
        try:
            out = subprocess.check_output(args)
            logging.debug(out.decode('utf8'))
            self.raw_result = out_tsv_file.read()
            out_tsv_file.seek(0)
            reader = csv.reader(out_tsv_file, delimiter='\t')
            # skip header
            next(reader)
            for line in reader:
                entry, data = self.__parse_tsv_line(line)
                if entry not in self.result:
                    self.result[entry] = []
                self.result[entry].append(data)
        except subprocess.CalledProcessError:
            traceback.print_exc()

    @staticmethod
    def __parse_tsv_line(line):
        entry = int(line[0])
        atom_id_1 = int(line[2])
        atom_id_2 = int(line[3])
        atom_id_3 = int(line[4])
        atom_id_4 = int(line[5])
        angle = float(line[6])
        quality = line[7]
        pattern_hierarchy = [p for p in line[8].split('|') if p.strip()]
        data = {
            'atomId1': atom_id_1,
            'atomId2': atom_id_2,
            'atomId3': atom_id_3,
            'atomId4': atom_id_4,
            'angle': angle,
            'quality': quality,
            'patternHierarchy': pattern_hierarchy
        }
        return entry, data
