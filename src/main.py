import simulacion

# Programa principal
iteraciones = int( input("Ingrese número de iteraciones: ") )
tiempoMaximo = float( input("Ingrese tiempo máximo para las iteraciones: ") )
modo = int( input("Ingrese 0 (modo lento) o 1 (modo normal): ") )
modoLento = False
delay = 0
if (modo == 0):
	modoLento = True
if (modoLento):
	delay = int( input("Ingrese delay (segundos): ") )
	simul= simulacion.Simulacion(iteraciones, tiempoMaximo, modoLento, delay)
else:
	simul = simulacion.Simulacion(iteraciones, tiempoMaximo)
iniciar = input("Presione Enter para iniciar la simulación")
simul.iniciar()