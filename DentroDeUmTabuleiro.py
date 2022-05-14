from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

pi = 3.14159265
largura: int
altura: int
pos: int


class Ponto():
    ident: int
    x: float
    y: float


class Casa(Ponto):
    # ident: int
    #x: float
    #y: float
    # vou usar essa variável preenchida para auxiliar quando já tiver um objeto na casa
    preenchida: bool

    def __init__(self):
        self.preenchida = False


MatPontoMedio: Casa() = []
objetoSelecionado: Ponto() = Ponto()


def calcula_PM():
    # aqui eu calculo todos os pontos médios a medida que vai criando a casa do tabuleiro
    contador = 0
    for x in range(8):
        for y in range(8):
            pontoMedio = Casa()
            pontoMedio.ident = contador
            pontoMedio.x = (x+(x+1))/2
            pontoMedio.y = (y+(y+1))/2
            MatPontoMedio.append(pontoMedio)
            contador = contador + 1


def inicio():
    global pos
    glClearColor(0.5, 0.5, 0.5, 1.0)
    calcula_PM()
    pos = random.randint(0, 63)
    objetoSelecionado.ident = 63
    objetoSelecionado.x = 7.5  # MatPontoMedio[pos]
    objetoSelecionado.y = 7.5
    MatPontoMedio[63].preenchida = True
    # MatPontoMedio[pos].preenchida = True


def resize(w: int, h: int):
    global largura, altura
    largura = w
    altura = h
    glutPostRedisplay()


def tecladoSpecial(key: int, x: int, y: int):

    global objetoSelecionado
    # //os códigos das teclas especiais sÃ£o valores inteiros
    # aqui eu verifico se o objeto selecionado tem um objeto preenchendo a casa do tabuleiro
    if MatPontoMedio[objetoSelecionado.ident].preenchida == True:
        if key == GLUT_KEY_LEFT:
            # verifico se o objeto selecionado ainda está em uma posição maior que a borda esquerda
            if objetoSelecionado.x - 1 > 0:
                # a casa esquerda é criada para fazer a troca de casa do objeto
                casa_esquerda = objetoSelecionado.ident - 8
                # verifica se essa casa não tem algum outro objeto
                if MatPontoMedio[casa_esquerda].preenchida == False:
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    # objetoSelecionado = MatPontoMedio[casa_esquerda]
                    objetoSelecionado.ident = MatPontoMedio[casa_esquerda].ident
                    objetoSelecionado.x = MatPontoMedio[casa_esquerda].x
                    objetoSelecionado.y = MatPontoMedio[casa_esquerda].y
                    # objetoSelecionado = MatPontoMedio[casa_esquerda].ident, MatPontoMedio[
                    #     casa_esquerda].x, MatPontoMedio[casa_esquerda].y
                    # objetoSelecionado.preenchida = True
                    # objetoSelecionado.ident = casa_esquerda
                    # objetoSelecionado.x = objetoSelecionado.x - 1
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        # //caso a seta esquerda seja pressionada, a coordenada x do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra esquerda
        elif key == GLUT_KEY_RIGHT:
            if objetoSelecionado.x + 1 < 8:
                casa_direita = objetoSelecionado.ident + 8
                if MatPontoMedio[casa_direita].preenchida == False:
                    # objetoSelecionado.preenchida = False
                    # objetoSelecionado.ident = casa_direita
                    # objetoSelecionado.x = objetoSelecionado.x + 1
                    # objetoSelecionado.preenchida = True
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    # objetoSelecionado = MatPontoMedio[casa_direita]
                    objetoSelecionado.ident = MatPontoMedio[casa_direita].ident
                    objetoSelecionado.x = MatPontoMedio[casa_direita].x
                    objetoSelecionado.y = MatPontoMedio[casa_direita].y
                    # objetoSelecionado.preenchida = True
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        # //caso a seta direita seja pressionada, a coordenada x do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra direita
        elif key == GLUT_KEY_DOWN:
            if objetoSelecionado.y - 1 > 0:
                casa_baixo = objetoSelecionado.ident - 1
                if MatPontoMedio[casa_baixo].preenchida == False:
                    # objetoSelecionado.preenchida = False
                    # objetoSelecionado.ident = casa_baixo
                    # objetoSelecionado.y = objetoSelecionado.y - 1
                    # objetoSelecionado.preenchida = True
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    # objetoSelecionado = MatPontoMedio[casa_baixo]
                    objetoSelecionado.ident = MatPontoMedio[casa_baixo].ident
                    objetoSelecionado.x = MatPontoMedio[casa_baixo].x
                    objetoSelecionado.y = MatPontoMedio[casa_baixo].y
                    # objetoSelecionado.preenchida = True
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        # //caso a seta pra baixo seja pressionada, a coordenada y do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra baixo
        elif key == GLUT_KEY_UP:
            # //caso a seta pra cima seja pressionada, a coordenada y do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra cima
            if objetoSelecionado.y + 1 < 8:
                casa_cima = objetoSelecionado.ident + 1
                if MatPontoMedio[casa_cima].preenchida == False:
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_cima].ident
                    objetoSelecionado.x = MatPontoMedio[casa_cima].x
                    objetoSelecionado.y = MatPontoMedio[casa_cima].y
                    # objetoSelecionado.preenchida = True
                    # objetoSelecionado.ident = casa_cima
                    # objetoSelecionado.y = objetoSelecionado.y + 1
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
    else:
        print("Nenhum objeto selecionado")
    # //InstruÃ§Ã£o que indica pra GLUT que o frame buffer deve ser atualizado
    glutPostRedisplay()


