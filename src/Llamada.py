
class Llamada:

	# Variables que deben ser asignadas durante la simulación
	hora_de_arribo
	hora_de_atencion
	hora_de_salida
	desviada
	# Para saber si la llamada dejó el sistema, para estadísticas
	fue_ruteada

	def __init__(self):
        self.hora_de_arribo = 0.0
		self.hora_de_atencion = 0.0
		self.hora_de_salida = 0.0
		self.desviada = False
		self.fue_ruteada = False

	# tiempo_en_colla = hora de atencion - hora de arribo
	def tiempo_en_cola()
		t_cola = 0.0
		# Se debe checkear que las horas hayan sido asignadas
		if(self.hora_de_arribo != 0.0 and self.hora_de_atencion != 0.0):
			t_cola = self.hora_de_atencion - self.hora_de_arribo
		return t_cola

	# tiempo en el sistema = hora de salida - hora de arribo
	def tiempo_en_sistema()
		t_cola = 0.0
		# Se debe checkear que las horas hayan sido asignadas
		if(self.hora_de_arribo != 0.0 and self.hora_de_salida != 0.0):
			t_cola = self.hora_de_atencion - self.hora_de_arribo
		return t_cola
