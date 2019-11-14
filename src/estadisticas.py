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

# esta clase es para estadísticas específicas de B, pero hereda de Estadísticas
class EstadisticasB(Estadisticas):
	
	# acumulador de tamaño de cola B ponderado por tiempo
	tamanoColaTiempoB = 0.0

	# acumuladores para promedio de llamadas perdidas en B
	llamadasPerdidasB = 0
	llamadasLocalesAB = 0
