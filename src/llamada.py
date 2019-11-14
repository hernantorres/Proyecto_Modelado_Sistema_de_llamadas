
class Llamada:

	def __init__(self, horaDeArribo):
		self.horaDeArribo = horaDeArribo
		self.horaDeSalida = 0.0
		self.tiempoAtencion = 0.0
		self.desviada = False
		self.tipo = 0

	# tiempo_en_cola = hora de atencion (que es = ) - hora de arribo
	def tiempoEnCola(self):
		tCola = 0.0
		tCola = self.horaDeSalida - self.tiempoAtencion - self.horaDeArribo
		return tCola

	# tiempo en el sistema = hora de salida - hora de arribo
	def tiempoEnSistema(self):
		tCola = 0.0
		tCola = self.horaDeSalida - self.horaDeArribo
		return tCola