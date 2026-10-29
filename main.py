
import pygame
import sys
import json
import os
import random
import math

pygame.init()

# ==================================================
# CONFIGURACAO
# ==================================================
LARGURA, ALTURA = 900, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Desafio da Matematica Discreta")
relogio = pygame.time.Clock()

ARQUIVO_RANKING = "ranking_matematica.json"

# ==================================================
# CORES NEON
# ==================================================
FUNDO = (12, 15, 35)
PAINEL = (24, 29, 59)
PAINEL_CLARO = (36, 43, 79)
BRANCO = (245, 248, 255)
CINZA = (165, 179, 210)
ROXO = (137, 92, 255)
ROXO_CLARO = (181, 145, 255)
CIANO = (65, 225, 240)
VERDE = (45, 210, 145)
VERMELHO = (255, 85, 115)
AMARELO = (255, 211, 100)
PRETO = (8, 10, 24)

# ==================================================
# FONTES
# ==================================================
fonte_logo = pygame.font.SysFont("arial", 43, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 30, bold=True)
fonte_subtitulo = pygame.font.SysFont("arial", 23, bold=True)
fonte_normal = pygame.font.SysFont("arial", 19)
fonte_pequena = pygame.font.SysFont("arial", 16)
fonte_mini = pygame.font.SysFont("arial", 13)
fonte_grande = pygame.font.SysFont("arial", 48, bold=True)

# ==================================================
# PERGUNTAS
# ==================================================
perguntas = [
    {
        "pergunta": "Ana tem 3 camisetas e 2 calcas.",
        "complemento": "Quantos conjuntos diferentes ela pode formar?",
        "opcoes": [
            "5 conjuntos", "6 conjuntos",
            "3 conjuntos", "9 conjuntos"
        ],
        "correta": 1,
        "explicacao": "Principio multiplicativo: 3 x 2 = 6 conjuntos."
    },
    {
        "pergunta": "Uma pessoa pode escolher uma bebida.",
        "complemento": "Existem 4 sucos ou 3 refrigerantes. Quantas opcoes ha?",
        "opcoes": [
            "7 bebidas", "12 bebidas",
            "4 bebidas", "1 bebida"
        ],
        "correta": 0,
        "explicacao": "Principio aditivo: 4 + 3 = 7 opcoes."
    },
    {
        "pergunta": "Existem 10 meias em 9 gavetas.",
        "complemento": "O que podemos afirmar?",
        "opcoes": [
            "Cada gaveta tem uma meia",
            "Uma gaveta tem pelo menos 2 meias",
            "Todas tem 2 meias",
            "Uma gaveta fica vazia"
        ],
        "correta": 1,
        "explicacao": "10 meias em 9 gavetas garantem pelo menos 2 em alguma gaveta."
    },
    {
        "pergunta": "Uma lanchonete oferece 3 sanduiches.",
        "complemento": "Tambem oferece 4 sucos. Quantos pedidos com 1 de cada?",
        "opcoes": [
            "7 pedidos", "12 pedidos",
            "4 pedidos", "9 pedidos"
        ],
        "correta": 1,
        "explicacao": "Principio multiplicativo: 3 x 4 = 12 pedidos."
    },
    {
        "pergunta": "Em uma turma ha 13 alunos.",
        "complemento": "Podemos garantir dois no mesmo mes de aniversario?",
        "opcoes": [
            "Nao, existem 13 meses",
            "Sim, existem 12 meses",
            "Apenas se forem gemeos",
            "Nunca podemos garantir"
        ],
        "correta": 1,
        "explicacao": "13 alunos e 12 meses garantem pelo menos 2 no mesmo mes."
    },
    {
        "pergunta": "Um restaurante oferece 2 entradas.",
        "complemento": "Ou 5 pratos principais. Quantas opcoes ha?",
        "opcoes": [
            "10 opcoes", "3 opcoes",
            "7 opcoes", "5 opcoes"
        ],
        "correta": 2,
        "explicacao": "Principio aditivo: 2 + 5 = 7 opcoes."
    },
    {
        "pergunta": "Uma senha tem 2 digitos.",
        "complemento": "Cada digito vai de 0 a 9, com repeticao. Quantas senhas?",
        "opcoes": [
            "20 senhas", "100 senhas",
            "10 senhas", "90 senhas"
        ],
        "correta": 1,
        "explicacao": "Principio multiplicativo: 10 x 10 = 100 senhas."
    },
    {
        "pergunta": "Ha 8 bolas e 3 caixas.",
        "complemento": "Qual a menor quantidade garantida em alguma caixa?",
        "opcoes": [
            "Pelo menos 2 bolas",
            "Pelo menos 3 bolas",
            "Pelo menos 4 bolas",
            "Pelo menos 8 bolas"
        ],
        "correta": 1,
        "explicacao": "8 bolas em 3 caixas garantem pelo menos 3 em alguma caixa."
    }
]

