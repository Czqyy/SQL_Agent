import os
import json
import requests
from langchain.tools import tool
import mysql.connector


class SQLTool():
	@tool("Query MySQL database")
	def query(sql_query):
		"""Useful to execute a SQL query in a MySQL database and return the query result
		The given SQL query must be in exact MySQL syntax."""
		cnx = mysql.connector.connect(
			user=os.environ["DB_USER"], 
			password=os.environ["USER_PASSWORD"], 
			host=os.environ["HOST"], 
			database=os.environ["DB"]
		)
		cursor = cnx.cursor()
		result = ""
		try:
			cursor.execute(sql_query)
			result = cursor.fetchall()
			cnx.commit()
		except Exception as e:
			result = f"Something is wrong with the SQL query, you got the error {e}"
		finally:
			cnx.close()
			return result
