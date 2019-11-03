
class Llamada:

	# Variables que deben ser asignadas durante la simulación
	horaDeArribo
	horaDeAtencion
	horaDeSalida
	desviada
	# Para saber si la llamada dejó el sistema, para estadísticas
	fueRuteada

	def __init__(self):
        self.horaDeArribo = 0.0
		self.horaDeAtencion = 0.0
		self.horaDeSalida = 0.0
		self.desviada = False
		self.fueRuteada = False

	# tiempo_en_colla = hora de atencion - hora de arribo
	def tiempoEnCola()
		tCola = 0.0
		# Se debe checkear que las horas hayan sido asignadas
		if(self.horaDeArribo != 0.0 and self.horaDeAtencion != 0.0):
			tCola = self.horaDeAtencion - self.horaDeArribo
		return tCola

	# tiempo en el sistema = hora de salida - hora de arribo
	def tiempo_en_sistema()
		tCola = 0.0
		# Se debe checkear que las horas hayan sido asignadas
		if(self.horaAe_arribo != 0.0 and self.horaDeSalida != 0.0):
			tCola = self.horaDeAtencion - self.horaDeArribo
		return tCola
