import random
# Koska ässää voidaan käyttää sekä 1:sen että 14:sta paikalla mutta avain on kuitenkin sama (mitä sanakirjassa ei voi
# olla), on peliä yksinkertaistettu niin että arvoa 1 vastaavaa korttia ei ole ollenkaan.
kortit = {"2♠":2,"3♠":3,"4♠":4,"5♠":5,"6♠":6,"7♠":7,"8♠":8,"9♠":9,"10♠":10,"J♠":11,"Q♠":12,"K♠":13,"A♠":14,
          "2♣":2,"3♣":3,"4♣":4,"5♣":5,"6♣":6,"7♣":7,"8♣":8,"9♣":9,"10♣":10,"J♣":11,"Q♣":12,"K♣":13,"A♣":14,
          "2♥":2,"3♥":3,"4♥":4,"5♥":5,"6♥":6,"7♥":7,"8♥":8,"9♥":9,"10♥":10,"J♥":11,"Q♥":12,"K♥":13,"A♥":14,
          "2♦":2,"3♦":3,"4♦":4,"5♦":5,"6♦":6,"7♦":7,"8♦":8,"9♦":9,"10♦":10,"J♦":11,"Q♦":12,"K♦":13,"A♦":14}


def arvo_kortit(): # Arpoo ja palauttaa pelaajalle 5 korttia, jotka eivät ole samoja.
    arvotut = []
    i = 0
    while i < 5:
        arvottu = random.choice(list(kortit.keys()))
        if arvottu not in arvotut:
            arvotut.append(arvottu)
            i += 1
    return arvotut


def vaihto(kasi,vaihdettavat): # Lukee pelaajan toiveen vaihdettavista korteista ja arpoo niiden paikalle uudet kortit.
    if vaihdettavat != "0":
        lista = vaihdettavat.split(",")
        for i in range(len(lista)):
            while True:
                arvottu = random.choice(list(kortit.keys()))
                if arvottu not in kasi:
                    kasi[int(lista[i])-1] = arvottu
                    break
    return kasi


def korkein_kortti(lopullinen): # Tulostaa käden suuriarvoisimman kortin, jos kädessä ei ole parempia yhdistelmiä
    suurin_arvo = kortit[lopullinen[0]]
    suurin_kortti = lopullinen[0]
    i = 1
    while i < 5:
        if kortit[lopullinen[i]] > suurin_arvo:
            suurin_arvo = kortit[lopullinen[i]]
            suurin_kortti = lopullinen[i]
        i += 1
    print(f"Sinulla on korkein kortti {suurin_kortti}!")


def samoja_numeroita(lopullinen): # Tarkastaa onko kädessä 2 tai useampi samaa korttia
    arvot = {}
    for kortti in lopullinen:
        if kortit[kortti] in arvot:
            arvot[kortit[kortti]] += 1
        else:
            arvot[kortit[kortti]] = 1
    samoja = max(arvot.values())
    if samoja == 3 or samoja == 2:
        maarat = list(arvot.values())
        suurin = max(maarat)
        maarat.remove(suurin)
        if max(maarat) == 3:
            return "tk"
        if max(maarat) == 2:
            return "2+2"
    return samoja


def onko_vari(lopullinen): # Tarkastaa onko kädessä väri
    pata = 0
    risti = 0
    hertta = 0
    ruutu = 0
    for kortti in lopullinen:
        if "♠" in kortti:
            pata += 1
        if "♣" in kortti:
            risti += 1
        if "♥" in kortti:
            hertta += 1
        if "♦" in kortti:
            ruutu += 1
    if pata == 5 or risti == 5 or hertta == 5 or ruutu == 5:
        return True
    else:
        return False


def onko_suora(lopullinen): # Tarkastaa onko kädessä suoraa
    arvot = []
    for kortti in lopullinen:
        arvot.append(kortit[kortti])
    arvot.sort()
    i = 4
    while i > 0:
        if arvot[i] - arvot[i - 1] != 1:
            return False
        i -= 1
    return True


def tallenna(voittokasi): # Tallentaa käden tiedostoon ennätykseksi jos se on edellistä ennätystä parempi
    jarjestys = {"korkein kortti":1,"pari":2,"2 paria":3,"3 samaa":4,"suora":5,"väri":6,"täyskäsi":7,"4 samaa":8,"värisuora":9}
    with open("ennatys.txt") as t:
        ennatys = t.read()
        if jarjestys[ennatys] < jarjestys[voittokasi]:
            with open("ennatys.txt","w") as t:
                t.write(voittokasi)
                print("Teit uuden ennätyksen!")


def ennatys(): # Lukee parhaan käden/ennätyksen tiedostosta
    with open("ennatys.txt") as t:
        return t.read()


def main():
    print("Tervetuloa pelaamaan pokeria!\n")
    print("Sinulle jaetaan 5 korttia. Saat halutessasi vaihtaa niistä\n"
          "kerran 0-5 korttia. Tavoitteenasi on saada mahdollisimman\n"
          "hyvät kortit pokerin sääntöjen mukaisesti.\n")
    print(input("Paina enter aloittaaksesi."))

    while True:
        kasi = arvo_kortit()
        print(f"Korttisi ovat: {kasi[0]} - {kasi[1]} - {kasi[2]} - {kasi[3]} - {kasi[4]}\n")

        print("Mitkä korteistasi haluaisit vaihtaa? Erota numerot pilkuilla.\n"
              f"1. {kasi[0]}\n"
              f"2. {kasi[1]}\n"
              f"3. {kasi[2]}\n"
              f"4. {kasi[3]}\n"
              f"5. {kasi[4]}\n"
              "0. En halua vaihtaa korttejani.")
        vaihdettavat = input("Vaihdettavat: ")
        lopullinen = vaihto(kasi,vaihdettavat)

        print(f"Lopulliset korttisi ovat: {lopullinen[0]} - {lopullinen[1]} - {lopullinen[2]} - {lopullinen[3]} - {lopullinen[4]}\n")
        samat = samoja_numeroita(lopullinen)
        vari = onko_vari(lopullinen)
        suora = onko_suora(lopullinen)
        if suora is True and vari is True:
            print("Kädessäsi on värisuora!")
            tallenna("värisuora")
        elif samat == 4:
            print("Kädessäsi on 4 samaa!")
            tallenna("4 samaa")
        elif samat == "tk":
            print("Sinulla on täyskäsi!")
            tallenna("täyskäsi")
        elif vari is True:
            print("Sinulla on väri!")
            tallenna("väri")
        elif suora is True:
            print("Sinulla on suora!")
            tallenna("suora")
        elif samat == 3:
            print("Sinulla on 3 samaa!")
            tallenna("3 samaa")
        elif samat == "2+2":
            print("Sinulla on 2 paria!")
            tallenna("2 paria")
        elif samat == 2:
            print("Sinulla on pari!")
            tallenna("pari")
        else:
            korkein_kortti(lopullinen)
            tallenna("korkein kortti")

        print(f"Paras kätesi on ollut {ennatys()}\n")
        uudelleen = input("Pelataanko uudelleen? (y/n) ")
        print("")
        if uudelleen == "n":
            break


main()
