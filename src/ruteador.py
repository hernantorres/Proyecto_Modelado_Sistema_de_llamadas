# implementar funciones generadores de tiempos

import math
import random
import time

class Ruteador:

	# Variables del ruteador
	ocupado = False
	llamadasEnCola = 0

	# Acumuladores de llamadas que entran al sistema, para estadísticas
	llamadasRecibidas = 0
	llamadasRuteadas = 0
	tiempoTotalCola = 0.0
	tiempoPermanencia = 0.0

	# cola de llamadas
	colaLlamadas = []


	llamadasRuteadasLocales = 0

	def __init__(self):
		self.ocupado = False
		self.llamadasEnCola = 0
		self.llamadasRecibidas = 0
		self.llamadasRuteadas = 0
		self.tiempoTotalCola = 0.0
		self.tiempoPermanencia = 0.0
		self.colaLlamadas = []

	def reiniciar(self):
		ocupado = False
		llamadasEnCola = 0
		llamadasRecibidas = 0
		llamadasRuteadas = 0
		tamanoPondCola = 0.0
		tiempoTotalCola = 0.0
		tiempoTotalAtencion = 0.0
		colaLlamadas.clear()

	def generarTipoLlamadaA(self):
		aleatorio = random.uniform(0,1)
		if( aleatorio <= 0.2 ):
			return 1
		else:
			return 2	

class RuteadorA(Ruteador):

	def generarTiempoArriboA(self):
		aleatorio = random.uniform(0, 1)
		if aleatorio != 1:
			valor = math.log(1 - aleatorio) / -(2/3)
		else:
			valor = math.log(1 - 0.999) / -(2/3)
		return valor

	def generarTiempoDesvioAB(self):
		return 0.5

	def generarTiempoTipo1A(self):
		aleatorio = random.uniform(0, 1)
		valor = 10 * math.sqrt(5 * aleatorio + 4)
		return valor

	def generarTiempoTipo2A(self):
		aleatorio = 0
		for index in range(12):
			aleatorio += random.uniform(0, 1)
		aleatorio -= 6
		valor = 1 * aleatorio + 15
		return valor

class RuteadorB(Ruteador):

	llamadasPerdidasB = 0
	llamadasLocalesB = 0
	llamadasRuteadasDesviadas = 0

	# este contador debería ir acá pues es B quien las rutea
	llamadasDesviadasAB = 0
	
	tamanoPondCola = 0.0

	tiempoTotalColaDesviadas = 0.0
	tiempoTotalPermanenciaDesviadas = 0.0

	# Cuando fue el ultimo cambio, duracion entre cambios
	tiempoUltimoCambio = 0.0

	def obtTiempoUltimoCambio(self, horaDeCambio):
		resultado = horaDeCambio - self.tiempoUltimoCambio
		self.tiempoUltimoCambio = horaDeCambio
		return resultado

	def generarTiempoArriboB(self):
		aleatorio = random.uniform(0, 1)
		valor = 2 * aleatorio + 1
		return valor

	def generarTiempoTipo1B(self):
		aleatorio = random.uniform(0, 1)
		if aleatorio != 1:
			valor = math.log(1 - aleatorio) / -(4/3)
		else:
			valor = math.log(1 - 0.999) / -(4/3)
		return valor

	def generarTiempoTipo2B(self):
		aleatorio = random.uniform(0, 1)
		if 0 < aleatorio and aleatorio < (1/3):
			valor = 2 * aleatorio
		elif (1/3) < aleatorio and aleatorio < 1:
			valor = 3 - 2 * math.sqrt(2 * (1 - aleatorio))
		return valor