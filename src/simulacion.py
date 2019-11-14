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
				#print("Eventos:", self.LA, self.LB, self.SA, self.SB, self.DAB)
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

				if self.modoLento:
					self.imprimirDuranteSimulacion(self.reloj, ruteadorA, ruteadorB)
					time.sleep(self.delay)

			"""
				Estas estadisticas finales creo que deberian estar dentro del for de iteraciones y
				luego dividirlas entre iteraciones totales para imprimir estadisticas promedio al
				 final de la simulacion
																									"""

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
			estadisticasAB.llamadasRuteadasTotal += ruteadorB.tiempoTotalPermanenciaDesviadas

			
			self.imprimirFinalCorrida(self.reloj, ruteadorA, ruteadorB, iteracion)
			time.sleep(self.delay)
		self.imprimirFinalSimulacion(estadisticasA, estadisticasB, estadisticasAB)

	def arriboA(self, ruteadorA):
		self.reloj = self.LA
		call = llamada.Llamada(self.reloj)
		ruteadorA.llamadasRecibidas += 1
		if ruteadorA.llamadasEnCola >= 5: # Desvio
			call.setDesviada(True)
			self.colaDesvioAB.append(call)
			tiempoDesvio = self.colaDesvioAB[0].horaDeArribo +  0.5 
			if self.DAB == INFINITO: # Si esta desprogramado
				self.DAB = tiempoDesvio
		else:
			#ruteadorA.llamadasRecibidas += 1
			ruteadorA.colaLlamadas.append(call) 
			ruteadorA.llamadasEnCola += 1
		if not ruteadorA.ocupado:
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			call.tipo = tipoLlamada
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
		call.tipo = 2
		ruteadorB.llamadasRecibidas += 1
		ruteadorB.llamadasLocalesB += 1
		ruteadorB.colaLlamadas.append(call) 
		ruteadorB.llamadasEnCola += 1 
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			call.tiempoAtencion = ruteadorB.generarTiempoTipo2B() 
			if self.SB == INFINITO:
				self.SB = self.reloj + call.tiempoAtencion
		self.LB = self.reloj + ruteadorB.generarTiempoArriboB()
		#print("Lapso arribos: ", self.LB - self.reloj)

	def salidaA(self, ruteadorA):
		self.reloj = self.SA
		self.SA = INFINITO
		ruteadorA.ocupado = False
		ruteadorA.llamadasEnCola -= 1
		ruteadorA.llamadasRuteadas += 1
		call = ruteadorA.colaLlamadas.pop(0)
		if call.tipo == 2:
			ruteadorA.llamadasRuteadasLocales += 1
		call.horaDeSalida = self.reloj
		ruteadorA.tiempoTotalCola += call.tiempoEnCola() 
		ruteadorA.tiempoPermanencia += call.tiempoEnSistema()
		if ruteadorA.llamadasEnCola > 0:
			ruteadorA.ocupado = True
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
		self.SB = INFINITO
		fuePerdida = False
		ruteadorB.ocupado = False
		ruteadorB.llamadasEnCola -= 1
		call = ruteadorB.colaLlamadas.pop(0)
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola # Revisar si deberia estar despues del popeo
		call.horaDeSalida = self.reloj
		if ruteadorB.llamadasEnCola > 4 and random.uniform(0, 1) <= 0.1:
			fuePerdida = True
			ruteadorB.llamadasPerdidasB += 1
		if not fuePerdida:
			ruteadorB.llamadasRuteadas += 1
			if call.tipo == 2 and not call.desviada:
				ruteadorB.llamadasRuteadasLocales += 1	
					
			if call.desviada == True:
				call.horaDeArribo = call.horaDeSalida - call.tiempoAtencion
				ruteadorB.tiempoTotalColaDesviadas += call.tiempoEnCola() #+ 0.5
				ruteadorB.tiempoTotalPermanenciaDesviadas += call.tiempoEnSistema() #+ 0.5
				ruteadorB.llamadasRuteadasDesviadas += 1
			else:
				ruteadorB.tiempoTotalCola += call.tiempoEnCola()
				ruteadorB.tiempoPermanencia += call.tiempoEnSistema()
			#ruteadorB.tiempoTotalCola += call.tiempoEnCola()
			#ruteadorB.tiempoPermanencia += call.tiempoEnSistema()
			#print("Arribo:", call.horaDeArribo, "Salida: ", call.horaDeSalida)
		print("Dios: ", ruteadorB.llamadasRecibidas, ruteadorB.llamadasRuteadas)
		if ruteadorB.llamadasEnCola > 0:
			ruteadorB.ocupado = True
			if ruteadorB.colaLlamadas[0].desviada == True:
				tipoLlamada = ruteadorA.generarTipoLlamadaA()
				ruteadorB.colaLlamadas[0].tipo = tipoLlamada
				if tipoLlamada == 1:
					ruteadorB.colaLlamadas[0].tiempoAtencion = ruteadorB.generarTiempoTipo1B()
					if self.SB == INFINITO:
						self.SB = self.reloj + ruteadorB.colaLlamadas[0].tiempoAtencion
				else:
					ruteadorB.colaLlamadas[0].tiempoAtencion = ruteadorB.generarTiempoTipo2B()
					if self.SB == INFINITO:
						self.SB = self.reloj + ruteadorB.colaLlamadas[0].tiempoAtencion
			else: # Generar tipo 2
				ruteadorB.colaLlamadas[0].tiempoAtencion = ruteadorB.generarTiempoTipo2B()
				if self.SB == INFINITO:
					self.SB = self.reloj + ruteadorB.colaLlamadas[0].tiempoAtencion


	def desvioAB(self, ruteadorA, ruteadorB):
		self.reloj = self.DAB
		#self.colaDesvioAB[0].horaDeArribo = self.reloj
		ruteadorB.colaLlamadas.append(self.colaDesvioAB.pop(0)) 
		ruteadorB.llamadasEnCola += 1
		ruteadorB.llamadasDesviadasAB += 1
		ruteadorB.llamadasRecibidas += 1
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if len(self.colaDesvioAB) > 0:
			if self.DAB == INFINITO:
				self.DAB = self.colaDesvioAB[0].horaDeArribo + 0.5
		else:
			self.DAB = INFINITO
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			call = ruteadorB.colaLlamadas[ruteadorB.llamadasEnCola-1]
			call.tipo = tipoLlamada
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
		# si no se han ruteado llamadas, evitamos dividir por 0
		if ruteadorA.llamadasRuteadas == 0:
			ruteadorA.llamadasRuteadas = 0.1 
		if ruteadorB.llamadasRuteadas == 0:
			ruteadorB.llamadasRuteadas = 0.1 
		if ruteadorA.tiempoPermanencia == 0:
			ruteadorA.tiempoPermanencia = 0.1 
		if ruteadorB.tiempoPermanencia == 0:
			ruteadorB.tiempoPermanencia = 0.1 
		if ruteadorB.tiempoTotalPermanenciaDesviadas == 0:
			ruteadorB.tiempoTotalPermanenciaDesviadas = 0.1 
		print("")
		print("////////////////////////////// RESULTADOS DE CORRIDA", corrida," //////////////////////////////")
		print("Tamaño prom. de la cola en B: ", ruteadorB.tamanoPondCola / reloj)
		print("")
		print("Tiempo prom. permanencia de una llamada en A: ", ruteadorA.tiempoPermanencia / ruteadorA.llamadasRuteadas)
		print("Tiempo prom. permanencia de una llamada en B: ", ruteadorB.tiempoPermanencia / ruteadorB.llamadasRuteadas)
		print("Tiempo prom. permanencia de una llamada desviada de A a B: ", ruteadorB.tiempoTotalPermanenciaDesviadas / ruteadorB.llamadasRuteadasDesviadas)
		print("")
		print("Tiempo prom. en cola de una llamada en A: ", ruteadorA.tiempoTotalCola / (ruteadorA.llamadasRecibidas - ruteadorB.llamadasDesviadasAB))
		print("Tiempo prom. en cola de una llamada en B: ", ruteadorB.tiempoTotalCola / ruteadorB.llamadasRecibidas)
		print("Tiempo prom. en cola de una llamada desviada de A a B: ", ruteadorB.tiempoTotalColaDesviadas / ruteadorB.llamadasDesviadasAB)
		print("")
		print("Porcentaje de llamadas perdidas por B :", ruteadorB.llamadasPerdidasB / ( ruteadorA.llamadasRuteadasLocales + ruteadorB.llamadasRuteadasLocales ) )
		print("Eficiencia A: ", (ruteadorA.tiempoTotalCola) / ruteadorA.tiempoPermanencia)
		print("Eficiencia B: ", (ruteadorB.tiempoTotalCola) / ruteadorB.tiempoPermanencia)
		print("Eficiencia desviadas A - B: ", (ruteadorB.tiempoTotalColaDesviadas) / ruteadorB.tiempoTotalPermanenciaDesviadas)

	def imprimirFinalSimulacion(self, estadisticasA, estadisticasB, estadisticasAB):
		# si no se han ruteado llamadas, evitamos dividir por 0
		if estadisticasA.llamadasRuteadasTotal == 0:
			estadisticasA.llamadasRuteadasTotal = 0.01 
		if estadisticasB.llamadasRuteadasTotal == 0:
			estadisticasB.llamadasRuteadasTotal = 0.1 
		if estadisticasA.tiempoPermanenciaTotal == 0:
			estadisticasA.tiempoPermanenciaTotal = 0.1 
		if estadisticasB.tiempoPermanenciaTotal == 0:
			ruteadorB.tiempoPermanenciaTotal = 0.1 
		if estadisticasB.tiempoPermanenciaTotal == 0:
			estadisticasB.tiempoPermanenciaTotal = 0.1 
		print("")
		print("////////////////////////////// RESULTADOS DE SIMULACIÓN //////////////////////////////")
		print("Tamaño prom. de la cola en B: ", estadisticasB.tamanoColaTiempoB / estadisticasB.tiempoTotal)
		print("")
		print("Tiempo prom. permanencia de una llamada en A: ", estadisticasA.tiempoPermanenciaTotal / estadisticasA.llamadasRuteadasTotal)
		print("Tiempo prom. permanencia de una llamada en B: ", estadisticasB.tiempoPermanenciaTotal / estadisticasB.llamadasRuteadasTotal)
		print("Tiempo prom. permanencia de una llamada desviada de A a B: ", estadisticasAB.tiempoPermanenciaTotal / estadisticasAB.llamadasRuteadasTotal)
		print("")
		print("Tiempo prom. en cola de una llamada en A: ", estadisticasA.tiempoColaTotal / estadisticasA.llamadasRecibidasTotal)
		print("Tiempo prom. en cola de una llamada en B: ", estadisticasB.tiempoColaTotal / estadisticasB.llamadasRecibidasTotal)
		print("Tiempo prom. en cola de una llamada desviada de A a B: ", estadisticasAB.tiempoColaTotal / estadisticasAB.llamadasRecibidasTotal)
		print("")
		print("Porcentaje de llamadas perdidas por B :", estadisticasB.llamadasPerdidasB / estadisticasB.llamadasLocalesAB )
		print("Eficiencia A: ", (estadisticasA.tiempoColaTotal) / estadisticasA.tiempoPermanenciaTotal)
		print("Eficiencia B: ", (estadisticasB.tiempoColaTotal) / estadisticasB.tiempoPermanenciaTotal)
		print("Eficiencia desviadas A - B: ", (estadisticasAB.tiempoColaTotal) / estadisticasAB.tiempoPermanenciaTotal)




