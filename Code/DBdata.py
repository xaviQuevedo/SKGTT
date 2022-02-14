from Analizador import AnalisisTexto
import pymysql
import sys
import spacy
from DBdata2 import *

class Datos:
	con= None;
	global analisis 
	global data
	data = Datos2()
	analisis= AnalisisTexto()
	def conexionDB():
		try:
			conexion = pymysql.connect(host='localhost',
            	                 user='root',
                	             password='',
                    	         db='data')
			#print("Conexión correcta")
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:

			print("Ocurrió un error al conectar: ", e)
		return conexion
	def guardarTripletas(id,s,p,o):
		db = pymysql.connect(host='localhost', user='root', password='', db='data')
		cur = db.cursor()
		sql = """INSERT INTO tripletas(Id ,sujeto, predicado, objeto) VALUES (%s, %s, %s, %s) """
		datos= (id,s,p,o)
		cur.execute(sql, datos)
		db.commit()
		print ("tripletas guardadas....")
		cur.close()
	#con = conexionDB()
	
	def guardarTripletasTemporales(id,s,p,o):
		db = pymysql.connect(host='localhost', user='root', password='', db='data')
		cur = db.cursor()
		sql = """INSERT INTO pruebas(id_recurso, su, predi, obj) VALUES (%s, %s, %s, %s) """
		datos= (id,s,p,o)
		cur.execute(sql, datos)
		db.commit()
		print ("tripletas guardadas....")
		cur.close()

	def info():
		db = pymysql.connect(host='localhost', user='root', password='', db='data')
		cur = db.cursor()
		cur.execute("""SELECT * FROM `tripletas` WHERE predicado ='https://w3id.org/scholarlydata/ontology/conference-ontology.owl#abstract' """)
		result = cur.fetchall ()
		for x in result:
		 print(x)
	
	def corregirResumen():
		db = pymysql.connect(host='localhost', user='root', password='', db='data')
		cur = db.cursor()
		cur.execute (u""" UPDATE tripletas
SET objeto = trim(substr(objeto, 1, INSTR(objeto, 'Keywords:')-1))
WHERE predicado = 'https://w3id.org/scholarlydata/ontology/conference-ontology.owl#abstract'
AND objeto LIKE '%Keywords:%'; """)
		db.commit()
		cur.close()
		
	def extraerDatos():
		db = pymysql.connect(host='localhost', user='root', password='', db='data')
		cur = db.cursor()
				
		cur.execute(u"""SELECT DISTINCT sujeto, group_concat(IF(predicado = 'https://w3id.org/scholarlydata/ontology/conference-ontology.owl#title',
		 objeto, '')) titulo, group_concat(IF(predicado = 'https://w3id.org/scholarlydata/ontology/conference-ontology.owl#abstract', objeto, ''))
		 resumen FROM tripletas WHERE predicado = 'https://w3id.org/scholarlydata/ontology/conference-ontology.owl#abstract' OR  predicado = 'https://w3id.org/scholarlydata/ontology/conference-ontology.owl#title' GROUP BY sujeto;""")

		filas = cur.fetchall()
		
		for fila in filas:
			paper = fila[0]
			titulo = fila[1].strip(',')
			resumen = fila[2].strip(',')
			
			listAbs = resumen.split('.')
			print(titulo,"lista")
			pos = 1
			for frase in listAbs:
				longitud=len(frase.split(' '))
				if longitud > 3:
					entidad= analisis.get_entities(frase)
					relacion=analisis.get_relation(frase)
					
					print (40 * "*", frase)
					print("Sujeto ->", entidad[0], "Predicado ->", relacion, "Objeto ->",entidad[1])
					print(longitud,"longitud")
					#data.guardarTriplesGenerados(paper,frase,pos, entidad[0], relacion, entidad[1], 'resumen', longitud)
					pos = pos + 1
			
	extraerDatos()
