import pygame
import random


# Inicializa o Pygame
pygame.init()

# Dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# FPS (Frames por segundo)
FPS = 60
relógio = pygame.time.Clock()

# Configurações do jogador
largura_jogador = 50
altura_jogador = 30
x_jogador = 50
y_jogador = ALTURA_TELA // 2
velocidade_jogador = 5
vidas_jogador = 5
tempo_invencibilidade = 60  # Tempo de invulnerabilidade (em frames)
contador_invencibilidade = 0  # Contador de invulnerabilidade

# Configurações do tiro do jogador
largura_tiro = 5
altura_tiro = 5
velocidade_tiro = 10
tiros_jogador = []

# Configurações do inimigo
largura_inimigo = 40
altura_inimigo = 40
velocidade_inimigo = 3
tiros_inimigos = []

# Lista de inimigos
inimigos = []

# Função para criar inimigos
def criar_inimigo():
    x_inimigo = LARGURA_TELA
    y_inimigo = random.randint(0, ALTURA_TELA - altura_inimigo)
    return [x_inimigo, y_inimigo]

# Função para mover inimigos
def mover_inimigos(inimigos):
    global velocidade_inimigo
    for inimigo in inimigos:
        inimigo[0] -= velocidade_inimigo

# Função para desenhar inimigos
def desenhar_inimigos(inimigos):
    for inimigo in inimigos:
        pygame.draw.rect(tela, VERMELHO, (inimigo[0], inimigo[1], largura_inimigo, altura_inimigo))

