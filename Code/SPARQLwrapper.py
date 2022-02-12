from DBdata import Datos
from SPARQLWrapper import SPARQLWrapper, JSON, RDF
from rdflib import Graph 
import json

db = Datos()
#con = DBdata.conexionDB()

#Punto final del grafo
endPoint = "http://www.scholarlydata.org/sparql/"

#Consulta para el titulo de los papers
Q1= """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX fabio: <http://purl.org/spar/fabio/>
SELECT DISTINCT ?Spaper ?prop ?value WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {conf:title}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}"""

#Consulta para el resumen de los papers
Q2= """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX fabio: <http://purl.org/spar/fabio/>
SELECT DISTINCT ?Spaper ?prop ?value WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {conf:abstract}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}
"""

#Consulta para el DOI con los papers
Q3 = """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX fabio: <http://purl.org/spar/fabio/>
SELECT DISTINCT ?Spaper ?prop ?value WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {conf:doi}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}"""

#Consulta palabras clave con los papers
Q4= """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX fabio: <http://purl.org/spar/fabio/>
SELECT DISTINCT ?Spaper ?prop ?value
WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {conf:keyword}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}
"""
#Consulta autores con URI autores
Q5= """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX fabio: <http://purl.org/spar/fabio/>
PREFIX autor: <http://purl.org/dc/elements/1.1/>
SELECT DISTINCT ?Spaper ?prop ?value
WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {foaf:made autor:creator}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}
"""
 #Consulta URI con los nombres de los autores.
Q6 = """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX made: <http://xmlns.com/foaf/0.1/>
PREFIX fabio: <http://purl.org/spar/fabio/>
PREFIX autor: <http://purl.org/dc/elements/1.1/>
SELECT DISTINCT ?Spaper ?prop ?value
WHERE{
  VALUES ?type {made:Person made:name}
  VALUES ?prop {made:name}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}
"""

#Consulta subject con los papers

Q7= """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX sub: <http://purl.org/dc/elements/1.1/>
PREFIX fabio: <http://purl.org/spar/fabio/>
SELECT DISTINCT ?Spaper ?prop ?value
WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {sub:subject}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}
"""

#Consulta sameAs con papers
Q8= """
PREFIX conf: <https://w3id.org/scholarlydata/ontology/conference-ontology.owl#>
PREFIX fabio: <http://purl.org/spar/fabio/>
PREFIX sam: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?Spaper ?prop ?value
WHERE{
  VALUES ?type {fabio:ProceedingsPaper conf:InProceedings}
  VALUES ?prop {sam:sameAs}
  ?Spaper a ?type .
  OPTIONAL {
    ?Spaper ?prop ?value
  }
}
"""

#print (Q)

def getTripletas(q):
  sparql=SPARQLWrapper(endPoint)
  sparql.setQuery(q)
  sparql.setReturnFormat(JSON)
  results=sparql.query().convert()
  #print(results)

#Recorrido del JSON y funcion para guardar en forma de tripletas
  for result in results["results"]["bindings"]:
      print (result['Spaper']["value"], result['prop']["value"], result['value']["value"])
      #funcion para guardar de la consulta Q1,Q2,Q3,Q4
      #db.guardarTripletas(result['Spaper']['value'], result['prop']['value'], result['value']['value'])
      db.guardarTripletasTemporales(result['Spaper']['value'], result['prop']['value'], result['value']['value'])
      #db.guardarTripletas(result['paper']['value'], result['person']['value'], result['name']['value'])

      #print (result['prop']['value'])
      #print (result['values']['value'])

#Ejecucion de las consultas
getTripletas(Q1)
#salta error por excepcion
#getTripletas(Q2)
#getTripletas(Q3)
#getTripletas(Q4)
#getTripletas(Q5)

#getTripletas(Q6)
#getTripletas(Q7)
#getTripletas(Q8)
