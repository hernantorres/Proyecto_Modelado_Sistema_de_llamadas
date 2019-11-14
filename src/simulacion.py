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

	def __init__(self, iteraciones, tiempoMaximo, modoLento = False, delay = 0):
		self.iteraciones = iteraciones
		self.tiempoMaximo = tiempoMaximo
		self.modoLento = modoLento
		self.delay = delay

	def iniciar(self):
		# se instancian las estructuras para estadísticas finales
		estadisticasA = estadisticas.Estadisticas()
		estadisticasB = estadisticas.EstadisticasB()
		estadisticasAB = estadisticas.Estadisticas()

		# ciclo de iteraciones
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
		
			# ciclo principal de eventos
			while(self.reloj < self.tiempoMaximo):
				# min es una función de python
				proximo_evento = min(self.LA, self.LB, self.SA, self.SB, self.DAB)
				# python no posee "switch", con 5 condiciones esta bien usar ifs
				if  proximo_evento == self.LA:
					self.arriboA(ruteadorA)
					self.eventoProcesado = "Arribo A"
				elif proximo_evento == self.LB:
					self.arriboB(ruteadorB)
					self.eventoProcesado = "Arribo B"
				elif proximo_evento == self.SA:
					self.salidaA(ruteadorA)
					self.eventoProcesado = "Salida A"
				elif proximo_evento == self.SB:
					self.salidaB(ruteadorA, ruteadorB)
					self.eventoProcesado = "Salida B"
				elif proximo_evento == self.DAB:
					self.desvioAB(ruteadorA, ruteadorB)
					self.eventoProcesado = "Desvío A a B"

				# si corre en modo lento, se imprimen datos después de cada evento
				if self.modoLento:
					self.imprimirDuranteSimulacion(self.reloj, ruteadorA, ruteadorB)
					time.sleep(self.delay)

			# se recopilan datos para estadisticas finales
			estadisticasA.tiempoTotal += self.reloj
			estadisticasB.tiempoTotal += self.reloj
			estadisticasAB.tiempoTotal += self.reloj
			estadisticasB.tamanoColaTiempoB += ruteadorB.tamanoPondCola
			estadisticasB.llamadasPerdidasB += ruteadorB.llamadasPerdidasB
			estadisticasB.llamadasLocalesAB += ruteadorA.llamadasRuteadasLocales + ruteadorB.llamadasRuteadasLocales
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
			estadisticasAB.llamadasRuteadasTotal += ruteadorB.llamadasRuteadasDesviadas

			# imprimimos las estadísticas para cada final de corrida
			self.imprimirFinalCorrida(self.reloj, ruteadorA, ruteadorB, iteracion)
			if self.modoLento:
				time.sleep(self.delay)

		# se imprimen estadísticas finales	
		self.imprimirFinalSimulacion(estadisticasA, estadisticasB, estadisticasAB)

	def arriboA(self, ruteadorA):
		self.reloj = self.LA
		# IMPORTANTE: al instanciarse un objeto llamada, se le provee su hora de arribo
		call = llamada.Llamada(self.reloj)
		ruteadorA.llamadasRecibidas += 1
		# se revisa la cola para saber si se desvía la llamada
		if ruteadorA.llamadasEnCola >= 5: 
			call.desviada = True
			self.colaDesvioAB.append(call)
			tiempoDesvio = self.colaDesvioAB[0].horaDeArribo +  0.5
			# Si esta desprogramado, se programa
			if self.DAB == INFINITO: 
				self.DAB = tiempoDesvio
		# introducimos la llamada a la cola de A
		else:
			ruteadorA.colaLlamadas.append(call) 
			ruteadorA.llamadasEnCola += 1
		# si esta el ruteador desocupado, podemos programar la salida
		if not ruteadorA.ocupado:
			# generamos el tipo
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			call.tipo = tipoLlamada
			ruteadorA.ocupado = True
			# generamos el tiempo de atención depenediendo del tipo
			if tipoLlamada == 1:
				call.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
				self.SA = self.reloj + call.tiempoAtencion
			else: 
				call.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
				self.SA = self.reloj + call.tiempoAtencion
		# reprogramamos el evento de arribo
		self.LA = self.reloj + ruteadorA.generarTiempoArriboA()

	def arriboB(self, ruteadorB):
		self.reloj = self.LB
		call = llamada.Llamada(self.reloj)
		# B solo recibe llamadas locales directamente
		call.tipo = 2
		ruteadorB.llamadasRecibidas += 1
		ruteadorB.llamadasLocalesB += 1
		# introducimos la llamada a la cola de B
		ruteadorB.colaLlamadas.append(call) 
		ruteadorB.llamadasEnCola += 1 
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		# si esta el ruteador desocupado, programamos la salida
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			call.tiempoAtencion = ruteadorB.generarTiempoTipo2B() 
			if self.SB == INFINITO:
				self.SB = self.reloj + call.tiempoAtencion
		# reprogramamos el evento de arribo
		self.LB = self.reloj + ruteadorB.generarTiempoArriboB()

	def salidaA(self, ruteadorA):
		self.reloj = self.SA
		# hay una salida, se desprograma el evento y se desocupa el ruteador
		self.SA = INFINITO
		ruteadorA.ocupado = False
		ruteadorA.llamadasEnCola -= 1
		ruteadorA.llamadasRuteadas += 1
		# sacamos la llamada de la cola de A ( pop(0) saca la llamada al inicio de la cola, osea, con índice 0)
		call = ruteadorA.colaLlamadas.pop(0)
		# si la llamada es local, aumentamos un contador necesario para estadísticas (porcentaje de perdidas por B)
		if call.tipo == 2:
			ruteadorA.llamadasRuteadasLocales += 1
		call.horaDeSalida = self.reloj
		ruteadorA.tiempoTotalCola += call.tiempoEnCola() 
		ruteadorA.tiempoPermanencia += call.tiempoEnSistema()
		# si hay llamadas en cola, programamos otra salida
		if ruteadorA.llamadasEnCola > 0:
			ruteadorA.ocupado = True
			# generamos el tipo de la llamada y la hora de salida respectiva
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			call.tipo = tipoLlamada
			if tipoLlamada == 1:
				call.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
				if self.SA == INFINITO:
					self.SA = self.reloj + call.tiempoAtencion
			else:
				call.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
				if self.SA == INFINITO:
					self.SA = self.reloj + call.tiempoAtencion
		

	def salidaB(self, ruteadorA, ruteadorB):
		self.reloj = self.SB
		# desprogramamos el evento y desocupamos el ruteador
		self.SB = INFINITO
		fuePerdida = False
		ruteadorB.ocupado = False
		ruteadorB.llamadasEnCola -= 1
		# sacamos la llamada de la cola
		call = ruteadorB.colaLlamadas.pop(0)
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola # Revisar si deberia estar despues del popeo
		call.horaDeSalida = self.reloj
		# si la cola de B es mayor a 4, hay probabilidad de que se pierda la llamada
		if ruteadorB.llamadasEnCola > 4 and random.uniform(0, 1) <= 0.1:
			fuePerdida = True
			ruteadorB.llamadasPerdidasB += 1
		# si no se perdió la llamada, se aumenta el contador de ruteadas
		if not fuePerdida:
			ruteadorB.llamadasRuteadas += 1
			# si es una llamada local, se aumenta un contador necesario para estadísticas
			if call.tipo == 2:
				ruteadorB.llamadasRuteadasLocales += 1	
			
			# si fue desviada, aumentamos contadores para estadísticas respectivamente
			if call.desviada == True:
				#call.horaDeArribo = call.horaDeSalida - call.tiempoAtencion
				ruteadorB.tiempoTotalColaDesviadas += call.tiempoEnCola()
				ruteadorB.tiempoTotalPermanenciaDesviadas += call.tiempoEnSistema()
				ruteadorB.llamadasRuteadasDesviadas += 1
			else:
				ruteadorB.tiempoTotalCola += call.tiempoEnCola()
				ruteadorB.tiempoPermanencia += call.tiempoEnSistema()
		# si hay mas llamadas en cola, programamos otra salida
		if ruteadorB.llamadasEnCola > 0:
			ruteadorB.ocupado = True
			# si la llamada que al inicio de la cola fue desviada, generamos su tipo según las probabilidades de A
			if ruteadorB.colaLlamadas[0].desviada == True:
				tipoLlamada = ruteadorA.generarTipoLlamadaA()
				ruteadorB.colaLlamadas[0].tipo = tipoLlamada
				# generamos la hora de salida según el tipo
				if tipoLlamada == 1:
					ruteadorB.colaLlamadas[0].tiempoAtencion = ruteadorB.generarTiempoTipo1B()
					if self.SB == INFINITO:
						self.SB = self.reloj + ruteadorB.colaLlamadas[0].tiempoAtencion
				else:
					ruteadorB.colaLlamadas[0].tiempoAtencion = ruteadorB.generarTiempoTipo2B()
					if self.SB == INFINITO:
						self.SB = self.reloj + ruteadorB.colaLlamadas[0].tiempoAtencion
			# si no fue desviada, se sabe que es local (tipo 2)
			else:
				ruteadorB.colaLlamadas[0].tiempoAtencion = ruteadorB.generarTiempoTipo2B()
				if self.SB == INFINITO:
					self.SB = self.reloj + ruteadorB.colaLlamadas[0].tiempoAtencion


	def desvioAB(self, ruteadorA, ruteadorB):
		self.reloj = self.DAB
		# sacamos la llamada de la cola de desvíos y la insertamos en la cola de B
		ruteadorB.colaLlamadas.append(self.colaDesvioAB.pop(0)) 
		ruteadorB.llamadasEnCola += 1
		ruteadorB.llamadasDesviadasAB += 1
		ruteadorB.llamadasRecibidas += 1
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		# si hay más llamadas en la cola de desviós, programamos otro desvío
		if len(self.colaDesvioAB) > 0:
			if self.DAB == INFINITO:
				self.DAB = self.colaDesvioAB[0].horaDeArribo + 0.5
		# si no hay más llamadas en la cola de desvíos, se desprograma el evento
		else:
			self.DAB = INFINITO
		# si el ruteador está desocupado, podemos programar una salida
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			# generamos el tipo según las probabilidades de A
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			call = ruteadorB.colaLlamadas[ruteadorB.llamadasEnCola-1]
			call.tipo = tipoLlamada
			# generamos la hora de salida según el ruteador B
			if tipoLlamada == 1:
				call.tiempoAtencion = ruteadorB.generarTiempoTipo1B()
				if self.SB == INFINITO:
					self.SB = self.reloj + call.tiempoAtencion
			else:
				call.tiempoAtencion = ruteadorB.generarTiempoTipo2B()
				if self.SB == INFINITO:
					self.SB = self.reloj + call.tiempoAtencion
		
		
	def imprimirDuranteSimulacion(self, reloj, ruteadorA, ruteadorB):
		print("")
		print("////////////////////////////// RESULTADOS DE EVENTO //////////////////////////////")
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
		print("Número llamadas perdidas por B:", ruteadorB.llamadasPerdidasB)

	def imprimirFinalCorrida(self, reloj, ruteadorA, ruteadorB, corrida):
		print("")
		print("////////////////////////////// RESULTADOS DE CORRIDA", corrida," //////////////////////////////")
		print("Tamaño prom. de la cola en B: ", ruteadorB.tamanoPondCola / reloj)
		print("")
		print("Tiempo prom. permanencia de una llamada en A: ", ruteadorA.tiempoPermanencia / ruteadorA.llamadasRuteadas )
		print("Tiempo prom. permanencia de una llamada en B: ", ruteadorB.tiempoPermanencia / (ruteadorB.llamadasRuteadas - ruteadorB.llamadasRuteadasDesviadas) ) 
		print("Tiempo prom. permanencia de una llamada desviada de A a B: ", ruteadorB.tiempoTotalPermanenciaDesviadas / ruteadorB.llamadasRuteadasDesviadas)
		print("")
		print("Tiempo prom. en cola de una llamada en A: ", ruteadorA.tiempoTotalCola / (ruteadorA.llamadasRecibidas - ruteadorB.llamadasDesviadasAB) )
		print("Tiempo prom. en cola de una llamada en B: ", ruteadorB.tiempoTotalCola / (ruteadorB.llamadasRecibidas - ruteadorB.llamadasDesviadasAB) )
		print("Tiempo prom. en cola de una llamada desviada de A a B: ", ruteadorB.tiempoTotalColaDesviadas / ruteadorB.llamadasDesviadasAB)
		print("")
		print("Porcentaje de llamadas perdidas por B :", ruteadorB.llamadasPerdidasB / ( ruteadorA.llamadasRuteadasLocales + ruteadorB.llamadasRuteadasLocales ) )
		print("Eficiencia A: ", (ruteadorA.tiempoTotalCola) / ruteadorA.tiempoPermanencia)
		print("Eficiencia B: ", (ruteadorB.tiempoTotalCola) / ruteadorB.tiempoPermanencia)
		print("Eficiencia desviadas A - B: ", (ruteadorB.tiempoTotalColaDesviadas) / ruteadorB.tiempoTotalPermanenciaDesviadas)

	def imprimirFinalSimulacion(self, estadisticasA, estadisticasB, estadisticasAB):
		print("")
		print("////////////////////////////// RESULTADOS DE SIMULACIÓN //////////////////////////////")
		print("Tamaño prom. de la cola en B: ", estadisticasB.tamanoColaTiempoB / estadisticasB.tiempoTotal)
		print("")
		print("Tiempo prom. permanencia de una llamada en A: ", estadisticasA.tiempoPermanenciaTotal / estadisticasA.llamadasRuteadasTotal )
		print("Tiempo prom. permanencia de una llamada en B: ", estadisticasB.tiempoPermanenciaTotal / (estadisticasB.llamadasRuteadasTotal - estadisticasAB.llamadasRuteadasTotal) )
		print("Tiempo prom. permanencia de una llamada desviada de A a B: ", estadisticasAB.tiempoPermanenciaTotal / estadisticasAB.llamadasRuteadasTotal)
		print("")
		print("Tiempo prom. en cola de una llamada en A: ", estadisticasA.tiempoColaTotal / (estadisticasA.llamadasRecibidasTotal - estadisticasAB.llamadasRecibidasTotal) )
		print("Tiempo prom. en cola de una llamada en B: ", estadisticasB.tiempoColaTotal / (estadisticasB.llamadasRecibidasTotal - estadisticasAB.llamadasRecibidasTotal) )
		print("Tiempo prom. en cola de una llamada desviada de A a B: ", estadisticasAB.tiempoColaTotal / estadisticasAB.llamadasRecibidasTotal)
		print("")
		print("Porcentaje de llamadas perdidas por B :", estadisticasB.llamadasPerdidasB / estadisticasB.llamadasLocalesAB )
		print("Eficiencia A: ", (estadisticasA.tiempoColaTotal) / estadisticasA.tiempoPermanenciaTotal)
		print("Eficiencia B: ", (estadisticasB.tiempoColaTotal) / estadisticasB.tiempoPermanenciaTotal)
		print("Eficiencia desviadas A - B: ", (estadisticasAB.tiempoColaTotal) / estadisticasAB.tiempoPermanenciaTotal)




