DNA
=====

#### Método ####

el método que se va a usar en este caso para el lenguaje de programación python

```
    def hasMutation(dna:[str]) -> bool
```

#### Endpoints ####

http://127.0.0.1:5000/mutation

version de servidor

https://dna-calculator.herokuapp.com/mutation

Post

```
    {
    "dna":[
            "GGCATA",
            "TTTCCC",
            "CCCTCT",
            "CGGTAC",
            "CTCTGA",
            "AAGAGC"]
    }
```

http://127.0.0.1:5000/stats

version de servidor

https://dna-calculator.herokuapp.com/stats

Get

```
    {
        "count_mutations": 3,
        "count_no_mutation": 4,
        "ratio": 0.75
    }
```

### Como correr ###

debes tener instalado la dependencia de flask en python si no la tienes 

comando para instalar
```
   pip install flask
```

y lo corres como si fuera una aplicación normal de python

```
    py main.py
```