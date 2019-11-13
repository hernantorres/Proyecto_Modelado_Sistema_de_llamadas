
class Llamada:

	# Variables que deben ser asignadas durante la simulación
	"""
	horaDeArribo = 0.0
	horaDeSalida = 0.0
	tiempoAtencion = 0.0
	desviada = False
	tipo = 0
	"""
	def __init__(self, horaDeArribo):
		self.horaDeArribo = horaDeArribo
		self.horaDeSalida = 0.0
		self.tiempoAtencion = 0.0
		self.desviada = False
		self.tipo = 0

	# tiempo_en_cola = hora de atencion - hora de arribo
	def tiempoEnCola(self):
		tCola = 0.0
		tCola = self.horaDeSalida - self.tiempoAtencion - self.horaDeArribo
		return tCola

	# tiempo en el sistema = hora de salida - hora de arribo
	def tiempoEnSistema(self):
		tCola = 0.0
		tCola = self.horaDeSalida - self.horaDeArribo
		return tCola

	def setHoraDeArribo(self, horaDeArribo):
		self.horaDeArribo = horaDeArribo

	def setHoraDeAtencion(self, horaDeAtencion):
		self.horaDeAtencion = horaDeAtencion

	def setHoraDeSalida(self, horaDeSalida):
		self.horaDeSalida = horaDeSalida

	def setDesviada(self, desviada):
		self.desviada = desviada