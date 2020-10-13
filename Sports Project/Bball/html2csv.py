###html2list.py created by telimus for the purpose of pulling statistics from basketball-reference.com into a spreadsheet
##to-do list: write to csv
##QoL improvements: load htmls and then check urls for new one to load (that way old htmls don't need to be fetched atain)
import bs4,requests,os,sys,csv
from bs4 import Comment

####SETTINGS VARIABLES####
verbose = True
debug = False
#stats = ('orb','drb','opp_orb','opp_drb') #stats = tuple(str), list of stats to look for (planned to be imported like htmls)
stats = ('ft', 'fta')
output_filename = 'freethrows.csv'

####STORAGE CLASS####
class Site: #class to store info
	def __init__(self, year: str = '-1', team: str  = '', content = ''):
		self.year = year
		self.team = team
		self.content = content # can be html str or soup
		
####FUNCTIONS####
#def AppendData(data, appendList):
#	if data is not None:
#		appendList.append(data.string)
		
def DeleteHTMLs():
	if os.path.exists('htmls'):
		for filename in os.listdir('htmls'):
			os.remove('htmls/' + filename)
		os.rmdir('htmls')

def ImportFilesInDir(directory: str):
	sites = []
	n = ''
	c = 0
	for filename in sorted(os.listdir(directory)):
		n = filename.strip('.htmls').split('_')
		s = Site(n[0],n[1])
		filename = directory + '/' + filename
		s.content = ImportFile(filename)
		sites.append(s)
		if debug:
			c += 1
			print(n)
			print('File Loaded: ' + str(c))
	return sites

def ImportFile(filepath: str) -> str: #mainly used to import HTMLs through ImportFilesInDir or to independently import urls
	t = ''
	with open(filepath,'r') as f:
		 return f.read()

def FixURLs(l): #remove duplicates from list and sort
	if verbose:
		print('Removing any duplicates and Sorting the list')
	return list(set(l))

def URLs2Sites(urls):
	sites = []
	temp = ''
	team_name = ''
	year = '-1'
	os.makedirs('htmls',0o777,True)
	urls = urls.strip()
	if debug:
		print(urls)
	urlsList = FixURLs(urls.split('\n'))
	if debug:
		print(urlsList)
	
	for url in urlsList:
		if debug:
			print(url)
		temp = url.strip('https://www.basketball-reference.com/teams/')
		temp = temp.strip('.html').split('/')
		if debug:
			print(temp)
		team_name = temp[0]
		year = temp[1]
		
		page = requests.get(url)
		p = page.content
		s = Site(year,team_name,p)
		with open('htmls/' + s.year + '_' + s.team + '.htmls','w') as f:
			f.write(str(p))
		sites.append(s)
	return sites

def HTMLs2Soups(h):
	for site in h:
		site.content = bs4.BeautifulSoup(site.content,'lxml')

def StatFromSoup(stat, soup):
	#result = []
	#AppendData(soup.find('td', {'data-stat' : stat,'class' : 'center'}), result)

	comments = soup.find_all(string=lambda text: isinstance(text, Comment))
	for c in comments:
		cs = bs4.BeautifulSoup(c,'lxml')
		data = cs.find('td', {'data-stat': stat,'class' : 'center'})
		if data is not None:
			return data.string
		
		#AppendData(cs.find('td', {'data-stat': stat,'class' : 'center'}), result)
	return 'N/A'
	#return result

def Soups2Stats(soups, keywords):
	output = {}
	count = 0
	for site in soups:
		if not site.team in output:
			output[site.team] = {}
		for stat in keywords:
			key = site.year + ' ' + stat.capitalize()
			output[site.team][key] = StatFromSoup(stat, site.content)
			if debug:
				count += 1
				print(f"{site.team}: {key}: {output[site.team][key]}")
				print('Stat Loaded: ' + str(count))
	#print(output) #debug purposes
	return output
	
def GenerateKeys(statsDict):
	global team_keys,stat_keys
	team_keys = sorted(statsDict.keys())
	if debug:
		print('team_keys: ' + str(team_keys))	
	stat_keys = ['']
	for team in statsDict.values():
		stat_keys.extend(team.keys())
	stat_keys = sorted(list(set(stat_keys)))
	if debug:
		print('stats_keys: ' + str(stat_keys))

def Write2CSV(statsDict,row_names,col_names):
	with open(output_filename,'w', newline = '') as s:
		w = csv.writer(s, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		if debug:
			print('Writing row: ' + str(col_names))
		w.writerow(col_names)
		col_names.pop(0)
		for r in row_names:
			row = [r]
			for c in col_names:
				row.append(statsDict[r].get(c,'N/A'))
			if debug:
				print('Writing row: ' + str(row))
			w.writerow(row)
			
####Variables####
#stats = ('orb','drb','opp_orb','opp_drb') #stats = tuple(str), list of stats to look for (planned to be imported like htmls)
websites = [] #websites = list(Sites())
stats_output = {} #stats_output = dict{team:dict{year + stat:str}}
stat_keys = [] # list(str), list of dictionary keys of year + stat
team_keys = [] # same as stat_keys but for teams

####MAIN CODE###
#DeleteHTMLs()
#check for existing csv
if os.path.exists(output_filename):
	i = input(f'{output_filename} exists. Overwrite and Proceed with operations? y/n (Responding with "y" will overwrite the csv file)')
	if i.lower() != 'y':
		sys.exit(f'Operations stopped due to csv existance. Delete {output_filename} or respond "y/n" with "y" to Proceed')
	if verbose:
		print('Proceeding with operations. The csv file will be overwritten')
#first try getting content from htmls
if os.path.exists('htmls'):
	if len(os.listdir('htmls')) > 0:
		i = input('Htmls detected. Load?y/n \n(Input "n" to delete the htmls and fetch data from urls.txt again, Input "y" or any other keys to load the htmls)')
		if i.lower() == 'n':
			DeleteHTMLs()
		else:
			if verbose:
				print('Htmls detected. Loading files')
			websites = ImportFilesInDir('htmls')
#if it fails or gets nothing, try getting from url
if len(websites) < 1:
	if os.path.exists('urls.txt'):
		if debug:
			print('Htmls not found, but urls.txt detected. Fetching data from urls')
		urls = ImportFile('urls.txt')
		websites = URLs2Sites(urls)
		if verbose:
			print('Finished loading urls')
	else:
		sys.exit('CUSTOM ERROR:No file named "urls.txt" to import')

#final error for failed import
if verbose:
	print('Performing final checks on imported data')
if len(websites) < 1:
	sys.exit('CUSTOM ERROR: Failed to import sites from either "htmls" directory or "urls.txt" file')
if verbose:
	print('Sites loaded. Parsing html to soups')
	
HTMLs2Soups(websites)

if verbose:
	print('Parsing HTML2Soup completed.')
	print('Proceeding to get stats from soups')

stats_output = Soups2Stats(websites, stats)
if verbose:
	print('Stats Loading Complete: ' + str(stats_output))
	print('Proceeding to generate keys for csv file')
#Generate list of keys for columns and rows, internally sets stat_keys and team_keys
GenerateKeys(stats_output)
if verbose:
	print('Keys generated. Writing to csv')
Write2CSV(stats_output,team_keys,stat_keys)
print(f'File "{output_filename}" generated. Operation complete')
	
