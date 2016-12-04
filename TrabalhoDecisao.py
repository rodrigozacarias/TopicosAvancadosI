#!/usr/bin/python
# -*- coding: UTF-8 -*-


from random import randint
from random import choice


def main():

	print "\nTrabalho de Tópicos Avançados I\n"

	print "Pesquisa: Preferência de Cidades\n"

	print "Determinar a ordem das cidades em que voce moraria, atribuindo notas de 0 a 10:"
	print "Sendo 10 para que você tem mais vontade de morar e 0 para que você tem menos vontade de morar\n"

	print "Resultados:\n"

	cidades=[
		'Rio de Janeiro',
		'São Paulo',
		'Belo Horizonte',
		'Brasília',
		'Salvador',
		'Curitiba',
		'Porto Alegre',
		'Fortaleza',
		'Manaus',
		'Goiânia'
		]

	nLinhas= 10
	nColunas = 10
	
	vetorPesos=[0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.15, 0.15, 0.15, 0.15]
	#Peso 0.05 - Pessoas que vivem no interior
	#Peso 0.1 - Pessoas que vivem em cidade grande
	#Peso 0.15 - Pessoas que vivem em uma das cidades da pesquisa

	#indice de concordancia
	c = 0.55
	#indice de discordancia
	d = 0.45
	#limite de preferência
	p = 3.5
	#limite de indiferença
	q = 2.0
	#limite de veto
	v = 1.5

	tabela = geraTabelaPagamento(nLinhas, nColunas)
		
	for i in range(nLinhas):
		print tabela[i], cidades[i]

	tecnicaNominalGrupo(cidades, tabela, nLinhas)

	media(cidades, tabela, nLinhas)

	mediaPonderada(cidades, tabela, nLinhas, vetorPesos)

	mediaWindsor(cidades, tabela, nLinhas)

	print "\nMétodo Electre I\n"

	mConcordanciaI = matrizConcordanciaI(cidades, tabela, nLinhas, nColunas, vetorPesos)

	mDiscordanciaI = matrizDiscordanciaI(cidades, tabela, nLinhas, nColunas)

	calculaKernel(mConcordanciaI, mDiscordanciaI, c, d, nLinhas, cidades)

	print "\n\nMétodo Electre III\n"

	mConcordanciaIII = matrizConcordanciaIII(cidades, tabela, nLinhas, nColunas, vetorPesos, p, q)

	matrizDisconcordanciaIII(cidades, tabela, nLinhas, nColunas, vetorPesos, p, v)

	print "\n"

