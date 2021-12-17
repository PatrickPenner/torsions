"""Tester for the TorsionAnalyzer wrapper"""
import os
from django.test import TestCase
from torsions.settings import BASE_DIR
from ..torsion_analyzer_wrapper import TorsionAnalyzerWrapper
from ..settings import BINARY, TORLIB


class TorsionAnalyzerWrapperTester(TestCase):
    """Tester for the TorsionAnalyzer wrapper"""

    def test_analyze(self):
        """Test analyze for a single mol"""
        mol_string = 'DX9\n  -ISIS-            3D\n\n 61 64  0  0  0  0  0  0  0  0  0\n   29.1290   11.4250   15.9630 C   0  0  0  0  0\n   28.8110   10.6450   17.0780 C   0  0  0  0  0\n   28.3350   11.2370   18.2700 C   0  0  0  0  0\n   28.1740   12.6380   18.3360 C   0  0  0  0  0\n   28.4890   13.4200   17.2120 C   0  0  0  0  0\n   28.3420   14.8070   17.2320 C   0  0  0  0  0\n   28.6700   15.5540   16.0850 C   0  0  0  0  0\n   29.1590   14.9250   14.9110 C   0  0  0  0  0\n   29.2930   13.5430   14.8900 C   0  0  0  0  0\n   28.9740   12.8030   16.0210 C   0  0  0  0  0\n   29.5010   15.7310   13.6910 C   0  0  0  0  0\n   28.9960   17.0900   13.6140 N   0  0  0  0  0\n   30.1770   15.1780   12.7650 N   0  0  0  0  0\n   29.0130    9.1480   16.9340 C   0  0  0  0  0\n   28.0140    6.8790   17.4520 C   0  0  0  0  0\n   27.6190    6.2270   18.4150 O   0  0  0  0  0\n   28.6210    6.2620   16.5880 O   0  0  0  0  0\n   27.7540    8.3360   17.3380 C   0  0  0  0  0\n   21.9360    7.1010   11.9800 N   0  0  0  0  0\n   21.9280    6.9890   13.4310 C   0  0  0  0  0\n   21.9820    8.4810   13.8330 C   0  0  0  0  0\n   21.0260    9.0990   12.7970 C   0  0  0  0  0\n   21.5120    8.4190   11.4890 C   0  0  0  0  0\n   22.2830    6.0930   11.2050 C   0  0  0  0  0\n   22.2530    6.1890    9.9300 N   0  0  0  0  0\n   22.7350    4.7550   11.8050 C   0  0  0  0  0\n   25.0330    8.2720   17.0890 C   0  0  0  0  0\n   24.0060    8.4440   16.2600 C   0  0  0  0  0\n   26.6970    8.8470   15.0930 C   0  0  0  0  0\n   25.5950    9.0090   14.2620 C   0  0  0  0  0\n   24.2920    8.8250   14.7840 C   0  0  0  0  0\n   23.3160    9.0370   13.8050 O   0  0  0  0  0\n   26.4880    8.4970   16.4490 C   0  0  0  0  0\n   29.4940   10.9580   15.0600 H   0  0  0  0  0\n   28.0960   10.6220   19.1250 H   0  0  0  0  0\n   27.8130   13.1040   19.2410 H   0  0  0  0  0\n   27.9800   15.3030   18.1200 H   0  0  0  0  0\n   28.5470   16.6270   16.0990 H   0  0  0  0  0\n   29.6440   13.0460   13.9980 H   0  0  0  0  0\n   21.0280    6.4830   13.8100 H   0  0  0  0  0\n   29.3190   17.4670   12.7460 H   0  0  0  0  0\n   30.3730   14.2460   13.0700 H   0  0  0  0  0\n   30.4570   15.5940   11.9000 H   0  0  0  0  0\n   29.2470    8.9280   15.8820 H   0  0  0  0  0\n   29.8320    8.8540   17.6070 H   0  0  0  0  0\n   28.6780    5.3460   16.8330 H   0  0  0  0  0\n   27.5310    8.7940   18.3130 H   0  0  0  0  0\n   22.7450    6.3780   13.8430 H   0  0  0  0  0\n   19.9720    8.8750   13.0170 H   0  0  0  0  0\n   22.3380    8.9710   11.0160 H   0  0  0  0  0\n   20.7460    8.3740   10.7010 H   0  0  0  0  0\n   22.5440    5.3420    9.4850 H   0  0  0  0  0\n   21.0520   10.1980   12.7650 H   0  0  0  0  0\n   22.8430    4.0110   11.0020 H   0  0  0  0  0\n   23.7010    4.8890   12.3130 H   0  0  0  0  0\n   21.9840    4.4060   12.5300 H   0  0  0  0  0\n   24.8960    7.9990   18.1250 H   0  0  0  0  0\n   22.9910    8.3200   16.6090 H   0  0  0  0  0\n   27.6970    8.9860   14.7100 H   0  0  0  0  0\n   25.7320    9.2740   13.2240 H   0  0  0  0  0\n   21.6900    8.6770   14.8750 H   0  0  0  0  0\n  1  2  2  0  0  0\n  1 10  1  0  0  0\n  1 34  1  0  0  0\n  2  3  1  0  0  0\n  2 14  1  0  0  0\n  3  4  2  0  0  0\n  3 35  1  0  0  0\n  4  5  1  0  0  0\n  4 36  1  0  0  0\n  5  6  2  0  0  0\n  5 10  1  0  0  0\n  6  7  1  0  0  0\n  6 37  1  0  0  0\n  7  8  2  0  0  0\n  7 38  1  0  0  0\n  8  9  1  0  0  0\n  8 11  1  0  0  0\n  9 10  2  0  0  0\n  9 39  1  0  0  0\n 11 12  2  0  0  0\n 11 13  1  0  0  0\n 12 41  1  0  0  0\n 13 42  1  0  0  0\n 13 43  1  0  0  0\n 14 18  1  0  0  0\n 14 44  1  0  0  0\n 14 45  1  0  0  0\n 15 16  2  0  0  0\n 15 17  1  0  0  0\n 15 18  1  0  0  0\n 17 46  1  0  0  0\n 18 33  1  0  0  0\n 18 47  1  0  0  0\n 19 20  1  0  0  0\n 19 23  1  0  0  0\n 19 24  1  0  0  0\n 20 40  1  0  0  0\n 20 21  1  0  0  0\n 20 48  1  0  0  0\n 21 22  1  0  0  0\n 21 32  1  0  0  0\n 21 61  1  0  0  0\n 22 23  1  0  0  0\n 22 49  1  0  0  0\n 22 53  1  0  0  0\n 23 50  1  0  0  0\n 23 51  1  0  0  0\n 24 25  2  0  0  0\n 24 26  1  0  0  0\n 25 52  1  0  0  0\n 26 54  1  0  0  0\n 26 55  1  0  0  0\n 26 56  1  0  0  0\n 27 28  2  0  0  0\n 27 33  1  0  0  0\n 27 57  1  0  0  0\n 28 31  1  0  0  0\n 28 58  1  0  0  0\n 29 30  1  0  0  0\n 29 33  2  0  0  0\n 29 59  1  0  0  0\n 30 31  2  0  0  0\n 30 60  1  0  0  0\n 31 32  1  0  0  0\nM  END\n$$$$\n'
        file_type = '.sdf'
        analyzer = TorsionAnalyzerWrapper(BINARY, mol_string, file_type, TORLIB)
        self.assertIsNotNone(analyzer.raw_result)
        self.assertEqual(1, len(analyzer.result))
        self.assertEqual(8, len(analyzer.result[0]))

    def test_analyze_multiple_mols(self):
        """Test analyze for multiple mols"""
        with open(os.path.join(BASE_DIR, 'torsion_analyzer', 'test', '5j1r_hits.sdf')) as mol_file:
            mol_string = mol_file.read()
        file_type = '.sdf'
        analyzer = TorsionAnalyzerWrapper(BINARY, mol_string, file_type, TORLIB)
        self.assertEqual(20, len(analyzer.result))
        self.assertEqual(3, len(analyzer.result[0]))

    def test_failing_mol(self):
        """Test handling of failing molecules"""
        with open(os.path.join(BASE_DIR, 'torsion_analyzer', 'test', 'filtered.sdf')) as mol_file:
            mol_string = mol_file.read()
        file_type = '.sdf'
        analyzer = TorsionAnalyzerWrapper(BINARY, mol_string, file_type, TORLIB)
        # 4 molecules 1 fails
        self.assertEqual(3, len(analyzer.result))
        for entry in analyzer.result:
            # error in processing prevented reading more than one result
            self.assertTrue(len(analyzer.result[entry]) > 1)