# Função para criar tiros do jogador
def criar_tiro(x, y):
    return [x + largura_jogador, y + altura_jogador // 2]

# Função para mover os tiros
def mover_tiros(tiros):
    for tiro in tiros:
        tiro[0] += velocidade_tiro

# Função para criar tiros inimigos
def criar_tiro_inimigo(x, y):
    return [x, y + altura_inimigo // 2]

# Função para mover os tiros dos inimigos
def mover_tiros_inimigos(tiros):
    for tiro in tiros:
        tiro[0] -= velocidade_tiro

# Função para desenhar os tiros
def desenhar_tiros(tiros, cor):
    for tiro in tiros:
        pygame.draw.rect(tela, cor, (tiro[0], tiro[1], largura_tiro, altura_tiro))

# Função para checar colisões
def checar_colisao(retangulo1, retangulo2):
    return retangulo1.colliderect(retangulo2)

# Função principal do jogo
def loop_jogo():
    global velocidade_inimigo
    jogando = True
    pontuacao = 0
    x_jogador = 50
    y_jogador = ALTURA_TELA // 2
    vidas_jogador = 5
    inimigos = []
    temporizador_novo_inimigo = 0
    temporizador_tiro_inimigo = 0
    tiros_jogador = []
    tiros_inimigos = []
    contador_invencibilidade = 0
    contador_dificuldade = 0  # Contador para aumentar a dificuldade

    while jogando:
        tela.fill(PRETO)
        temporizador_novo_inimigo += 1
        temporizador_tiro_inimigo += 1
        contador_dificuldade += 1

        # Aumenta a velocidade dos inimigos a cada 30 segundos
        if contador_dificuldade >= FPS * 30:
            velocidade_inimigo += 0.5  # Aumenta a velocidade gradualmente
            contador_dificuldade = 0

        # Tratamento de eventos (fechar janela e outros)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Criação de novos inimigos a cada 80 frames
        if temporizador_novo_inimigo > 80:
            inimigos.append(criar_inimigo())
            temporizador_novo_inimigo = 0

        # Inimigos atirando a cada 120 frames
        if temporizador_tiro_inimigo > 120:
            for inimigo in inimigos:
                tiros_inimigos.append(criar_tiro_inimigo(inimigo[0], inimigo[1]))
            temporizador_tiro_inimigo = 0

        # Eventos de controle (teclas pressionadas)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and y_jogador > 0:
            y_jogador -= velocidade_jogador
        if teclas[pygame.K_DOWN] and y_jogador < ALTURA_TELA - altura_jogador:
            y_jogador += velocidade_jogador
        if teclas[pygame.K_LEFT] and x_jogador > 0:
            x_jogador -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and x_jogador < LARGURA_TELA - largura_jogador:
            x_jogador += velocidade_jogador

        # Disparar tiro ao pressionar a barra de espaço
        if teclas[pygame.K_SPACE]:
            if len(tiros_jogador) < 5:  # Limita a quantidade de tiros na tela
                tiros_jogador.append(criar_tiro(x_jogador, y_jogador))

        # Move os tiros do jogador
        mover_tiros(tiros_jogador)
        tiros_jogador = [tiro for tiro in tiros_jogador if tiro[0] < LARGURA_TELA]

        # Move os tiros dos inimigos
        mover_tiros_inimigos(tiros_inimigos)
        tiros_inimigos = [tiro for tiro in tiros_inimigos if tiro[0] > 0]

        # Desenha o jogador com efeito de invulnerabilidade (piscar)
        if contador_invencibilidade % 20 < 10:
            cor_jogador = BRANCO if contador_invencibilidade == 0 else VERDE  # Muda para verde quando atingido
            retangulo_jogador = pygame.Rect(x_jogador, y_jogador, largura_jogador, altura_jogador)
            pygame.draw.rect(tela, cor_jogador, retangulo_jogador)

        # Move e desenha os inimigos
        mover_inimigos(inimigos)
        desenhar_inimigos(inimigos)

        # Desenha os tiros
        desenhar_tiros(tiros_jogador, AZUL)
        desenhar_tiros(tiros_inimigos, VERMELHO)

        # Verifica colisão entre tiros do jogador e inimigos
        for tiro in tiros_jogador:
            for inimigo in inimigos:
                retangulo_inimigo = pygame.Rect(inimigo[0], inimigo[1], largura_inimigo, altura_inimigo)
                if checar_colisao(pygame.Rect(tiro[0], tiro[1], largura_tiro, altura_tiro), retangulo_inimigo):
                    inimigos.remove(inimigo)
                    tiros_jogador.remove(tiro)
                    pontuacao += 10
                    break

        # Verifica colisão entre o jogador e tiros inimigos
        if contador_invencibilidade == 0:  # Se não estiver invulnerável
            for tiro in tiros_inimigos:
                if checar_colisao(pygame.Rect(tiro[0], tiro[1], largura_tiro, altura_tiro), retangulo_jogador):
                    tiros_inimigos.remove(tiro)
                    vidas_jogador -= 1
                    contador_invencibilidade = tempo_invencibilidade  # Ativa o tempo de invulnerabilidade
                    if vidas_jogador == 0:
                        loop_jogo()  # Reinicia o jogo
                        return

        # Verifica colisão entre o jogador e inimigos
        for inimigo in inimigos:
            retangulo_inimigo = pygame.Rect(inimigo[0], inimigo[1], largura_inimigo, altura_inimigo)
            if contador_invencibilidade == 0 and checar_colisao(retangulo_jogador, retangulo_inimigo):
                inimigos.remove(inimigo)
                vidas_jogador -= 1
                contador_invencibilidade = tempo_invencibilidade  # Ativa o tempo de invulnerabilidade
                if vidas_jogador == 0:
                    loop_jogo()  # Reinicia o jogo
                    return

        # Reduz o contador de invulnerabilidade
        if contador_invencibilidade > 0:
            contador_invencibilidade -= 1

        # Mostra a pontuação e vidas na tela
        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
        texto_vidas = fonte.render(f"Vidas: {vidas_jogador}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))
        tela.blit(texto_vidas, (10, 50))

        pygame.display.flip()
        relógio.tick(FPS)

# Executa o jogo
loop_jogo()
pygame.quit()
