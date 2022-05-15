from glob import glob
from tkinter import ON
from turtle import onclick
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random
import keyboard
# from PyGLM import glm

pi = 3.14159265
largura: int
altura: int
pos: int


class Ponto():
    ident: int
    x: float
    y: float

# a classe casa herda os atributos da classe ponto


class Objeto(Ponto):
    tipo: str


class Casa(Ponto):
    # vou usar essa variável preenchida para auxiliar quando já tiver um objeto na casa
    preenchida: bool

    def __init__(self):
        self.preenchida = False


MatPontoMedio: Casa() = []
listaObjetosDoTabuleiro: Objeto() = []
objetoSelecionado: Objeto() = Objeto()
camera: Objeto() = Objeto()
quadrado: Objeto() = Objeto()
circulo: Objeto() = Objeto()


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
    global pos, objetoSelecionado
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glPointSize(10)
    calcula_PM()
    # objeto não cair em cima da camera
    pos = random.randint(0, 63)
    pos2 = random.randint(0, 63)
    camera.ident = MatPontoMedio[63].ident
    camera.x = MatPontoMedio[63].x
    camera.y = MatPontoMedio[63].y
    camera.tipo = "Camera"
    listaObjetosDoTabuleiro.append(camera)
    quadrado.ident = MatPontoMedio[pos].ident  # 63
    quadrado.x = MatPontoMedio[pos].x
    quadrado.y = MatPontoMedio[pos].y
    quadrado.tipo = "Quadrado"
    listaObjetosDoTabuleiro.append(quadrado)
    circulo.ident = MatPontoMedio[pos2].ident
    circulo.x = MatPontoMedio[pos2].x
    circulo.y = MatPontoMedio[pos2].y
    circulo.tipo = "Circulo"
    listaObjetosDoTabuleiro.append(circulo)
    objetoSelecionado = camera
    # objetoSelecionado.tipo = input("Digite qual objeto deseja se basear:")
    # if objetoSelecionado.tipo == "C":
    #     objetoSelecionado = camera
    # # //caso a tecla R seja pressionada, a componente vermelha Ã© ligada e as demais desligadas.
    # elif objetoSelecionado.tipo == "c":
    #     objetoSelecionado = circulo
    # elif objetoSelecionado.tipo == "q":
    #     objetoSelecionado = quadrado
    MatPontoMedio[63].preenchida = True
    MatPontoMedio[pos].preenchida = True
    MatPontoMedio[pos2].preenchida = True


def resize(w: int, h: int):
    global largura, altura
    largura = w
    altura = h
    print(largura, altura)
    glutPostRedisplay()


def tecladoSpecial(key: int, x: int, y: int):

    global objetoSelecionado
    # //os códigos das teclas especiais são valores inteiros
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

                    objetoSelecionado.ident = MatPontoMedio[casa_esquerda].ident
                    objetoSelecionado.x = MatPontoMedio[casa_esquerda].x
                    objetoSelecionado.y = MatPontoMedio[casa_esquerda].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        # //caso a seta esquerda seja pressionada, a coordenada x do ponto inferior esquerdo será reduzida, deslocando o quadrado pra esquerda
        elif key == GLUT_KEY_RIGHT:
            if objetoSelecionado.x + 1 < 8:
                casa_direita = objetoSelecionado.ident + 8
                if MatPontoMedio[casa_direita].preenchida == False:
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_direita].ident
                    objetoSelecionado.x = MatPontoMedio[casa_direita].x
                    objetoSelecionado.y = MatPontoMedio[casa_direita].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        # //caso a seta direita seja pressionada, a coordenada x do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra direita
        elif key == GLUT_KEY_DOWN:
            if objetoSelecionado.y - 1 > 0:
                casa_baixo = objetoSelecionado.ident - 1
                if MatPontoMedio[casa_baixo].preenchida == False:
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_baixo].ident
                    objetoSelecionado.x = MatPontoMedio[casa_baixo].x
                    objetoSelecionado.y = MatPontoMedio[casa_baixo].y
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
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
    else:
        print("Nenhum objeto selecionado")
    # //Instrução que indica pra GLUT que o frame buffer deve ser atualizado
    glutPostRedisplay()


def tecladoASCII(key: str, x: int, y: int):
    global objetoSelecionado
    """O is_pressed() recebe um caractere como entrada e, se corresponder à tecla que o usuário pressionou, retornará True e False caso contrário."""
    if keyboard.is_pressed("x"):
        objetoSelecionado = camera
    # //caso a tecla R seja pressionada, a componente vermelha Ã© ligada e as demais desligadas.
    elif keyboard.is_pressed("c"):
        objetoSelecionado = circulo
    elif keyboard.is_pressed("q"):
        objetoSelecionado = quadrado

    # //InstruÃ§Ã£o que indica pra GLUT que o frame buffer deve ser atualizado
    glutPostRedisplay()


