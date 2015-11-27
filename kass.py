# -*- coding: UTF-8 -*-
import os, sys, sqlite3, random, time, subprocess, pyowm, json, urllib2



class developer:
	debug_mode = False



class Program:
	name = 'Kass Data Management'
	version = '0.2.1'
	banner = '''
	 _   __              
	| | / /              
	| |/ /  __ _ ___ ___ 
	|    \ / _` / __/ __|
	| |\  \ (_| \__ \__ \\
	\_| \_/\__,_|___/___/
	_____________________________\n
	''' +  str(name) + ' v' + str(version)
	author = 'n3st0r'
	class script:
		current_folder = str(os.path.dirname(sys.argv[0]))
		file_name = str(sys.argv[0])
		full_path = current_folder + '/' + file_name



class Kass:

	# update_progress() : Displays or updates a console progress bar
	## Accepts a float between 0 and 1. Any int will be converted to a float.
	## A value under 0 represents a 'halt'.
	## A value at 1 or bigger represents 100%
	@staticmethod
	def update_progress(progress):
	    barLength = 10 # Modify this to change the length of the progress bar
	    status = ""
	    if isinstance(progress, int):
	        progress = float(progress)
	    if not isinstance(progress, float):
	        progress = 0
	        status = "error: progress var must be float\r\n"
	    if progress < 0:
	        progress = 0
	        status = "Halt...\r\n"
	    if progress >= 1:
	        progress = 1
	        status = "Done...\r\n"
	    block = int(round(barLength*progress))
	    text = "\r Percent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), str(progress*100)[:4], status)
	    sys.stdout.write(text)
	    sys.stdout.flush()




	@staticmethod
	def talk(string):
		print '\n Kass: ' + str(string)

	@staticmethod
	def dont_understand():
		array = ["Eu não entendi oque você disse!", "Não entendi.","Oque?","Pode repetir, por favor?"]
		rand_index = random.randrange(0,len(array))
		Kass.talk(array[rand_index])

	@staticmethod
	def random_answer(lister):
		rand_index = random.randrange(0,len(lister))
		Kass.talk(lister[rand_index])

	@staticmethod
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

	@staticmethod
	def clean():
		if(os.name == 'nt'):
			os.system('cls')
		if(os.name == 'posix'):
			os.system('clear')

	@staticmethod
	def print_list(lista,filtro):
		element_index = 1
		if(filtro == None):
			for i in lista:
				print str(element_index) +'. ' + i + '\n'
				element_index+=1
		else:
			res = [k for k in lista if filtro in k]
			for i in res:
				print str(element_index) + '. ' + i + '\n'
				element_index+=1
	

	class Calculate:
		"""This class is responsible for math operations dealt by Kass."""
		@classmethod
		def IMC_Status(self, number):
			number = float(number)
			str_imc_status = ''
			if(number < 17):
				str_imc_status = 'Muito Abaixo'
			elif(number > 17 and number < 19):
				str_imc_status = 'Abaixo'
			elif(number > 19 and number < 25):
				str_imc_status = 'Normal'
			elif(number > 25 and number < 30):
				str_imc_status = 'Sobrepeso'
			elif(number > 30 and number < 35):
				str_imc_status = 'Obesidade I'
			elif(number > 35 and number < 40):
				str_imc_status = 'Obesidade II'
			elif(number > 40):
				str_imc_status = 'Obesidade III (Morbido)'
			else:
				print ' [!] Numero Invalido.'
				return False
			return str_imc_status

		@classmethod
		def IMC_Report(self, person, weight, height, imc_num, imc_status):
			if(imc_status <> None):
				Kass.clean()
				print '\n RELATORIO DE CALCULO:'
				print '\n ____________________________________________\n'
				print ' NOME: ' + str(person)
				print ' PESO: ' + str(weight)
				print ' ALTURA: ' + str(height)
				print ' IMC: ' + str(imc_num)
				print ' RESULTADO: ' + str(imc_status)
				print '\n ____________________________________________\n'

		@classmethod
		def IMC_DB_Insertion(self, person, weight, height, imc_num, imc_status):
			c = conn.cursor()
			c.execute("INSERT INTO IMC VALUES (" + "'" + str(person) + "','" + str(weight) + "','" + str(height) + "','" + str(imc_num) + "','" + str(imc_status) + "')")
			print ' [+] SQLITE3: Resultados adicionados a Tabela IMC.\n'

		@classmethod
		def IMC(self, person, weight, height):
			if(person <> None):
				weight = int(weight)
				height = float(height)
				imc = (weight / (height **2))
				str_imc_num = str(imc)[:4]
				int_imc_num = float(str_imc_num)
				str_imc_status = 'None'
				if(Kass.Calculate.IMC_Status(int_imc_num) <> False):
					str_imc_status = Kass.Calculate.IMC_Status(int_imc_num)
				Kass.Calculate.IMC_Report(str(person), str(weight), str(height), str(int_imc_num), str(str_imc_status))
				Kass.Calculate.IMC_DB_Insertion(str(person), str(weight), str(height), str(int_imc_num), str(str_imc_status))


			


	@staticmethod
	def climate(city):
		API_KEY = '88bef2e2314e0affe5c32f6caf8a3a4d'
		owm = pyowm.OWM(API_KEY)

		observation = owm.weather_at_place(city)
		w = observation.get_weather()
		l = observation.get_location()

		class Forecast():
			def __init__(self, city_name, city_temp, city_status,city_pressure, city_sunrise,city_humidity,city_wind,city_time,city_lon,city_lat,city_ID,city_rain,city_sunset):
				self.name = city_name
				self.status = city_status
				self.pressure = city_pressure
				self.sunrise = city_sunrise
				self.humidity = city_humidity
				self.wind = city_wind
				self.time = city_time
				self.lon = city_lon
				self.lat = city_lat
				self.ID = city_ID
				self.rain = city_rain
				self.sunset = city_sunset

				def convertTemp(city_temp):
					for i in city_temp:
						if(i == 'temp'):
							self.temp = city_temp[i]
				convertTemp(city_temp)

				def display_info():
					print '\n____________________________________________\n'
					print ' Hora da consulta:  ' + str(self.time) + '\n'
					print ' Informacao metereologica da cidade "' + str(self.name) + '" :\n'
					print ' Nome: ' + str(self.name) + ' - ID: ' + str(self.ID)
					print ' Geolocation: Lat(' + str(self.lat) + ') Lon(' + str(self.lon) + ')' 
					print ' Temperatura: ' + str(self.temp) + ' Celsius'
					print ' Estado atual: ' + str(self.status)
					print ' Chuva: ' + str(self.rain)
					print ' Pressao Atmosferica: ' + str(self.pressure)
					print ' Humidade relativa do ar: ' + str(self.humidity)
					print ' Nascer do Sol: ' + str(self.sunrise)
					print ' Por do Sol: ' + str(self.sunset)
					print '\n____________________________________________\n'
				display_info()
				

		weatherForecast = Forecast(l.get_name(),w.get_temperature(unit='celsius'),w.get_detailed_status(),w.get_pressure(),w.get_sunrise_time('iso'),w.get_humidity(), w.get_wind(),w.get_reference_time(timeformat='iso'),l.get_lon(),l.get_lat(),l.get_ID(),w.get_rain(),w.get_sunset_time('iso'))

	class Browser:
		def __init__(self, browser_name,browser_path):
			self.name = browser_name
			self.path = browser_path

		def start(self, link):
			if(os.path.isfile(self.path)):
				start_cmd = str(self.path) + ' "' + str(link) + '"'
				p = subprocess.Popen(start_cmd)
			else:
				print 'Could not find ' + str(self.name) + ' executable.'
				return 

		@staticmethod
		def find_browser_exe():
			global Chrome
			global Firefox
			global Iexplore
			browser_exe_names = ['chrome.exe','iexplore.exe','firefox.exe']
			common_dir_names = ['C:\\Program Files\\Google\\','C:\\Program Files (x86)\\Google\\','C:\\Program Files\\Mozilla Firefox\\','C:\\Program Files (x86)\\Mozilla Firefox\\','C:\\Program Files\\Internet Explorer\\','C:\\Program Files (x86)\\Internet Explorer\\']
			for dir_name in common_dir_names:
				if(os.path.isdir(dir_name)):
					for browser_name in browser_exe_names:
						for root, dirs, files in os.walk(dir_name):
							for file in files:
								if file.endswith(browser_name):
									if(file == 'chrome.exe'):
										Chrome = Kass.Browser('Google Chrome',os.path.join(root,file))
										#print ' ' + Chrome.name + ' encontrado.\n'
									if(file == 'firefox.exe'):
										Firefox = Kass.Browser('Mozilla Firefox',os.path.join(root,file))
										#print ' ' + Firefox.name + ' encontrado.\n'
									if(file == 'iexplore.exe'):
										Iexplore = Kass.Browser('Internet Explorer',os.path.join(root,file))
										#print ' ' + Iexplore.name + ' encontrado.\n'