# ==================================================
# ESTADO DO JOGO
# ==================================================
tela_atual = "menu"
nome_jogador = ""
digitando_nome = False

indice = 0
pontos = 0
respondida = False
escolhida = -1
partida_salva = False

# ==================================================
# RANKING PERSISTENTE
# ==================================================
def carregar_ranking():
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return []


ranking = carregar_ranking()


def salvar_ranking():
    try:
        with open(ARQUIVO_RANKING, "w", encoding="utf-8") as arquivo:
            json.dump(ranking, arquivo, ensure_ascii=False, indent=4)
    except OSError:
        print("Nao foi possivel salvar o ranking.")


# ==================================================
# BOTOES E CAMPOS
# ==================================================
campo_nome = pygame.Rect(250, 245, 400, 48)

botao_iniciar = pygame.Rect(300, 315, 300, 53)
botao_ranking = pygame.Rect(300, 382, 300, 53)
botao_sair = pygame.Rect(300, 449, 300, 53)

botoes = [
    pygame.Rect(85, 282, 730, 48),
    pygame.Rect(85, 340, 730, 48),
    pygame.Rect(85, 398, 730, 48),
    pygame.Rect(85, 456, 730, 48)
]

botao_proximo = pygame.Rect(575, 555, 240, 42)
botao_reiniciar = pygame.Rect(300, 438, 300, 48)
botao_menu = pygame.Rect(300, 498, 300, 45)
botao_voltar = pygame.Rect(300, 535, 300, 42)

# ==================================================
# PARTICULAS ANIMADAS
# ==================================================
particulas = []

for _ in range(55):
    particulas.append({
        "x": random.randint(0, LARGURA),
        "y": random.randint(0, ALTURA),
        "vel": random.uniform(0.15, 0.65),
        "raio": random.choice([1, 1, 2]),
        "fase": random.uniform(0, 6.28)
    })


def desenhar_particulas():
    tempo = pygame.time.get_ticks() / 1000

    for p in particulas:
        p["y"] -= p["vel"]

        if p["y"] < -5:
            p["y"] = ALTURA + 5
            p["x"] = random.randint(0, LARGURA)

        brilho = int(100 + 100 * (0.5 + 0.5 *
                     math.sin(tempo * 2 + p["fase"])))

        cor = (min(brilho, 180), 100, min(brilho + 40, 220))

        pygame.draw.circle(
            tela, cor,
            (int(p["x"]), int(p["y"])),
            p["raio"]
        )


# ==================================================
# FUNCOES DE DESENHO
# ==================================================
def texto(msg, fonte, cor, x, y, centralizar=False):
    imagem = fonte.render(str(msg), True, cor)
    ret = imagem.get_rect()

    if centralizar:
        ret.center = (x, y)
    else:
        ret.topleft = (x, y)

    tela.blit(imagem, ret)


def texto_quebrado(msg, fonte, cor, x, y, largura, limite_y):
    linha = ""
    altura_linha = fonte.get_linesize()

    for palavra in msg.split():
        teste = (linha + " " + palavra).strip()

        if fonte.size(teste)[0] <= largura:
            linha = teste
        else:
            if y + altura_linha > limite_y:
                return

            texto(linha, fonte, cor, x, y)
            y += altura_linha
            linha = palavra

    if linha and y + altura_linha <= limite_y:
        texto(linha, fonte, cor, x, y)


def cartao(rect, cor, raio=15, borda=None):
    pygame.draw.rect(tela, cor, rect, border_radius=raio)

    if borda:
        pygame.draw.rect(
            tela, borda, rect,
            width=1, border_radius=raio
        )


def desenhar_fundo():
    tela.fill(FUNDO)
    desenhar_particulas()

    # Formas decorativas
    pygame.draw.circle(tela, (23, 30, 66), (0, 0), 145)
    pygame.draw.circle(tela, (23, 30, 66), (900, 650), 160)

    pygame.draw.circle(tela, ROXO, (40, 130), 3)
    pygame.draw.circle(tela, CIANO, (850, 170), 3)
    pygame.draw.circle(tela, ROXO, (830, 550), 3)


