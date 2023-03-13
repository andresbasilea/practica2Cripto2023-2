
import fileinput

def DES(clave):
	

if __name__ == '__main__':
	lines = []
	for line in fileinput.input():
		lines.append(line.rstrip("\n"))
	clave =  lines[0]
	clave = bytes(clave, encoding='ascii')
	S = KSA(clave)
	cifrado = PRGA(S, lines[1])
	i=0
	for x in cifrado:
		if len(x)==1:
			cifrado[i] = "0" + cifrado[i]
		i+=1
	print(''.join(cifrado))