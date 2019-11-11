# Agregar guardado de estadisticas al final de cada iteracion
# e imprimirlas finales

# terminar de implementar la función principal iniciar()

# implementar eventos

import math
import time
import estadisticas
import llamada
import ruteador
import random

INFINITO = math.inf

class Simulacion:
	# Parámetros del usuario
	iteraciones = 0
	tiempoMaximo = 0.0
	modoLento = False
	delay = 0

	reloj = 0.0

	# Horas para los eventos
	# Llega una llamada al ruteador A
	LA = 0.0
	# Llega una llamada al ruteador B
	LB = 0.0
	# Sale una llamada del ruteador A
	SA = INFINITO
	# Sale una llamada del ruteador B
	SB = INFINITO
	# Desvío de una llamada de A a B
	DAB = INFINITO

	eventoProcesado = ""

	# Necesaria para no superponer llamadas
	# (un desvío podría darse después del otros
	# y se perdería la anterior)
	colaDesvioAB = []

	# ubicamos los ruteadores aca para lo eventos puedan acceder a ellos
	#ruteadorA = ruteador.RuteadorA()
	#ruteadorB = ruteador.RuteadorB()

	def __init__(self, iteraciones, tiempoMaximo, modoLento = False, delay = 0):
		self.iteraciones = iteraciones
		self.tiempoMaximo = tiempoMaximo
		self.modoLento = modoLento
		self.delay = delay

	def iniciar(self):
		estadisticasA = estadisticas.Estadisticas(self.iteraciones)
		estadisticasB = estadisticas.EstadisticasB(self.iteraciones)
		estadisticasAB = estadisticas.Estadisticas(self.iteraciones)

		for iteracion in range(self.iteraciones):
			# se reinician variables
			self.reloj = 0.0
			self.LA = 0.0
			self.LB = 0.0
			self.SA = INFINITO
			self.SB = INFINITO
			self.DAB = INFINITO
			self.eventoProcesado = ""
			self.colaDesvioAB.clear()
			ruteadorA = ruteador.RuteadorA()
			ruteadorB = ruteador.RuteadorB()
			

			while(self.reloj < self.tiempoMaximo):
			# min es una función de python
				proximo_evento = min(self.LA, self.LB, self.SA, self.SB, self.DAB)
				# python no posee "switch", con 5 condiciones esta bien usar ifs
				if  (proximo_evento == self.LA):
					self.arriboA(ruteadorA)
					self.eventoProcesado = "Arribo A"
				elif(proximo_evento == self.LB):
					self.arriboB(ruteadorB)
					self.eventoProcesado = "Arribo B"
				elif(proximo_evento == self.SA):
					self.salidaA(ruteadorA)
					self.eventoProcesado = "Salida A"
				elif(proximo_evento == self.SB):
					self.salidaB(ruteadorA, ruteadorB)
					self.eventoProcesado = "Salida B"
				elif(proximo_evento == self.DAB):
					self.desvioAB(ruteadorA, ruteadorB)
					self.eventoProcesado = "Desvío A a B"
				#print("Evento ejecutado:", self.eventoProcesado, str(proximo_evento))
				#print("Cola de A: ", len(ruteadorA.colaLlamadas) ,". Cola de B: ", len(ruteadorB.colaLlamadas), "Cola desvio: ", len(self.colaDesvioAB))
				if self.modoLento:
					self.imprimirDuranteSimulacion(self.reloj, ruteadorA, ruteadorB)
					time.sleep(self.delay)

			# se recopilan datos para estadisticas finales
			estadisticasA.tiempoTotal += self.reloj
			estadisticasB.tiempoTotal += self.reloj
			estadisticasAB.tiempoTotal += self.reloj
			estadisticasA.tiempoColaTotal += ruteadorA.tiempoTotalCola
			estadisticasB.tiempoColaTotal += ruteadorB.tiempoTotalCola
			estadisticasAB.tiempoColaTotal += ruteadorB.tiempoTotalColaDesviadas
			estadisticasA.tiempoPermanenciaTotal += ruteadorA.tiempoPermanencia
			estadisticasB.tiempoPermanenciaTotal += ruteadorB.tiempoPermanencia
			estadisticasAB.tiempoPermanenciaTotal += ruteadorB.tiempoTotalPermanenciaDesviadas
			estadisticasA.llamadasRecibidasTotal += ruteadorA.llamadasRecibidas
			estadisticasB.llamadasRecibidasTotal += ruteadorB.llamadasRecibidas
			estadisticasAB.llamadasRecibidasTotal += ruteadorB.llamadasDesviadasAB
			estadisticasA.llamadasRuteadasTotal += ruteadorA.llamadasRuteadas
			estadisticasB.llamadasRuteadasTotal += ruteadorB.llamadasRuteadas
			estadisticasAB.llamadasRuteadasTotal += ruteadorB.tiempoTotalPermanenciaDesviadas

			self.imprimirFinalCorrida(self.reloj, ruteadorA, ruteadorB)
			#if self.modoLento:
			#	self.imprimirDuranteSimulacion(self.reloj, ruteadorA, ruteadorB)
			#	time.sleep(self.delay)
					
		# ...

	def arriboA(self, ruteadorA):
		# Tener cuidado de olvidarnos sumar el 0.5 
		self.reloj = self.LA
		call = llamada.Llamada(self.reloj)
		#if ruteadorA.ocupado == True: 
		if ruteadorA.llamadasEnCola >= 5: # Desvio
			call.setDesviada(True)
			self.colaDesvioAB.append(call)
			tiempoDesvio = self.reloj + ruteadorA.generarTiempoDesvioAB()
			if self.DAB == INFINITO: # Si esta programado
				# Si esta desprogramado
				self.DAB = tiempoDesvio
		#	else: 								 # No desvio
		#		ruteadorA.colaLlamadas.append(call) 
		#		ruteadorA.llamadasEnCola += 1
		else:
			ruteadorA.colaLlamadas.append(call) 
			ruteadorA.llamadasEnCola += 1
			ruteadorA.llamadasRecibidas += 1
		if not ruteadorA.ocupado:
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			ruteadorA.ocupado = True
			if tipoLlamada == 1:
				call.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
				self.SA = self.reloj + call.tiempoAtencion
			else: 
				call.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
				self.SA = self.reloj + call.tiempoAtencion
		self.LA = self.reloj + ruteadorA.generarTiempoArriboA()

	def arriboB(self, ruteadorB):
		self.reloj = self.LB
		call = llamada.Llamada(self.reloj)
		ruteadorB.llamadasRecibidas += 1
		ruteadorB.colaLlamadas.append(call) 
		ruteadorB.llamadasEnCola += 1 
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			call.tiempoAtencion = ruteadorB.generarTiempoTipo2B() 
			self.SB = self.reloj + call.tiempoAtencion
		self.LB = self.reloj + ruteadorB.generarTiempoArriboB()

	def salidaA(self, ruteadorA):
		self.reloj = self.SA
		self.SA = INFINITO
		ruteadorA.ocupado = False
		ruteadorA.llamadasEnCola -= 1
		ruteadorA.llamadasRuteadas += 1
		call = ruteadorA.colaLlamadas.pop(0)
		call.horaDeSalida = self.reloj
		ruteadorA.tiempoTotalCola += call.tiempoEnCola() 
		ruteadorA.tiempoPermanencia += call.tiempoEnSistema()
		if ruteadorA.llamadasEnCola > 0:
			ruteadorA.ocupado = True
			#ruteadorA.llamadasRuteadas += 1
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			if tipoLlamada == 1:
				call.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
				self.SA = self.reloj + call.tiempoAtencion
			else:
				call.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
				self.SA = self.reloj + call.tiempoAtencion
		

	def salidaB(self, ruteadorA, ruteadorB):
		self.reloj = self.SB
		self.SB = INFINITO
		ruteadorB.ocupado = False
		ruteadorB.llamadasEnCola -= 1
		call = ruteadorB.colaLlamadas.pop(0)
		call.horaDeSalida = self.reloj
		if call.desviada == True: 
			ruteadorB.tiempoTotalColaDesviadas += call.tiempoEnCola()
			ruteadorB.tiempoTotalPermanenciaDesviadas += call.tiempoEnSistema()
		else:
			ruteadorB.tiempoTotalCola += call.tiempoEnCola()
			ruteadorB.tiempoPermanencia += call.tiempoEnSistema()
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if ruteadorB.llamadasEnCola > 0:
			ruteadorB.ocupado = True
			ruteadorB.llamadasRuteadas += 1
			if ruteadorB.llamadasEnCola > 4:
				if random.uniform(0, 1) <= 0.1:
					ruteadorB.llamadasRuteadas -= 1
					ruteadorB.llamadasPerdidasB += 1
			if call.desviada == True:
				tipoLlamada = ruteadorA.generarTipoLlamadaA()
				if tipoLlamada == 1:
					call.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
					self.SB = self.reloj + call.tiempoAtencion
				else:
					call.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
					self.SB = self.reloj + call.tiempoAtencion
			else: # Generar tipo 2
				call.tiempoAtencion = ruteadorB.generarTiempoTipo2B()
				self.SB = self.reloj + call.tiempoAtencion

	def desvioAB(self, ruteadorA, ruteadorB):
		self.reloj = self.DAB

		ruteadorB.colaLlamadas.append(self.colaDesvioAB.pop(0)) 
		ruteadorB.llamadasEnCola += 1
		ruteadorB.llamadasDesviadasAB += 1
		ruteadorB.llamadasRecibidas += 1
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if len(self.colaDesvioAB) > 0:
			self.DAB = self.reloj + self.colaDesvioAB[0].horaDeArribo + 0.5
		else:
			self.DAB = INFINITO
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			if tipoLlamada == 1:
				self.SB = self.reloj + ruteadorA.generarTiempoTipo1A()
			else:
				self.SB = self.reloj + ruteadorA.generarTiempoTipo2A()
		
		
	def imprimirDuranteSimulacion(self, reloj, ruteadorA, ruteadorB):
		print("################################################################")
		print("Reloj: " , str(reloj) , " (de " , str(self.tiempoMaximo), ")")
		print("Evento procesandose: ", self.eventoProcesado )
		if ruteadorA.ocupado:
			print("Ruteador A: ocupado")
		else:
			print("Ruteador A: libre")
		if ruteadorB.ocupado:
			print("Ruteador B: ocupado")
		else:
			print("Ruteador B: libre")
		print("Longitud cola de A:", ruteadorA.llamadasEnCola)
		print("Longitud cola de B:", ruteadorB.llamadasEnCola)
		print("Número llamadas que han llegado a A:", ruteadorA.llamadasRecibidas)
		print("Número llamadas que han llegado a B:", ruteadorB.llamadasRecibidas)
		print("Número llamadas desviadas de A a B:", ruteadorB.llamadasDesviadasAB)
		print("Número llamadas ruteadas por A:", ruteadorA.llamadasRuteadas)
		print("Número llamadas ruteadas por B:", ruteadorB.llamadasRuteadas)

	def imprimirFinalCorrida(self, reloj, ruteadorA, ruteadorB):
		# si no se han ruteado llamadas, evitamos dividir por 0
		if ruteadorA.llamadasRuteadas == 0:
			ruteadorA.llamadasRuteadas = 1 
		if ruteadorB.llamadasRuteadas == 0:
			ruteadorB.llamadasRuteadas = 1 
		if ruteadorA.tiempoPermanencia == 0:
			ruteadorA.tiempoPermanencia = 1 
		if ruteadorB.tiempoPermanencia == 0:
			ruteadorB.tiempoPermanencia = 1 
		if ruteadorB.tiempoTotalPermanenciaDesviadas == 0:
			ruteadorB.tiempoTotalPermanenciaDesviadas = 1 
		print("/////////////////////////////////////////////////////////////////")
		print("Tamaño prom. de la cola en B: ", ruteadorB.tamanoPondCola / reloj)
		print("Tiempo prom. permanencia de una llamada en A: ", ruteadorA.tiempoPermanencia / ruteadorA.llamadasRuteadas)
		print("Tiempo prom. permanencia de una llamada en B: ", ruteadorB.tiempoPermanencia / ruteadorB.llamadasRuteadas)
		print("Tiempo prom. permanencia de una llamada desviada de A a B: ", ruteadorB.tiempoTotalPermanenciaDesviadas / ruteadorB.llamadasRuteadas)
		print("Tiempo prom. en cola de una llamada en A: ", ruteadorA.tiempoTotalCola / ruteadorA.llamadasRecibidas)
		print("Tiempo prom. en cola de una llamada en B: ", ruteadorB.tiempoTotalCola / ruteadorB.llamadasRecibidas)
		print("Tiempo prom. en cola de una llamada desviada de A a B: ", ruteadorB.tiempoTotalColaDesviadas / ruteadorB.llamadasDesviadasAB)
		# print("Porcentaje de llamadas perdidas por B :" )
		print("Eficiencia A: ", (ruteadorA.tiempoPermanencia - ruteadorA.tiempoTotalCola) / ruteadorA.tiempoPermanencia)
		print("Eficiencia B: ", (ruteadorB.tiempoPermanencia - ruteadorB.tiempoTotalCola) / ruteadorB.tiempoPermanencia)
		print("Eficiencia desviadas A - B: ", (ruteadorB.tiempoTotalPermanenciaDesviadas - ruteadorB.tiempoTotalColaDesviadas) / ruteadorB.tiempoTotalPermanenciaDesviadas)





