import unittest

from neperansys.konwerter import Konwerter
from neperansys.konwerter import WyjatekParsowania

class Test_Konwerter(unittest.TestCase):

    def setUp(self):
        self.konwerter = Konwerter()

    def test_dziala(self):
        self.assertEqual('Dziala', 'Dziala')
    
    def test_parsuj_punkt(self):
        self.assertEqual(self.konwerter.parsuj_punkt('4 1 2 3.2 0'), (4, 1.0, 2.0, 3.2))
        self.assertEqual(self.konwerter.parsuj_punkt("   1  -0.000000000000 -0.000000000000 0.480836332398     0"), (1, -0.0, -0.0, 0.480836332398))

    def test_parsuj_linie(self):
        self.assertEqual(self.konwerter.parsuj_linie('2 1 3 1'), (2, 1, 3))

    def test_parsuj_pwrzchnie_zlinii(self):
        self.assertEqual(self.konwerter.parsuj_pwrzchnie_zlinii('1 3 1 2 3', ' 3 1 3 4', 'mumble', 'mumble'),
                         (1, 1, 3, 4));
        self.assertRaises(WyjatekParsowania, self.konwerter.parsuj_pwrzchnie_zlinii,'1 3 1 2 3','3 1 2', 'mubmle', 'mumble')         

    def test_parsuj_objetosc(self):
        self.assertEqual(self.konwerter.parsuj_objetosc('1 5 13 2 3 5 7'), (1, 13, 2, 3, 5, 7))
        self.assertEqual(self.konwerter.parsuj_objetosc('1 5 -13 2 3 5 -7'), (1, 13, 2, 3, 5, 7))
        self.assertRaises(WyjatekParsowania, self.konwerter.parsuj_objetosc, '1 2 1')         

    def test_tworz_ans_punkt(self):
        self.assertEqual(self.konwerter.tworz_ans_punkt((5, 1, 1.3, 3)), 'K, 5, 1, 1.3, 3')

    def test_tworz_ans_linia(self):
        self.assertEqual(self.konwerter.tworz_ans_linia((2, 1, 3)), 'L, 1, 3')

    def test_tworz_ans_pwrzchnia_zlinii(self):
        self.assertEqual(self.konwerter.tworz_ans_pwrzchnia_zlinii((1, 1, 3, 4)), 'ALLSEL,all\nLSEL,s,,,1\nLSEL,a,,,3\nLSEL,a,,,4\nAL,all')
        self.assertEqual(self.konwerter.tworz_ans_pwrzchnia_zlinii((1, 1, 3, 4, 6)), 'ALLSEL,all\nLSEL,s,,,1\nLSEL,a,,,3\nLSEL,a,,,4\nLSEL,a,,,6\nAL,all')

    def test_tworz_ans_objetosc(self):
        self.assertEqual(self.konwerter.tworz_ans_objetosc((1, 13, 2, 3, 5, 7)), 'ALLSEL,all\nASEL,s,,,13\nASEL,a,,,2\nASEL,a,,,3\nASEL,a,,,5\nASEL,a,,,7\nVA,all')
        self.assertEqual(self.konwerter.tworz_ans_objetosc((1, 13, 2, 3, 5, 7, 127)), 'ALLSEL,all\nASEL,s,,,13\nASEL,a,,,2\nASEL,a,,,3\nASEL,a,,,5\nASEL,a,,,7\nASEL,a,,,127\nVA,all')
    
    def test_tlumacz_punkt(self):
        self.assertEqual(self.konwerter.tlumacz_punkt('4 2 3 4.5 0'),'K, 4, 2.0, 3.0, 4.5')     

    def test_tlumacz_linie(self):
        self.assertEqual(self.konwerter.tlumacz_linie('2 1 3 1'), 'L, 1, 3')

    def test_tlumacz_pwrzchnia_zlinii(self):
        self.assertEqual(self.konwerter.tlumacz_pwrzchnia_zlinii('1 3 1 2 3', '3 1 3 4', 'mumble', 'mumble'),'ALLSEL,all\nLSEL,s,,,1\nLSEL,a,,,3\nLSEL,a,,,4\nAL,all')

    def test_tlumacz_ans_objetosc(self):
        self.assertEqual(self.konwerter.tlumacz_ans_objetosc('1 6 1 2 3 4 5 6'), 'ALLSEL,all\nASEL,s,,,1\nASEL,a,,,2\nASEL,a,,,3\nASEL,a,,,4\nASEL,a,,,5\nASEL,a,,,6\nVA,all')
    
    def test_konwertuj_komendy(self):
        """Otworz plik z testami 
        w petli: wczytuj pary wejscie - prawidłowe wyjscie
        stworz plik temp.in i tam zapisz co jest w wejsciu
        uruchom konwerter z tym plikiem
        sprawdz, czy to co zapisał konwerter do drugiego pliku
         i prawidłowe wyjście pokrywają się 
        skasuj oba pliki       
        """
        import os
        import os.path
        import filecmp
        nazwaKomend =  "./test/komendy.in"
        nazwaWejscia = "./test/disposable.plik.in"
        nazwaWyjscia = "./test/disposable.plik.out"
        nazwaWzorca =  "./test/disposable.wzorzec.out"
        with open(nazwaKomend, 'r') as plikKomend:
            linia = plikKomend.readline()
            while linia.strip() != "##" and linia != '':
                with open(nazwaWejscia, 'a') as plikWejsciowy:
                    plikWejsciowy.write(linia)
                    linia = plikKomend.readline()
            linia = plikKomend.readline()
            while linia.strip() != "###" and linia != '':
                with open(nazwaWzorca, 'a') as plikWzorca:
                    plikWzorca.write(linia)
                    linia = plikKomend.readline()
        self.konwerter.konwertuj_komendy(nazwaWejscia, nazwaWyjscia)
        self.assertTrue(filecmp.cmp(nazwaWyjscia, nazwaWzorca))
        os.remove(nazwaWejscia)
        os.remove(nazwaWyjscia)
        os.remove(nazwaWzorca)

if __name__ == '__main__':
    unittest.main()
   
