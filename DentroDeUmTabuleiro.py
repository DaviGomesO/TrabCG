"""
Aluno: Francisco Davi Gomes de Oliveira
Matricula: 475548
"""
from lib2to3.pgen2.token import COLONEQUAL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# importo a math para fazer o calculo do cosseno e desenhar o circulo
import math
# importo a random para obter posições aleatórias ao adicionar um objeto
import random
# e importo a keyboard para obter as entradas do teclado ASCII, de forma que vai esperar uma tecla ser pressionada
import keyboard
# from PyGLM import glm

# defino o valor de pi, pois estava dando problema ao importar a M_PI
pi = 3.14159265

# defino essas variaveis para ter o tamanho da tela quando aumento e quando diminuo
largura: int
altura: int


class Ponto():
    ident: int
    x: float
    y: float

# as classes Objeto e Casa herdam os atributos da classe ponto


class Objeto(Ponto):
    # só para indicar quais tipos de objetos são
    tipo: str


class Casa(Ponto):
    # vou usar essa variável preenchida para auxiliar quando já tiver um objeto na casa
    # a principio todas inicializam vazias(False)
    preenchida: bool

    def __init__(self):
        self.preenchida = False


""" Essa lista de pontos medios vai receber mais na frente as coordenadas de pontos medios de cada casa do tabuleiro, as casas serão identificadas com valores que irão de 0 a 63, ou seja, 64(8x8) casas do tabuleiro, onde nessa lista será manipulada ao preencher as casas, seja com criação ou movimentação de objeto """
MatPontoMedio: Casa() = []

"""crio essa lista para conter todos os objetos que estarão dispostos no tabuleiro"""
listaObjetosDoTabuleiro: Objeto() = []

"""essa variavel vai servir como copia para o objeto que está sendo selecionado para movimentar, onde o objeto servirá para atualização da posição do objeto"""
objetoSelecionado: Objeto() = Objeto()

"""uma variavel especifica para ter os valores da câmera, já que teremos apenas uma câmera na cena"""
camera: Objeto() = Objeto()

# quadrado: Objeto() = Objeto()
"""uma lista para guardar todos os objetos do tipo quadrado"""
listaQuadrados: Objeto() = []

# circulo: Objeto() = Objeto()
"""uma lista para guardar todos os objetos do tipo quadrado"""
listaCirculos: Objeto() = []

listaTriangulos: Objeto() = []


def calcula_PM():
    # aqui eu calculo todos os pontos médios a medida que vai criando a casa do tabuleiro
    contador = 0
    for x in range(8):
        for y in range(8):
            pontoMedio = Casa()
            pontoMedio.ident = contador
            pontoMedio.x = (x+(x+1))/2
            pontoMedio.y = (y+(y+1))/2
            # adiciono esse ponto medio na lista de pontos medio, só para guardar as coordenadas da casa
            MatPontoMedio.append(pontoMedio)
            contador = contador + 1  # a identificação do numero da casa sai daqui


def inicio():
    global objetoSelecionado
    glClearColor(0.5, 0.5, 0.5, 1.0)

    calcula_PM()

    # aloca os valores da câmera que inicialmente será posicionada na casa 63, que é o ponto 8X8 do tabuleiro
    camera.ident = MatPontoMedio[63].ident
    camera.x = MatPontoMedio[63].x
    camera.y = MatPontoMedio[63].y
    camera.tipo = "Camera"
    listaObjetosDoTabuleiro.append(camera)
    MatPontoMedio[63].preenchida = True

    # inicia os valores do quadrado, escolhendo uma casa aleatória para o mesmo entrar
    # objeto não cair em cima da camera
    pos = random.randint(0, 63)
    while MatPontoMedio[pos].preenchida == True:
        pos = random.randint(0, 63)
    quadrado: Objeto() = Objeto()
    quadrado.ident = MatPontoMedio[pos].ident  # 63
    quadrado.x = MatPontoMedio[pos].x
    quadrado.y = MatPontoMedio[pos].y
    quadrado.tipo = "Quadrado"
    # aloco o mesmo na lista geral de objetos
    listaObjetosDoTabuleiro.append(quadrado)
    listaQuadrados.append(quadrado)  # aloco na lista apenas de quadrados
    MatPontoMedio[pos].preenchida = True

    # faço meu objeto selecionado inicial, que poderá se mover, ser a camera
    objetoSelecionado = camera


def resize(w: int, h: int):
    global largura, altura
    largura = w
    altura = h
    # aqui informo qual as medidas da minha janela a cada vez que ela é redimensionada
    print(largura, altura)
    glutPostRedisplay()


