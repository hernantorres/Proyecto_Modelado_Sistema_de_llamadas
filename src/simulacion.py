# Agregar guardado de estadisticas al final de cada iteracion
# e imprimirlas finales

# terminar de implementar la función principal iniciar()

# implementar eventos

import math
import estadisticas
import ruteador

INFINITO = math.inf

class Simulacion:
	# Parámetros del usuario
	iteraciones = 0
	tiempoMaximo = 0.0
	modoLento = False
	delay = 0

	reloj = 0.0

	# Horas para los eventos
	# Llega una llamada al ruteador A
	LA = 0.0
	# Llega una llamada al ruteador B
	LB = 0.0
	# Sale una llamada del ruteador A
	SA = INFINITO
	# Sale una llamada del ruteador B
	SB = INFINITO
	# Desvío de una llamada de A a B
	DAB = INFINITO

	# Necesaria para no superponer llamadas
	# (un desvío podría darse después del otros
	# y se perdería la anterior)
	colaDesvioAB = []

	#Lista de estadísticas para cada simulación 
	#listaEstadisticas = []

	def __init__(self, iteraciones, tiempoMaximo, modoLento = False, delay = 0):
		self.iteraciones = iteraciones
		self.tiempoMaximo = tiempoMaximo
		self.modoLento = modoLento
		self.delay = delay

	def iniciar(self):
		for iteracion in range(self.iteraciones):
			# se reinician variables
			self.reloj = 0.0
			self.LA = 0.0
			self.LB = 0.0
			self.SA = INFINITO
			self.SB = INFINITO
			self.DAB = INFINITO
			ruteadorA = ruteador.RuteadorA()
			ruteadorB = ruteador.RuteadorB()

			while(self.reloj < self.tiempoMaximo)
			# min es una función de python
				proximo_evento = min(self.LA, self.LB, self.SA, self.SB, self.DAB)
				# python no posee "switch", con 5 condiciones esta bien usar ifs
				if  (proximo_evento == self.LA):
					arriboA()
				elif(proximo_evento == self.LB):
					arriboB()
				elif(proximo_evento == self.SA):
					salidaA()
				elif(proximo_evento == self.SB):
					salidaB()
				elif(proximo_evento == self.DAB):
					desvioAB()
		# ...


	#def arriboA(self):
		# ...

	#def arriboB(self):
		# ...

	#def salidaA(self):
		# ...

	#def salidaB(self):
		# ...

	#def desvioAB(self):
		# ...



