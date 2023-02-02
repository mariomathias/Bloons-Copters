import pygame
from pygame.locals import*
from sys import exit
from math import inf as infinito
from random import randint, choice

pygame.init()
pygame.display.set_caption("Bloons Copters")

# TODO
# efeitos sonoros 🔈 (formato .ogg ou .wav, mp3 nao funciona)

# Configurações 🔧
gravidade = pygame.Vector2(0.2, 0)
velocidade = 3

# tamanho da tela 📺
largura = 400
altura = 600
b_largura = 320
b_altura = 30
b_margem = 90
# HITBOX: 43x64 📦

# Fonte ⛲
font = pygame.font.Font('LuckiestGuy-Regular.ttf', 25)

# Imagens 🌆
background = pygame.image.load('imagens/main_menu.png')
cenario1 = pygame.image.load('imagens/cenario1-2.png')
cenario2 = pygame.image.load('imagens/cenario2-2.png')
cenario3 = pygame.image.load('imagens/cenario3-2.png')
cenario4 = pygame.image.load('imagens/cenario4-2.png')
cenario5 = pygame.image.load('imagens/cenario5-2.png')
cenario1_inicio = pygame.image.load('imagens/cenario1.png')
cenario2_inicio = pygame.image.load('imagens/cenario2.png')
cenario3_inicio = pygame.image.load('imagens/cenario3.png')
cenario4_inicio = pygame.image.load('imagens/cenario4.png')
cenario5_inicio = pygame.image.load('imagens/cenario5.png')
tutorial_tela = pygame.image.load('imagens/tutorial_tela.png')
cenario_fases = pygame.image.load('imagens/fases.png')
barras1 = pygame.image.load('imagens/barras.png')
barras2 = pygame.image.load('imagens/barras2.png')
barras3 = pygame.image.load('imagens/barras3.png')
vida = pygame.image.load('imagens/vida.png')
vida_rect = vida.get_rect()
# Balões
bloon_red = pygame.image.load('imagens/red.png')
bloon_blue = pygame.image.load('imagens/blue.png')
bloon_green = pygame.image.load('imagens/green.png')
bloon_yellow = pygame.image.load('imagens/yellow.png')
bloon_pink = pygame.image.load('imagens/pink.png')
bloon_white = pygame.image.load('imagens/white.png')
bloon_zebra = pygame.image.load('imagens/zebra.png')
bloon_rainbow = pygame.image.load('imagens/rainbow.png')
bloon_ceramic = pygame.image.load('imagens/ceramic.png')
bloon_lead = pygame.image.load('imagens/lead.png')
# Boss
moab = pygame.image.load('imagens/moab.png') #172x112
###
creditos = pygame.image.load('imagens/creditos.png')
loja_botao = pygame.image.load('imagens/loja-botao.png')
sairpromenu = pygame.image.load('imagens/sair-pro-menu.png')
try_again = pygame.image.load('imagens/try_again.png')
tela_derrota = pygame.image.load('imagens/tela_derrota.png')
tela_inventario = pygame.image.load('imagens/inventario.png')
tela_loja = pygame.image.load('imagens/loja.png')
inventario_botao = pygame.image.load('imagens/inventario-botao.png')
tela_vitoria = pygame.image.load('imagens/tela_vitoria.png')
mira_cursor = pygame.cursors.Cursor((17, 17), pygame.image.load('imagens/mira.png'))
tela_creditos = pygame.image.load('imagens/tela_creditos.png')

iFase2 = pygame.image.load('imagens/fase_botao2.png')
iFase3 = pygame.image.load('imagens/fase_botao3.png')
iFase4 = pygame.image.load('imagens/fase_botao4.png')
iFase5 = pygame.image.load('imagens/fase_botao5.png')

# Sons 🔊
# kc = pygame.mixer.Sound('sons/kc.ogg')

screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

keys = []

