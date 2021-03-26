from Conexion.DB import INSERT_MUTACION,INSERT_REQUEST

#variables globales
NUM = {"val":0}

#imprimir las matrizes por si sola
def imprimirLista(lista:[]):
    for i in lista:
        print(i)

#valida si hay una cadena de 4 o mas del mismo caracter
def ValidarMutaciones(ATCG:[int],contador:int)->int:
    for i in ATCG:
        if i > 3:
            contador += 1
    return contador

#suma los valores que son para 
def ContadorValores(ATCG:[int],val:str,contador=0,validator=dict()) -> int:
    if val == 'A':
        ATCG[0] += 1
    elif val == 'T':
        ATCG[1] += 1
    elif val == 'C':
        ATCG[2] += 1
    elif val == 'G':
        ATCG[3] += 1
    else:
        INSERT_REQUEST("una entrada no valida")
        validator["discrepancia"] = True

    return contador

#funcion que hace los recorridos ya sea horizontal vertical u oblicuo
def Fetcher(lista = [str] ,direccion=0,m=0,n=0,x=0,y=0,contador=0) -> int :

    ATCG = [0,0,0,0]

    if direccion < 3:
        x1 = 0
        y1 = 0
    else:
        x1 = m
        y1 = n

    if direccion == 1: #horizontal
        while x1 < x:

            contador = ContadorValores(ATCG,lista[n][x1],contador)

            x1 += 1
    elif direccion == 2: #vertical
        while y1 < y:

            contador = ContadorValores(ATCG,lista[y1][m],contador)

            y1 += 1
    elif direccion == 3: #diagonal derecha
        while x1 < x or y1 < y:

            if x1 == x:
                return ValidarMutaciones(ATCG,contador)
            
            if y1 == y:
                return ValidarMutaciones(ATCG,contador)

            contador = ContadorValores(ATCG,lista[y1][x1],contador)

            x1 += 1
            y1 += 1
    elif direccion == 4: #diagonal izquierda
        while x1 >= 0 or y1 < y:

            contador = ContadorValores(ATCG,lista[y1][x1],contador)

            if x1 == 0:
                return ValidarMutaciones(ATCG,contador)
            
            if y1 == y-1:
                return ValidarMutaciones(ATCG,contador)

            x1 -= 1
            y1 += 1
    
    return ValidarMutaciones(ATCG,contador)

#recorre la lista de componentes
def Recorrido(lista:[str],x=0,y=0,n = 0,m = 0,contador=0) -> int:

    if m==x and y>=4:
        return Recorrido(lista=lista,x=x,y=y,n=n+1,m=0,contador=contador)#paso abajo

    if ( m == x or n == y ):
        return contador

    if y < 4:
        contador = Fetcher(lista,1,m,n,x,y)#recorrido horizontal
        return Recorrido(lista=lista,x=x,y=y,n=n+1,m=m,contador=contador)#paso abajo

    if x < 4:
        contador = Fetcher(lista,2,m,n,x,y)#recorrido vertical
        return Recorrido(lista=lista,x=x,y=y,n=n,m=m+1,contador=contador)#paso a la derecha

    if n==0 and y>=4:
        if m==0:

            contador = Fetcher(lista,1,m,n,x,y,contador=contador)#recorrido horizontal
            contador = Fetcher(lista,2,m,n,x,y,contador=contador)#recorrido vertical
            contador = Fetcher(lista,3,m,n,x,y,contador=contador)#recorrido derecha-abajo

        else:
            contador = Fetcher(lista,2,m,n,x,y,contador=contador)#recorrido vertical
            if m >= 3:
                contador = Fetcher(lista,4,m,n,x,y,contador=contador)#recorrido izquierda-abajo
            if m < x-3:
                contador = Fetcher(lista,3,m,n,x,y,contador=contador)#recorrido derecha-abajo

        return Recorrido(lista=lista,x=x,y=y,n=n,m=m+1,contador=contador)#paso a la derecha
    else:
        if (y>=4):
            contador = Fetcher(lista,1,m,n,x,y,contador=contador)#recorrido horizontal

            if n < y-3:
                contador = Fetcher(lista,3,0,n,x,y,contador=contador)#recorrido derecha-abajo
                contador = Fetcher(lista,4,x-1,n,x,y,contador=contador)#recorrido izquierda-abajo

            return Recorrido(lista=lista,x=x,y=y,n=n+1,m=m,contador=contador)#paso abajo
    
    return contador

#funcion principal que valida si una cadena tiene o no mutaciones
def hasMutation(dna:[str]) -> bool :

    TieneMutacion = Recorrido(dna,len(dna[0]),len(dna))

    NUM['val'] = TieneMutacion

    if TieneMutacion > 1:
        INSERT_MUTACION(dna,1)
        return True
    else:
        INSERT_MUTACION(dna,0)
        return False