class Database:
	db_name = 'Kass.db'
	db_Path = Program.script.current_folder + '/' + db_name


	@staticmethod
	def find_db():
		#database exists?
		if os.path.isfile(Database.db_name):
			conn = sqlite3.connect(Program.dbPath)
			conn.text_factory = str
		else:
			if(Database.create() == True):
				Critical = False
			else:
				Critical = True

	class Data:
		'''This class is responsible for importing database structure (table names, and columns names) into memory.'''
		
		@classmethod
		def colNameFormat(self, lista, tableName):
			dataStruct = {}
			for table in lista:
				main_table = table[0]
				main_table = str(main_table)
				main_table = main_table.replace('CREATE TABLE','')
				main_table = main_table.replace(tableName, '')
				main_table = main_table.replace('"','')
				main_table = main_table.replace('(','')
				main_table = main_table.replace(')','')
				main_table = main_table.replace(' ','')
				listColumn = main_table.split(',')

				dataStruct[tableName] = listColumn
			return dataStruct

		@classmethod
		def structureFetch(self):
			c = conn.cursor()
			c.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;''')
			tableList = c.fetchall()
			formattedTableList = Kass.remove(tableList)
			global dataStruct
			dataStruct = {}
			for table in formattedTableList:
				c.execute("SELECT sql FROM sqlite_master WHERE tbl_name = " + "'" + str(table) + "'" + " AND type='table'")
				col_names = c.fetchall()
				#print col_names
				dataStruct.update(Database.Data.colNameFormat(col_names,table))
				
			#print dataStruct
			return dataStruct

	@staticmethod
	def list():
		c = conn.cursor()
		c.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;''')
		tableList = c.fetchall()
		formattedTableList = Kass.remove(tableList)
		Database_InfoList = []
		for command in formattedTableList:
			c.execute("SELECT sql FROM sqlite_master WHERE tbl_name = " + "'" + str(command) + "'" + " AND type='table'")
			result = c.fetchall()
			result = str(result)
			result = result[len('[("CREATE TABLE ' + str(command) + ' '):-4]
			c.execute("SELECT Count(*) FROM " + str(command))
			number = c.fetchall()
			number = str(number)[2:-3]
			daString = '[' + str(command) + ']:[' + str(number) + ']  ' + str(result) + '\n'
			daString = daString.strip('"')
			Database_InfoList.append(daString)
		return Database_InfoList

	@staticmethod
	def create():
		global conn
		if not os.path.isfile(Database.db_name):
			conn = sqlite3.connect(Database.db_Path)
			conn.text_factory = str
			return True