# Classes 🤖
class Botão:
    def __init__(self, img = None, rect = pygame.Rect(40, 0, b_largura, b_altura)):
        self.img = None
        if img != None:
            self.img = pygame.image.load(img)
        self.rect = rect

    def mouse_sobre(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def desenhar(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class ItemLoja(Botão):
    SEM_DINHEIRO = 1
    JA_POSSUI = 2
    def __init__(self, item, valor):
        super().__init__()
        self.img = item.img_normal
        self.valor = valor
        self.item = item
        self.comprado = False

    def comprar(self, player):
        if self.comprado:
            return self.JA_POSSUI
        if player.bananas - self.valor < 0:
            return self.SEM_DINHEIRO
        player.bananas -= self.valor
        self.img = self.item.img_comprado
        self.comprado = True
        player.inventario.append(self.item)
        return None

class ItemInventario(Botão):
    def __init__(self, item):
        super().__init__()
        self.img = item.img_normal
        self.item = item
        self.equipado = False

    def desenhar(self):
        self.img = self.item.img_equipado if self.equipado else self.item.img_normal
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Dardo:
    def __init__(self, normal, comprado, equipado, dano) -> None:
        self.img_normal = pygame.image.load(normal) if normal != None else None
        self.img_comprado = pygame.image.load(comprado) if comprado != None else None
        self.img_equipado = pygame.image.load(equipado) if equipado != None else None
        self.dano = dano

class DardoNormal(Dardo):
    def __init__(self) -> None:
        super().__init__('imagens/dardo-normal.png',None,'imagens/dardo-normal_equipado.png',1)

    def causar_dano(self, inimigo):
        if inimigo.img != bloon_lead:
            return [1, inimigo.levar_dano(self.dano)]
        return [0, False]

class DardoAfiado(Dardo):
    def __init__(self) -> None:
        super().__init__('imagens/dardo-afiado.png','imagens/dardo-afiado_comprado.png','imagens/dardo-afiado_equipado.png', 2)

    def causar_dano(self, inimigo):
        if inimigo.img != bloon_lead:
            morreu = inimigo.levar_dano(self.dano)
            return [2, morreu]
        return [0, False]

class DardoTriplo(Dardo):
    def __init__(self) -> None:
        super().__init__('imagens/dardo-triplo.png','imagens/dardo-triplo_comprado.png','imagens/dardo-triplo_equipado.png', 3)

    def causar_dano(self, inimigo):
        if inimigo.img != bloon_lead:
            morreu = inimigo.levar_dano(self.dano)
            return [3, morreu]
        return [0, False]

class DardoQuente(Dardo):
    def __init__(self) -> None:
        super().__init__('imagens/dardo-quente.png','imagens/dardo-quente_comprado.png','imagens/dardo-quente_equipado.png', 1)
    
    def causar_dano(self, inimigo):
        morreu = inimigo.levar_dano(self.dano)
        return [1, morreu]

class Juggernaut(Dardo):
    def __init__(self) -> None:
        super().__init__('imagens/juggernaut.png','imagens/juggernaut_comprado.png','imagens/juggernaut_equipado.png', 4)
    
    def causar_dano(self, inimigo):
        morreu = inimigo.levar_dano(self.dano)
        return [4, morreu]

class Barras:
    BARRA_MEIO = 1 
    BARRA_ESQUERDA = 2
    BARRA_DIREITA = 3
    def __init__(self, altura, type) -> None:
        self.rects = [None, None]
        if type == self.BARRA_MEIO:
            self.img = barras1
            self.rects[0] = pygame.Rect(0, altura, 108, 20)
            self.rects[1] = pygame.Rect(288, altura, 108, 20)
        elif type == self.BARRA_ESQUERDA:
            self.img = barras2
            self.rects[0] = pygame.Rect(0, altura, 49, 20)
            self.rects[1] = pygame.Rect(229, altura, 171, 20)
        elif type == self.BARRA_DIREITA:
            self.img = barras3
            self.rects[0] = pygame.Rect(0, altura, 184, 20)
            self.rects[1] = pygame.Rect(364, altura, 36, 20)

    def atualizar(self):
        self.rects[0].y += velocidade
        self.rects[1].y += velocidade

    def mouse_sobre(self):
        return False

    def colidir(self, objeto):
        colisao_esquerda = self.rects[0].colliderect(objeto)
        if colisao_esquerda == False:
            return self.rects[1].colliderect(objeto)
        return colisao_esquerda

    def desenhar(self):
        screen.blit(self.img, (0, self.rects[0].y))

    def altura(self):
        return self.rects[0].y

class Balão:
    def __init__(self, x, y, balão) -> None:
        self.img = balão
        self.rect = pygame.Rect(x, y, 23, 30)
        
    def atualizar(self):
        self.rect.y += velocidade

    def colidir(self, objeto):
        return self.rect.colliderect(objeto)

    def desenhar(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def altura(self):
        return self.rect.y

    def mouse_sobre(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def levar_dano(self, dano):
        if dano == 0:
            return False
        if self.img == bloon_red:
            return True
        elif self.img == bloon_blue:
            self.img = bloon_red
        elif self.img == bloon_green:
            self.img = bloon_blue
        elif self.img == bloon_yellow:
            self.img = bloon_green
        elif self.img == bloon_pink:
            self.img = bloon_yellow
        elif self.img == bloon_white:
            self.img = bloon_pink
        elif self.img == bloon_zebra:
            self.img = bloon_white
        elif self.img == bloon_rainbow:
            self.img = bloon_zebra
        elif self.img == bloon_ceramic:
            self.img = bloon_rainbow
        elif self.img == bloon_lead:
            self.img = bloon_pink
        return self.levar_dano(dano - 1)

class Boss:
    def __init__(self) -> None:
        self.vida = 250
        self.img = moab
        self.rect = moab.get_rect()
        self.rect.x = (largura/2) - (self.rect.width/2)
        self.rect.y = -self.rect.height

    def atualizar(self):
        # Entrada Triunfal
        t = 0.01
        self.rect.y = self.rect.y + (120 - self.rect.y) * t

    def levar_dano(self, dano):
        self.vida -= dano
        return self.vida <= 0

    def colidir(self, player):
        return False

    def mouse_sobre(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def altura(self):
        return self.rect.y

    def desenhar(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def mouse_sobre(self):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
            return False

class Player:
    def __init__(self) -> None:
        self.inventario = [DardoNormal()]
        self.arma = self.inventario[0]
        self.rect = pygame.Rect(largura/2, 700, 43, 64)
        self.vel = pygame.Vector2(0, 0)
        self.acel = pygame.Vector2(0, 0)
        self.limite = 4
        self.img = pygame.image.load('imagens/player.png')
        self.bananas = 0

    def desenhar(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def virar(self):
        self.img = pygame.transform.flip(self.img, True, False)

    def aplicar_forca(self, forca):
        self.acel += forca

    def atualizar(self):
        self.rect.y = animacao(self.rect.y, altura*0.75, 0.05)
        self.vel += self.acel
        if self.vel.x > self.limite:
            self.vel.x = self.limite
        if self.vel.x < -self.limite:
            self.vel.x = -self.limite
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        self.acel.update(0, 0)

        if self.rect.x > largura+self.rect.width:
            self.rect.x = -self.rect.width
        if self.rect.x < -self.rect.width:
            self.rect.x = largura

    def atacar(self, inimigo):
        inimigos = [Balão, Boss] # Inimigos que podem receber dano
        if type(inimigo) in inimigos:
            resultado = self.arma.causar_dano(inimigo) # (bananas, morreu)
            self.bananas += resultado[0]
            return resultado[1]

player = Player()
# TESTE
# player.bananas = 99999

# Botões ✅
bJogar = Botão('imagens/jogar.png', pygame.Rect(125, -150, 133, 44))
bLoja = Botão('imagens/loja-botao.png', pygame.Rect(125, -194, 133, 44))
bInventario = Botão('imagens/inventario-botao.png', pygame.Rect(125, -238, 133, 44))
bTutorial = Botão('imagens/tutorial.png', pygame.Rect(125, -282, 133, 44))
bCreditos = Botão('imagens/creditos.png', pygame.Rect(125, -326, 133, 44))
bSair = Botão('imagens/sair.png', pygame.Rect(125, -370, 133, 44))

bFase1 = Botão('imagens/fase_botao1.png', pygame.Rect((largura/2)-117, 100, 235, 66))
bFase2 = Botão('imagens/fase_botao2B.png', pygame.Rect((largura/2)-117, 175, 235, 66))
bFase3 = Botão('imagens/fase_botao3B.png', pygame.Rect((largura/2)-117, 250, 235, 66))
bFase4 = Botão('imagens/fase_botao4B.png', pygame.Rect((largura/2)-117, 325, 235, 66))
bFase5 = Botão('imagens/fase_botao5B.png', pygame.Rect((largura/2)-117, 400, 235, 66))
# TODO apagar comentario abaixo após a conclusão do jogo
fases_bloqueadas = [2,3,4,5]

bTryagain = Botão('imagens/try_again.png', pygame.Rect((largura/2)-100, 300, 200, 80))
bSairpromenu = Botão('imagens/sair-pro-menu.png', pygame.Rect((largura/2)-100, 400, 200, 50))

bProxfase = Botão('imagens/proxima-fase.png', pygame.Rect((largura/2)-100, 330, 200, 50))

itensLoja = [
    ItemLoja(DardoQuente(), 100),
    ItemLoja(DardoAfiado(), 100),
    ItemLoja(DardoTriplo(), 200),
    ItemLoja(Juggernaut(), 400)
]

# Desenhar texto ✏️
def draw_text(text, color, x, y, topright=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if topright:
        textrect.topright = (x, y)
    else:
        textrect.topleft = (x, y)
    screen.blit(textobj, textrect)

# Animacao
def animacao(a,b,t):
    return a + (b - a)*t

# Menu 📋
def main_menu():

    while True:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        click = False
        for event in pygame.event.get():
            if event.type == KEYUP:
                keys.append(event.key)
                if len(keys) > 11:
                    keys.pop(0)
                if keys == [1073741906, 1073741906, 1073741905, 1073741905, 1073741904, 1073741903, 1073741904, 1073741903, 98, 97, 13]:
                    print("Konami Code You now have infinite bananas")
                    player.bananas = infinito
                    player.img = pygame.image.load('imagens/marco.png')
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(background, (0, 0))

        # 150, 194, 238, 282, 326, 370
        bJogar.rect.y = animacao(bJogar.rect.y, 150, 0.1)
        bLoja.rect.y = animacao(bLoja.rect.y, 194, 0.1)
        bInventario.rect.y = animacao(bInventario.rect.y, 238, 0.1)
        bTutorial.rect.y = animacao(bTutorial.rect.y, 282, 0.1)
        bCreditos.rect.y = animacao(bCreditos.rect.y, 326, 0.1)
        bSair.rect.y = animacao(bSair.rect.y, 370, 0.1)

        bJogar.desenhar()
        bLoja.desenhar()
        bInventario.desenhar()
        bTutorial.desenhar()
        bCreditos.desenhar()
        bSair.desenhar()

        if bJogar.mouse_sobre() and click:
            fases()
        elif bLoja.mouse_sobre() and click:
            loja()
        elif bInventario.mouse_sobre() and click:
            inventario()
        elif bTutorial.mouse_sobre() and click:
            tut()
        elif bCreditos.mouse_sobre() and click:
            screen_creditos()
        elif bSair.mouse_sobre() and click:
            pygame.quit()
            exit()
        pygame.display.update()
        clock.tick(60)

# Tutorial 👶
def tut():
    while True:
        screen.blit(tutorial_tela, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pygame.display.update()
        clock.tick(60)

# Loja
def loja():
    for i in range(len(itensLoja)):
        itensLoja[i].rect = pygame.Rect(40, 40 + b_altura + i * b_margem, b_largura, b_altura)
    while True:
        screen.blit(tela_loja,(0,0))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        draw_text(f'{player.bananas}', (255, 255, 10), 192, 545)

        for i in itensLoja:
            i.desenhar()
            if i.mouse_sobre() and click:
                i.comprar(player)

        pygame.display.update()
        clock.tick(60)

def inventario():
    bItens = []
    b_altura = 50
    b_margem = 60
    for i in range(len(player.inventario)):
        item = player.inventario[i]
        bItens.append(ItemInventario(item))
        bItens[i].rect = pygame.Rect(40, 40 + b_altura + i * b_margem, b_largura, b_altura)
        if item == player.arma:
            bItens[i].equipado = True
    
    while True:
        screen.blit(tela_inventario,(0,0))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        for i in bItens:
            i.desenhar()
            if i.mouse_sobre() and click:
                for j in bItens:
                    j.equipado = False
                i.equipado = True
                player.arma = i.item
       
        pygame.display.update()
        clock.tick(60)

def screen_creditos():
    while True:
        screen.blit(tela_creditos,(0,0))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)

# Fases 🤔hmm
def fases():
    global fases_bloqueadas

    if 2 not in fases_bloqueadas:
        bFase2.img = iFase2
    if 3 not in fases_bloqueadas:
        bFase3.img = iFase3
    if 4 not in fases_bloqueadas:
        bFase4.img = iFase4
    if 5 not in fases_bloqueadas:
        bFase5.img = iFase5

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(cenario_fases, (0, 0))
        bFase1.desenhar()
        bFase2.desenhar()
        bFase3.desenhar()
        bFase4.desenhar()
        bFase5.desenhar()

        if bFase1.mouse_sobre() and click:
            fase1()
            return
        elif bFase2.mouse_sobre() and click and 2 not in fases_bloqueadas:
            fase2()
            return
        elif bFase3.mouse_sobre() and click and 3 not in fases_bloqueadas:
            fase3()
            return
        elif bFase4.mouse_sobre() and click and 4 not in fases_bloqueadas:
            fase4()
            return
        elif bFase5.mouse_sobre() and click and 5 not in fases_bloqueadas:
            fase5()
            return

        pygame.display.update()
        clock.tick(60)

def derrota(fase):
    player.rect.y = 700
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        screen.blit(tela_derrota,(0,0))
        bTryagain.desenhar()
        bSairpromenu.desenhar()

        if bTryagain.mouse_sobre() and click:
            fase()
            return
        elif bSairpromenu.mouse_sobre() and click:
            main_menu()

        pygame.display.update()
        clock.tick(60)

def vitoria(fase=None):
    player.rect.y = 700
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        screen.blit(tela_vitoria,(0,0))
        if fase != None:
            bProxfase.desenhar()

            if bProxfase.mouse_sobre() and click:
                fase()
                return
        else:
            bSairpromenu.desenhar()
            if bSairpromenu.mouse_sobre() and click:
                return

        pygame.display.update()
        clock.tick(60)

# Fase 1 🌎✏️
def fase1():
    global gravidade, player
    
    pygame.mouse.set_cursor(mira_cursor)

    metros = 0
    cenario1_y = altura-2000
    cenario2_y = cenario1_y-1000
    cenario1_inicio_y = altura-1000

    inimigos = []
    inimigos_fase = [bloon_red, bloon_blue, bloon_green]
    padrão_barras = [Barras.BARRA_MEIO, Barras.BARRA_DIREITA, Barras.BARRA_MEIO, Barras.BARRA_ESQUERDA]

    y = -100
    for i in range(8):
        barra = Barras(y, padrão_barras[i%4])
        inimigos.append(barra)
        bpos = barra.rects[0].width + 79
        inimigos.append(Balão(bpos, y, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-200, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-400, choice(inimigos_fase)))
        y += -600

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.virar()
                    gravidade *= -1
                elif event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(cenario1_inicio, (0, cenario1_inicio_y))
        screen.blit(cenario1, (0, cenario1_y))
        screen.blit(cenario1, (0, cenario2_y))

        draw_text("%3.1f Metros" % metros, (90, 110, 90), 10, 10)
        draw_text(f"{player.bananas}", (155, 155, 25), 390, 10, True)

        player.desenhar()
        player.aplicar_forca(gravidade)
        player.atualizar()

        for inimigo in inimigos:
            inimigo.atualizar()
            inimigo.desenhar()
            if inimigo.colidir(player):
                inimigos.remove(inimigo)
                derrota(fase1)
                return
            if inimigo.mouse_sobre() and type(inimigo) == Balão and click:
                if player.atacar(inimigo): # Se retornar True, o inimigo morreu com o ataque
                    inimigos.remove(inimigo)

            if inimigo.altura() > altura:
                inimigos.remove(inimigo)

        metros += 0.03
        #uma ideia massa pra fazer depois
        if metros > 50:
            if 2 in fases_bloqueadas:
                fases_bloqueadas.remove(2)
            vitoria(fase2)
            return

        cenario1_y += velocidade
        cenario2_y += velocidade

        if cenario1_inicio_y < altura:
            cenario1_inicio_y += velocidade

        if cenario1_y >= altura:
            cenario1_y = cenario2_y-1000
        elif cenario2_y >= altura:
            cenario2_y = cenario1_y-1000
        pygame.display.update()
        clock.tick(60)

# FASE 2 ✏️
def fase2():
    global gravidade, player
    
    pygame.mouse.set_cursor(mira_cursor)

    metros = 0
    cenario1_y = altura-2000
    cenario2_y = cenario1_y-1000
    cenario1_inicio_y = altura-1000

    inimigos = []
    # inimigos_fase = [3, 4, 5]
    inimigos_fase = [bloon_green, bloon_yellow, bloon_pink]
    padrão_barras = [Barras.BARRA_DIREITA, Barras.BARRA_ESQUERDA, Barras.BARRA_DIREITA, Barras.BARRA_MEIO]

    y = -100
    for i in range(13):
        barra = Barras(y, padrão_barras[i%4])
        inimigos.append(barra)
        bpos = barra.rects[0].width + 79
        inimigos.append(Balão(bpos, y, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-200, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-400, choice(inimigos_fase)))
        y += -600

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.virar()
                    gravidade *= -1
                elif event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(cenario2_inicio, (0, cenario1_inicio_y))
        screen.blit(cenario2, (0, cenario1_y))
        screen.blit(cenario2, (0, cenario2_y))

        draw_text("%3.1f Metros" % metros, (90, 110, 90), 10, 10)
        draw_text(f"{player.bananas}", (155, 155, 25), 390, 10, True)

        player.desenhar()
        player.aplicar_forca(gravidade)
        player.atualizar()

        for inimigo in inimigos:
            inimigo.atualizar()
            inimigo.desenhar()
            if inimigo.colidir(player):
                inimigos.remove(inimigo)
                derrota(fase2)
                return
            if inimigo.mouse_sobre() and type(inimigo) == Balão and click:
                if player.atacar(inimigo): # Se retornar True, o inimigo morreu com o ataque
                    inimigos.remove(inimigo)

            if inimigo.altura() > altura:
                inimigos.remove(inimigo)

        metros += 0.03
        #uma ideia massa pra fazer depois
        if metros > 70:
            if 3 in fases_bloqueadas:
                fases_bloqueadas.remove(3)
            vitoria(fase3)
            return

        cenario1_y += velocidade
        cenario2_y += velocidade

        if cenario1_inicio_y < altura:
            cenario1_inicio_y += velocidade

        if cenario1_y >= altura:
            cenario1_y = cenario2_y-1000
        elif cenario2_y >= altura:
            cenario2_y = cenario1_y-1000
        pygame.display.update()
        clock.tick(60)

# FASE 3 ✏️
def fase3():
    global gravidade, player
    
    pygame.mouse.set_cursor(mira_cursor)

    metros = 0
    cenario1_y = altura-2000
    cenario2_y = cenario1_y-1000
    cenario1_inicio_y = altura-1000

    inimigos = []
    # inimigos_fase = [3, 4, 5, 10]
    inimigos_fase = [bloon_green, bloon_yellow, bloon_pink, bloon_lead]
    padrão_barras = [Barras.BARRA_DIREITA, Barras.BARRA_ESQUERDA, Barras.BARRA_DIREITA, Barras.BARRA_ESQUERDA]

    y = -100
    for i in range(17):
        barra = Barras(y, padrão_barras[i%4])
        inimigos.append(barra)
        bpos = barra.rects[0].width + 79
        inimigos.append(Balão(bpos, y, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-200, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-400, choice(inimigos_fase)))
        y += -600

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.virar()
                    gravidade *= -1
                elif event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(cenario3_inicio, (0, cenario1_inicio_y))
        screen.blit(cenario3, (0, cenario1_y))
        screen.blit(cenario3, (0, cenario2_y))

        draw_text("%3.1f Metros" % metros, (90, 110, 90), 10, 10)
        draw_text(f"{player.bananas}", (155, 155, 25), 390, 10, True)

        player.desenhar()
        player.aplicar_forca(gravidade)
        player.atualizar()

        for inimigo in inimigos:
            inimigo.atualizar()
            inimigo.desenhar()
            if inimigo.colidir(player):
                inimigos.remove(inimigo)
                derrota(fase3)
                return
            if inimigo.mouse_sobre() and type(inimigo) == Balão and click:
                if player.atacar(inimigo): # Se retornar True, o inimigo morreu com o ataque
                    inimigos.remove(inimigo)

            if inimigo.altura() > altura:
                inimigos.remove(inimigo)

        metros += 0.03
        #uma ideia massa pra fazer depois
        if metros > 80:
            if 4 in fases_bloqueadas:
                fases_bloqueadas.remove(4)
            vitoria(fase4)
            return

        cenario1_y += velocidade
        cenario2_y += velocidade

        if cenario1_inicio_y < altura:
            cenario1_inicio_y += velocidade

        if cenario1_y >= altura:
            cenario1_y = cenario2_y-1000
        elif cenario2_y >= altura:
            cenario2_y = cenario1_y-1000
        pygame.display.update()
        clock.tick(60)

# FASE 4 ✏️
def fase4():
    global gravidade, player
    
    pygame.mouse.set_cursor(mira_cursor)

    metros = 0
    cenario1_y = altura-2000
    cenario2_y = cenario1_y-1000
    cenario1_inicio_y = altura-1000

    inimigos = []
    # inimigos_fase = [4, 5, 7, 8]
    inimigos_fase = [bloon_yellow, bloon_pink, bloon_white, bloon_rainbow]
    padrão_barras = [Barras.BARRA_DIREITA, Barras.BARRA_ESQUERDA, Barras.BARRA_DIREITA, Barras.BARRA_ESQUERDA, Barras.BARRA_MEIO]

    y = -100
    for i in range(20):
        barra = Barras(y, padrão_barras[i%5])
        inimigos.append(barra)
        bpos = barra.rects[0].width + 79
        inimigos.append(Balão(bpos, y, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-200, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-400, choice(inimigos_fase)))
        y += -600

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.virar()
                    gravidade *= -1
                elif event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(cenario4_inicio, (0, cenario1_inicio_y))
        screen.blit(cenario4, (0, cenario1_y))
        screen.blit(cenario4, (0, cenario2_y))

        draw_text("%3.1f Metros" % metros, (90, 110, 90), 10, 10)
        draw_text(f"{player.bananas}", (155, 155, 25), 390, 10, True)

        player.desenhar()
        player.aplicar_forca(gravidade)
        player.atualizar()

        for inimigo in inimigos:
            inimigo.atualizar()
            inimigo.desenhar()
            if inimigo.colidir(player):
                inimigos.remove(inimigo)
                derrota(fase4)
                return
            if inimigo.mouse_sobre() and type(inimigo) == Balão and click:
                if player.atacar(inimigo): # Se retornar True, o inimigo morreu com o ataque
                    inimigos.remove(inimigo)

            if inimigo.altura() > altura:
                inimigos.remove(inimigo)

        metros += 0.03
        #uma ideia massa pra fazer depois
        if metros > 90:
            if 5 in fases_bloqueadas:
                fases_bloqueadas.remove(5)
            vitoria(fase5)
            return


        cenario1_y += velocidade
        cenario2_y += velocidade

        if cenario1_inicio_y < altura:
            cenario1_inicio_y += velocidade

        if cenario1_y >= altura:
            cenario1_y = cenario2_y-1000
        elif cenario2_y >= altura:
            cenario2_y = cenario1_y-1000
        pygame.display.update()
        clock.tick(60)

# FASE 5 ✏️
def fase5():
    global gravidade, player
    
    pygame.mouse.set_cursor(mira_cursor)

    metros = 0
    cenario1_y = altura-2000
    cenario2_y = cenario1_y-1000
    cenario1_inicio_y = altura-1000

    chefão = False

    inimigos = []
    inimigos_chefão = []

    boss_text_font = font.render(f"CHEFÃO", 1, (255, 150, 150))
    boss_text_rect = boss_text_font.get_rect()
    boss_text_rect.centerx = 200
    boss_text_rect.centery = -100

    vida_max = 0
    vida_rect.y = 700

    inimigos_fase = [bloon_zebra,bloon_rainbow,bloon_lead,bloon_ceramic]
    inimigos_fase_chefão = [bloon_red, bloon_blue, bloon_green]
    padrão_barras = [Barras.BARRA_ESQUERDA, Barras.BARRA_ESQUERDA, Barras.BARRA_DIREITA, Barras.BARRA_ESQUERDA, Barras.BARRA_MEIO, Barras.BARRA_DIREITA]

    y = -100
    for i in range(25):
        barra = Barras(y, padrão_barras[i%6])
        inimigos.append(barra)
        bpos = barra.rects[0].width + 79
        inimigos.append(Balão(bpos, y, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-200, choice(inimigos_fase)))
        inimigos.append(Balão(randint(0, largura-23), y-400, choice(inimigos_fase)))
        y += -600

        # Calculo -> largura = 400; 400/5 = 80; x1 = 80-b.w/2
    # Inimigos que aparecerão quando chegar o chefão
    y = -100
    for i in range(20):
        # TRÊS BALÕES
        inimigos_chefão.append(Balão(89, y-200,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(189, y-200,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(289, y-200,choice(inimigos_fase_chefão)))
        # DOIS BALÕES
        inimigos_chefão.append(Balão(139, y-400,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(239, y-400,choice(inimigos_fase_chefão)))
        # PAREDE
        inimigos_chefão.append(Balão(10, y-500,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(367, y-500,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(10, y-550,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(367, y-550,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(10, y-600,choice(inimigos_fase_chefão)))
        inimigos_chefão.append(Balão(367, y-600,choice(inimigos_fase_chefão)))
        y += -600

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.virar()
                    gravidade *= -1
                elif event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(cenario5_inicio, (0, cenario1_inicio_y))
        screen.blit(cenario5, (0, cenario1_y))
        screen.blit(cenario5, (0, cenario2_y))

        if chefão:
            vida_rect.y = animacao(vida_rect.y, 575, 0.08)

            if boss_text_rect.centery <= 295:
                boss_text_rect.centery = animacao(boss_text_rect.centery, 310, 0.07)
            else:
                boss_text_rect.centery = animacao(boss_text_rect.centery, 700, 0.1)
            # Ciência da computação
            # 400 = vida_max
            #  X  = inimigos[0].vida
            # X = (400 * inimigos[0].vida) / vida_max
            vida_porc = (400 * inimigos[0].vida) / vida_max
            vida_rect.width = vida_porc
            vida_nova = vida.subsurface((0, 0, vida_porc, 20))

            screen.blit(vida_nova, vida_rect)
            screen.blit(boss_text_font, boss_text_rect)

        draw_text("%3.1f Metros" % metros, (90, 110, 90), 10, 10)
        draw_text(f"{player.bananas}", (155, 155, 25), 390, 10, True)

        player.desenhar()
        player.aplicar_forca(gravidade)
        player.atualizar()

        for inimigo in inimigos:
            inimigo.atualizar()
            inimigo.desenhar()
            if inimigo.colidir(player):
                inimigos.remove(inimigo)
                derrota(fase5)
                return
            if inimigo.mouse_sobre() and click:  # and type(inimigo) == Balão
                if player.atacar(inimigo): # Se retornar True, o inimigo morreu com o ataque
                    if type(inimigo) == Boss:
                        return vitoria()
                    inimigos.remove(inimigo)

            if inimigo.altura() > altura:
                inimigos.remove(inimigo)
        # Qual o metro que o chefão tem que spawnar? 100 👍 
        if metros >= 100 and chefão == False:
            chefão = True
            inimigos.clear()
            inimigos.append(Boss())
            inimigos.extend(inimigos_chefão)
            vida_max = inimigos[0].vida

        metros += 0.03

        cenario1_y += velocidade
        cenario2_y += velocidade

        if cenario1_inicio_y < altura:
            cenario1_inicio_y += velocidade

        if cenario1_y >= altura:
            cenario1_y = cenario2_y-1000
        elif cenario2_y >= altura:
            cenario2_y = cenario1_y-1000
        pygame.display.update()
        clock.tick(60)

main_menu()