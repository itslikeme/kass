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
		array = ["Eu n�o entendi oque voc� disse!", "N�o entendi.","Oque?","Pode repetir, por favor?"]
		rand_index = random.randrange(0,len(array))
		Kass.talk(array[rand_index])
	@staticmethod
	def random_answer(lister):
		rand_index = random.randrange(0,len(lister))
		Kass.talk(lister[rand_index])


class keywords:
		query = ['oque','�','significa','onde','quem','fica','sin�nimos','sin�nimo','sinonimos','sinonimos','procura','procurar','buscar','busca','qual','mostrar','mostra']
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
				talkOptions_01 = ['Ok. Mostrando resultados...', 'Tudo bem, mostrando resultado #1...','Vou mostrar o primeiro resultado, ent�o.']
				
				for each in result:
					striggi = each.split(',')
					f_striggi = []
					for string in striggi:
						charmap = {"?":"","""\\xC0""":"""�""","""\\xC1""":"""�""","""\\xC2""":"""�""","""\\xC3""":"""�""","""\\xC4""":"""�""","""\\xC5""":"""�""","""\\xC6""":"""�""","""\\xC7""":"""�""","""\\xC8""":"""�""","""\\xC9""":"""�""","""\\xCA""":"""�""","""\\xCB""":"""�""","""\\xCC""":"""�""","""\\xCD""":"""�""","""\\xCE""":"""�""","""\\xCF""":"""�""","""\\xD0""":"""�""","""\\xD1""":"""�""","""\\xD2""":"""�""","""\\xD3""":"""�""","""\\xD4""":"""�""","""\\xD5""":"""�""","""\\xD6""":"""�""","""\\xD7""":"""""","""\\xD8""":"""�""","""\\xD9""":"""�""","""\\xDA""":"""�""","""\\xDB""":"""�""","""\\xDC""":"""�""","""\\xDD""":"""�""","""\\xDE""":"""�""","""\\xDF""":"""�""","""\\xE0""":"""�""","""\\xE1""":"""�""","""\\xE2""":"""�""","""\\xE3""":"""�""","""\\xE4""":"""�""","""\\xE5""":"""�""","""\\xE6""":"""�""","""\\xE7""":"""�""","""\\xE8""":"""�""","""\\xE9""":"""�""","""\\xEA""":"""�""","""\\xEB""":"""�""","""\\xEC""":"""�""","""\\xED""":"""�""","""\\xEE""":"""�""","""\\xEF""":"""�""","""\\xF0""":"""�""","""\\xF1""":"""�""","""\\xF2""":"""�""","""\\xF3""":"""�""","""\\xF4""":"""�""","""\\xF5""":"""�""","""\\xF6""":"""�""","""\\xF7""":"""""","""\\xF8""":"""�""","""\\xF9""":"""�""","""\\xFA""":"""�""","""\\xFB""":"""�""","""\\xFC""":"""�""","""\\xFD""":"""�""","""\\xFE""":"""�""","""\\xFF""":"""�"""}
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
				talkOptions_00 = ['Pesquisa cancelada','Ok, cancelar ent�o.','Voc� que sabe.', "Tudo bem. Abortando...",'Tudo bem.','Pronto.']
				Kass.random_answer(talkOptions_00)
	except KeyboardInterrupt:
		question()

def create_database():
	global conn
	user_input = raw_input('Kass: Deseja criar um novo banco de dados? \n Operador: ')
	words_positive = ['sim','afirmativo','quero','criar','novo','certeza']
	words_negative = ['nao','n�o','negativo','cancelar','abortar']
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
			Kass.talk('Banco de dados j� existe!')
			return False
	elif(yes == no):
		Kass.talk("Voc� me deixou confusa... Tenta de novo, ok?")
		sys.exit(0)
	else:
		Kass.talk("N�o quer banco de dados? Abortar...")
		sys.exit(0)




	



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
		Kass.talk("Eu n�o encontrei o banco de dados!")
		if(create_database() == True):
			Critical = False
		else:
			Critical = True

	#end_of_init
	if Critical == True:
		Kass.talk('Erro cr�tico na inicializa��o. Abortando...')
		sys.exit(0)



def interpreter(string):
	UND = False

	if(string[0:1] == '"'):
		if(string[len(string)-1:]=='"'):
			UND = True
			KassMessage = 'Vou adicionar ' + str(string.upper()) + ' para o meu banco de dados...'
			Kass.talk(KassMessage)
			c = conn.cursor()
			wisdom = string[1:-1]
			chars = {'�':'a','�':'a','�':'a','�':'a','�':'e','�':'e','�':'e','�':'i','�':'i','�':'o','�':'o','�':'o','�':'o','�':'u','�':'u','�':'u'}
			for i in chars:
				wisdom = wisdom.replace(i,chars[i])
			wisdom = wisdom.upper()
			c.execute("INSERT INTO KNOWLEDGE VALUES (" + "'" + str(wisdom) + "'" + ")")
			conn.commit()
			#Kass.talk(sucess)
	if(string[0:len('console')] == 'console'):
		UND = True
		c = conn.cursor()
		try:
			c.execute(string[len('console '):].upper())
			conn.commit()
			print c.fetchall()
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
				talkOptions_03 = 'Ocorreu um erro e n�o foi poss�vel completar o procedimento.'
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
		Kass.talk("Ol�!")
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