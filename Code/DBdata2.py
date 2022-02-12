import pymysql
import sys
import spacy

class Datos2:

	def guardarTriplesGenerados(self,uri,frase,posicion,sujeto,predicado,objeto,tipo,longitud):
		db = pymysql.connect(host='localhost', user='root', password='', db='data')
		cur = db.cursor()
		sql = """INSERT INTO tripletasgeneradas (uripaper, frase, posicion, sujeto, predicado, objeto, tipo, longitud) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)  """
		datos = (uri,frase,posicion,sujeto,predicado,objeto,tipo,longitud)
		cur.execute(sql,datos)
		db.commit()
		print("...tripletas almacenadas...")
		cur.close()

	def guardarTripletasTagme(self,sujeto,predicado, objeto, score1, score2):
		db = pymysql.connect(host='localhost', user='root', password='',db='data')
		cur = db.cursor()
		sql = """INSERT INTO tripletastagme (sujeto, predicado, objeto, score1, score2) VALUES (%s, %s, %s, %s, %s) """
		datos = (sujeto, predicado, objeto, score1, score2)
		cur.execute(sql,datos)
		db.commit()
		print("...tripletas almacenadas...")
		cur.close()
