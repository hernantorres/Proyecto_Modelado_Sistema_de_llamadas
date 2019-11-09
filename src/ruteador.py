# implementar funciones generadores de tiempos

import math

class Ruteador:

	# Variables del ruteador
	ocupado = False
	llamadasEnCola = 0

	# Acumuladores de llamadas que entran al sistema, para estadísticas
	llamadasRecibidas = 0
	llamadasRuteadas = 0
	tamanoPromCola = 0.0
	tiempoPromCola = 0.0
	tiempoPromAtencion = 0.0

	# cola de llamadas
	colaLlamadas = []
	

class RuteadorA(Ruteador):

	llamadasDesviadasAB = 0

	#def generarTiempoArriboA(self):
		# ...

	#def generarTiempoDesvioAB(self):
		# ...

	#def generarTiempoTipo1A(self):
		# ...

	#def generatTiempoTipo2A(self):
		# ...

class RuteadorB(Ruteador):

	llamadasPerdidasB = 0

	#def generarTiempoArriboB(self):
		# ...

	#def generarTiempoTipo1B(self):
		# ...

	#def generatTiempoTipo2B(self):
		# ...