def tecladoSpecial(key: int, x: int, y: int):

    global objetoSelecionado
    # //os códigos das teclas especiais são valores inteiros
    # aqui eu verifico se o objeto selecionado tem um objeto preenchendo a casa do tabuleiro
    if MatPontoMedio[objetoSelecionado.ident].preenchida == True:
        if key == GLUT_KEY_LEFT:
            # //caso a seta esquerda seja pressionada, a coordenada x do ponto inferior esquerdo será reduzida, deslocando o quadrado pra esquerda
            # verifico se o objeto selecionado ainda está em uma posição maior que a borda esquerda
            if objetoSelecionado.x - 1 > 0:
                # a casa esquerda é criada para fazer a troca de casa do objeto
                casa_esquerda = objetoSelecionado.ident - 8
                # verifica se essa casa não tem algum outro objeto
                if MatPontoMedio[casa_esquerda].preenchida == False:
                    # como a casa está vazia, move o objeto selecionado para essa casa a esquerda
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_esquerda].ident
                    objetoSelecionado.x = MatPontoMedio[casa_esquerda].x
                    objetoSelecionado.y = MatPontoMedio[casa_esquerda].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        elif key == GLUT_KEY_RIGHT:
            # //caso a seta direita seja pressionada, a coordenada x do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra direita
            if objetoSelecionado.x + 1 < 8:
                casa_direita = objetoSelecionado.ident + 8
                if MatPontoMedio[casa_direita].preenchida == False:
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_direita].ident
                    objetoSelecionado.x = MatPontoMedio[casa_direita].x
                    objetoSelecionado.y = MatPontoMedio[casa_direita].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        elif key == GLUT_KEY_DOWN:
            # //caso a seta pra baixo seja pressionada, a coordenada y do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra baixo
            if objetoSelecionado.y - 1 > 0:
                casa_baixo = objetoSelecionado.ident - 1
                if MatPontoMedio[casa_baixo].preenchida == False:
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_baixo].ident
                    objetoSelecionado.x = MatPontoMedio[casa_baixo].x
                    objetoSelecionado.y = MatPontoMedio[casa_baixo].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True

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
    global objetoSelecionado, qtdcirculos, listaCirculos
    """O is_pressed() recebe um caractere como entrada e, se corresponder à tecla que o usuário pressionou, retornará True e False caso contrário."""
    if keyboard.is_pressed("x"):
        objetoSelecionado = camera
    elif keyboard.is_pressed("c"):
        circulo: Objeto() = Objeto()
        posAleat = random.randint(0, 63)
        while MatPontoMedio[posAleat].preenchida == True:
            posAleat = random.randint(0, 63)
        circulo.ident = MatPontoMedio[posAleat].ident
        circulo.x = MatPontoMedio[posAleat].x
        circulo.y = MatPontoMedio[posAleat].y
        circulo.tipo = "Circulo"
        listaObjetosDoTabuleiro.append(circulo)
        listaCirculos.append(circulo)
        MatPontoMedio[posAleat].preenchida = True
    elif keyboard.is_pressed("q"):
        quadrado: Objeto() = Objeto()
        posAleat = random.randint(0, 63)
        while MatPontoMedio[posAleat].preenchida == True:
            posAleat = random.randint(0, 63)
        quadrado.ident = MatPontoMedio[posAleat].ident
        quadrado.x = MatPontoMedio[posAleat].x
        quadrado.y = MatPontoMedio[posAleat].y
        quadrado.tipo = "Quadrado"
        listaObjetosDoTabuleiro.append(quadrado)
        listaQuadrados.append(quadrado)
        MatPontoMedio[posAleat].preenchida = True
    elif keyboard.is_pressed("t"):
        triangulo: Objeto() = Objeto()
        posAleat = random.randint(0, 63)
        while MatPontoMedio[posAleat].preenchida == True:
            posAleat = random.randint(0, 63)
        triangulo.ident = MatPontoMedio[posAleat].ident
        triangulo.x = MatPontoMedio[posAleat].x
        triangulo.y = MatPontoMedio[posAleat].y
        triangulo.tipo = "Triangulo"
        listaObjetosDoTabuleiro.append(triangulo)
        listaTriangulos.append(triangulo)
        MatPontoMedio[posAleat].preenchida = True

    glutPostRedisplay()


def mouseClique(button: int, state: int, x: int, y: int):
    global objetoSelecionado
    # não consegui ajustar o clique direito pois não cheguei a fazer o 3D
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    selecao = Objeto()
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        selecao.x = x
        selecao.y = altura - y
        selecao.x = int(selecao.x/(largura/8))+0.5
        selecao.y = int(selecao.y/(altura/8))+0.5

        for i in range(8*8):
            if MatPontoMedio[i].x == selecao.x and MatPontoMedio[i].y == selecao.y:
                selecao.ident = MatPontoMedio[i].ident
                j = 0
                while j < len(listaObjetosDoTabuleiro):
                    if listaObjetosDoTabuleiro[j].x == selecao.x and listaObjetosDoTabuleiro[j].y == selecao.y:
                        selecao.tipo = listaObjetosDoTabuleiro[j].tipo
                    j = j+1
                if MatPontoMedio[i].preenchida == True:
                    objetoSelecionado = selecao
                    print(
                        f'\nMudando para: {selecao.tipo} {selecao.ident} {selecao.x} {selecao.y} \n')
                else:
                    print(f'\nA casa {selecao.ident} está vazia.\n')
    glutPostRedisplay()


