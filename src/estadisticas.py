# toDo: especificar atributos y metodos para estadísticas GLOBALES
# implementar metodos para generar estadisticas

# estructura para alamacenar los datos de cada corrida
class Estadisticas:

	iteraciones = 0

	# acumulador de tiempo de cada corrida
	tiempoTotal = 0.0

	# acumulador de tiempos de permanencia de cada corrida
	tiempoPermanenciaTotal = 0.0

	# acumulador de tiempos en cola de cada corrida
	tiempoColaTotal = 0.0

	# acumuladores de recibidas y ruteadas
	# note que llamadas Recibidas puede ser usado para "desviadas"
	llamadasRecibidasTotal = 0
	llamadasRuteadasTotal = 0


	def __init__(self, iteraciones):
		self.iteraciones =  iteraciones

	def tiempoPromedioPermanencia(self):
		prom = tiempoPermanenciaTotal / llamadasRuteadasTotal
		return prom

	def tiempoPromedioCola(self):
		prom = tiempoColaTotal / llamadasRecibidasTotal
		return prom


	def eficiencia():
		# (t. permanencia - t. cola) / t. permanencia
		efic = tiempoPromedioPermanencia() - tiempoPromedioCola()
		efic = efic / tiempoPromedioPermanencia()
		return efic

	#def imprimirDatosDuranteSimulacion():
	#	# ...

	#def imrpimirDatosFinalSimulacion():
	#	# ...

# esta clase es para estadísticas específicas de B, pero hereda de Estadísticas
class EstadisticasB(Estadisticas):
	
	# acumulador de tamaño de cola B ponderado por tiempo
	tamañoColaTiempoB = 0.0

	# acumuladores para promedio de llamadas perdidas en B
	llamadasPerdidasB = 0
	llamadasLocalesB = 0

	def tamañoPromedioColaB(self):
		prom = tamañoColaTiempoB / tiempoTotal
		return prom

	def porcentajeLlamadasPerdidasB(perdidas, total)
		porcentaje = llamadasPerdidasB / llamadasLocalesB
		return porcentaje