def desenhar_cabecalho():
    texto("DESAFIO DA", fonte_pequena, CIANO, 450, 17, True)
    texto("MATEMATICA DISCRETA", fonte_titulo, BRANCO, 450, 49, True)

    pygame.draw.line(tela, ROXO, (275, 83), (625, 83), 2)


def desenhar_botao(rect, rotulo, cor=ROXO, ativo=True):
    mouse = pygame.mouse.get_pos()
    cor_final = cor

    if ativo and rect.collidepoint(mouse):
        cor_final = ROXO_CLARO if cor == ROXO else tuple(
            min(c + 22, 255) for c in cor
        )

    cartao(rect, cor_final, 13)

    # Pequeno detalhe decorativo
    pygame.draw.circle(
        tela, (255, 255, 255),
        (rect.x + 18, rect.centery), 3
    )

    texto(
        rotulo, fonte_normal, BRANCO,
        rect.centerx, rect.centery, True
    )


def desenhar_etiqueta(rotulo, x, y, cor=CIANO):
    imagem = fonte_mini.render(rotulo, True, cor)
    ret = imagem.get_rect(center=(x, y))
    fundo = ret.inflate(20, 12)
    cartao(fundo, PAINEL_CLARO, 8, cor)
    tela.blit(imagem, ret)


# ==================================================
# MENU PRINCIPAL
# ==================================================
def desenhar_menu():
    desenhar_fundo()
    desenhar_cabecalho()

    cartao(
        pygame.Rect(175, 100, 550, 470),
        PAINEL, 25, (62, 72, 125)
    )

    # Logo feita com formas geometricas
    pygame.draw.circle(tela, ROXO, (450, 137), 23, 3)
    pygame.draw.circle(tela, CIANO, (450, 137), 10, 2)
    pygame.draw.line(tela, CIANO, (435, 137), (465, 137), 2)
    pygame.draw.line(tela, CIANO, (450, 122), (450, 152), 2)

    texto("BEM-VINDO!", fonte_logo, BRANCO, 450, 184, True)
    texto("APRENDA JOGANDO", fonte_pequena, CIANO, 450, 216, True)

    texto("NOME DO JOGADOR", fonte_pequena, CINZA, 250, 225)

    cor_campo = ROXO if digitando_nome else PAINEL_CLARO
    cartao(campo_nome, cor_campo, 12)

    exibido = nome_jogador if nome_jogador else "Digite seu nome..."
    cor_texto = BRANCO if nome_jogador else CINZA

    texto(exibido, fonte_normal, cor_texto,
          campo_nome.x + 15, campo_nome.y + 13)

    desenhar_botao(botao_iniciar, "▶   INICIAR DESAFIO", ROXO)
    desenhar_botao(botao_ranking, "★   RANKING", PAINEL_CLARO)
    desenhar_botao(botao_sair, "SAIR DO JOGO", (105, 43, 70))

    desenhar_etiqueta("8 PERGUNTAS", 275, 540, CIANO)
    desenhar_etiqueta("LOGICA", 450, 540, ROXO_CLARO)
    desenhar_etiqueta("MATEMATICA", 625, 540, VERDE)

    texto("Clique no campo para digitar seu nome",
          fonte_mini, CINZA, 450, 590, True)


# ==================================================
# BARRA DE PROGRESSO
# ==================================================
def desenhar_progresso():
    total = len(perguntas)
    x, y, largura = 210, 111, 480

    cartao(pygame.Rect(x, y, largura, 9), PAINEL_CLARO, 8)

    preenchimento = int(largura * (indice + 1) / total)

    cartao(
        pygame.Rect(x, y, preenchimento, 9),
        CIANO, 8
    )

    for i in range(total):
        px = x + int(largura * i / (total - 1))
        pygame.draw.circle(
            tela,
            VERDE if i < indice else (CIANO if i == indice else CINZA),
            (px, y + 4), 3
        )


