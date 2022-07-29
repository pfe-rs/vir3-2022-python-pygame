import pygame
import numpy as np

pygame.init()
pygame.font.init()
selektovano = []

igra_beli = True
sahiran = False
matiran = False
patiran = False

pomeraj_x = 50
pomeraj_y = 150
polje = 100
notacija_sirina = 400

promotion_table = False

screen_w = 8*polje + 2*pomeraj_x
screen_h = 8*polje + pomeraj_y+pomeraj_x
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Chess')

font = pygame.font.Font('freesansbold.ttf', 70)
boja_slova = (200, 200, 200)
sah = font.render('ŠAH', True, boja_slova)
mat = font.render('MAT', True, boja_slova)
pat = font.render('PAT', True, boja_slova)
#screen.blit(sah, (screen_w//2,pomeraj_y//4))

promotion_size = 150

damaprom = pygame.image.load("dama.png")
damaprom = pygame.transform.scale(damaprom, (promotion_size, promotion_size))

damacprom = pygame.image.load("damac.png")
damacprom = pygame.transform.scale(damacprom, (promotion_size, promotion_size))

topprom = pygame.image.load("top.png")
topprom = pygame.transform.scale(topprom, (promotion_size, promotion_size))

topcprom = pygame.image.load("topc.png")
topcprom = pygame.transform.scale(topcprom, (promotion_size, promotion_size))

lovasprom = pygame.image.load("lovac.png")
lovasprom = pygame.transform.scale(lovasprom, (promotion_size, promotion_size))

lovascprom = pygame.image.load("lovacc.png")
lovascprom = pygame.transform.scale(lovascprom, (promotion_size, promotion_size))

konjprom = pygame.image.load("konj.png")
konjprom = pygame.transform.scale(konjprom, (promotion_size, promotion_size))

konjcprom = pygame.image.load("konjc.png")
konjcprom = pygame.transform.scale(konjcprom, (promotion_size, promotion_size))

tacke = []
for i in range(64): tacke.append("nista")
tacke = np.array(tacke).reshape(8,8)

tabla = []
for i in range(64): tabla.append("0000000000")
tabla = np.array(tabla).reshape(8,8)

tabela_napadanja = []
for i in range(64): tabela_napadanja.append("nijenapadnutonista")
tabela_napadanja = np.array(tabela_napadanja).reshape(8, 8)

####figure
tabla[0][0] = "topc1"
tabla[0][1] = "konjc1"
tabla[0][2] = "lovasc1"
tabla[0][3] = "damac"
tabla[0][4] = "kraljc"
tabla[0][5] = "lovasc2"
tabla[0][6] = "konjc2"
tabla[0][7] = "topc2"
############
tabla[7][0] = "top1"
tabla[7][1] = "konj1"
tabla[7][2] = "lovas1"
tabla[7][3] = "dama"
tabla[7][4] = "kralj"
tabla[7][5] = "lovas2"
tabla[7][6] = "konj2"
tabla[7][7] = "top2"
####pesaci
tabla[1][0] = "pesakc1"
tabla[1][1] = "pesakc2"
tabla[1][2] = "pesakc3"
tabla[1][3] = "pesakc4"
tabla[1][4] = "pesakc5"
tabla[1][5] = "pesakc6"
tabla[1][6] = "pesakc7"
tabla[1][7] = "pesakc8"
############
tabla[6][0] = "pesak1"
tabla[6][1] = "pesak2"
tabla[6][2] = "pesak3"
tabla[6][3] = "pesak4"
tabla[6][4] = "pesak5"
tabla[6][5] = "pesak6"
tabla[6][6] = "pesak7"
tabla[6][7] = "pesak8"

dict = {};figure = []


