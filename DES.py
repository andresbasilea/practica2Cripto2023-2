
import fileinput


sBoxS0 = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]
sBoxS1 = [[0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]


def Subkeys(clave):
	claveLst = []
	for c in clave:
		claveLst.append(c)

	claveLstPermutada = [None] * 10  
	claveLstPermutada[0] = claveLst[2]
	claveLstPermutada[1] = claveLst[4]
	claveLstPermutada[2] = claveLst[1]
	claveLstPermutada[3] = claveLst[6]
	claveLstPermutada[4] = claveLst[3]
	claveLstPermutada[5] = claveLst[9]
	claveLstPermutada[6] = claveLst[0]
	claveLstPermutada[7] = claveLst[8]
	claveLstPermutada[8] = claveLst[7]
	claveLstPermutada[9] = claveLst[5]

	claveLstPermutada1 = claveLstPermutada[0:5]
	claveLstPermutada2 = claveLstPermutada[5:10]

	# Round 1

	subkey_ = Shift(claveLstPermutada1, 1)
	subkey__ = Shift(claveLstPermutada2, 1)
	subkey_ = subkey_ + subkey__ 
	subkeytmp1 = []
	for c in subkey_:
		subkeytmp1.append(c)


	subkey1 = [None] * 8
	subkey1[0] = subkeytmp1[5]
	subkey1[1] = subkeytmp1[2]
	subkey1[2] = subkeytmp1[6]
	subkey1[3] = subkeytmp1[3]
	subkey1[4] = subkeytmp1[7]
	subkey1[5] = subkeytmp1[4]
	subkey1[6] = subkeytmp1[9]
	subkey1[7] = subkeytmp1[8]
	
	# Round 2

	subkey___ = Shift(subkey_[0:5],2)
	subkey____ = Shift(subkey_[5:10],2)
	subkey___ = subkey___ + subkey____
	subkeytmp2 = []
	for c in subkey___:
		subkeytmp2.append(c)

	subkey2 = [None] * 8
	subkey2[0] = subkeytmp2[5]
	subkey2[1] = subkeytmp2[2]
	subkey2[2] = subkeytmp2[6]
	subkey2[3] = subkeytmp2[3]
	subkey2[4] = subkeytmp2[7]
	subkey2[5] = subkeytmp2[4]
	subkey2[6] = subkeytmp2[9]
	subkey2[7] = subkeytmp2[8]

	return subkey1, subkey2


def Shift(arr, n):
	nc = ""
	for i in range(n):
		for j in range(1,len(arr)):
			nc = nc + arr[j]
		nc = nc + arr[0]	
		arr = nc
		nc = ""

	return arr	


def Mixing(subkey, mensajePermutado):
	mensajePermutado2 = []
	for x in mensajePermutado[4:8]:
		mensajePermutado2.append(x)
	# print(mensajePermutado2)
	mensajePermutadoExpanded = [None] * 8
	mensajePermutadoExpanded[0] = mensajePermutado2[3]
	mensajePermutadoExpanded[1] = mensajePermutado2[0]
	mensajePermutadoExpanded[2] = mensajePermutado2[1]
	mensajePermutadoExpanded[3] = mensajePermutado2[2]
	mensajePermutadoExpanded[4] = mensajePermutado2[1]
	mensajePermutadoExpanded[5] = mensajePermutado2[2]
	mensajePermutadoExpanded[6] = mensajePermutado2[3]
	mensajePermutadoExpanded[7] = mensajePermutado2[0]
	# print("mensaje permutado expanded: ", mensajePermutadoExpanded)

	ssk = ""
	for c in subkey:
		ssk = ssk + c


	smpe = ""
	for c in mensajePermutadoExpanded:
		smpe = smpe + c

	# print("subkey: ", ssk, "mensajePermutadoExpanded: ", smpe)

	XOR = int(ssk,2) ^ int(smpe,2)
	
	XOR = format(XOR,'08b')
	# print("XOR subkey y mensajePermutadoExpanded",XOR)

	XOR1 = XOR[0:4]
	# print("First four bits of XOR for S0: ", XOR1)
	XOR2 = XOR[4:8]
	# print("Last four bits of XOR for S1: ", XOR2)

	row1 = XOR1[0] + XOR1[3]
	# print('row1', row1)
	col1 = XOR1[1:3]
	# print("col1", col1)
	row2 = XOR2[0] + XOR2[3]
	# print("row2", row2)
	col2 = XOR2[1:3]
	# print("col2", col2)


	sBoxS0Val = sBoxS0[int(row1,2)][int(col1,2)]
	sBoxS1Val = sBoxS1[int(row2,2)][int(col2,2)]
	binsBoxS0val = format(sBoxS0Val,'02b')
	binsBoxS1val = format(sBoxS1Val,'02b')
	# print("s0",binsBoxS0val)
	# print("s1",binsBoxS1val)
	concatS0S1 = str(binsBoxS0val) + str(binsBoxS1val)
	# print(concatS0S1)

	concatS0S1Lst = []
	for c in concatS0S1:
		concatS0S1Lst.append(c)

	concatS0S1Permut = [None] * 4
	concatS0S1Permut[0] = concatS0S1Lst[1]
	concatS0S1Permut[1] = concatS0S1Lst[3]
	concatS0S1Permut[2] = concatS0S1Lst[2]
	concatS0S1Permut[3] = concatS0S1Lst[0]

	scs0s1p = ""
	for c in concatS0S1Permut:
		scs0s1p = scs0s1p + c

	smp = ""
	for c in mensajePermutado[0:4]:
		smp = smp + c

		
	XORs0s1permutLeftHalf = int(scs0s1p,2) ^ int(smp,2)

	output = format(XORs0s1permutLeftHalf,'04b')
	# print(output)
	return output

def InitialPermutation(mensaje):
	mensajeLst = []
	for c in mensaje:
		mensajeLst.append(c)

	mensajeLstPermutado = [None] * 8

	mensajeLstPermutado[0] = mensajeLst[1]
	mensajeLstPermutado[1] = mensajeLst[5]
	mensajeLstPermutado[2] = mensajeLst[2]
	mensajeLstPermutado[3] = mensajeLst[0]
	mensajeLstPermutado[4] = mensajeLst[3]
	mensajeLstPermutado[5] = mensajeLst[7]
	mensajeLstPermutado[6] = mensajeLst[4]
	mensajeLstPermutado[7] = mensajeLst[6]

	return mensajeLstPermutado

def InversePermutation(mensaje):
	mensajeLst = []
	for c in mensaje:
		mensajeLst.append(c)

	mensajeLstPermutado = [None] * 8

	mensajeLstPermutado[0] = mensajeLst[3]
	mensajeLstPermutado[1] = mensajeLst[0]
	mensajeLstPermutado[2] = mensajeLst[2]
	mensajeLstPermutado[3] = mensajeLst[4]
	mensajeLstPermutado[4] = mensajeLst[6]
	mensajeLstPermutado[5] = mensajeLst[1]
	mensajeLstPermutado[6] = mensajeLst[7]
	mensajeLstPermutado[7] = mensajeLst[5]

	return mensajeLstPermutado


if __name__ == '__main__':
	lines = []
	for line in fileinput.input():
		lines.append(line.rstrip("\n"))
	if "E" in lines[0]:
		#cifrar
		subkey1, subkey2 = Subkeys(lines[1])
		mensajePermutado = InitialPermutation(lines[2])
		# print("initial permutation: ", mensajePermutado)
		mix1 = Mixing(subkey1, mensajePermutado) # Step 2
		
		strConcatStep2 = ""
		for c in mensajePermutado[4:8]:
			strConcatStep2 = strConcatStep2 + c
		strStep3 = strConcatStep2+mix1 #Step 3
		# print(strStep3)

		mix2 = Mixing(subkey2, strStep3)
		# print("mix2", mix2)
		strConcatStep4 = ""
		for c in strStep3[4:8]:
			strConcatStep4 = strConcatStep4 + c
		strConcatStep4 = mix2 + strConcatStep4
		# print("paso 4: ", strConcatStep4)

		encrypted = InversePermutation(strConcatStep4)
		print(''.join(encrypted))
		# print("encrypted", encrypted)

	if "D" in lines[0]:
		#descifrar
		subkey1, subkey2 = Subkeys(lines[1])
		mensajePermutado = InitialPermutation(lines[2])
		
		mix1 = Mixing(subkey2, mensajePermutado) # Step 2
		
		strConcatStep2 = ""
		for c in mensajePermutado[4:8]:
			strConcatStep2 = strConcatStep2 + c
		strStep3 = strConcatStep2+mix1 #Step 3
		# print(strStep3)

		mix2 = Mixing(subkey1, strStep3)
		# print("mix2", mix2)
		strConcatStep4 = ""
		for c in strStep3[4:8]:
			strConcatStep4 = strConcatStep4 + c
		strConcatStep4 = mix2 + strConcatStep4
		# print("paso 4: ", strConcatStep4)

		encrypted = InversePermutation(strConcatStep4)
		print(''.join(encrypted))

# Antes de enviar a alphagrader: 
#	Borrar el archivo de prueba en al función input del main. 