# ==================================================
# TELA DO QUIZ
# ==================================================
def desenhar_quiz():
    desenhar_fundo()
    desenhar_cabecalho()

    q = perguntas[indice]

    cartao(
        pygame.Rect(45, 100, 810, 500),
        PAINEL, 22, (58, 68, 115)
    )

    desenhar_progresso()

    texto(
        f"PERGUNTA {indice + 1:02d} / {len(perguntas):02d}",
        fonte_pequena, CIANO, 70, 132
    )

    cartao(pygame.Rect(690, 126, 135, 34), PAINEL_CLARO, 10)
    texto(f"★ {pontos} pontos", fonte_pequena,
          AMARELO, 757, 143, True)

    texto_quebrado(
        q["pergunta"], fonte_subtitulo, BRANCO,
        70, 177, 750, 218
    )

    texto_quebrado(
        q["complemento"], fonte_normal, CINZA,
        70, 218, 750, 265
    )

    for i, botao in enumerate(botoes):
        cor = PAINEL_CLARO
        borda = None

        if respondida:
            if i == q["correta"]:
                cor = (27, 100, 79)
                borda = VERDE
            elif i == escolhida:
                cor = (105, 37, 57)
                borda = VERMELHO
        elif botao.collidepoint(pygame.mouse.get_pos()):
            cor = (65, 52, 120)
            borda = ROXO_CLARO

        cartao(botao, cor, 12, borda)

        circulo = (botao.x + 28, botao.centery)
        pygame.draw.circle(tela, ROXO, circulo, 15)

        texto(
            chr(65 + i), fonte_pequena, BRANCO,
            circulo[0], circulo[1], True
        )

        texto_quebrado(
            q["opcoes"][i], fonte_pequena, BRANCO,
            botao.x + 55, botao.y + 14, 650, botao.bottom - 2
        )

    if respondida:
        if escolhida == q["correta"]:
            texto("✓ RESPOSTA CORRETA!", fonte_pequena,
                  VERDE, 70, 516)
        else:
            texto("✗ RESPOSTA INCORRETA", fonte_pequena,
                  VERMELHO, 70, 516)

        texto_quebrado(
            q["explicacao"], fonte_mini, AMARELO,
            70, 538, 475, 582
        )

        rotulo = (
            "VER RESULTADO  →"
            if indice == len(perguntas) - 1
            else "PROXIMA  →"
        )

        desenhar_botao(botao_proximo, rotulo, ROXO)
    else:
        texto("ESCOLHA UMA ALTERNATIVA",
              fonte_mini, CINZA, 70, 555)


# ==================================================
# RESULTADO FINAL
# ==================================================
def desenhar_resultado():
    desenhar_fundo()
    desenhar_cabecalho()

    cartao(
        pygame.Rect(150, 105, 600, 480),
        PAINEL, 25, (70, 83, 135)
    )

    texto("DESAFIO CONCLUIDO!", fonte_titulo,
          CIANO, 450, 145, True)

    pygame.draw.circle(tela, AMARELO, (450, 205), 29, 3)
    texto("★", fonte_grande, AMARELO, 450, 205, True)

    texto(nome_jogador or "Jogador",
          fonte_normal, BRANCO, 450, 250, True)

    texto(f"{pontos} / {len(perguntas)}",
          fonte_grande, AMARELO, 450, 305, True)

    porcentagem = int(pontos / len(perguntas) * 100)

    texto(f"{porcentagem}% DE ACERTOS",
          fonte_pequena, CIANO, 450, 345, True)

    cartao(pygame.Rect(250, 367, 400, 13), PAINEL_CLARO, 7)

    if porcentagem:
        cartao(
            pygame.Rect(250, 367, int(400 * porcentagem / 100), 13),
            VERDE, 7
        )

    if pontos == 8:
        mensagem = "INCRIVEL! VOCE E UM MESTRE!"
    elif pontos >= 6:
        mensagem = "MUITO BEM! CONTINUE ASSIM!"
    elif pontos >= 4:
        mensagem = "BOM TRABALHO! SIGA PRATICANDO!"
    else:
        mensagem = "NAO DESISTA! TENTE NOVAMENTE!"

    texto(mensagem, fonte_pequena, BRANCO, 450, 405, True)

    desenhar_botao(botao_reiniciar, "↻   JOGAR NOVAMENTE", VERDE)
    desenhar_botao(botao_menu, "VOLTAR AO MENU", PAINEL_CLARO)


