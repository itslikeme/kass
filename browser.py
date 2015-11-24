import os, subprocess

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
									Chrome = Browser('Google Chrome',os.path.join(root,file))
								if(file == 'firefox.exe'):
									Firefox = Browser('Mozilla Firefox',os.path.join(root,file))
								if(file == 'iexplore.exe'):
									Iexplore = Browser('Internet Explorer',os.path.join(root,file))
print 'Searching for browser exeuctables...'
Browser.find_browser_exe()
Chrome.start('google.com.br/search?q="THIS+IS+A+TEST"')