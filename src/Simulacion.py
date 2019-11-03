

INFINITO = float(“inf”)

class Simulacion:
	# Parámetros del usuario
	iteraciones
	tiempoMaximo
	modoLento
	delay

	Reloj

	# Horas para los eventos
	# Llega una llamada al ruteador A
	LA
	# Llega una llamada al ruteador B
	LB
	# Sale una llamada del ruteador A
	SA
	# Sale una llamada del ruteador B
	SB
	# Desvío de una llamada de A a B
	DAB

	# Necesaria para no superponer llamadas
	# (un desvío podría darse después del otros
	# y se perdería la anterior)
	colaDesvioAB

	# Llamadas que entran al sistema, para estadísticas
	listaLlamadas_A
	listaLlamadas_B
	listaLlamadasDesviadasAB

	# Contador de llamadas perdidas por B
	llamadasPerdidasB

	#Lista de estadísticas para cada simulación
	listaEstadisticas



	def __init__(self, iteraciones, tiempoMaximo, modoLento = False, delay = 0):
		self.iteraciones = iteraciones
		self.tiempoMaximo = tiempoMaximo
		self.modoLento = modoLento
		self.delay = delay

		self.Reloj = 0.0
		self.LA = 0.0
		self.LB = 0.0
		self.SA = INFINITO
		self.SB = INFINITO
		self.DAB = INFINITO

	def iniciar()
		# ...
		for iteracion in list(range(self.iteraciones))
			# min es una función de python
			proximo_evento = min(self.LA, self.LB, self.SA, self.SB, self.DAB)
		# ...


	def arriboA:
		# ...

	def arriboB:
		# ...

	def salidaA:
		# ...

	def salidaB:
		# ...

	def desvioAB:
		# ...

	def imprimirDatosDuranteSimulacion:
		# ...

	def imrpimirDatosFinalSimulacion
		# ...

