import pygame
from pygame.locals import *
from random import randrange
import os

diretorio_principal = os.path.dirname(__file__)  # Indica o diretório/pasta atual
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')  # Junta a pasta principal com o diretório de imagens
diretorio_sons = os.path.join(diretorio_principal, 'sons')  # Junta o diretório de sons com a pasta dos sons
print(diretorio_principal)
pygame.init()  # Inicia os módulos pygame
pygame.mixer.init()
LARGURA = 640
ALTURA = 480
BRANCO = (255, 255, 255)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo do Dino')

# Cria uma variável que carrega uma imagem, depois junta o diretório de imagens com a imagem que tem dentro dele
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()
seta = pygame.image.load(os.path.join(diretorio_imagens, 'seta.png'))

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.som_do_tiro = pygame.mixer.Sound(os.path.join(diretorio_sons, 'tirododino.wav'))
        self.som_do_tiro.set_volume(1)
        # Foi criada uma lista de imagens
        self.imagens_dinossauro = []
        for i in range(3):
            # 1.ª Tupla, posição em x e y da imagem. 2.ª tupla: tamanho da imagem.
            img = sprite_sheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))

            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        # O atributo self.rect foi criado para armazenar o valor da imagem da sprite/frame, a partir daí ele vai pegar o retângulo dela
        self.rect = self.image.get_rect()
        # Posicione o centro desse retângulo na posição 100x e 100y
        self.rect.center = (100, ALTURA-64)
        self.pulo = False
        self.pos_y_inicial = ALTURA-64 - 96//2
    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def atirar(self):
        self.som_do_tiro.play()

    def update(self):
        if self.pulo == True:
            self.rect.y = self.rect.y - 20
            if self.rect.y <= 200:
                self.pulo = False
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista = self.index_lista + 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 1.ª tupla mostra a posição em x e em y -> A sprite está na posição 7, então deve-se multiplicar 32(que é a posição em x do
        # 1.º elemento) e multiplicar esse valor por 7 para que ele chege até a 7.ª posição e recorte
        self.image = sprite_sheet.subsurface((32*7, 0), (32, 32))

        self.image = pygame.transform.scale(self.image,(32*3, 32*3))  # Aumenta o tamanho da sprite
        self.rect = self.image.get_rect()

        self.rect.y = randrange(50, 200, 50)  # Vai deixar posicionado na tela na posição indicada entre parânteses
        self.rect.x = randrange(LARGURA, 0, -50)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50, 200, 50)
        self.rect.x = self.rect.x - 10


class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32*6, 0), (32, 32))  # Recorte da imagem
        self.rect = self.image.get_rect()  # Transforma a imagem em retângulo para poder manipulá-la melhor
        self.rect.center = (100, 400)
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64


    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x = self.rect.x - 10


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 5, 0), (32, 32))
        self.image = pygame.transform.scale(self.image,(32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, ALTURA - 64)
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        else:
            self.rect.x = self.rect.y - 10


todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)
cacto = Cacto()
todas_as_sprites.add(cacto)



for c in range(LARGURA*2//64):
    chao = Chao(c)
    todas_as_sprites.add(chao)

for i in range(3): # Ele vai criar 4 nuvens, mas elas vão estar posicionadas uma em cima da outra
    nuvens = Nuvens()
    todas_as_sprites.add(nuvens)

relogio = pygame.time.Clock()

deve_continuar = True

while deve_continuar:
    relogio.tick(30)
    tela.fill(BRANCO)

    for event in pygame.event.get():
        if event.type == QUIT:
            deve_continuar = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            if event.key == K_f:
                dino.atirar()
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()
    pygame.display.flip()