def Tabuleiro():
    global MatPontoMedio
    for i in range(8):
        for j in range(8):
            if(i+j) % 2 == 0:
                glColor3f(0, 0, 0)
            else:
                glColor3f(1, 1, 1)
            x = i
            y = j
            glVertex2f(x, y)
            glVertex2f(x+1, y)
            glVertex2f(x+1, y+1)
            glVertex2f(x, y+1)


def camera():
    N = 50
    R = 0.2
    CentroX = CentroY = 0
    # MatPontoMedio[63].preenchida = True
    glTranslatef(MatPontoMedio[63].x, MatPontoMedio[63].y, 0)
    glColor(0.7, 0.7, 0.7)
    glBegin(GL_POLYGON)

    for i in range(N):
        angulo = (i*2*pi)/N
        glVertex2f(CentroX+(math.cos(angulo)*R), CentroY+(math.sin(angulo)*R))

    glEnd()
    glFlush()


def circulo():
    MatPontoMedio[55].preenchida = True
    glTranslatef(MatPontoMedio[55].x, MatPontoMedio[55].y, 0)
    N = 25
    R = 0.3
    CentroX = CentroY = 0
    glBegin(GL_POLYGON)

    for i in range(N):
        angulo = (i*2*pi)/N
        glVertex2f(CentroX+(math.cos(angulo)*R), CentroY+(math.sin(angulo)*R))

    glEnd()
    glFlush()


def quadrado(pos: int):
    # glPushMatrix()
    # MatPontoMedio[pos].preenchida = True
    glTranslatef(MatPontoMedio[pos].x, MatPontoMedio[pos].y, 0)
    glBegin(GL_QUAD_STRIP)

    glColor3f(1, 0, 0.5)
    glVertex2f(-0.25, -0.25)
    glVertex2f(0.25, -0.25)
    glVertex2f(-0.25, 0.25)
    glVertex2f(0.25, 0.25)
    glEnd()
    # glPopMatrix()

    glFlush()


def desenha():
    global objetoSelecionado
    # glViewport(0, 0, 1366, 697)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #h = 16.0 * float(altura) / float(largura)
    glViewport(0, 0, largura, altura)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glOrtho(0, 8, 0, 8, -1, 1)

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    Tabuleiro()
    glEnd()

    glFlush()

    glPushMatrix()
    camera()
    glPopMatrix()

    # quadrado
    glPushMatrix()

    # print(posicao.x, posicao.y)
    # glTranslatef(0.5, 0.5, 0)
    glColor3f(1, 0, 0.5)
    quadrado(pos)
    glPopMatrix()
    # objetoSelecionado = 63, 6.5, 7.5
    # objetoSelecionado.ident = 63
    # objetoSelecionado.x = 7.5  # MatPontoMedio[pos]
    # objetoSelecionado.y = 7.5
    # objetoSelecionado.preenchida = True
    # glPushMatrix()
    # glTranslatef(6.5, 7.5, 0)
    glColor3f(0, 0.7, 0)
    circulo()
    # glPopMatrix()
    glFlush()

    # glColor3f(1, 1, 0)
    # quadrado()
    # glFlush()
    i = 0
    while i < len(MatPontoMedio):
        print(MatPontoMedio[i].ident, MatPontoMedio[i].x, MatPontoMedio[i].y,
              MatPontoMedio[i].preenchida)
        i = i+1
    print(objetoSelecionado.ident, objetoSelecionado.x, objetoSelecionado.y)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowPosition(500, 200)
glutCreateWindow(b'Dentro de um tabuleiro')
glutInitWindowSize(400, 400)
inicio()
glutDisplayFunc(desenha)
glutSpecialFunc(tecladoSpecial)
glutReshapeFunc(resize)
glutMainLoop()