class Interpreter:
	class keywords:
		query = ['oque','é','significa','onde','quem','fica','sinônimos','sinônimo','sinonimos','sinonimos','procura','procurar','buscar','busca','qual','mostrar','mostra']
		add = ['adicionar','criar','crie','adicione']
		remove = ['delete', 'remova', 'exclua', 'remover', 'excluir', 'deletar']
		update = ['alterar', 'modificar', 'mudar', 'change']

	@staticmethod
	def object(string):
		objIndex = string.find('"')
		if(objIndex == -1):
			word_list = string.split(' ')
			last_entry = word_list[(len(word_list)-1)]
			if(last_entry[(len(last_entry)-1):] == "?"):
				last_entry = last_entry[:-1]
			theLastVariable = last_entry
		else:
			remainingString = string[objIndex:]
			objFinalIndex = remainingString[1:].find('"')
			objFinalIndex = objFinalIndex + objIndex + 2
			theLastVariable = string[(objIndex+1):(objFinalIndex-1)]
		return theLastVariable

	@staticmethod
	def analyze(string):
		result = {"add":0,"query":0,"remove":0,"update":0}
		stringToAnalyze = string.split(' ')
		obj = ''
		for each_word in stringToAnalyze:
			each_word = each_word.lower()
			for key in Interpreter.keywords.query:
				if(each_word == key):
					result["query"]+=1
					string = string.strip(key)
			for key in Interpreter.keywords.add:
				if(each_word == key):
					result["add"]+=1
					string = string.strip(key)
			for key in Interpreter.keywords.remove:
				if(each_word == key):
					string = string.strip(key)
					result["remove"]+=1
			for key in Interpreter.keywords.update:
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

	@staticmethod
	def act2(action, tString, dataStruct):
		c = conn.cursor()
		banned_tables = ['IMC']
		num_results = 0
		str_result = []
		for table in dataStruct:
			if(table in banned_tables):
				pass
			else:
				
				for column in dataStruct[table]:
					sql = "SELECT * FROM " + str(table) + " WHERE " + str(column) + " LIKE '%" + str(tString) + "%'"
					#print sql
					query = c.execute(sql)
					res = c.fetchall()
					if len(res) <> 0:
						for entry in res:
							single_result = []
							single_result.append('\n Tabela: ' + str(table))
							single_result.append(' -----------------------------------')
							a = 0
							for data_col in entry:
								if(data_col <> 'None'):
									single_result.append(' ' + str(dataStruct[table][a]).upper() + ": " +  str(data_col))
									a+=1
							str_result.append(single_result)
		if(len(str_result) == 0):
			talkString = 'Nao encontrei nada sobre ' + str(tString) + ' no meu Banco de Dados.\n'
			Kass.talk(talkString)
			return
		else:
			talkString = 'Encontrei ' + str(len(str_result)) + ' resultados que podem ser do seu interesse. Oque deseja fazer?'
			Kass.talk(talkString)
			command = raw_input('\n Operador: ')
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
				Kass.talk(talkOptions_01)
				print '\n'
				for result in str_result:
					Kass.clean()
					print Program.banner
					print '\n'
					for data_row in result:
						if 'None' in data_row:
							continue
						print data_row
					print '\n'
					pause = raw_input(" Kass: Pressione uma tecla para o proximo...\n")

	@staticmethod
	def extract(table):
		c = conn.cursor()
		c.execute("SELECT * FROM " + str(table))
		content = c.fetchall()
		return content

	@staticmethod
	def populate(data, targetTable, sourceTable, sourceColumn):
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

	@staticmethod
	def interpreter(string):
		UND = False


		words = string.split(' ')
		c = conn.cursor()
		repeat = []
		data_tables = ['dict_substantivos','dict_adjetivos','dict_verbos']
		for word in words:
			if(word[(len(word) -1):] == '?'):
				word = str(word[:-1])
			for table in data_tables:
				sql = "SELECT vocabulo FROM " + str(table) + " WHERE vocabulo LIKE " + "'%" + str(word) + "%'"
				c.execute(sql)
				r = c.fetchall()
				if(len(r) == 0):
					if(str(word) in repeat):
						continue
					else:
						#print 'Nao achei na table ' + str(table)
						try:
							url = 'http://dicionario-aberto.net/search-json/' + str(word)
							unknown_word = urllib2.urlopen(url)
							data= unknown_word.read()
							#print data
							json_data = json.loads(data)
							keyList = json_data.keys()
							for key in keyList:
								if(key == 'superEntry'):
									word_list = json_data[key][0]['sense'][0]
								else:
									word_list = json_data[key]['sense']
									for entry in word_list:
										classifications = {'adj.':'dict_adjetivos','f.':'dict_substantivos','m.':'dict_substantivos','v.':'dict_verbos','M.':'dict_substantivos','V.':'dict_verbos','F.':'dict_subtantivos','ADJ.':'dict_adjetivos'}
										word_class = entry['gramGrp']
										for cl in classifications:
											if(cl == word_class):
												word_class = classifications[cl]
												if(str(table) <> str(word_class)):
													continue
											else:
												continue
										word_definition = entry['def']
										word_definition = word_definition.replace('<br/>','\n')
										word_definition = word_definition.replace('_','')
										if(table == word_class):
											
											talkString = 'Você quer adicionar ' + str(word) + ' para a tabela de ' + str(word_class) + ":" + str(table) + "?"
											#print data
											Kass.talk(talkString)
											opt = raw_input('\n Operador: ')
											if opt == 'sim' or opt == 'add':
												sql = "INSERT INTO " + word_class + " VALUES (" + "'" + str(word) + "','NULL','" + word_definition + "')" 
												if(c.execute(sql)):
													talkString = 'Adicionei uma nova palavra (' + str(word) + ') para a tabela ' + str(word_class)
													conn.commit()
													repeat.append(str(word))
													Kass.talk(talkString)
						except urllib2.HTTPError:
							pass
						except KeyError:
							pass
						except TypeError:
							pass
				else:
					#print 'Achei ' + str(word)
					continue






		if(string == ''):
			Interpreter.question()

		#DETECTA SE O QUOTE FOI UTILIZADO
		if(string[0:1] == '"'):

			#DETECTA SE O ULTIMO CHAR TAMBEM é QUOTE (OU SEJA, INSERCAO NO BANCO DE DADOS)
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

		#COMANDO CLEAN PARA LIMPAR A TABELA DE TRANSIÇÃO
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

		if(string[0:len('import')] == 'import'):
			UND = True
			arg = string[len('import '):]
			if(arg <> ""):
				if(os.path.isfile(arg)):
					f = open(arg,'r')
					lines = f.readlines()
					for i in lines:
						i = i.replace('\n','')
						Interpreter.interpreter(i)
				else:
					talkOptions_10 = ['Não encontrei o arquivo.','Não pude encontrar o arquivo.','Não foi possível encontrar o arquivo.']
					Kass.random_answer(talkOptions_10)

			else:
				talkOptions_09 = ['Não encontrei nenhum argumento.', 'É necessário um argumento.','É necessário um arquivo texto como argumento.']
				Kass.random_answer(talkOptions_09)


		if(string[0:len('internet')] == 'internet'):
			arg = string[len('internet '):]
			if(arg <> ''):
				
				UND = True
				def browsing():
					objList = [Chrome, Firefox, Iexplore]
					for obj in objList:
						if(obj.path is not None):
							obj.start(arg)
							return 'Abrindo ' + str(arg) + ' no ' + str(obj.name)
				Kass.talk(browsing())
			else:
				talkString = 'É necessário informar um URL válida!'
				Kass.talk(talkString)


		#COMANDO POPULATE PARA CLASSIFICAÇÃO DE DADOS NAS TABELAS DO BANCO DE DADOS
		if(string[0:len('populate')] == 'populate'):
			UND = True
			data = Interpreter.extract('KNOWLEDGE')
			c = conn.cursor()
			c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
			tableList = c.fetchall()
			formattedTableList = Kass.remove(tableList)
			for table in formattedTableList:
				Interpreter.populate(data,table,'KNOWLEDGE','wisdom')
			conn.commit()


		if(string == 'imc'):
			UND = True
			talkOptions_06 = 'Posso calcular o seu IMC, pra isso, preciso fazer algumas perguntas: '
			Kass.talk(talkOptions_06)
			talkOptions_07 = ['Me diga o seu nome: ', 'Me informe seu nome: ','Preciso do seu nome: ']
			Kass.random_answer(talkOptions_07)
			name = raw_input('\n Operador: ')
			talkOptions_08 = ['Agora, o seu peso: ', 'Preciso, agora, do seu peso:', 'Necessito saber o seu peso: ', 'Qual seu peso?']
			Kass.random_answer(talkOptions_08)
			weight = raw_input('\n Operador: ')
			Kass.talk('A altura deve ser informada no seguinte formato: X.XX')
			talkOptions_09 = ['Por ultimo, a sua altura: ', 'Enfim, a altura: ', 'Só resta a altura: ']
			Kass.random_answer(talkOptions_09)
			height = raw_input('\n Operador: ')
			Kass.Calculate.IMC(name, weight, height)

		#EXECUTAR CONSOLE COMMAND PROMPT
		if(string[0:len('cmd')] == 'cmd'):
			UND = True
			talkOptions_03 = 'Iniciando console command prompt...'
			Kass.talk(talkOptions_03)
			try:
				cmdConsole = ''
				while(cmdConsole <> 'QUIT'):
					cmdConsole = raw_input('\n 	CMD>')
					if cmdConsole <> 'QUIT':
						cmdCommand = subprocess.check_output(str(cmdConsole),shell=True)
						talkOptions_02 = 'Executando ' + str(cmdCommand) + '...'
						Kass.talk(talkOptions_02)
						print cmdCommand
			except:
				pass

		#COMANDO SQL PARA ABRIR O CONSOLE SQL
		if(string[0:len('sql')] == 'sql'):
			UND = True
			c = conn.cursor()
			global console
			console = True
			string = 'Iniciando console SQL para o Operador...'
			Kass.talk(string)
			try:
				sqlConsole = ''
				while (sqlConsole <> 'QUIT'):
					sqlConsole = raw_input('\n	sql> ')
					sqlConsole = str(sqlConsole).upper()
					
					#Se nao for quit, executa o comando
					if sqlConsole <> 'QUIT':
						string = 'Executando comando "' + str(sqlConsole) + '"...'
						Kass.talk(string)
						c.execute(sqlConsole)
						conn.commit()
						Kass.talk(str(c.fetchall()))
			except Exception as e:
				Kass.talk(e)


		#COMANDO LISTAR TABELAS PARA VISUALIZAR INFORMAÇÕES DO BANCO DE DADOS
		listarTables = ['tabelas','tabela']
		for i in listarTables:
			if(string[0:len(i)] == str(i)):
				UND = True
				string_analysis = string.split(' ')
				if(i in string_analysis):
					string_analysis.remove(i)
				if(len(string_analysis) == 1):
					Kass.print_list(Database.list(),str(string_analysis[0]).upper())
				else:
					Kass.print_list(Database.list(),None)

		previsao = ['previsao','temperatura','metereologia','clima']
		for i in previsao:
			if(string[0:len(i)] == str(i)):
				UND = True
				string_analysis = string.split(' ')
				if(i in string_analysis):
					string_analysis.remove(i)
				if(len(string_analysis) > 0):
					confString = 'Posso buscar o relatorio climatologico da cidade de ' + str(string_analysis[0]) + '?'
					Kass.talk(confString)
					confirmation = raw_input('\n Operador: ')
					posOptions = ['sim','ok','mostrar','visualizar','emitir','efetuar','tudo bem','em frente','vamos la','vamos lá']
					if(confirmation in posOptions):
						Kass.climate(string_analysis[0])
					else:
						talkOptions_00 = ['Pesquisa cancelada','Ok, cancelar então.','Você que sabe.', "Tudo bem. Abortando...",'Tudo bem.','Pronto.']
						Kass.random_answer(talkOptions_00)
				else:
					explainString = 'O formato para consultar metereologia é "CIDADE,PAIS" como por exemplo "ASSIS,BR'
					talkString = 'De qual cidade?'
					Kass.talk(talkString)
					city = raw_input('\n Operador: ')
					Kass.climate(city)


		else:
			if UND == False:
				result, tString = Interpreter.analyze(string)
				var = Interpreter.object(string)
				if(var == ''):
					Interpreter.act2(result,tString, dataStruct)
				else:
					Interpreter.act2(result,var,dataStruct)

	@staticmethod
	def question():
		global First
		global dataStruct
		dataStruct = Database.Data.structureFetch()
		
		while 1:
			Kass.clean()
			print Program.banner
			if(First == False):
				Kass.talk("Olá! Seja bem-vindo!")
				First = True
			else:
				talkOptions_05 = ['No que posso ajudar?','No que posso servi-lo?','Esqueceu de alguma coisa?','Meu nome é Kass. Vivo para servir.','Você confia em mim, né?']
				Kass.random_answer(talkOptions_05)
			command = raw_input('\n Operador: ')
			command = command.lower()
			Interpreter.interpreter(command)
			pause = raw_input(' Kass: Pressione qualquer tecla para seguir em frente...\n')
			if(pause <> ""):
				Interpreter.interpreter(pause)


