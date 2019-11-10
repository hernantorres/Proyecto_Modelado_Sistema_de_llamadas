
class Llamada:

	# Variables que deben ser asignadas durante la simulación
	horaDeArribo = 0.0
	horaDeAtencion = 0.0
	horaDeSalida = 0.0
	desviada = False

	def __init__(self, horaDeArribo):
        self.horaDeArribo = horaDeArribo
		self.horaDeAtencion = 0.0
		self.horaDeSalida = 0.0
		self.desviada = False

	# tiempo_en_cola = hora de atencion - hora de arribo
	def tiempoEnCola():
		tCola = 0.0
		# Se debe checkear que las horas hayan sido asignadas
		if(self.horaDeArribo != 0.0 and self.horaDeAtencion != 0.0):
			tCola = self.horaDeAtencion - self.horaDeArribo
		return tCola

	# tiempo en el sistema = hora de salida - hora de arribo
	def tiempo_en_sistema():
		tCola = 0.0
		# Se debe checkear que las horas hayan sido asignadas
		if(self.horaDeArribo != 0.0 and self.horaDeSalida != 0.0):
			tCola = self.horaDeSalida - self.horaDeArribo
		return tCola
