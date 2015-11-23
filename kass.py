# coding: iso-8859-1 -*-
import sqlite3, os, sys, random
debug_mode = True
class ProgramInfo:
	name = 'Kass Data Center'
	version = '0.1'
	act_folder = str(os.path.dirname(sys.argv[0]))
	script_name = str(sys.argv[0])
	fullPath = act_folder + '/' + script_name
	dbPath = act_folder + '/kass.db'
	populatorPath = act_folder + '/populator.py'
	banner = '''
	 _   __              
	| | / /              
	| |/ /  __ _ ___ ___ 
	|    \ / _` / __/ __|
	| |\  \ (_| \__ \__ \\
	\_| \_/\__,_|___/___/
	_____________________________
	Database Management Software
                     
	'''

class SQL:
	db_name = 'kass.db'
class Kass:
	@staticmethod
	def talk(string):
		print '\nKass: ' + str(string)
	@staticmethod
	def dont_understand():
		array = ["Eu não entendi oque você disse!", "Não entendi.","Oque?","Pode repetir, por favor?"]
		rand_index = random.randrange(0,len(array))
		Kass.talk(array[rand_index])
	@staticmethod
	def random_answer(lister):
		rand_index = random.randrange(0,len(lister))
		Kass.talk(lister[rand_index])


class keywords:
		query = ['oque','é','significa','onde','quem','fica','sinônimos','sinônimo','sinonimos','sinonimos','procura','procurar','buscar','busca','qual','mostrar','mostra']
		add = ['adicionar','criar','crie','adicione']
		remove = ['delete', 'remova', 'exclua', 'remover', 'excluir', 'deletar']
		update = ['alterar', 'modificar', 'mudar', 'change']


def objectOfQuestion(string):
	objIndex = string.find('"')
	remainingString = string[objIndex:]
	objFinalIndex = remainingString[1:].find('"')
	objFinalIndex = objFinalIndex + objIndex + 2
	theLastVariable = string[(objIndex+1):(objFinalIndex-1)]
	return theLastVariable

def analyze(string):
		result = {"add":0,"query":0,"remove":0,"update":0}
		stringToAnalyze = string.split(' ')
		obj = ''
		for each_word in stringToAnalyze:
			each_word = each_word.lower()
			for key in keywords.query:
				if(each_word == key):
					result["query"]+=1
					string = string.strip(key)
			for key in keywords.add:
				if(each_word == key):
					result["add"]+=1
					string = string.strip(key)
			for key in keywords.remove:
				if(each_word == key):
					string = string.strip(key)
					result["remove"]+=1
			for key in keywords.update:
				if(each_word == key):
					result["update"]+=1
					string = string.strip(key)
		maior = '' 
		maiorInt = 0
		for i in result:
			if(result[i] > maiorInt ):
				maior = i
				maiorInt = result[i]

		if maiorInt == 0:
			maior = 'nada'
		stringObj = string.split(' ')
		objectX = stringObj[len(stringObj)-1]
		return maior, objectX.lower()

def remove(LIST):
	newList = []
	for table in LIST:
		table = str(table)

		table = table.replace("(","")
		table = table.replace(")","")
		table = table.replace("u'",'')
		table = table.replace(',','')
		table = table.replace("'",'')
		if(table <> 'sqlite_sequence'):
			newList.append(table)
	return newList