def Tabuleiro():
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
    """desenho a camera no mesmo formato do objeto circulo, mas com um raio diferente e cor propria para a camera"""
    global objetoSelecionado
    N = 50
    R = 0.2
    CentroX = CentroY = 0
    if objetoSelecionado.tipo == "Camera":
        glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
        # atualizo as coordenadas da camera no proprio objeto câmera, obtendo os valores de acordo com a movimentação feita na variavel de objeto selecionado
        camera.ident = objetoSelecionado.ident
        camera.x = objetoSelecionado.x
        camera.y = objetoSelecionado.y
    else:
        # caso o objeto selecionado para mover, não seja a câmera, mantém a câmera nas últimas coordenadas do objeto
        glTranslatef(camera.x, camera.y, 0)
    glColor(0.7, 0.7, 0.7)
    glBegin(GL_POLYGON)

    for i in range(N):
        angulo = (i*2*pi)/N
        glVertex2f(CentroX+(math.cos(angulo)*R), CentroY+(math.sin(angulo)*R))

    glEnd()
    glFlush()


def circulo():
    N = 25
    R = 0.3
    CentroX = CentroY = 0
    glBegin(GL_POLYGON)

    for i in range(N):
        angulo = (i*2*pi)/N
        glVertex2f(CentroX+(math.cos(angulo)*R), CentroY+(math.sin(angulo)*R))

    glEnd()
    glFlush()


def quadrado():
    glBegin(GL_QUAD_STRIP)
    glVertex2f(-0.25, -0.25)
    glVertex2f(0.25, -0.25)
    glVertex2f(-0.25, 0.25)
    glVertex2f(0.25, 0.25)
    glEnd()

    glFlush()


def triangulo():
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.25, -0.25)
    glVertex2f(0.25, -0.25)
    glVertex2f(0.0,  0.25)
    glEnd()
    glFlush()


def desenha():
    global objetoSelecionado

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

    # desenho todos os quadrados que adicionei aleatoriamente no tabuleiro a partir da lista de quadrados
    j = 0
    while j < len(listaQuadrados):
        glPushMatrix()
        if objetoSelecionado.ident == listaQuadrados[j].ident:
            k = 0
            while k < len(listaObjetosDoTabuleiro):
                if objetoSelecionado.ident == listaObjetosDoTabuleiro[k].ident:
                    glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
                    listaQuadrados[j] = objetoSelecionado
                    listaObjetosDoTabuleiro[k] = objetoSelecionado
                k = k + 1
        else:
            glTranslatef(listaQuadrados[j].x, listaQuadrados[j].y, 0)
        glColor3f(1, 0, 0.5)
        quadrado()
        glPopMatrix()
        glFlush()

        j = j + 1

    # desenho todos os circulos que adicionei aleatoriamente no tabuleiro a partir da lista de circulos
    j = 0
    while j < len(listaCirculos):
        glPushMatrix()
        if objetoSelecionado.ident == listaCirculos[j].ident:
            k = 0
            while k < len(listaObjetosDoTabuleiro):
                if objetoSelecionado.ident == listaObjetosDoTabuleiro[k].ident:
                    glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
                    listaCirculos[j] = objetoSelecionado
                    listaObjetosDoTabuleiro[k] = objetoSelecionado
                k = k + 1
        else:
            glTranslatef(listaCirculos[j].x, listaCirculos[j].y, 0)
        glColor3f(0, 0.7, 0)
        circulo()
        glPopMatrix()
        glFlush()

        j = j + 1

    # desenho todos os quadrados que adicionei aleatoriamente no tabuleiro a partir da lista de quadrados
    j = 0
    while j < len(listaTriangulos):
        glPushMatrix()
        if objetoSelecionado.ident == listaTriangulos[j].ident:
            k = 0
            while k < len(listaObjetosDoTabuleiro):
                if objetoSelecionado.ident == listaObjetosDoTabuleiro[k].ident:
                    glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
                    listaTriangulos[j] = objetoSelecionado
                    listaObjetosDoTabuleiro[k] = objetoSelecionado
                k = k + 1
        else:
            glTranslatef(listaTriangulos[j].x, listaTriangulos[j].y, 0)
        glColor3f(1, 0.3, 0)
        triangulo()
        glPopMatrix()
        glFlush()

        j = j + 1

    # aqui eu imprimo todos os meus objetos no tabuleiro indicando o tipo, a casa que ele está e as coordenadas do ponto medio do mesmo
    i = 0
    while i < len(listaObjetosDoTabuleiro):
        print(
            f'{listaObjetosDoTabuleiro[i].tipo} {listaObjetosDoTabuleiro[i].ident} ({listaObjetosDoTabuleiro[i].x}, {listaObjetosDoTabuleiro[i].y})')
        i = i+1


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
