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

	# Necesaria para no superponer llamadas
	# (un desvío podría darse después del otros
	# y se perdería la anterior)
	colaDesvioAB = []

	# ubicamos los ruteadores aca para lo eventos puedan acceder a ellos
	ruteadorA = ruteador.RuteadorA()
	ruteadorB = ruteador.RuteadorB()

	def __init__(self, iteraciones, tiempoMaximo, modoLento = False, delay = 0):
		self.iteraciones = iteraciones
		self.tiempoMaximo = tiempoMaximo
		self.modoLento = modoLento
		self.delay = delay

	def iniciar(self):

		esdisticasA = estadisticas.Estadisticas()
		estadisticasB = estadisticas.EstadisticasB()
		estadisticasAB = estadisticas.Estadisticas()

		for iteracion in range(self.iteraciones):
			# se reinician variables
			self.reloj = 0.0
			self.LA = 0.0
			self.LB = 0.0
			self.SA = INFINITO
			self.SB = INFINITO
			self.DAB = INFINITO
			ruteadorA = ruteador.RuteadorA()
			ruteadorB = ruteador.RuteadorB()
			
			while(self.reloj < self.tiempoMaximo):
			# min es una función de python
				proximo_evento = min(self.LA, self.LB, self.SA, self.SB, self.DAB)
				# python no posee "switch", con 5 condiciones esta bien usar ifs
				if  (proximo_evento == self.LA):
					self.arriboA()
				elif(proximo_evento == self.LB):
					self.arriboB()
				elif(proximo_evento == self.SA):
					self.salidaA()
				elif(proximo_evento == self.SB):
					self.salidaB()
				elif(proximo_evento == self.DAB):
					self.desvioAB()

				if(modoLento):
					time.sleep(self.delay)

			# se recopilan datos para estadisticas finales
			self.estadisticasA.tiempoTotal += self.reloj
			self.estadisticasB.tiempoTotal += self.reloj
			self.estadisticasA.tiempoTotal += self.reloj
		# ...

	def arriboA(self, ruteadorA):
		# Tener cuidado de olvidarnos sumar el 0.5 
		self.reloj = self.LA
		llamada = Llamada(self.reloj)
		ruteadorA.llamadasRecibidas += 1
		if ruteadorA.ocupado == True: 
			if len(ruteadorA.colaLlamadas) == 5: # Desvio
				tiempoDesvio = reloj + ruteadorA.generarTiempoDesvioAB()
				if self.DAB != INFINITO: # Si esta programado
					llamada.setDesviada(True)
					self.colaDesvioAB.append(llamada)
				else:  					# Si esta desprogramado
					self.DAB = tiempoDesvio
			else: 								 # No desvio
				ruteadorA.colaLlamadas.append(llamada) 
				ruteadorA.llamadasEnCola += 1
		else:
			ruteadorA.colaLlamadas.append(llamada) 
			ruteadorA.llamadasEnCola += 1
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			ruteadorA.ocupado = True
			if tipoLlamada == 1:
				llamada.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
				self.SA = reloj + llamada.tiempoAtencion
			else: 
				llamada.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
				self.SA = reloj + llamada.tiempoAtencion
		self.LA = ruteadorA.generarTiempoArriboA()

	def arriboB(self, ruteadorB):
		self.reloj = self.LB
		llamada = Llamada(self.reloj)
		ruteadorB.colaLlamadas.append(llamada) 
		ruteadorB.llamadasEnCola += 1 
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			llamada.tiempoAtencion = ruteadorB.generarTiempoTipo2B() 
			self.SB = self.reloj + llamada.tiempoAtencion
		self.LB = ruteadorB.generarTiempoArriboB()

	def salidaA(self, ruteadorA):
		self.reloj = self.SA
		self.SA = INFINITO
		ruteadorA.ocupado = False
		ruteadorA.llamadasEnCola -= 1
		llamada = ruteadorA.colaLlamadas.pop(0)
		llamada.horaDeSalida = self.reloj
		ruteadorA.tiempoTotalCola += llamada.tiempoEnCola() 
		ruteadorA.tiempoPermanencia += llamada.tiempoEnSistema()
		if len(ruteadorA.colaLlamadas) > 0:
			ruteadorA.ocupado = True
			ruteadorA.llamadasRuteadas += 1
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			if tipoLlamada == 1:
				llamada.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
				self.SA = self.reloj + llamada.tiempoAtencion
			else:
				llamada.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
				self.SA = self.reloj + llamada.tiempoAtencion
		

	def salidaB(self, ruteadorA, ruteadorB):
		self.reloj = self.SB
		self.SB = INFINITO
		ruteadorB.ocupado = False
		ruteadorB.llamadasEnCola -= 1
		llamada = ruteadorB.colaLlamadas.pop(0)
		llamada.horaDeSalida = self.reloj
		if llamada.desviada == True: 
			ruteadorB.tiempoTotalColaDesviadas += llamada.tiempoEnCola()
			ruteadorB.tiempoTotalPermanenciaDesviadas += llamada.tiempoEnSistema()
		else:
			ruteadorB.tiempoTotalCola += llamada.tiempoEnCola()
			ruteadorB.tiempoPermanencia += llamada.tiempoEnSistema()
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		if len(ruteadorB.colaLlamadas) > 0:
			ruteadorB.ocupado = True
			ruteadorB.llamadasRuteadas += 1
			if len(ruteadorB.colaLlamadas) > 4:
				if random.uniform(0, 1) <= 0.1:
					ruteadorB.llamadasRuteadas -= 1
					ruteadorB.llamadaPerdidas += 1
			if llamada.desviada == True:
				tipoLlamada = ruteadorA.generarTipoLlamadaA()
				if tipoLlamada == 1:
					llamada.tiempoAtencion = ruteadorA.generarTiempoTipo1A()
					self.SB = self.reloj + llamada.tiempoAtencion
				else:
					llamada.tiempoAtencion = ruteadorA.generarTiempoTipo2A()
					self.SB = self.reloj + llamada.tiempoAtencion
			else: # Generar tipo 2
				llamada.tiempoAtencion = ruteadorB.generarTiempoTipo2B()
				self.SB = self.reloj + llamada.tiempoAtencion

	def desvioAB(self, ruteadorA, ruteadorB):
		self.reloj = self.DAB
		ruteadorB.colaLlamadas.append(self.colaDesvioAB.pop(0)) 
		ruteadorB.llamadasEnCola += 1
		ruteadorB.tamanoPondCola += ruteadorB.obtTiempoUltimoCambio(self.reloj) * ruteadorB.llamadasEnCola
		self.DAB = INFINITO
		if ruteadorB.ocupado == False:
			ruteadorB.ocupado = True
			tipoLlamada = ruteadorA.generarTipoLlamadaA()
			if tipoLlamada == 1:
				self.SB = self.reloj + ruteadorA.generarTiempoTipo1A()
			else:
				self.SB = self.reloj + ruteadorA.generarTiempoTipo2A()
		if len(self.colaDesvioAB) > 0:
			self.DAB = self.colaDesvioAB[0].horaDeArribo0 + 0.5
		
		
	