def geraTabelaPagamento(nLinhas, nColunas):
	matriz = []
	for i in range(nLinhas):
		linha = []
		for j in range(nColunas):
			achounumero = 0
			colunaatual = []
			for k in range(i):
				colunaatual.append(matriz[k][j])
			while (achounumero == 0):
				num = choice([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
				if num in colunaatual:
					continue
				else:
					achounumero = 1
			linha.append(num)
		matriz.append(linha)
	return matriz


def tecnicaNominalGrupo(cidades, tabela, nLinhas):
	print "\nTécnica Nominal de Grupo\n"

	print "Total de Valores\n"
	maiorValor = 0
	indiceMaiorValor = 0

	for i in range(nLinhas):
		somaLinha = 0
		#somaValores = []
		for j in range(len(tabela[i])):
			somaLinha +=tabela[i][j]
		#somaValores.append(somaLinha)
		if somaLinha > maiorValor:
			maiorValor = somaLinha
			indiceMaiorValor = i
		print cidades[i], "=", somaLinha
	print "\nA maior preferência é para a cidade de", cidades[indiceMaiorValor], "com valor de", maiorValor


def media(cidades, tabela, nLinhas):
	print "\nMédias\n"

	for i in range(nLinhas):
		somaTotal = 0
		for j in range(len(tabela[i])):
			somaTotal += tabela[i][j]
		media = somaTotal/len(tabela[i])
		print cidades[i], " = ", media

def mediaPonderada(cidades, tabela, nLinhas, vetorPesos):
	print "\nMédias Ponderadas\n"
		
	somaPesos = 0

	for x in range(len(vetorPesos)):
		somaPesos += vetorPesos[x]

	for i in range(nLinhas):
		somaValorDividendo = 0
		for j in range(len(tabela[i])):
			somaValorDividendo += tabela[i][j]*vetorPesos[j]
			#print tabela[i][j], vetorPesos[j]
		mediaPonderada = somaValorDividendo/somaPesos
		print cidades[i], " = ", format(mediaPonderada)



def mediaWindsor(cidades, tabela, nLinhas):
	print "\nMédias de Windsor\n"

	for i in range(nLinhas):
		somaTotal = 0
		linhaOrdenada = []
		qtdeElementos = -1
		for j in range(len(tabela[i])):
			linhaOrdenada.append(tabela[i][j])
			qtdeElementos += 1
		linhaOrdenada.sort()
		#print linhaOrdenada
		linhaOrdenada.pop(qtdeElementos)
		linhaOrdenada.pop(0)
		#print linhaOrdenada
		#print len(linhaOrdenada)
		for k in range(len(linhaOrdenada)):
			somaTotal += linhaOrdenada[k];
		mediaWindsor = somaTotal/len(linhaOrdenada)
		print cidades[i], " = ", mediaWindsor

def matrizConcordanciaI(cidades, tabela, nLinhas, nColunas, vetorPesos):
	print "\nMatriz de Concordância\n"

	somaPesos = 0
	mConcordancia = []

	for x in range(len(vetorPesos)):
		somaPesos += vetorPesos[x]

	#Laço para alternativa a ser comparada
	for i in range(nLinhas):
		linha = []		
		#Laço para o criterio a ser comparado
		for j in range(len(tabela[i])):
			#Laço para percorrer matriz
			somatorioW = 0
			for y in range(nColunas):
				if tabela[i][y] >= tabela[j][y]:
					somatorioW += vetorPesos[y]
			result = 1.0/somaPesos * somatorioW
			linha.append(round(result, 2))
			#print result
		mConcordancia.append(linha)
		print mConcordancia[i], cidades[i]
	return mConcordancia

def matrizDiscordanciaI(cidades, tabela, nLinhas, nColunas):
	print "\nMatriz de Discordância\n"

	#Calculando a diferença entre o maior e menor valor de cada criterio
	vetorDiferencas = []

	for i in range(nLinhas):
		valoresCriterio = []
		for j in range(len(tabela[i])):
			valoresCriterio.append(tabela[j][i])
		valorMin = min(valoresCriterio)
		valorMax = max(valoresCriterio)
		result = valorMax - valorMin
		vetorDiferencas.append(result)
	#print vetorDiferencas

	#Calculando Matriz de Discordancia
	mDiscordancia = []

	#Laço para alternativa a ser comparada
	for i in range(nLinhas):
		linha = []
		#Laço para o criterio a ser comparado
		for j in range(len(tabela[i])):
			#Laço para percorrer matriz
			vetorIndices = []
			for y in range(nColunas):
				vResultante = (tabela[j][y] - tabela[i][y])/vetorDiferencas[y]
				#print vResultante
				vetorIndices.append(round(vResultante, 2))
			linha.append(max(vetorIndices))
		mDiscordancia.append(linha)
		print mDiscordancia[i], cidades[i]
	return mDiscordancia

def calculaKernel(mConcordanciaI, mDiscordanciaI, c, d, nLinhas, cidades):
	print "\nMatriz de Veto\n"

	matrizVeto = []

	#Preenchendo matriz veto
	for i in range(nLinhas):
		linha = []
		for j in range(len(mConcordanciaI[i])):
			if (mConcordanciaI[i][j] >= c) and (mDiscordanciaI[i][j] <= d):
				linha.append(1)
			else:
				linha.append(0)
		matrizVeto.append(linha)
		print matrizVeto[i], cidades[i]

	matrizSobreclassifica = []

	#identificando as sobreclassificações
	for i in range(nLinhas):
		linha = []
		for j in range(len(matrizVeto[i])):
			if matrizVeto[i][j] == 1 and i!=j:
				linha.append(j)
		matrizSobreclassifica.append(linha)
		#print matrizSobreclassifica[i]

	kernel = []

	print "\nKernel\n"

	for k in range(nLinhas):
		achou = False
		vazio = False
		for i in range(nLinhas):
			for j in range(len(matrizSobreclassifica[i])):
				if matrizSobreclassifica[i][j] == k:
					achou = True
				if not matrizSobreclassifica[i]:
					vazio = True	
		#print vazio
		if (achou == False) and (vazio == False):
			print cidades[k]
	

def matrizConcordanciaIII(cidades, tabela, nLinhas, nColunas, vetorPesos, p, q):
	print "\nMatriz de Concordância Global\n"

	somaPesos = 0
	mConcordancia = []

	for x in range(len(vetorPesos)):
		somaPesos += vetorPesos[x]

	#Laço para alternativa a ser comparada
	for i in range(nLinhas):
		linha = []		
		#Laço para o criterio a ser comparado
		for j in range(len(tabela[i])):
			#Laço para percorrer matriz
			somatorioW = 0
			for y in range(nColunas):
				valor = 0
				if tabela[i][y] > (tabela[j][y] - q):
					valor = 1
				else: 
					if tabela[i][y] <= (tabela[j][y] - p):
						valor = 0
						#print tabela[i][y], tabela[j][y], q, tabela[j][y] - q
					else: 
						somatorioW += vetorPesos[y] * ((p-(tabela[i][y]- tabela[j][y]))/p-q)
				if valor == 1:
					somatorioW += vetorPesos[y]
			result = 1.0/somaPesos * somatorioW
			linha.append(round(result, 2))
			#print result
		mConcordancia.append(linha)
		print mConcordancia[i], cidades[i]
	return mConcordancia

def matrizDisconcordanciaIII(cidades, tabela, nLinhas, nColunas, vetorPesos, p, v):
	print "\nMatrizes de Discordância  por Critério\n"

	#Laço para alternativa a ser comparada
	for i in range(nLinhas):
		mDiscordancia = []	
		print "\nEntrevistado",i+1
		#Laço para o criterio a ser comparado
		for j in range(len(tabela[i])):
			linha = []
			#Laço para percorrer matriz
			for y in range(nColunas):
				if tabela[i][y] > (tabela[j][y] - p):
					linha.append(0)
				else: 
					if tabela[i][y] < (tabela[j][y] - v):
						linha.append(1)
						#print tabela[i][y], tabela[j][y], q, tabela[j][y] - q
					else: 
						result = ((tabela[i][y] - tabela[j][y] - p)/v-p)
						linha.append(round(result, 2))
			#print result
			mDiscordancia.append(linha)
		
		for x in range(len(mDiscordancia[j])):
			print mDiscordancia[x], cidades[x]

main()