class WyjatekParsowania(Exception): pass

class Konwerter:
    def parsuj_punkt(self, tekst):
        tekst = tekst.strip()
        dane = tekst.split()
        id = int(dane[0])
        x = float(dane[1])
        y = float(dane[2])
        z = float(dane[3])
        return (id, x, y, z)

    def parsuj_linie(self, tekst):
        tekst = tekst.strip()
        dane = tekst.split()
        id = int(dane[0])
        p1 = int(dane[1])
        p2 = int(dane[2])
        return (id, p1, p2)

    def parsuj_pwrzchnie_zlinii(self, tekst1, tekst2, tekst3, tekst4):
        tekst1 = tekst1.strip()
        dane1 = tekst1.split()
        id = int(dane1[0])

        tekst2 = tekst2.strip()
        dane2 = tekst2.split()
        for i in range(0, len(dane2)):
            dane2[i] = abs(int(dane2[i]))
        ile_linii = dane2[0]
        if ile_linii+1 != len(dane2):
            raise WyjatekParsowania('Zadeklarowana i podana ilosc linii powierzchni %d nie zgadzaja sie!' % id)
        return (id,) +  tuple(dane2[1:])

    def parsuj_objetosc(self, tekst):
        tekst = tekst.strip()
        dane = tekst.split()
        for i in range(0, len(dane)):
            dane[i] = abs(int(dane[i]))
        id = dane[0]
        ile_pwrzchni = dane[1]
        if ile_pwrzchni+2 != len(dane):
            raise WyjatekParsowania('Zadeklarowana i podana ilosc powierzchni w objetosci %d nie zgadzaja sie!' % id)
        return (id,) + tuple(dane[2:])

    def tworz_ans_punkt(self, dane):
        return 'K, ' + str(dane[0]) + ', ' + str(dane[1]) + ', ' + str(dane[2]) + ', ' + str(dane[3])

    def tworz_ans_linia(self, dane):
        '''
        Funkcja zmodyfikowana bo al przyjmuje tylko 10 (albo 9) linii
        '''
        return 'L, ' + str(dane[1]) + ', ' + str(dane[2])

    def tworz_ans_pwrzchnia_zlinii(self, dane):
        komenda = 'ALLSEL,all\nLSEL,s,,,' + str(dane[1]) + '\n'
        for i in range(2, len(dane)):
            komenda = komenda + 'LSEL,a,,,' + str(dane[i]) + '\n'
        komenda = komenda + 'AL,all'
        return komenda
    
    def tworz_ans_objetosc(self, dane):
        '''
        Funkcja zmodyfikowana bo va przyjmuje tylko 10 powierzchni
        '''
        komenda = 'ALLSEL,all\nASEL,s,,,' + str(dane[1])+'\n'
        for i in range(2, len(dane)):
            komenda = komenda + 'ASEL,a,,,' + str(dane[i]) + '\n'
        komenda = komenda + 'VA,all'
        return komenda

    def tlumacz_punkt(self, tekst):
        return self.tworz_ans_punkt(self.parsuj_punkt(tekst))

    def tlumacz_linie(self, tekst):
        return self.tworz_ans_linia(self.parsuj_linie(tekst))

    def tlumacz_pwrzchnia_zlinii(self, tekst1, tekst2, tekst3, tekst4):
        return self.tworz_ans_pwrzchnia_zlinii(self.parsuj_pwrzchnie_zlinii(tekst1, tekst2, tekst3, tekst4))

    

    def tlumacz_ans_objetosc(self, tekst):
        return self.tworz_ans_objetosc(self.parsuj_objetosc(tekst))
    
    def ignoruj(self, tekst):
        return ''

    def konwertuj_komendy(self, nazwaWejscia, nazwaWyjscia):
        ileLinii = 1
        pomin = 0
        funkcja = self.ignoruj
        akumuluj = 0
        akumulator = []
        
        with open(nazwaWejscia, 'r') as plikWe, open(nazwaWyjscia, 'w') as plikWy:
            lines = plikWe.readlines()
            for line in lines:
                tekst = line.strip()
                print(tekst)
                if tekst == "**vertex":
                    print("napotkano **vertex")
                    ileLinii = 1
                    pomin = 1        ## tyle linii pomija bo jest tam liczba punktow
                    funkcja = self.tlumacz_punkt
                elif tekst == "**edge":
                    print("napotkano **edge")
                    ileLinii = 1
                    pomin = 1        ## tyle linii pomija bo jest tam liczba linii
                    funkcja = self.tlumacz_linie
                elif tekst == "**face":
                    print("napotkano **face")
                    ileLinii = 4
                    pomin = 1        ## tyle linii pomija bo jest tam liczba powierzchni
                    funkcja = self.tlumacz_pwrzchnia_zlinii
                elif tekst == "**polyhedron":
                    print("napotkano **polyhedron")
                    ileLinii = 1
                    pomin = 1        ## tyle linii pomija bo jest tam liczba linii
                    funkcja = self.tlumacz_ans_objetosc
                elif tekst[0] == '*':
                    funkcja = self.ignoruj
                    ileLinii = 0
                    pomin = 0
                    continue
                elif pomin > 0:
                    pomin = pomin - 1
                    continue
                elif ileLinii > 1:    # dla wielowierszowych funkcji
                    akumulator.append(line)
                    ileLinii = ileLinii - 1
                    continue
                elif funkcja != self.ignoruj:
                    if funkcja == self.tlumacz_pwrzchnia_zlinii:
                        akumulator.append(line)
                        plikWy.write(funkcja(*akumulator) + "\n")
                        akumulator = []
                        ileLinii = 4
                    else:
                        plikWy.write(funkcja(tekst) + "\n")


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Program konwertuje plik tess z programu NEPER")
        print("na komendy wejściowe pakietu ANSYS. Użycie: ")
        print("sciezka_do_programu plik_wejsciowy.tess plik_wynikowy")
        exit()
    knw = Konwerter()
    try:
        knw.konwertuj_komendy(sys.argv[1], sys.argv[2])
        print("Gotowe")
    except Exception as blad:
        print("Nie udało się: " + blad)