class figura:
    def __init__(self, ime, pozicija,tip):
        self.slika = pygame.image.load(ime)
        self.slika = pygame.transform.scale(self.slika, (polje,polje))
        self.pozicija = pozicija
        self.pojeden = False
        self.pomeren = False
        self.tip = tip
        self.selektovan = False
        self.x = (self.pozicija[0]-pomeraj_x)//polje
        self.y = (self.pozicija[1]-pomeraj_y)//polje
        self.ime = tabla[self.y][self.x]
        if "c" in self.ime:
            self.boja = "crna"
        else:
            self.boja = "bela"   

    def promote(self, u_sta):
        self.tip = u_sta
        if u_sta == "dama" and igra_beli:
            if igra_beli:
                self.slika = pygame.image.load("dama.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
            else:
                self.slika = pygame.image.load("damac.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
        elif u_sta == "top":
            if  igra_beli:
                self.slika = pygame.image.load("top.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
            else:
                self.slika = pygame.image.load("topc.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
        if u_sta == "lovas" and igra_beli:
            if igra_beli:
                self.slika = pygame.image.load("lovac.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
            else:
                self.slika = pygame.image.load("lovacc.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
        elif u_sta == "konj":
            if  igra_beli:
                self.slika = pygame.image.load("konj.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
            else:
                self.slika = pygame.image.load("konjc.png")
                self.slika = pygame.transform.scale(self.slika, (polje, polje))
        

    def dobar_potez(self, destinacija):
        global sahiran
        global tabela_napadanja
        global tabla
        global selektovano
        pom_tabela = tabela_napadanja.copy()
        pom_tabla = tabla.copy()
        pom_sahiran = not (sahiran == False)
        tabla[self.y][self.x] = "0000000000"
        if tabla[destinacija[1]][destinacija[0]] != "0000000000":
            pojeden_li_je = figure[dict[tabla[destinacija[1]][destinacija[0]]]].pojeden
            figure[dict[tabla[destinacija[1]][destinacija[0]]]].pojeden = True
        tabla[destinacija[1]][destinacija[0]] = self.ime
        if self.tip != "kralj":
            pomx = kralj.x
            pomy = kralj.y
            pomxc = kraljc.x
            pomyc = kraljc.y
        else:
            if self.ime == "kralj":
                pomx = destinacija[0]
                pomy = destinacija[1]
                pomxc = kraljc.x
                pomyc = kraljc.y
            else:
                pomx = kralj.x
                pomy = kralj.y
                pomxc = destinacija[0]
                pomyc = destinacija[1]
            
        for i in range(8):
            for j in range(8): tabela_napadanja[i][j] = "nistanijenapadnuto"
        izracunaj_tabelu_napadanja()
        if (igra_beli and ("crna" in tabela_napadanja[pomx][pomy])) or ((not igra_beli) and ("bela" in tabela_napadanja[pomxc][pomyc])): sahiran = True
        else: sahiran = False
        if sahiran: 
            povratna = False
        else: 
            povratna = True
            #selektovano = [self.x,self.y]
            sahiran = False
        tabela_napadanja = pom_tabela.copy()
        tabla = pom_tabla.copy()
        self.selektovan = False
        if tabla[destinacija[1]][destinacija[0]] != "0000000000":
            figure[dict[tabla[destinacija[1]][destinacija[0]]]].pojeden = pojeden_li_je
        return povratna
    def nacrtaj(self):
        if self.pojeden: return
        screen.blit(self.slika, (self.pozicija[0], self.pozicija[1], polje, polje))
    def pomeri(self, destinacija):
        global selektovano, promotion_table,promotion_size
        if self.pojeden: return
        if tacke[destinacija[0]][destinacija[1]] != "tacka":
            selektovano = []
            self.selektovan = False
            for i in range(8): 
                for j in range(8): tacke[i][j] = "nista"
            return False
        global igra_beli
        if ((igra_beli and self.boja == "bela") or (not igra_beli and self.boja == "crna")):
            if self.tip == "kralj" and destinacija[1] == self.y and (destinacija[0] == self.x+2 or destinacija[0] == self.x-2):
                if self.boja == "bela": pomeraj = 0
                else: pomeraj = 16
                if self.x - destinacija[0] > 0:
                    pomeraj += 6
                    tabla[self.y][self.x] = "0000000000"
                    self.pozicija = [destinacija[0]*100 + pomeraj_x, destinacija[1]*100 + pomeraj_y]
                    tabla[destinacija[1]][destinacija[0]] = self.ime
                    self.x = (self.pozicija[0]-pomeraj_x)//polje
                    self.y = (self.pozicija[1]-pomeraj_y)//polje
                    tabla[figure[pomeraj].y][figure[pomeraj].x] = "0000000000"
                    figure[pomeraj].x = self.x+1
                    figure[pomeraj].y = self.y
                    tabla[self.y][self.x+1] = figure[pomeraj].ime
                    figure[pomeraj].x = self.x+1
                    figure[pomeraj].y = self.y
                    figure[pomeraj].pozicija = [(self.x+1)*polje + pomeraj_x, (self.y)*polje + pomeraj_y]
                else:
                    pomeraj += 7
                    tabla[self.y][self.x] = "0000000000"
                    self.pozicija = [destinacija[0]*100 + pomeraj_x, destinacija[1]*100 + pomeraj_y]
                    tabla[destinacija[1]][destinacija[0]] = self.ime
                    self.x = (self.pozicija[0]-pomeraj_x)//polje
                    self.y = (self.pozicija[1]-pomeraj_y)//polje
                    tabla[figure[pomeraj].y][figure[pomeraj].x] = "0000000000"
                    figure[pomeraj].x = self.x-1
                    figure[pomeraj].y = self.y
                    tabla[self.y][self.x-1] = figure[pomeraj].ime
                    figure[pomeraj].pozicija = [(self.x-1)*polje + pomeraj_x, (self.y)*polje + pomeraj_y]
                
                igra_beli = igra_beli == False
                return True
              
            tabla[self.y][self.x] = "0000000000"
            self.pozicija = [destinacija[0]*100 + pomeraj_x, destinacija[1]*100 + pomeraj_y]
            tabla[destinacija[1]][destinacija[0]] = self.ime
            self.x = (self.pozicija[0]-pomeraj_x)//polje
            self.y = (self.pozicija[1]-pomeraj_y)//polje

            if self.tip == "pesak" and (self.y == 7 or self.y == 0):
                selektovano_pom = selektovano.copy()
                promotion_table = True
                pomerajx = pomeraj_x//2 + polje + 25
                pomerajy = pomeraj_y//2 + polje*4
                while promotion_table:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            (x,y) = pygame.mouse.get_pos()
                            if not(pomerajx <= x <= pomerajx + 4*promotion_size and  pomerajy <= y <=  pomerajy+promotion_size): break
                            x = (x - (pomerajx))//150
                            y = (y - (pomerajy))//150
                            niz_tipova = ["dama", "top", "lovas", "konj"]
                            self.promote(niz_tipova[x])
                            selektovano = selektovano_pom.copy()
                            promotion_table = False
                            break
                    nacrtaj_tablu(True)
                    pygame.draw.rect(screen, (150, 150, 150), (pomerajx, pomerajy, promotion_size*4, promotion_size))
                    if igra_beli:
                        screen.blit(damaprom, (pomerajx, pomerajy , 150, 150))
                        screen.blit(topprom, (pomerajx+150, pomerajy , 150, 150))
                        screen.blit(lovasprom, (pomerajx+150*2, pomerajy , 150, 150))
                        screen.blit(konjprom, (pomerajx+150*3, pomerajy , 150, 150))
                    else:
                        screen.blit(damacprom, (pomerajx, pomerajy , 150, 150))
                        screen.blit(topcprom, (pomerajx+150, pomerajy , 150, 150))
                        screen.blit(lovascprom, (pomerajx+150*2, pomerajy , 150, 150))
                        screen.blit(konjcprom, (pomerajx+150*3, pomerajy , 150, 150))

                    pygame.display.flip()
                            
            igra_beli = igra_beli == False
            self.pomeren = True
        return True
    def klikni(self):
        global selektovano
        global igra_beli
        self.selektovan = self.selektovan == False ## menja vrednost iz true u false i obrnuto
        if self.selektovan and ((igra_beli and self.boja == "bela") or (not igra_beli and self.boja == "crna")):
            selektovano = [self.x, self.y]
        else:
            selektovano = []
            for i in range(8): 
                for j in range(8): tacke[i][j] = "nista"
        return selektovano
    def crtaj_tacke(self, racunanje_tabele = False, proveri = True):
        global tabela_napadanja
        global tacke, selektovano
        for i in range(8):
            for j in range(8):
                tacke[i][j] = "nista"
        if self.pojeden: return
        boja_tacke = (150, 150, 150)
        if racunanje_tabele:
            if(self.tip == "lovas" or self.tip == "dama"):
                x = self.x-1; y = self.y-1
                while x >= 0 and y >= 0:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj": break
                    x-=1;y-=1

                x = self.x+1; y = self.y+1
                while x <= 7 and y <= 7:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj":break
                    x+=1;y+=1

                x = self.x-1; y = self.y+1
                while x >= 0 and y <= 7:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj":break
                    x-=1;y+=1

                x = self.x+1; y = self.y-1
                while x <= 7 and y >= 0:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj": break
                    x+=1;y-=1           
            if(self.tip == "top" or self.tip == "dama"):
                x = self.x; y = self.y-1
                while y >= 0:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj": break
                    y-=1

                x = self.x; y = self.y+1
                while y <= 7:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj": break
                    y+=1

                x = self.x-1; y = self.y
                while x >= 0:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj": break
                    x-=1

                x = self.x+1; y = self.y
                while x <= 7:
                    tacke[x][y] = "tacka"
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                    if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja and figure[dict[tabla[y][x]]].tip != "kralj": break
                    x+=1           
            if(self.tip == "konj"):
                if(self.x + 2 <= 7 and self.y + 1 <= 7): tacke[self.x+2][self.y+1] = "tacka"
                if(self.x + 2 <= 7 and self.y - 1 >= 0): tacke[self.x+2][self.y-1] = "tacka"
                if(self.x - 2 >= 0 and self.y + 1 <= 7): tacke[self.x-2][self.y+1] = "tacka"
                if(self.x - 2 >= 0 and self.y - 1 >= 0): tacke[self.x-2][self.y-1] = "tacka"
                if(self.x + 1 <= 7 and self.y + 2 <= 7): tacke[self.x+1][self.y+2] = "tacka"
                if(self.x + 1 <= 7 and self.y - 2 >= 0): tacke[self.x+1][self.y-2] = "tacka"
                if(self.x - 1 >= 0 and self.y + 2 <= 7): tacke[self.x-1][self.y+2] = "tacka"
                if(self.x - 1 >= 0 and self.y - 2 >= 0): tacke[self.x-1][self.y-2] = "tacka"               
            if(self.tip == "pesak"):
                if self.boja == "bela":
                    if 0 <= self.x-1 <=7 and 0 <= self.y-1 <=7: tacke[self.x-1][self.y-1] = "tacka"
                    if 0 <= self.x+1 <=7 and 0 <= self.y-1 <=7: tacke[self.x+1][self.y-1] = "tacka"
                else:
                    if 0 <= self.x-1 <=7 and 0 <= self.y+1 <=7: tacke[self.x-1][self.y+1] = "tacka"
                    if 0 <= self.x+1 <=7 and 0 <= self.y+1 <=7: tacke[self.x+1][self.y+1] = "tacka"           
            if(self.tip == "kralj"):
                if self.boja == "bela": boja = "crna"
                else: boja = "bela"
                if (0 <= self.x+1 <=7) and (0 <= self.y+1 <=7): tacke[self.x+1][self.y+1] = "tacka"
                if 0 <= self.x-1 <=7 and 0 <= self.y+1 <=7: tacke[self.x-1][self.y+1] = "tacka"
                if 0 <= self.x <=7 and 0 <= self.y+1 <=7: tacke[self.x][self.y+1] = "tacka"
                if 0 <= self.x+1 <=7 and 0 <= self.y-1 <=7: tacke[self.x+1][self.y-1] = "tacka"
                if 0 <= self.x-1 <=7 and 0 <= self.y-1 <=7: tacke[self.x-1][self.y-1] = "tacka"
                if 0 <= self.x <=7 and 0 <= self.y-1 <=7:tacke[self.x][self.y-1] = "tacka"
                if 0 <= self.x+1 <=7 and 0 <= self.y <=7:tacke[self.x+1][self.y] = "tacka"
                if 0 <= self.x-1 <=7 and 0 <= self.y <=7:tacke[self.x-1][self.y] = "tacka"
            return
        if(self.tip == "lovas" or self.tip == "dama"):
            x = self.x-1; y = self.y-1
            while x >= 0 and y >= 0 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                x-=1;y-=1

            x = self.x+1; y = self.y+1
            while x <= 7 and y <= 7 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                x+=1;y+=1

            x = self.x-1; y = self.y+1
            while x >= 0 and y <= 7 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                x-=1;y+=1

            x = self.x+1; y = self.y-1
            while x <= 7 and y >= 0 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                x+=1;y-=1
        if(self.tip == "top" or self.tip == "dama"):
            x = self.x; y = self.y-1
            while y >= 0 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                y-=1
            x = self.x; y = self.y+1
            while y <= 7 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                y+=1
            
            x = self.x-1; y = self.y
            while x >= 0 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                x-=1
            x = self.x+1; y = self.y
            while x <= 7 and (tabla[y][x] == "0000000000" or figure[dict[tabla[y][x]]].boja != self.boja):
                tacke[x][y] = "tacka"
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja == self.boja: break
                if tabla[y][x] != "0000000000" and figure[dict[tabla[y][x]]].boja != self.boja:
                    break
                x+=1
        if(self.tip == "konj"):
            if(self.x + 2 <= 7 and self.y + 1 <= 7 and (tabla[self.y+1][self.x+2] == "0000000000" or figure[dict[tabla[self.y+1][self.x+2]]].boja != self.boja)):
                tacke[self.x+2][self.y+1] = "tacka"
            if(self.x + 2 <= 7 and self.y - 1 >= 0 and (tabla[self.y-1][self.x+2] == "0000000000" or figure[dict[tabla[self.y-1][self.x+2]]].boja != self.boja)):
                tacke[self.x+2][self.y-1] = "tacka"
            if(self.x - 2 >= 0 and self.y + 1 <= 7 and (tabla[self.y+1][self.x-2] == "0000000000" or figure[dict[tabla[self.y+1][self.x-2]]].boja != self.boja)):
                tacke[self.x-2][self.y+1] = "tacka"
            if(self.x - 2 >= 0 and self.y - 1 >= 0 and (tabla[self.y-1][self.x-2] == "0000000000" or figure[dict[tabla[self.y-1][self.x-2]]].boja != self.boja)):
                tacke[self.x-2][self.y-1] = "tacka"
            if(self.x + 1 <= 7 and self.y + 2 <= 7 and (tabla[self.y+2][self.x+1] == "0000000000" or figure[dict[tabla[self.y+2][self.x+1]]].boja != self.boja)):
                tacke[self.x+1][self.y+2] = "tacka"
            if(self.x + 1 <= 7 and self.y - 2 >= 0 and (tabla[self.y-2][self.x+1] == "0000000000" or figure[dict[tabla[self.y-2][self.x+1]]].boja != self.boja)):
                tacke[self.x+1][self.y-2] = "tacka"
            if(self.x - 1 >= 0 and self.y + 2 <= 7 and (tabla[self.y+2][self.x-1] == "0000000000" or figure[dict[tabla[self.y+2][self.x-1]]].boja != self.boja)):
                tacke[self.x-1][self.y+2] = "tacka"
            if(self.x - 1 >= 0 and self.y - 2 >= 0 and (tabla[self.y-2][self.x-1] == "0000000000" or figure[dict[tabla[self.y-2][self.x-1]]].boja != self.boja)):
                tacke[self.x-1][self.y-2] = "tacka"   
        if(self.tip == "pesak"):
            if self.boja == "bela":
                if self.y == 6:
                    if 0 <= self.x <=7 and 0 <= self.y-1 <=7 and tabla[self.y-1][self.x] == "0000000000":
                        tacke[self.x][self.y-1] = "tacka"
                        if 0 <= self.x <=7 and 0 <= self.y-2 <=7 and tabla[self.y-2][self.x] == "0000000000":    
                            tacke[self.x][self.y-2] = "tacka"
                elif 0 <= self.x <=7 and 0 <= self.y-1 <=7 and tabla[self.y-1][self.x] == "0000000000":
                    tacke[self.x][self.y-1] = "tacka"
                if 0 <= self.x-1 <=7 and 0 <= self.y-1 <=7 and tabla[self.y-1][self.x-1] != "0000000000" and figure[dict[tabla[self.y-1][self.x-1]]].boja == "crna":
                    tacke[self.x-1][self.y-1] = "tacka"
                if 0 <= self.x+1 <=7 and 0 <= self.y-1 <=7 and tabla[self.y-1][self.x+1] != "0000000000" and figure[dict[tabla[self.y-1][self.x+1]]].boja == "crna":
                    tacke[self.x+1][self.y-1] = "tacka"
            else:
                if self.y == 1:
                    if 0 <= self.x <=7 and 0 <= self.y+1 <=7 and tabla[self.y+1][self.x] == "0000000000":
                        #pygame.draw.circle(screen, boja_tacke, ((self.x)*polje + pomeraj_x + polje/2, (self.y+1)*polje + pomeraj_y + polje/2), 25)
                        tacke[self.x][self.y+1] = "tacka"
                        if 0 <= self.x <=7 and 0 <= self.y+2 <=7 and tabla[self.y+2][self.x] == "0000000000":
                            #pygame.draw.circle(screen, boja_tacke, ((self.x)*polje + pomeraj_x + polje/2, (self.y+2)*polje + pomeraj_y + polje/2), 25)
                            tacke[self.x][self.y+2] = "tacka"
                elif 0 <= self.x <=7 and 0 <= self.y+1 <=7 and tabla[self.y+1][self.x] == "0000000000":
                    #pygame.draw.circle(screen, boja_tacke, ((self.x)*polje + pomeraj_x + polje/2, (self.y+1)*polje + pomeraj_y + polje/2), 25)
                    tacke[self.x][self.y+1] = "tacka"
                if 0 <= self.x-1 <=7 and 0 <= self.y+1 <=7 and tabla[self.y+1][self.x-1] != "0000000000" and figure[dict[tabla[self.y+1][self.x-1]]].boja == "bela":
                    #pygame.draw.circle(screen, boja_tacke, ((self.x-1)*polje + pomeraj_x + polje/2, (self.y+1)*polje + pomeraj_y + polje/2), 25)
                    tacke[self.x-1][self.y+1] = "tacka"
                if 0 <= self.x+1 <=7 and 0 <= self.y+1 <=7 and tabla[self.y+1][self.x+1] != "0000000000" and figure[dict[tabla[self.y+1][self.x+1]]].boja == "bela":
                    #pygame.draw.circle(screen, boja_tacke, ((self.x+1)*polje + pomeraj_x + polje/2, (self.y+1)*polje + pomeraj_y + polje/2), 25)
                    tacke[self.x+1][self.y+1] = "tacka"
        if(self.tip == "kralj"):
            if self.boja == "bela": boja = "crna"
            else: boja = "bela"
            if (0 <= self.x+1 <=7) and (0 <= self.y+1 <=7) and (not boja in tabela_napadanja[self.x+1][self.y+1]) and ((tabla[self.y+1][self.x+1] != "0000000000" and figure[dict[tabla[self.y+1][self.x+1]]].boja != self.boja) or tabla[self.y+1][self.x+1] == "0000000000"):
                tacke[self.x+1][self.y+1] = "tacka"
            if 0 <= self.x-1 <=7 and 0 <= self.y+1 <=7 and (not boja in tabela_napadanja[self.x-1][self.y+1]) and ((tabla[self.y+1][self.x-1] != "0000000000" and figure[dict[tabla[self.y+1][self.x-1]]].boja != self.boja) or tabla[self.y+1][self.x-1] == "0000000000"):
                tacke[self.x-1][self.y+1] = "tacka"
            if 0 <= self.x <=7 and 0 <= self.y+1 <=7 and (not boja in tabela_napadanja[self.x][self.y+1]) and ((tabla[self.y+1][self.x] != "0000000000" and figure[dict[tabla[self.y+1][self.x]]].boja != self.boja) or tabla[self.y+1][self.x] == "0000000000"):
                tacke[self.x][self.y+1] = "tacka"
            if 0 <= self.x+1 <=7 and 0 <= self.y-1 <=7 and (not boja in tabela_napadanja[self.x+1][self.y-1]) and ((tabla[self.y-1][self.x+1] != "0000000000" and figure[dict[tabla[self.y-1][self.x+1]]].boja != self.boja) or tabla[self.y-1][self.x+1] == "0000000000"):
                tacke[self.x+1][self.y-1] = "tacka"
            if 0 <= self.x-1 <=7 and 0 <= self.y-1 <=7 and (not boja in tabela_napadanja[self.x-1][self.y-1]) and ((tabla[self.y-1][self.x-1] != "0000000000" and figure[dict[tabla[self.y-1][self.x-1]]].boja != self.boja) or tabla[self.y-1][self.x-1] == "0000000000"):
                tacke[self.x-1][self.y-1] = "tacka"
            if 0 <= self.x <=7 and 0 <= self.y-1 <=7 and (not boja in tabela_napadanja[self.x][self.y-1]) and ((tabla[self.y-1][self.x] != "0000000000" and figure[dict[tabla[self.y-1][self.x]]].boja != self.boja) or tabla[self.y-1][self.x] == "0000000000"):
                tacke[self.x][self.y-1] = "tacka"
            if 0 <= self.x+1 <=7 and 0 <= self.y <=7 and (not boja in tabela_napadanja[self.x+1][self.y]) and ((tabla[self.y][self.x+1] != "0000000000" and figure[dict[tabla[self.y][self.x+1]]].boja != self.boja) or tabla[self.y][self.x+1] == "0000000000"):
                tacke[self.x+1][self.y] = "tacka"
            if 0 <= self.x-1 <=7 and 0 <= self.y <=7 and (not boja in tabela_napadanja[self.x-1][self.y]) and ((tabla[self.y][self.x-1] != "0000000000" and figure[dict[tabla[self.y][self.x-1]]].boja != self.boja) or tabla[self.y][self.x-1] == "0000000000"):
                tacke[self.x-1][self.y] = "tacka"
            if igra_beli and not sahiran:
                izracunaj_tabelu_napadanja()
                if tabla[7][5] == "0000000000" and tabla[7][6] == "0000000000" and not top2.pomeren and not kralj.pomeren and not "crna" in tabela_napadanja[kralj.x+2][kralj.y] and not "crna" in tabela_napadanja[kralj.x+1][kralj.y]:
                    tacke[kralj.x+2][kralj.y] = "tacka"
                if tabla[7][1] == "0000000000" and tabla[7][2] == "0000000000" and tabla[7][3] == "0000000000" and not top1.pomeren and not kralj.pomeren and not "crna" in tabela_napadanja[kralj.x-2][kralj.y] and not "crna" in tabela_napadanja[kralj.x-1][kralj.y]:
                    tacke[kralj.x-2][kralj.y] = "tacka"
            elif not igra_beli and not sahiran:
                izracunaj_tabelu_napadanja()
                if tabla[0][5] == "0000000000" and tabla[0][6] == "0000000000" and not topc2.pomeren and not kraljc.pomeren and not "bela" in tabela_napadanja[kraljc.x+2][kraljc.y] and not "bela" in tabela_napadanja[kraljc.x+1][kraljc.y]:
                    tacke[kraljc.x+2][kraljc.y] = "tacka"
                if tabla[0][1] == "0000000000" and tabla[0][2] == "0000000000" and tabla[0][3] == "0000000000" and not topc1.pomeren and not kraljc.pomeren and not "bela" in tabela_napadanja[kraljc.x-2][kraljc.y] and not "bela" in tabela_napadanja[kraljc.x-1][kraljc.y]:
                    tacke[kraljc.x-2][kraljc.y] = "tacka"
        if proveri:
            for i in range(8):
                for j in range(8):
                    if tacke[i][j] == "tacka":
                        if self.dobar_potez([i, j]):
                            pygame.draw.circle(screen, boja_tacke, (i*polje + pomeraj_x + polje/2, j*polje + pomeraj_y + polje/2), 25)
                            selektovano = [self.x, self.y]
                            self.selektovan = True
                        else:
                            tacke[i][j] = "nista"
    

kralj = figura("kralj.png", [pomeraj_x + polje*4, pomeraj_y + polje*7], "kralj");figure.append(kralj);dict["kralj"] = 0
dama = figura("dama.png", [pomeraj_x + polje*3, pomeraj_y + polje*7], "dama");figure.append(dama);dict["dama"] = 1
lovas1 = figura("lovac.png", [pomeraj_x + polje*2, pomeraj_y + polje*7], "lovas");figure.append(lovas1);dict["lovas1"] = 2
lovas2 = figura("lovac.png", [pomeraj_x + polje*5, pomeraj_y + polje*7], "lovas");figure.append(lovas2);dict["lovas2"] = 3
konj1 = figura("konj.png", [pomeraj_x + polje*1, pomeraj_y + polje*7], "konj");figure.append(konj1);dict["konj1"] = 4
konj2 = figura("konj.png", [pomeraj_x + polje*6, pomeraj_y + polje*7], "konj");figure.append(konj2);dict["konj2"] = 5
top1 = figura("top.png", [pomeraj_x + polje*0, pomeraj_y + polje*7], "top");figure.append(top1);dict["top1"] = 6
top2 = figura("top.png", [pomeraj_x + polje*7, pomeraj_y + polje*7], "top");figure.append(top2);dict["top2"] = 7
pesak1 = figura("pesak.png", [pomeraj_x + polje*0, pomeraj_y + polje*6], "pesak");figure.append(pesak1);dict["pesak1"] = 8
pesak2 = figura("pesak.png", [pomeraj_x + polje*1, pomeraj_y + polje*6], "pesak");figure.append(pesak2);dict["pesak2"] = 9
pesak3 = figura("pesak.png", [pomeraj_x + polje*2, pomeraj_y + polje*6], "pesak");figure.append(pesak3);dict["pesak3"] = 10
pesak4 = figura("pesak.png", [pomeraj_x + polje*3, pomeraj_y + polje*6], "pesak");figure.append(pesak4);dict["pesak4"] = 11
pesak5 = figura("pesak.png", [pomeraj_x + polje*4, pomeraj_y + polje*6], "pesak");figure.append(pesak5);dict["pesak5"] = 12
pesak6 = figura("pesak.png", [pomeraj_x + polje*5, pomeraj_y + polje*6], "pesak");figure.append(pesak6);dict["pesak6"] = 13
pesak7 = figura("pesak.png", [pomeraj_x + polje*6, pomeraj_y + polje*6], "pesak");figure.append(pesak7);dict["pesak7"] = 14
pesak8 = figura("pesak.png", [pomeraj_x + polje*7, pomeraj_y + polje*6], "pesak");figure.append(pesak8);dict["pesak8"] = 15
kraljc = figura("kraljc.png", [pomeraj_x + polje*4, pomeraj_y + polje*0], "kralj");figure.append(kraljc);dict["kraljc"] = 16
damac = figura("damac.png", [pomeraj_x + polje*3, pomeraj_y + polje*0], "dama");figure.append(damac);dict["damac"] = 17
lovasc1 = figura("lovacc.png", [pomeraj_x + polje*2, pomeraj_y + polje*0], "lovas");figure.append(lovasc1);dict["lovasc1"] = 18
lovasc2 = figura("lovacc.png", [pomeraj_x + polje*5, pomeraj_y + polje*0], "lovas");figure.append(lovasc2);dict["lovasc2"] = 19
konjc1 = figura("konjc.png", [pomeraj_x + polje*1, pomeraj_y + polje*0], "konj");figure.append(konjc1);dict["konjc1"] = 20
konjc2 = figura("konjc.png", [pomeraj_x + polje*6, pomeraj_y + polje*0], "konj");figure.append(konjc2);dict["konjc2"] = 21
topc1 = figura("topc.png", [pomeraj_x + polje*0, pomeraj_y + polje*0], "top");figure.append(topc1);dict["topc1"] = 22
topc2 = figura("topc.png", [pomeraj_x + polje*7, pomeraj_y + polje*0], "top");figure.append(topc2);dict["topc2"] = 23
pesakc1 = figura("pesakc.png", [pomeraj_x + polje*0, pomeraj_y + polje*1], "pesak");figure.append(pesakc1);dict["pesakc1"] = 24
pesakc2 = figura("pesakc.png", [pomeraj_x + polje*1, pomeraj_y + polje*1], "pesak");figure.append(pesakc2);dict["pesakc2"] = 25
pesakc3 = figura("pesakc.png", [pomeraj_x + polje*2, pomeraj_y + polje*1], "pesak");figure.append(pesakc3);dict["pesakc3"] = 26
pesakc4 = figura("pesakc.png", [pomeraj_x + polje*3, pomeraj_y + polje*1], "pesak");figure.append(pesakc4);dict["pesakc4"] = 27
pesakc5 = figura("pesakc.png", [pomeraj_x + polje*4, pomeraj_y + polje*1], "pesak");figure.append(pesakc5);dict["pesakc5"] = 28
pesakc6 = figura("pesakc.png", [pomeraj_x + polje*5, pomeraj_y + polje*1], "pesak");figure.append(pesakc6);dict["pesakc6"] = 29
pesakc7 = figura("pesakc.png", [pomeraj_x + polje*6, pomeraj_y + polje*1], "pesak");figure.append(pesakc7);dict["pesakc7"] = 30
pesakc8 = figura("pesakc.png", [pomeraj_x + polje*7, pomeraj_y + polje*1], "pesak");figure.append(pesakc8);dict["pesakc8"] = 31

#pat = font.render('PAT', True, boja_slova)
font = pygame.font.Font('freesansbold.ttf', 20)
def nacrtaj_tablu(promote = False):
    global running
    border = 20
    if matiran:
        screen.blit(mat, (screen_w//2-70,pomeraj_y//4))
    elif sahiran:
        screen.blit(sah, (screen_w//2-70,pomeraj_y//4))
    elif patiran:
        screen.blit(pat, (screen_w//2-70,pomeraj_y//4))
    pygame.draw.rect(screen, (0,100,200), (pomeraj_x-border, pomeraj_y-border, 2*border+8*polje, 2*border+8*polje))
    y = pomeraj_y - polje
    for i in range(8):
        y += polje
        x = pomeraj_x
        for j in range(8):
            index = (i+j+1) % 2
            if index == 0: color = (0, 200, 0)
            else: color = (255, 255, 255)
            if selektovano != [] and selektovano[1] == i and selektovano[0] == j:
                pygame.draw.rect(screen, (255, 255, 0), (x, y, polje, polje))
                x += polje
                continue
            pygame.draw.rect(screen, color, (x, y, polje, polje))
            x += polje
    for figura in figure:
        figura.nacrtaj()
    x_slova = pomeraj_x
    for i in range(8):
        screen.blit(font.render(chr(97+i), True,(0,0,0)), (x_slova,pomeraj_y + polje*8))
        x_slova += polje
    y_brojevi = pomeraj_y + 8*polje
    for i in range(8):
        screen.blit(font.render(str(1+i), True,(0,0,0)), (pomeraj_x-2*border//3, y_brojevi-border))
        y_brojevi -= polje
    
    if promote:
        return
    if selektovano != []:    
        figure[dict[tabla[selektovano[1]][selektovano[0]]]].crtaj_tacke()
    if matiran or patiran: running = False

def izracunaj_tabelu_napadanja():
    global tacke
    global tabela_napadanja
    for i in range(8):
        for j in range(8):
            tabela_napadanja[i][j] = "nistanijenapadnuto"
    pom_tacke = tacke.copy()
    for figura in figure:
        if figura.boja == "bela": boja = "crna"
        else: boja = "bela"
        global selektovano
        figura.selektovan = True
        a = selektovano.copy()
        selektovano = [figura.x, figura.y]
        figura.crtaj_tacke(True, False)
        figura.selektovan = False
        selektovano = a.copy()
        for i in range(8):
            for j in range(8):
                if tacke[i][j] == "tacka":
                    if boja in tabela_napadanja[i][j]:
                        tabela_napadanja[i][j] = "napadnutocrnabela"
                        continue
                    tabela_napadanja[i][j] = "napadnuto"+figura.boja
        
        for i in range(8):
            for j in range(8):
                tacke[i][j] = "nista"
    tacke = pom_tacke.copy()
    
bg = (0, 0, 0)
screen.fill(bg)

running = True
while running:
    if igra_beli:
        screen.fill((255,255,255))
    else:
        screen.fill(bg)
    izracunaj_tabelu_napadanja()
    if ("crna" in tabela_napadanja[kralj.x][kralj.y] and kralj.pojeden == False) or ("bela" in tabela_napadanja[kraljc.x][kraljc.y] and kraljc.pojeden == False): sahiran = True
    else: sahiran = False
    print(selektovano)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x,y) = pygame.mouse.get_pos()
            if x < pomeraj_x or y < pomeraj_y or x > pomeraj_x + polje*8 or y > pomeraj_y + polje*8: break
            x = (x-pomeraj_x)//polje
            y = (y-pomeraj_y)//polje
            if tabla[y][x] != "0000000000":
                if selektovano != [] and selektovano[0] == x and selektovano[1] == y:
                    figure[dict[tabla[y][x]]].klikni()
                    selektovano = []
                    break
                if selektovano != [] and tabla[selektovano[1]][selektovano[0]] != "0000000000" and figure[dict[tabla[selektovano[1]][selektovano[0]]]].boja != figure[dict[tabla[y][x]]].boja:
                    if tacke[x][y] == "tacka": figure[dict[tabla[y][x]]].pojeden = True
                    figure[dict[tabla[selektovano[1]][selektovano[0]]]].pomeri([x, y])
                    selektovano = []
                    figure[dict[tabla[y][x]]].klikni()
                    izracunaj_tabelu_napadanja()
                    break
                if selektovano != [] and tabla[selektovano[1]][selektovano[0]] != "0000000000" and figure[dict[tabla[selektovano[1]][selektovano[0]]]].boja == figure[dict[tabla[y][x]]].boja:
                    figure[dict[tabla[selektovano[1]][selektovano[0]]]].klikni()
                    figure[dict[tabla[y][x]]].klikni()
                    izracunaj_tabelu_napadanja()
                    break
                if selektovano != [] and y != selektovano[1] and x != selektovano[0]:
                    figure[dict[tabla[selektovano[1]][selektovano[0]]]].klikni()
                    izracunaj_tabelu_napadanja()
                else:
                    figure[dict[tabla[y][x]]].selektovan = False
                    figure[dict[tabla[y][x]]].klikni()
            else:
                if selektovano != []:
                    if figure[dict[tabla[selektovano[1]][selektovano[0]]]].pomeri([x, y]):
                        figure[dict[tabla[y][x]]].klikni()
                izracunaj_tabelu_napadanja()
        if event.type == pygame.QUIT:
            running = False
            continue
    
    pomocna = selektovano.copy()
    if igra_beli:
        br_tacaka = 0 
        for figurica in figure:
            if figurica.boja == "bela":
                figurica.crtaj_tacke()
                for i in range(8):
                    for j in range(8):
                        if tacke[i][j] == "tacka": 
                            br_tacaka += 1
                            tacke[i][j] = "nista"
    else:
        br_tacaka = 0 
        for figurica in figure:
            if figurica.boja == "crna":
                figurica.crtaj_tacke()
                for i in range(8):
                    for j in range(8):
                        if tacke[i][j] == "tacka": 
                            br_tacaka += 1
                            tacke[i][j] = "nista"
    if br_tacaka == 0: 
        if sahiran: matiran = True
        patiran = True
    selektovano = pomocna.copy()
    izracunaj_tabelu_napadanja()
    if ("crna" in tabela_napadanja[kralj.x][kralj.y] and kralj.pojeden == False) or ("bela" in tabela_napadanja[kraljc.x][kraljc.y] and kraljc.pojeden == False): sahiran = True
    else: sahiran = False
    nacrtaj_tablu()
    pygame.display.flip()     
try:
    if matiran or patiran:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
except:
    pygame.quit()

pygame.quit()