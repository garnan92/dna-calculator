DNA
=====

#### Metedo ####

el metodo que se va usar en este caso para el lenguaje de programacion python

```
    def hasMutation(dna:[str]) -> bool
```

#### Endpoints ####

http://127.0.0.1:5000/mutation

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

Get

```
    {
        "count_mutations": 3,
        "count_no_mutation": 4,
        "ratio": 0.75
    }
```

### Como correr ###

deves tener instalado la dependencia de flask en python si no la tienes 

comando para instalar
```
   pip install flask
```

y lo corres como si fuera una aplicacion normal de python

```
    py main.py
```

[npm]: https://img.shields.io/npm/v/three
[npm-url]: https://www.npmjs.com/package/three