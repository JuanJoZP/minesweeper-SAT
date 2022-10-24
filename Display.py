from selenium import webdriver
from selenium.webdriver import ActionChains
import chromedriver_autoinstaller
from random import randint


chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
actionChains = ActionChains(driver)
driver.get("https://buscaminas-pro.com/")


def casilla_id(xy):
    tile = xy[1]*9+xy[0]
    return "tile{0}".format(tile)


def minas(interpretacion):
    resultado = []
    for i in interpretacion:
        if interpretacion[i] == 1:
            resultado.append(i)
    return resultado


def libres(interpretacion):
    resultado = []
    for i in interpretacion:
        if interpretacion[i] == -1:
            resultado.append(i)
    return resultado


def marcar_minas(minas):
    for xy in minas:
        id = casilla_id(xy)
        casilla = driver.find_element("id", id)
        actionChains.context_click(casilla).perform()


def destapar_casillas(casillas):
    for xy in casillas:
        id = casilla_id(xy)
        casilla = driver.find_element("id", id)
        actionChains.click(casilla).perform()
# oe eso no me deja crear variables, lo toma como si estuviera agarrando algo de un modulo no importado y dice que no esta accesed


# datos de ejemplo
interpretacion = {}
for x in range(8):
    for y in range(8):
        rand = randint(-10, 10)
        interpretacion[(x, y)] = 0 if rand != 1 and rand != -1 else rand

print("\n".join("{}\t{}".format(k, v) for k, v in interpretacion.items()))
# marcar_minas(minas(interpretacion))
# cuidado porque si destapa mina, las que van despues no sirven
destapar_casillas(libres(interpretacion))