def ListAllTables():
	c = conn.cursor()
	c.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;''')
	tableList = c.fetchall()
	formattedTableList = remove(tableList)
	print formattedTableList


def act(action,tString):
	try:
		if(action == 'nada'):
			Kass.dont_understand()
		c = conn.cursor()
		c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
		tableList = c.fetchall()
		formattedTableList = remove(tableList)
		result = []
		#print formattedTableList
		for i in formattedTableList:
			c.execute("SELECT sql FROM sqlite_master WHERE tbl_name = " + "'" + str(i) + "'" + " AND type='table'")
			col_names = c.fetchall()
			laString = "[(u' CREATE TABLE "
			tableLenght = len(i)
			laStringFullLenght = (len(laString)-1) + tableLenght
			col_names = str(col_names)[(laStringFullLenght+1):-5]
			column_List = col_names.split(',')
			column_List = [x.strip(' ') for x in column_List]
			column_List = [x.strip('(') for x in column_List]
			#print column_List
			for column in column_List:
				#print "SELECT * FROM " + str(i) + " WHERE " + str(column) + " LIKE '%" + str(tString) + "%'"
				c.execute("SELECT * FROM " + str(i) + " WHERE " + str(column) + " LIKE '%" + str(tString) + "%'")
				table_name_for_print = str(i)
				resultList = c.fetchall()
				#print resultList
				for strResult in resultList:
					strResult = str(strResult) 
					finalResult = str(strResult)  + ' da tabela ' + str(table_name_for_print)
					result.append(finalResult)
		striggilen = str(len(result))
		intilen = int(striggilen)

		if(intilen > 0):
			talkstring = "Encontrei " + str(len(result)) + " resultados que podem ser de seu interesse."
			Kass.talk(talkstring)
			resultIndx = 1
			talkstring = 'Oque deseja fazer?'
			command = raw_input('\nOperator: ')
			command = command.lower()
			commandList = command.split(' ')
			abortStrings = ['cancelar','abortar','ignorar','sai fora','sair','parar','nao']
			visualizationStrings = ['ver','visualizar','mostre','mostrar','deixa eu ver','me mostra','mostra','me mostre','visualize','printar','print','ver']
			abortChance = 0
			visualizationChance = 0
			for i in commandList:
				for a in abortStrings:
					if(i[0:len(a)] == a):
						abortChance+=1
				for a in visualizationStrings:
					if(i[0:len(a)] == a):
						visualizationChance +=1

			if(visualizationChance > abortChance):
				talkOptions_01 = ['Ok. Mostrando resultados...', 'Tudo bem, mostrando resultado #1...','Vou mostrar o primeiro resultado, então.']
				
				for each in result:
					striggi = each.split(',')
					f_striggi = []
					for string in striggi:
						charmap = {"?":"","""\\xC0""":"""Á""","""\\xC1""":"""Á""","""\\xC2""":"""Â""","""\\xC3""":"""Ã""","""\\xC4""":"""Ä""","""\\xC5""":"""Å""","""\\xC6""":"""Æ""","""\\xC7""":"""Ç""","""\\xC8""":"""È""","""\\xC9""":"""É""","""\\xCA""":"""Ê""","""\\xCB""":"""Ë""","""\\xCC""":"""Ì""","""\\xCD""":"""Í""","""\\xCE""":"""Î""","""\\xCF""":"""Ï""","""\\xD0""":"""Ð""","""\\xD1""":"""Ñ""","""\\xD2""":"""Ò""","""\\xD3""":"""Ó""","""\\xD4""":"""Ô""","""\\xD5""":"""Õ""","""\\xD6""":"""Ö""","""\\xD7""":"""""","""\\xD8""":"""Ø""","""\\xD9""":"""Ù""","""\\xDA""":"""Ú""","""\\xDB""":"""Û""","""\\xDC""":"""Ü""","""\\xDD""":"""Ý""","""\\xDE""":"""Þ""","""\\xDF""":"""ß""","""\\xE0""":"""à""","""\\xE1""":"""á""","""\\xE2""":"""â""","""\\xE3""":"""ã""","""\\xE4""":"""ä""","""\\xE5""":"""å""","""\\xE6""":"""æ""","""\\xE7""":"""ç""","""\\xE8""":"""è""","""\\xE9""":"""é""","""\\xEA""":"""ê""","""\\xEB""":"""ë""","""\\xEC""":"""ì""","""\\xED""":"""í""","""\\xEE""":"""î""","""\\xEF""":"""ï""","""\\xF0""":"""ð""","""\\xF1""":"""ñ""","""\\xF2""":"""ò""","""\\xF3""":"""ó""","""\\xF4""":"""ô""","""\\xF5""":"""õ""","""\\xF6""":"""ö""","""\\xF7""":"""""","""\\xF8""":"""ø""","""\\xF9""":"""ù""","""\\xFA""":"""ú""","""\\xFB""":"""û""","""\\xFC""":"""ü""","""\\xFD""":"""ý""","""\\xFE""":"""þ""","""\\xFF""":"""ÿ"""}
						for key in charmap:
							keyInString = key.lower()
							string = string.replace(keyInString,charmap[key])
						string = string 
						f_striggi.append(string)
					print '\nResultado #' + str(resultIndx)
					resultIndx+=1
					
					for i in f_striggi:
						
						for key in charmap:
							keyInString = key.lower()
						print (i.replace(keyInString,charmap[key])).upper()
						
					print '\n'
					pause = raw_input('Kass: Pressione qualquer tecla para seguir em frente...')
			else:
				talkOptions_00 = ['Pesquisa cancelada','Ok, cancelar então.','Você que sabe.', "Tudo bem. Abortando...",'Tudo bem.','Pronto.']
				Kass.random_answer(talkOptions_00)
	except KeyboardInterrupt:
		question()

def create_database():
	global conn
	user_input = raw_input('Kass: Deseja criar um novo banco de dados? \n Operador: ')
	words_positive = ['sim','afirmativo','quero','criar','novo','certeza']
	words_negative = ['nao','não','negativo','cancelar','abortar']
	user_input = str(user_input).lower()
	user_words = user_input.split()
	for i in user_words:
		i = i.strip()
	yes = 0
	no = 0


	#relacionamento de dados
	for u_word in user_words:
		for word in words_negative:
			if(u_word == word):
				no+=1
		for word in words_positive:
			if(u_word == word):
				yes+=1


	#analise do resultado
	if(yes > no):
		if not os.path.isfile(SQL.db_name):
			conn = sqlite3.connect(ProgramInfo.dbPath)
			conn.text_factory = str
			Kass.talk('Banco de dados criado!')
			return True
		else:
			Kass.talk('Banco de dados já existe!')
			return False
	elif(yes == no):
		Kass.talk("Você me deixou confusa... Tenta de novo, ok?")
		sys.exit(0)
	else:
		Kass.talk("Não quer banco de dados? Abortar...")
		sys.exit(0)


def extractData(table):
	c = conn.cursor()
	people_db_columns = ['NOME','NASCIMENTO','CPF','RG','ENDERECO','EMAIL','TELEFONE', 'CELULAR']
	c.execute("SELECT * FROM " + str(table))
	content = c.fetchall()
	return content

def removeUnformatted(string):
	string = str(string)
	characters = ["u'","(",")","'",","]
	for i in characters:
		string.replace(i,'')
	return string

def remove(LIST):
	newList = []
	for table in LIST:
		table = str(table)

		table = table.replace("(","")
		table = table.replace(")","")
		table = table.replace("u'",'')
		table = table.replace(',','')
		table = table.replace("'",'')
		if(table <> 'sqlite_sequence'):
			newList.append(table)
	return newList


def classifyData(data,targetTable,sourceTable,sourceColumn):
	
	for i in data:
		columns = []
		info = []
		i = str(i)
		eachList = i.split(':')
		for each in eachList:
			if((eachList.index(each) % 2 )== 1):
				if(eachList.index <> 0 ):
					columns.append(each)
			else:
				info.append(each)
		#return columns, info
		infoString = ''
		columnString = ''
		for information in info:
			infoString+= "'" + information + "'" +  ','
		infoString = infoString[5:-4]
		infoString = str(infoString)
		#print infoString

		for column in columns:
			columnString+= column + ','
		columnString = columnString[:-1]
		columnString = str(columnString)
		#print columnString

		try:
			c = conn.cursor()
			c.execute("SELECT * FROM " + str(targetTable) + " WHERE " + str(columns[0]) + "=" + "'" + str(info[1]) + "'")
			exist = c.fetchone()
			if(exist == None):
				c.execute("INSERT INTO " + str(targetTable) + " (" + str(columnString) + ") " + " VALUES (" + str(infoString) + ")")

				print "Values %s added to table %s." % (infoString, targetTable)
				#print "DELETE FROM " + str(sourceTable) + " WHERE " + str(sourceColumn) + "=" + "'" + str(info[1]) + "'"
				c.execute("DELETE FROM " + str(sourceTable) + " WHERE " + str(sourceColumn) + " LIKE " + "'%" + str(info[1]) + "%'")
				c.execute("DELETE FROM " + str(sourceTable) + " WHERE " + str(sourceColumn) + " LIKE " + "'%" + str(info[2]) + "%'")
			if(exist[0] == str(info[1])):
				if(targetTable == 'people'):
					updateString = ''
					i = 0
					while(i < len(columns)):
						updateString += str(columns[i]) + "='" + str(info[i+1]) + "',"
						i+=1
					updateString = updateString[:-4]
					print updateString
					c.execute("UPDATE " + str(targetTable) + " SET "+str(updateString)+" WHERE " + str(columns[0]) + "='" + str(info[1]) + "'")
					print 'Values %s updated from table %s' % (updateString, targetTable)
					#print "DELETE FROM " + str(sourceTable) + " WHERE " + str(sourceColumn) + "=" + "'" + str(info[1]) + "'"
					c.execute("DELETE FROM " + str(sourceTable) + " WHERE " + str(sourceColumn) + " LIKE " + "'%" + str(info[1]) + "%'")
					c.execute("DELETE FROM " + str(sourceTable) + " WHERE " + str(sourceColumn) + " LIKE " + "'%" + str(info[2][:-3]) + "%'")
					print 'Source Table cleansed.'
		except Exception as e:
			#print 'SOURCE TABLE:' + str(sourceTable) + '\nTARGET TABLE:' + str(targetTable) + '\nSource Column:' + str(sourceColumn) + '\nError:' + str(e) + '\n'
			pass

	



def init():
	global conn
	Critical = False
	#database exists?
	#Kass.talk('Trying to find my database...')
	if os.path.isfile(SQL.db_name):
		#Kass.talk('Database found.')
		conn = sqlite3.connect(ProgramInfo.dbPath)
		conn.text_factory = str
		#Kass.talk('I have successfully connected to the database.')
	else:
		Kass.talk("Eu não encontrei o banco de dados!")
		if(create_database() == True):
			Critical = False
		else:
			Critical = True

	#end_of_init
	if Critical == True:
		Kass.talk('Erro crítico na inicialização. Abortando...')
		sys.exit(0)

def clean():
	if(os.name == 'nt'):
		os.system('cls')
	if(os.name == 'posix'):
		os.system('clear')

def interpreter(string):
	UND = False

	if(string[0:1] == '"'):
		if(string[len(string)-1:]=='"'):
			UND = True
			KassMessage = 'Vou adicionar ' + str(string.upper()) + ' para o meu banco de dados...'
			Kass.talk(KassMessage)
			c = conn.cursor()
			wisdom = string[1:-1]
			chars = {'á':'a','à':'a','â':'a','ã':'a','é':'e','è':'e','ê':'e','í':'i','ì':'i','ô':'o','ó':'o','ò':'o','õ':'o','ú':'u','ù':'u','û':'u'}
			for i in chars:
				wisdom = wisdom.replace(i,chars[i])
			wisdom = wisdom.upper()
			c.execute("INSERT INTO KNOWLEDGE VALUES (" + "'" + str(wisdom) + "'" + ")")
			conn.commit()
			#Kass.talk(sucess)
	if(string[0:len('clean')] == 'clean'):
		UND = True
		c = conn.cursor()
		try:
			c.execute('DROP TABLE KNOWLEDGE')
			c.execute('CREATE TABLE KNOWLEDGE (wisdom)')
			Kass.talk('Tabela de transição de dados limpa.')
			conn.commit()
		except Exception as e:
			errorString = 'Ocorreu um erro: ' + str(e)
			Kass.talk(errorString)
	if(string[0:len('populate')] == 'populate'):
		UND = True
		import subprocess
		data = extractData('KNOWLEDGE')
		c = conn.cursor()
		c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
		tableList = c.fetchall()
		formattedTableList = remove(tableList)
		#print formattedTableList
		for table in formattedTableList:
			classifyData(data,table,'KNOWLEDGE','wisdom')
		conn.commit()
	if(string[0:len('sql')] == 'sql'):
		UND = True
		c = conn.cursor()
		global console
		console = True
		string = 'Iniciando console SQL para o Operador...'
		Kass.talk(string)
		try:
			while console == True:
				sqlConsole = raw_input('\n	sql> ')
				if(sqlConsole == 'quit'):
					console == False
				else:
					string = 'Executando comando "' + str(sqlConsole) + '"...'
					Kass.talk(string)
					c.execute(sqlConsole)
					conn.commit()
					Kass.talk(str(c.fetchall()))
		except Exception as e:
			Kass.talk(e)
	listarTables = ['listar tabelas', 'mostrar tabelas','todas as tabelas']
	for i in listarTables:
		if(string[0:len(i)] == str(i)):
			UND = True
			ListAllTables()


	listarColunas = ['listar colunas','mostrar colunas','todas as colunas']
	for i in listarColunas:
		if(string[0:len(i)] == str(i)):
			UND = True
			try:
				c = conn.cursor()
				talkOptions_02 = i + ' de qual tabela?'
				Kass.talk(talkOptions_02)
				command = raw_input('\nOperator: ')
				c.execute("SELECT sql FROM sqlite_master WHERE tbl_name = " + "'" + str(command) + "'" + " AND type='table'")
				result = c.fetchall()
				result = str(result)
				result = result[len('[("CREATE TABLE ' + str(command) + ' '):-4]
				Kass.talk(result)
			except Exception as e:
				talkOptions_03 = 'Ocorreu um erro e não foi possível completar o procedimento.'
				if(debug_mode == True):
					print e
				Kass.talk(talkOptions_03)
				pass
	
	

	
		
	
	else:
		if UND == False:
			result, tString = analyze(string)
			var = objectOfQuestion(string)
			if(var == ''):
				act(result,tString)
			else:
				act(result,var)

			#Kass.dont_understand()
def question():
		Kass.talk("Olá!")
		while 1:
			if(os.name == 'nt'):
				os.system('cls')
			if(os.name == 'posix'):
				os.system('clear')
			print ProgramInfo.banner

			command = raw_input('\n Operador: ')
			command = command.lower()
			interpreter(command)
			pause = raw_input('Kass: Pressione qualquer tecla para seguir em frente...')

def main():
	try:
		if(str(os.name) == 'nt'):
			os.system('set path = %\path%;C:\\python27')
			os.system('chcp 1252 > nul')
	except Exception as e:
		#debug
		print str(e)
		pass
	init()
	
	question()




main()