import sqlite3
from datetime import datetime

DATABASE = "dna.sqlite"

def execute_query(query="",commit=True):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()
    cursor.execute(query)
    if commit:
        conn.commit()
        conn.close()

    return cursor
    

def CREATE_TABLES():

    sql_query = """

        CREATE TABLE IF NOT EXISTS Log (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CADENA TEXT NULL,
            MUTADO INT NULL
        );

    """

    execute_query(sql_query)

    sql_query = """

        create table if not exists Log_request (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ENTRADA TEXT NULL
        );

    """

    execute_query(sql_query)



def INSERT_REQUEST(entrada:str):

    CREATE_TABLES()

    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    sql_query = "insert into Log_request (ENTRADA) values ('"+entrada+"_"+dt_string+"')"

    execute_query(sql_query)


def INSERT_MUTACION(cadena:[str],mutado:int):

    CREATE_TABLES()

    INSERT_REQUEST("insertar mutacion: "+(",".join(cadena)))

    sql_query = "insert into Log (CADENA,MUTADO) values ('"+  (",".join(cadena) ) +"',"+str(mutado)+")"

    execute_query(sql_query)


def GET_DNAS() -> []:
    CREATE_TABLES()

    cursor = execute_query("select ID,CADENA,MUTADO from Log",False)

    registros = [
        dict(ID=row[0],CADENA=row[1],MUTADO=row[2])
        for row in cursor.fetchall()
    ]

    INSERT_REQUEST("programacion de cadenas")

    return registros

def GET_STATS() -> dict:

    CREATE_TABLES()

    cursor = execute_query("select ID,CADENA,MUTADO from Log where MUTADO = 1",False)

    registros_mutados = [
        dict(ID=row[0],CADENA=row[1],MUTADO=row[2])
        for row in cursor.fetchall()
    ]

    cursor = execute_query("select ID,CADENA,MUTADO from Log where MUTADO = 0",False)

    registros_no_mutados = [
        dict(ID=row[0],CADENA=row[1],MUTADO=row[2])
        for row in cursor.fetchall()
    ]

    m = len(registros_mutados)
    nm = len(registros_no_mutados)
    if m == 0.0 or nm == 0.0:
        r = 0.0
    else:
        r = m/nm

    INSERT_REQUEST("obtencion de stats")

    return {
        "count_mutations" : m,
        "count_no_mutation" : nm,
        "ratio" : float(r)
    }
    

def CLEAN_BLACKBOARD():
    CREATE_TABLES()

    sql_query = "drop table Log"

    execute_query(sql_query)

    INSERT_REQUEST("limpiar pizarra")

def CLEAN_LOG():
    CREATE_TABLES()

    sql_query = "drop table Log_request"

    execute_query(sql_query)

    CREATE_TABLES()    

def GET_LOG():

    CREATE_TABLES()

    cursor = execute_query("select ID,ENTRADA from Log_request",False)

    log = [
        dict(ID=row[0],ENTRADA=row[1])
        for row in cursor.fetchall()
    ]

    return { "registros" : log }

