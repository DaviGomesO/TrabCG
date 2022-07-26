"""
Aluno: Francisco Davi Gomes de Oliveira
Matricula: 475548
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# from OpenGL import glm

# importo a math para fazer o calculo do cosseno e desenhar o circulo
import math
# importo a random para obter posições aleatórias ao adicionar um objeto
import random
# e importo a keyboard para obter as entradas do teclado ASCII, de forma que vai esperar uma tecla ser pressionada
import keyboard

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
"""uma lista para guardar todos os objetos do tipo cubo"""
listaCubos: Objeto() = []

# circulo: Objeto() = Objeto()
"""uma lista para guardar todos os objetos do tipo quadrado"""
listaCones: Objeto() = []

listaTriangulos: Objeto() = []

listaBules: Objeto() = []


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
    cubo: Objeto() = Objeto()
    cubo.ident = MatPontoMedio[pos].ident  # 63
    cubo.x = MatPontoMedio[pos].x
    cubo.y = MatPontoMedio[pos].y
    cubo.tipo = "Cubo"
    # aloco o mesmo na lista geral de objetos
    listaObjetosDoTabuleiro.append(cubo)
    listaCubos.append(cubo)  # aloco na lista apenas de quadrados
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
            # verifico se o objeto selecionado ainda está em uma posição maior que a borda direita
            if objetoSelecionado.x + 1 < 8:
                # a casa direita é criada para fazer a troca de casa do objeto
                casa_direita = objetoSelecionado.ident + 8
                if MatPontoMedio[casa_direita].preenchida == False:
                    # como a casa está vazia, move o objeto selecionado para essa casa a direita
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_direita].ident
                    objetoSelecionado.x = MatPontoMedio[casa_direita].x
                    objetoSelecionado.y = MatPontoMedio[casa_direita].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True
        elif key == GLUT_KEY_DOWN:
            # //caso a seta pra baixo seja pressionada, a coordenada y do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra baixo
            # verifico se o objeto selecionado ainda está em uma posição maior que a borda de baixo
            if objetoSelecionado.y - 1 > 0:
                # a casa baixo é criada para fazer a troca de casa do objeto
                casa_baixo = objetoSelecionado.ident - 1
                if MatPontoMedio[casa_baixo].preenchida == False:
                    # como a casa está vazia, move o objeto selecionado para essa casa de baixo
                    MatPontoMedio[objetoSelecionado.ident].preenchida = False
                    objetoSelecionado.ident = MatPontoMedio[casa_baixo].ident
                    objetoSelecionado.x = MatPontoMedio[casa_baixo].x
                    objetoSelecionado.y = MatPontoMedio[casa_baixo].y
                    MatPontoMedio[objetoSelecionado.ident].preenchida = True

        elif key == GLUT_KEY_UP:
            # //caso a seta pra cima seja pressionada, a coordenada y do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra cima
            # verifico se o objeto selecionado ainda está em uma posição maior que a borda de cima
            if objetoSelecionado.y + 1 < 8:
                # a casa cima é criada para fazer a troca de casa do objeto
                casa_cima = objetoSelecionado.ident + 1
                if MatPontoMedio[casa_cima].preenchida == False:
                    # como a casa está vazia, move o objeto selecionado para essa casa de cima
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
    """Caso aperte a tecla x, eu vou selecionar a camera para movimentar,
    caso pressione a tecla 'c' irei criar um cone
    pressionando a tecla 'q', cria-se um cubo
    e caso pressione a tecla 't', crio um triangulo"""
    if keyboard.is_pressed("x"):
        objetoSelecionado = camera
    elif keyboard.is_pressed("c"):
        """irei criar o objeto do tipo que estou querendo, procurar uma casa aleatoria no tabuleiro, que não esteja preenchida. Em seguuida, passo os valores da casa para o objeto criado, passo o tipo a depender da tecla, e em seguida aloco esse objeto tanto na lista geral de objetos do tabuleiro, como na lista própria para aquele tipo de objetos"""
        cone: Objeto() = Objeto()
        posAleat = random.randint(0, 63)
        while MatPontoMedio[posAleat].preenchida == True:
            posAleat = random.randint(0, 63)
        cone.ident = MatPontoMedio[posAleat].ident
        cone.x = MatPontoMedio[posAleat].x
        cone.y = MatPontoMedio[posAleat].y
        cone.tipo = "Cone"
        listaObjetosDoTabuleiro.append(cone)
        listaCones.append(cone)
        MatPontoMedio[posAleat].preenchida = True
    elif keyboard.is_pressed("q"):
        cubo: Objeto() = Objeto()
        posAleat = random.randint(0, 63)
        while MatPontoMedio[posAleat].preenchida == True:
            posAleat = random.randint(0, 63)
        cubo.ident = MatPontoMedio[posAleat].ident
        cubo.x = MatPontoMedio[posAleat].x
        cubo.y = MatPontoMedio[posAleat].y
        cubo.tipo = "Cubo"
        listaObjetosDoTabuleiro.append(cubo)
        listaCubos.append(cubo)
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
    elif keyboard.is_pressed("b"):
        bule: Objeto() = Objeto()
        posAleat = random.randint(0, 63)
        while MatPontoMedio[posAleat].preenchida == True:
            posAleat = random.randint(0, 63)
        bule.ident = MatPontoMedio[posAleat].ident
        bule.x = MatPontoMedio[posAleat].x
        bule.y = MatPontoMedio[posAleat].y
        bule.tipo = "Bule"
        listaObjetosDoTabuleiro.append(bule)
        listaBules.append(bule)
        MatPontoMedio[posAleat].preenchida = True

    glutPostRedisplay()


def mouseClique(button: int, state: int, x: int, y: int):
    global objetoSelecionado
    # não consegui ajustar o clique direito pois não cheguei a fazer o 3D
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    selecao = Objeto()
    """para o clique no botão esquerdo do mouse, pego o objeto seleção criado para receber as coordenadas do ponto medio que representa a casa onde o mouse clicou em cima. A principio esse objeto recebe os valores como coordenada em pixel da janela, para converter de pixel para minha coordenada mundo faço a seguinte maneira:
        faço esse objeto na coordenada correspondente a largura(coordenada x) receber um inteiro dela mesmo dividida pelo tamanho do lado na coordenada x da casa do tabuleiro, adicionada de 0.5, que dará a coordenada x do ponto medio
        faço esse objeto na coordenada correspondente a altura(coordenada y) receber um inteiro dela mesmo dividida pelo tamanho do lado na coordenada y da casa do tabuleiro, adicionada de 0.5, que dará a coordenada y do ponto medio
    Apos esse calculo do ponto medio correspondente a casa clicada pelo mouse, procura-se esse ponto medio na lista de pontos medios, e ao achar passa os valores restantes para o objeto de seleção.
    Em seguida irei verificar se a casa selecionada está preenchida, se sim, pega o objeto que está lá dentro e atribui a variavel objetoSelecionado para poder movimenta-lo, se não informa que a casa está vazia."""
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
                        f'\nMudando para: {selecao.tipo} {selecao.ident} ({selecao.x}, {selecao.y}) \n')
                else:
                    print(f'\nA casa {selecao.ident} está vazia.\n')
    glutPostRedisplay()


def Tabuleiro():
    """Cria-se o tabuleiro do tamanho 8x8, e vou colorindo a medida que vai caminhando as casas, se for uma casa de identificação par ela é colorida com a cor preto, se for de identificação impar, é colorida com a cor branco"""
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


def Cubo():
    A = [-0.25, -0.25, -0.25]
    B = [0.25, -0.25, -0.25]
    C = [0.25, 0.25, -0.25]
    D = [-0.25, 0.25, -0.25]
    E = [-0.25, -0.25, 0.25]
    F = [0.25, -0.25, 0.25]
    G = [0.25, 0.25, 0.25]
    H = [-0.25, 0.25, 0.25]

    glBegin(GL_QUAD_STRIP)

    glVertex3fv(A)
    glVertex3fv(D)
    glVertex3fv(C)
    glVertex3fv(B)

    glVertex3fv(C)
    glVertex3fv(D)
    glVertex3fv(H)
    glVertex3fv(G)

    glVertex3fv(A)
    glVertex3fv(E)
    glVertex3fv(H)
    glVertex3fv(D)

    glVertex3fv(B)
    glVertex3fv(C)
    glVertex3fv(G)
    glVertex3fv(F)

    glVertex3fv(E)
    glVertex3fv(F)
    glVertex3fv(G)
    glVertex3fv(H)

    glVertex3fv(A)
    glVertex3fv(B)
    glVertex3fv(F)
    glVertex3fv(E)

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

    # Não consegui configurar a posição da câmera
    # gluLookAt(0, 0, 0, camera.x, camera.y, 2, 0, 0, 1)

    """Defino minhas coordenadas de mundo para serem de acordo com a quantidade de casas, portando indo de 0 até 8 nas coordenadas x e y, inicia-se a chamada do tabuleiro e em seguida ja desenho a camera"""
    glOrtho(0, 8, 0, 8, -1, 1)

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    Tabuleiro()
    glEnd()

    glFlush()

    glPushMatrix()
    camera()
    glPopMatrix()

    """desenho todos os bules que adicionei aleatoriamente no tabuleiro a partir da lista de bules, nos seguintes passos:
    percorrer a listas de objetos que quero desenhar, verifico se o objeto selecionado da vez tem a mesma identificação que alguns daqueles objetos que estão na lista especifica, se tiver, vou atrás desse objeto dentro da lista geral de objetos para poder alterar as coordenadas dele em ambas as listas, e aplica-se a translação com as coordenadas do objeto já com as movimentações atualizadas e atualiza nas duas listas que o objeto está. Caso não seja o objeto selecionado, ele terá a translação que corresponde a posição dele dentro da lista especifica daquele tipo de objeto.
    Esse passo vale para todos os objetos desenhados"""
    j = 0
    while j < len(listaBules):

        glPushMatrix()

        if objetoSelecionado.ident == listaBules[j].ident:
            k = 0
            while k < len(listaObjetosDoTabuleiro):
                if objetoSelecionado.ident == listaObjetosDoTabuleiro[k].ident:
                    glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
                    listaBules[j] = objetoSelecionado
                    listaObjetosDoTabuleiro[k] = objetoSelecionado
                k = k + 1
        else:
            glTranslatef(listaBules[j].x, listaBules[j].y, 0)

        # aplico essa rotação de 90° no eixo x para aparecer a parte de cima do objeto
        glRotatef(90, 1, 0, 0)
        glColor3f(1, 1, 0.5)
        glutSolidTeapot(0.25)
        glPopMatrix()
        glFlush()

        j = j + 1

    # desenho todos os cubos que adicionei aleatoriamente no tabuleiro a partir da lista de cubos
    j = 0
    while j < len(listaCubos):
        glPushMatrix()
        if objetoSelecionado.ident == listaCubos[j].ident:
            k = 0
            while k < len(listaObjetosDoTabuleiro):
                if objetoSelecionado.ident == listaObjetosDoTabuleiro[k].ident:
                    glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
                    listaCubos[j] = objetoSelecionado
                    listaObjetosDoTabuleiro[k] = objetoSelecionado
                k = k + 1
        else:
            glTranslatef(listaCubos[j].x, listaCubos[j].y, 0)
        glRotatef(90, 1, 0, 0)
        glColor3f(1, 0, 0.5)
        Cubo()
        glPopMatrix()
        glFlush()

        j = j + 1

    # desenho todos os cones que adicionei aleatoriamente no tabuleiro a partir da lista de cones
    j = 0
    while j < len(listaCones):
        glPushMatrix()
        if objetoSelecionado.ident == listaCones[j].ident:
            k = 0
            while k < len(listaObjetosDoTabuleiro):
                if objetoSelecionado.ident == listaObjetosDoTabuleiro[k].ident:
                    glTranslatef(objetoSelecionado.x, objetoSelecionado.y, 0)
                    listaCones[j] = objetoSelecionado
                    listaObjetosDoTabuleiro[k] = objetoSelecionado
                k = k + 1
        else:
            glTranslatef(listaCones[j].x, listaCones[j].y, 0)
        glColor3f(0, 0.7, 0)
        glutSolidCone(0.35, 0.25, 10, 8)
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
