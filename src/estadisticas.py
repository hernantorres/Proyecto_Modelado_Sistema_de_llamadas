# toDo: especificar atributos y metodos para estadísticas GLOBALES
# implementar metodos para generar estadisticas

class Estadisticas:

	# Acumuladores de llamadas que entran al sistema, para estadísticas
	llamadasA = 0
	llamadasB = 0
	llamadasDesviadasAB = 0
	llamadasPerdidasB = 0

	def __init__(self):
		self.llamadasA = 0.0
		self.llamadasB = 0.0
		self.llamadasDesviadasAB = 0.0
		self.llamadasPerdidasB = 0.0


	#def tamañoPromedioCola(self):
		# ...

	#def tiempoPromedioPermanencia(self):
		# ...

	#def tiempoPromedioCola(self):
		# ...

	#def porcentajeLlamadasPerdidas(perdidas, total)
	#	porcentaje = perdidas / total
	#	return total

	#def eficiencia():
		# (t. permanencia - t. cola) / t. permanencia
	#	efic = tiempoPromedioPermanencia() - tiempoPromedioCola()
	#	efic = efic / tiempoPromedioPermanencia()
	#	return efic

	#def imprimirDatosDuranteSimulacion():
	#	# ...

	#def imrpimirDatosFinalSimulacion():
	#	# ...