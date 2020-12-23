
import urllib.request
from bs4 import BeautifulSoup
import csv

url2 = 'https://www.espn.com/nfl/team/depth/_/name/lac/los-angeles-chargers'

req2 = urllib.request.Request(url2)
con2 = urllib.request.urlopen(req2)


parse2 = BeautifulSoup(con2, 'html.parser')


t = parse2.find_all('a', {'class' : 'AnchorLink'})


with open('index.csv', 'a') as csv_file:
  writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
  #i=0
  for col1, col2, col3 in zip(t):
    writer.writerow([col1.get_text().strip()])
    if(col2.get_text().strip() != ""):
      writer.writerow([col2.get_text().strip()])
    if(col3.get_text().strip() != ""):
      writer.writerow([col3.get_text().strip()])