def mouseClique(button: int, state: int, x: int, y: int):
    # ta errado aqui pois preciso pegar as coordenadas certinhas do ponto selecionado
    # concertar para ter as medidas da casa em pixel ou saber os pixels de cada ponto medio
    global objetoSelecionado
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    selecao = Objeto()
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        selecao.x = x
        selecao.y = altura - y
        if altura <= 300 and largura <= 300:
            selecao.x = int(selecao.x/37.5)+0.5
            selecao.y = int(selecao.y/37.5)+0.5
            # aplicar escala 1366/300 para x
            # aplicar escala 697/300 para y
        else:
            selecao.x = int(selecao.x/170.75)+0.5
            selecao.y = int(selecao.y/87.125)+0.5
        print("\n", selecao.x, selecao.y, "\n")
        for i in range(8*8):
            if MatPontoMedio[i].x == selecao.x and MatPontoMedio[i].y == selecao.y:
                selecao.ident = MatPontoMedio[i].ident
                print(selecao.ident)
                j = 0
                while j < len(listaObjetosDoTabuleiro):
                    if listaObjetosDoTabuleiro[j].x == selecao.x and listaObjetosDoTabuleiro[j].y == selecao.y:
                        selecao.tipo = listaObjetosDoTabuleiro[j].tipo
                        print(selecao.tipo)
                    j = j+1
                if MatPontoMedio[i].preenchida == True:
                    objetoSelecionado = selecao
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
    global objetoSelecionado
    N = 50
    R = 0.2
    CentroX = CentroY = 0
    if objetoSelecionado.tipo == "Camera":
        glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
        # atualizo as coordenadas da camera na lista de objetos
        camera.ident = objetoSelecionado.ident
        camera.x = objetoSelecionado.x
        camera.y = objetoSelecionado.y
    else:
        glTranslatef(camera.x, camera.y, 0)
    # glTranslatef(MatPontoMedio[63].x, MatPontoMedio[63].y, 0)
    glColor(0.7, 0.7, 0.7)
    glBegin(GL_POLYGON)

    for i in range(N):
        angulo = (i*2*pi)/N
        glVertex2f(CentroX+(math.cos(angulo)*R), CentroY+(math.sin(angulo)*R))

    glEnd()
    glFlush()


def circulo():
    # MatPontoMedio[55].preenchida = True
    # glTranslatef(circulo.x, circulo.y, 0)
    if objetoSelecionado.tipo == "Circulo":
        glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
        # atualizo as coordenadas da camera na lista de objetos
        circulo.ident = objetoSelecionado.ident
        circulo.x = objetoSelecionado.x
        circulo.y = objetoSelecionado.y
    else:
        glTranslatef(circulo.x, circulo.y, 0)
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
    global objetoSelecionado
    # glPushMatrix()
    # MatPontoMedio[pos].preenchida = True
    if(objetoSelecionado.tipo == "Quadrado"):
        glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
        quadrado.ident = objetoSelecionado.ident
        quadrado.x = objetoSelecionado.x
        quadrado.y = objetoSelecionado.y
    else:
        glTranslatef(quadrado.x, quadrado.y, 0)
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

    glPushMatrix()
    # glTranslatef(circulo.x, circulo.y, 0)
    # glTranslatef(6.5, 7.5, 0)
    glColor3f(0, 0.7, 0)
    circulo()
    glPopMatrix()
    glFlush()

    # glColor3f(1, 1, 0)
    # quadrado()
    # glFlush()
    # i = 0
    # while i < len(MatPontoMedio):
    #     # print(MatPontoMedio[i].ident, MatPontoMedio[i].x, MatPontoMedio[i].y, MatPontoMedio[i].preenchida)
    #     # to desenhando só para ter noção de onde estão os pontos medios
    #     glColor3f(1, 0, 0)
    #     glBegin(GL_POINTS)
    #     glVertex2f(MatPontoMedio[i].x, MatPontoMedio[i].y)
    #     glEnd()
    #     glFlush()
    #     i = i+1
    print(objetoSelecionado.ident, objetoSelecionado.x,
          objetoSelecionado.y, objetoSelecionado.tipo)
    # aqui já percebo que meus objetos se atualizam dentro dessa lista de objetos
    print(listaObjetosDoTabuleiro[0].ident,
          listaObjetosDoTabuleiro[0].x, listaObjetosDoTabuleiro[0].y)
    print(listaObjetosDoTabuleiro[1].ident,
          listaObjetosDoTabuleiro[1].x, listaObjetosDoTabuleiro[1].y)
    print(listaObjetosDoTabuleiro[2].ident,
          listaObjetosDoTabuleiro[2].x, listaObjetosDoTabuleiro[2].y)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowPosition(500, 200)
glutCreateWindow(b'Dentro de um tabuleiro')
glutInitWindowSize(300, 300)
inicio()
glutDisplayFunc(desenha)
glutKeyboardFunc(tecladoASCII)
glutSpecialFunc(tecladoSpecial)
glutMouseFunc(mouseClique)
glutReshapeFunc(resize)
glutMainLoop()
