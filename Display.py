from selenium import webdriver
from selenium.webdriver import ActionChains

from utils import numeros
from minesweeper import Tablero
import time

class Jugador:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://buscaminas-pro.com/")
        self.actionChains = ActionChains(self.driver)
        self.tablero = Tablero(9, 9)
        self.tablero.update([[9 for j in range(9)] for i in range(9)])
        self.first = True
        self.estancado = False
        self.acabo = False

    def casilla_id(self, yx):
        """"devuelve el id de html correspondiente a la casilla"""
        tile = yx[1]*9+yx[0]
        return "tile{0}".format(tile)

    def turno(self):
        """da click izquierdo en la pagina web a las casillas sin minas
        para destaparlas.
        da click derecho en la pagina web a las casillas con minas
        para marcarlas con la bandera"""
        interpretacion = self.sacar_interpretacion()
        for letra in interpretacion:
            yx = self.tablero.MenC.inv(letra)
            id = self.casilla_id(yx)
            casilla = self.driver.find_element("id", id)
            if interpretacion[letra] == 1:
                self.actionChains.context_click(casilla).perform()
            elif interpretacion[letra] == -1:
                self.actionChains.click(casilla).perform()

    def jugar(self):
        if self.first:
            casilla = self.driver.find_element("id", "tile1")
            self.actionChains.click(casilla).perform()
            time.sleep(1)

        while not self.estancado and not self.acabo:
            self.actualizar_tablero()
            self.turno()
            time.sleep(1)

    def actualizar_tablero(self):
        """Obtiene la matriz del tablero en la pagina web y la actualiza en la clase tablero"""
        matriz = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(numeros[self.driver.find_element(
                    "id", self.casilla_id((i, j))).get_attribute("src")])
            matriz.append(row)
        self.tablero.update(matriz)

    def sacar_interpretacion(self):
        result = {}
        soluciones = self.tablero.solve()

        for letra in soluciones[0]:
            result[letra] = 0

        for solucion in self.tablero.solve():
            for letra in solucion:
                if solucion[letra] == True:
                    result[letra] += 1

        for letra in result:
            if result[letra] == len(soluciones):
                result[letra] = 1
            elif result[letra] == 0:
                result[letra] = -1
            else:
                result[letra] = 0

        return result

if __name__ == "__main__":
    jugador = Jugador()
    jugador.jugar()