# ==================================================
# RANKING
# ==================================================
def desenhar_ranking():
    desenhar_fundo()
    desenhar_cabecalho()

    cartao(
        pygame.Rect(115, 105, 670, 480),
        PAINEL, 23, (62, 72, 125)
    )

    texto("HALL DA FAMA", fonte_titulo,
          AMARELO, 450, 145, True)

    texto("POS.", fonte_mini, CINZA, 205, 194)
    texto("JOGADOR", fonte_mini, CINZA, 300, 194)
    texto("PONTOS", fonte_mini, CINZA, 570, 194)
    texto("ACERTOS", fonte_mini, CINZA, 680, 194)

    melhores = sorted(
        ranking,
        key=lambda j: j.get("pontos", 0),
        reverse=True
    )

    if not melhores:
        texto("Ainda nao ha jogadores no ranking.",
              fonte_normal, BRANCO, 450, 330, True)
        texto("Complete o desafio para registrar sua pontuacao!",
              fonte_pequena, CINZA, 450, 365, True)
    else:
        for i, jogador in enumerate(melhores[:8]):
            y = 220 + i * 34

            if i % 2 == 0:
                cartao(
                    pygame.Rect(180, y - 5, 540, 30),
                    PAINEL_CLARO, 7
                )

            if i == 0:
                cor_pos = AMARELO
                medalha = "1"
            elif i == 1:
                cor_pos = (210, 220, 235)
                medalha = "2"
            elif i == 2:
                cor_pos = (220, 155, 105)
                medalha = "3"
            else:
                cor_pos = CINZA
                medalha = str(i + 1)

            texto(medalha, fonte_normal, cor_pos, 207, y)

            nome = str(jogador.get("nome", "Jogador"))
            if len(nome) > 19:
                nome = nome[:16] + "..."

            texto(nome, fonte_pequena, BRANCO, 300, y)

            valor = jogador.get("pontos", 0)
            texto(f"{valor}/8", fonte_pequena, CIANO, 590, y)

            acertos = int(valor / len(perguntas) * 100)
            texto(f"{acertos}%", fonte_pequena, VERDE, 690, y)

    desenhar_botao(botao_voltar, "←  VOLTAR AO MENU", ROXO)


# ==================================================
# CONTROLE DAS TELAS
# ==================================================
def iniciar_quiz():
    global indice, pontos, respondida
    global escolhida, tela_atual, partida_salva

    indice = 0
    pontos = 0
    respondida = False
    escolhida = -1
    partida_salva = False
    tela_atual = "quiz"


def voltar_menu():
    global tela_atual, digitando_nome
    tela_atual = "menu"
    digitando_nome = False


def finalizar_partida():
    global tela_atual, partida_salva

    if not partida_salva:
        ranking.append({
            "nome": nome_jogador or "Jogador",
            "pontos": pontos
        })

        ranking.sort(
            key=lambda jogador: jogador.get("pontos", 0),
            reverse=True
        )

        # Mantem os 100 melhores resultados
        del ranking[100:]

        salvar_ranking()
        partida_salva = True

    tela_atual = "resultado"


# ==================================================
# LOOP PRINCIPAL
# ==================================================
executando = True

while executando:
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:

            if tela_atual == "menu" and digitando_nome:
                if evento.key == pygame.K_RETURN:
                    digitando_nome = False

                elif evento.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]

                elif evento.key == pygame.K_ESCAPE:
                    digitando_nome = False

                elif evento.unicode.isprintable():
                    if len(nome_jogador) < 22:
                        nome_jogador += evento.unicode

            elif evento.key == pygame.K_ESCAPE:
                if tela_atual == "menu":
                    executando = False
                else:
                    voltar_menu()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            # MENU
            if tela_atual == "menu":
                if campo_nome.collidepoint(pos):
                    digitando_nome = True

                elif botao_iniciar.collidepoint(pos):
                    digitando_nome = False

                    if not nome_jogador.strip():
                        nome_jogador = "Jogador"

                    iniciar_quiz()

                elif botao_ranking.collidepoint(pos):
                    digitando_nome = False
                    tela_atual = "ranking"

                elif botao_sair.collidepoint(pos):
                    executando = False

            # QUIZ
            elif tela_atual == "quiz":
                if not respondida:
                    for i, botao in enumerate(botoes):
                        if botao.collidepoint(pos):
                            escolhida = i
                            respondida = True

                            if escolhida == perguntas[indice]["correta"]:
                                pontos += 1
                            break

                elif botao_proximo.collidepoint(pos):
                    if indice < len(perguntas) - 1:
                        indice += 1
                        respondida = False
                        escolhida = -1
                    else:
                        finalizar_partida()

            # RESULTADO
            elif tela_atual == "resultado":
                if botao_reiniciar.collidepoint(pos):
                    iniciar_quiz()

                elif botao_menu.collidepoint(pos):
                    voltar_menu()

            # RANKING
            elif tela_atual == "ranking":
                if botao_voltar.collidepoint(pos):
                    voltar_menu()

    # DESENHO DA TELA
    if tela_atual == "menu":
        desenhar_menu()

    elif tela_atual == "quiz":
        desenhar_quiz()

    elif tela_atual == "resultado":
        desenhar_resultado()

    elif tela_atual == "ranking":
        desenhar_ranking()

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()
