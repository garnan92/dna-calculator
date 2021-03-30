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
    

def create_tables():

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



def insert_request(entrada:str):

    create_tables()

    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    sql_query = "insert into Log_request (ENTRADA) values ('"+entrada+"_"+dt_string+"')"

    execute_query(sql_query)


def insert_mutation(cadena:[str],mutado:int):

    create_tables()

    dna = (",".join(cadena))

    if seek_dna(dna):

        insert_request("insertar mutacion: "+(dna))

        sql_query = "insert into Log (CADENA,MUTADO) values ('"+  dna  +"',"+str(mutado)+")"

        execute_query(sql_query)

def seek_dna(dna:str) -> bool:

    cursor = execute_query("select CADENA from Log where CADENA = '"+dna+"'",False)

    registros = [
        dict(CADENA=row[0])
        for row in cursor.fetchall()
    ]

    if len(registros) > 0:
        return False
    else:
        return True

def get_dnas() -> []:
    create_tables()

    cursor = execute_query("select ID,CADENA,MUTADO from Log",False)

    registros = [
        dict(ID=row[0],CADENA=row[1],MUTADO=row[2])
        for row in cursor.fetchall()
    ]

    insert_request("programacion de cadenas")

    return registros

def get_stats() -> dict:

    create_tables()

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

    insert_request("obtencion de stats")

    return {
        "count_mutations" : m,
        "count_no_mutation" : nm,
        "ratio" : float(r)
    }
    

def clean_blackboard():
    create_tables()

    sql_query = "drop table Log"

    execute_query(sql_query)

    insert_request("limpiar pizarra")

def clean_log():
    create_tables()

    sql_query = "drop table Log_request"

    execute_query(sql_query)

def get_log():

    create_tables()

    cursor = execute_query("select ID,ENTRADA from Log_request",False)

    log = [
        dict(ID=row[0],ENTRADA=row[1])
        for row in cursor.fetchall()
    ]

    return { "registros" : log }

