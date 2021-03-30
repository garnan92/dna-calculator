from connetion.db import insert_mutation,insert_request

#global values
NUM = {"val":0}

#prints the list
def _printList(lista:[]):
    for i in lista:
        print(i)

#checks if the sequence has a mutation
def checkMutation(ATCG:[int],counter:int)->int:
    for i in ATCG:
        if i > 3:
            counter += 1
    return counter

#resets the count if the sequence is interrupted
def reseter(ATCG:[int],pos:int):
    for i in range(4):
        if i == pos:
            ATCG[i] += 1
        elif ATCG[i] < 4:
            ATCG[i] = 0

#sums the values of the sequence
def listCounter(ATCG:[int],val:str,counter=0,validator=dict(),reset=True) -> int:
    if val == 'A':
        if reset:
            reseter(ATCG,0)
    elif val == 'T':
        if reset:
            reseter(ATCG,1)
    elif val == 'C':
        if reset:
            reseter(ATCG,2)
    elif val == 'G':
        if reset:
            reseter(ATCG,3)
        
    else:
        insert_request("una entrada no valida")
        validator["fail"] = True

    return counter

#traveles throught the path which the direction is asigned
def fetcher(_list = [str] ,direction=0,m=0,n=0,x=0,y=0,counter=0) -> int :

    ATCG = [0,0,0,0]
    _tmp_list = list()
    check = 0

    if direction < 3:
        x1 = 0
        y1 = 0
    else:
        x1 = m
        y1 = n

    if direction == 1:
        while x1 < x:

            _tmp_list.append(_list[n][x1])

            counter = listCounter(ATCG,_list[n][x1],counter)

            x1 += 1
    elif direction == 2:
        while y1 < y:

            _tmp_list.append(_list[y1][m])
            counter = listCounter(ATCG,_list[y1][m],counter)

            y1 += 1
    elif direction == 3:
        while x1 < x or y1 < y:

            if x1 == x:
                check = checkMutation(ATCG,counter)
                # if checkMutation(ATCG,0) > 0:
                #     print("checados ",check," direction: ",direction," lista: ",_tmp_list)
                return check
            
            if y1 == y:
                check = checkMutation(ATCG,counter)
                # if checkMutation(ATCG,0) > 0:
                #     print("checados ",check," direction: ",direction," lista: ",_tmp_list)
                return check

            _tmp_list.append(_list[y1][x1])
            counter = listCounter(ATCG,_list[y1][x1],counter)

            x1 += 1
            y1 += 1
    elif direction == 4:
        while x1 >= 0 or y1 < y:

            _tmp_list.append(_list[y1][x1])
            counter = listCounter(ATCG,_list[y1][x1],counter)

            if x1 == 0:
                check = checkMutation(ATCG,counter)
                # if checkMutation(ATCG,0) > 0:
                #     print("checados ",check," direction: ",direction," lista: ",_tmp_list)
                return check
            
            if y1 == y-1:
                check = checkMutation(ATCG,counter)
                # if checkMutation(ATCG,0) > 0:
                #     print("checados ",check," direction: ",direction," lista: ",_tmp_list)
                return check

            x1 -= 1
            y1 += 1
    
    check = checkMutation(ATCG,counter)
    # if checkMutation(ATCG,0) > 0:
    #     print("checados ",check," direction: ",direction," lista: ",_tmp_list)
    return check

#travels throught the dna sequence
def path(_list:[str],x=0,y=0,n = 0,m = 0,counter=0) -> int:

    if m==x and y>=4:
        return path(_list=_list,x=x,y=y,n=n+1,m=0,counter=counter)

    if ( m == x or n == y ):
        return counter

    if y < 4:
        counter = fetcher(_list,1,m,n,x,y)
        return path(_list=_list,x=x,y=y,n=n+1,m=m,counter=counter)

    if x < 4:
        counter = fetcher(_list,2,m,n,x,y)
        return path(_list=_list,x=x,y=y,n=n,m=m+1,counter=counter)

    if n==0 and y>=4:
        if m==0:

            counter = fetcher(_list,1,m,n,x,y,counter=counter)
            counter = fetcher(_list,2,m,n,x,y,counter=counter)
            counter = fetcher(_list,3,m,n,x,y,counter=counter)

        else:
            counter = fetcher(_list,2,m,n,x,y,counter=counter)
            if m >= 3:
                counter = fetcher(_list,4,m,n,x,y,counter=counter)
            if m < x-3:
                counter = fetcher(_list,3,m,n,x,y,counter=counter)

        return path(_list=_list,x=x,y=y,n=n,m=m+1,counter=counter)
    else:
        if (y>=4):
            counter = fetcher(_list,1,m,n,x,y,counter=counter)

            if n < y-3:
                counter = fetcher(_list,3,0,n,x,y,counter=counter)
                counter = fetcher(_list,4,x-1,n,x,y,counter=counter)

            return path(_list=_list,x=x,y=y,n=n+1,m=m,counter=counter)
    
    return counter

#main fuction which verifies if the sequence has a mutation or not
def hasMutation(dna:[str]) -> bool :

    _hastMutation = path(dna,len(dna[0]),len(dna))

    NUM['val'] = _hastMutation

    if _hastMutation > 1:
        insert_mutation(dna,1)
        return True
    else:
        insert_mutation(dna,0)
        return False