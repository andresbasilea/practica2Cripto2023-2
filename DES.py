
import fileinput


sBoxS0 = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]
sBoxS1 = [[0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]

mp = 	{ "0000": 0,
          "0001": 1,
          "0010": 2,
          "0011": 3,
          "0100": 4,
          "0101": 5,
          "0110": 6,
          "0111": 7,
          "1000": 8,
          "1001": 9,
          "1010": 10,
          "1011": 11,
          "1100": 12,
          "1101": 13,
          "1110": 14,
          "1111": 15}
		

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
	mensajePermutadoExpanded = [None] * 8
	mensajePermutadoExpanded[0] = mensajePermutado[3]
	mensajePermutadoExpanded[1] = mensajePermutado[0]
	mensajePermutadoExpanded[2] = mensajePermutado[1]
	mensajePermutadoExpanded[3] = mensajePermutado[2]
	mensajePermutadoExpanded[4] = mensajePermutado[1]
	mensajePermutadoExpanded[5] = mensajePermutado[2]
	mensajePermutadoExpanded[6] = mensajePermutado[3]
	mensajePermutadoExpanded[7] = mensajePermutado[0]

	ssk = ""
	for c in subkey:
		ssk = ssk + c

	smpe = ""
	for c in mensajePermutadoExpanded:
		smpe = smpe + c

	print(ssk, smpe)
	xorarg1 = mp[ssk[0:4]]
	xorarg2 = mp[smpe[0:4]]
	xorarg3 = mp[ssk[4:8]]
	xorarg4 = mp[smpe[4:8]]

	xorarg1 = xorarg1+xorarg3
	xorarg2 = xorarg2+xorarg4

	XOR = xorarg1 ^ xorarg2

	XOR = format(XOR,'08b')
	print("XOR",XOR)

	XOR1 = XOR[0:4]
	XOR2 = XOR[4:8]

	row1 = XOR1[0:2]
	col1 = XOR1[2:3]
	row2 = XOR2[0:2]
	col2 = XOR2[2:3]


	sBoxS0Val = sBoxS0[int(col1,2)][int(row1,2)]
	sBoxS1Val = sBoxS1[int(col2,2)][int(row2,2)]
	binsBoxS0val = format(sBoxS0Val,'02b')
	binsBoxS1val = format(sBoxS1Val,'02b')

	concatS0S1 = str(binsBoxS0val) + str(binsBoxS1val)

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
	for c in mensajePermutado:
		smp = smp + c


	xorarg1 = mp[scs0s1p]
	xorarg2 = mp[smp]

	XORs0s1permutLeftHalf = xorarg2 ^ xorarg1
	
	output = format(XORs0s1permutLeftHalf,'04b')

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
	for line in fileinput.input("DES.txt"):
		lines.append(line.rstrip("\n"))
	subkey1, subkey2 = Subkeys(lines[0])
	mensajePermutado = InitialPermutation(lines[1])
	mix1 = Mixing(subkey1, mensajePermutado[4:8]) # Step 2
	strConcatStep2 = ""
	for c in mensajePermutado[0:4]:
		strConcatStep2 = strConcatStep2 + c
	strStep3 = strConcatStep2+mix1 #Step 3
	print(strStep3)

	mix2 = Mixing(subkey2, strStep3[4:8])
	strConcatStep4 = ""
	for c in strStep3[0:4]:
		strConcatStep4 = strConcatStep4 + c
	strConcatStep4 = strConcatStep4+mix2
	print(strConcatStep4)

	encrypted = InversePermutation(strConcatStep4)
	print(encrypted)


# Antes de enviar a alphagrader: 
#	Borrar el archivo de prueba en al función input del main. 
# 	Comentar todos los print
