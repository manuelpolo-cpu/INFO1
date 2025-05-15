#BLO-6(files)
F = open('matches.txt', 'r')
linea = F.readline()
equipo = str(input("Introduzca su equipo: "))
goles = 0
puntos = 0
while linea != "":
    elementos = linea.split(" ")
    if equipo == elementos[0]:
        goles += int(elementos[1])
        if int(elementos[1]) > int(elementos[3]):
            puntos += 3
        elif int(elementos[1]) == int(elementos[3]):
            puntos += 1
    elif equipo == elementos[2]:
        goles += int(elementos[3])
        if int(elementos[3]) > int(elementos [1]):
            puntos += 3
        elif int(elementos[3]) == int(elementos[1]):
            puntos += 1
    linea = F.readline()
F.close()
print("Tu equipo",equipo,"tiene",puntos,"puntos y tiene",goles,"goles a favor.")

#BLO-7(functions)
def ChangeWord(words, A, B):
    replacements = 0
    i = 0
    while i < len(words):
        if words[i] == A:
            words[i] = B
            replacements += 1
        elif words[i] == B:
            words[i] = A
            replacements += 1
        i += 1
    print(replacements)
    print(words)
ChangeWord((['manuel', 'javier', 'alex', 'manuel', 'pablo', 'ruben']), 'manuel', 'alex')