def debug():
	#INITIALIZATION AND PARAMETERS CHECK
	print Program.banner
	print '\n	Version: ' + str(Program.version)
	print '\n	Script Info:'
	print '		Current folder:' + str(Program.script.current_folder)
	print '		File name: ' + str(Program.script.file_name)
	print '		Full path: ' + str(Program.script.full_path)
	print '\n'
	print ' 	Database Info:'
	print '		Database Name: ' + str(Database.db_name)
	print '		Database Location: ' + str(Database.db_Path)



def init():
	Kass.clean()
	init_TalkString_05 = '[*] Inicializando...'
	Kass.talk(init_TalkString_05)
	global conn
	global First
	First = False
	Critical = False
	init_Steps = {'[+] Procurando pelo banco de dados...\n':Database.find_db(),'[+] Procurando por executaveis de Browser...\n':Kass.Browser.find_browser_exe(),'[+] Injetando dados do banco de dados na memoria...\n':Database.Data.structureFetch()}
	
	max_steps = float(len(init_Steps))
	one_step = float(1)
	calc = (one_step/max_steps)
	for step in init_Steps:
		Kass.clean()
		Kass.talk(step)
		init_Steps[step]
		Kass.update_progress(calc)
		calc = calc+calc
		time.sleep(1)

		

	init_TalkString_04 = ' [*] Inicializacao concluida.'
	Kass.talk(init_TalkString_04)
	cont = raw_input('')
	#end_of_init
	if Critical == True:
		Kass.talk('Erro crítico na inicialização. Abortando...')
		sys.exit(0)



def main():
	if(developer.debug_mode == True):
		debug()
	try:
		if(str(os.name) == 'nt'):
			os.system('chcp 1252 > nul')
	except Exception as e:
		print str(e)
		pass
	init()
	
	Interpreter.question()


if __name__ == '__main__':
	main()
