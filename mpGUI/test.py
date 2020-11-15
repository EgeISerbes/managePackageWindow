from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from urllib import parse
from urllib import request
from bs4 import BeautifulSoup
import requests
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.show()

    def setUI(self):
        self.baseUrl = 'https://pypi.org' #datayı cekecegimiz sayfa
        self.searchurl = 'https://pypi.org/search/?q=' #sayfanın arama kısmı
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'} #bağlantının engellenmemesi için kullanılan user agent
        self.setStyleSheet(open('styling.qss','r').read())
        widget = QWidget()
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        h_box1 = QHBoxLayout()

        self.searchLine = QLineEdit("")
        self.searchLine.setPlaceholderText("Enter a package name :")
        self.searchButton = QPushButton("Find package from PyPI")
        self.listItems = QListWidget()
        self.listItems.setFixedWidth(200)
        self.listItems.setFixedHeight(300)

        self._setInstructıonPage() #GUI ilk açıldığında gözüken sayfa

        self.sonuc = QTextEdit()
        self.sonuc.setFrameStyle(0)
        self.sonuc.setReadOnly(True)
        self.sonuc.setFixedHeight(300)
        v_box.addLayout(h_box)
        v_box.addLayout(h_box1)

        h_box.addWidget(self.searchLine)
        h_box.addWidget(self.searchButton)
        h_box1.addWidget(self.listItems)
        h_box1.addWidget(self.sonuc)

        self.searchButton.clicked.connect(lambda: self._searchQuery(self.searchLine)) #buton tıklanıldığında arama algoritması çalışır
        self.listItems.itemClicked.connect(lambda: self._installClicked()) #listedeki install elemanına tıklanıldığında instruction gelir
        widget.setLayout(v_box)
        widget.setFixedWidth(600)
        widget.setFixedHeight(400)
        self.setCentralWidget(widget)

    def _searchQuery(self, query):

        if query.text().strip() == "": #whitespace girilmesi ya da bir şey girilmemesi kontrolü
            self._packageNotFound()
            return

        targetUrl = self.searchurl + query.text().strip() + '&o=' #lineedit'e yazılan değere göre sitede arama yapıyoruz

        r = requests.get(targetUrl, headers=self.headers) #siteye bağlanma kısmı
        soup = BeautifulSoup(r.content, 'html.parser')
        packageDict = {} #bilgileri toplayacağımız dictionary yapısı
        try :
            callout_block = soup.find('div',class_='callout-block')

        except :
            self._packageNotFound()
            print(".")
        packages = soup.find_all('ul', class_='unstyled')
        isnotFound = True


        for link in packages:
            for name in link.find_all('span', class_='package-snippet__name'):

                if name.text.strip().lower() != query.text().strip():
                    continue
                else:
                    isnotFound = False
                    pversion = soup.find('span', class_='package-snippet__version').text.strip()
                    #print(pversion)
                    try:
                        pdetails = soup.find('p', class_='package-snippet__description').text.strip()


                    except:
                        pdetails = 'none'

                    packageDict['name'] = name
                    packageDict['version'] = pversion
                    if pdetails == 'none':
                        packageDict['details'] = ""
                    else:
                        packageDict['details'] = pdetails
                    return self._fetchPackageInfo(query, packageDict)
        if isnotFound :
            self._packageNotFound()

    def _ekle(self):
        return self.searchLine

    def _fetchPackageData(self):
        pass

    def _fetchPackageInfo(self, query, packageDict):
        packageUrl = self.baseUrl + f'/project/{query.text().strip()}/' #arama yapılan kelimenin pypi sayfası (eğer varsa)
        packageDict['PyPI page'] = packageUrl
        targetHeader1 = 'Project links'
        targetHeader2 = 'Meta'

        r = requests.get(packageUrl, self.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        findAuthor = 0
        findHeaders= []
        findLinks = []
        try:

            sidebar_section = soup.find('a',class_='vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed') #paketin kendi sayfasının linkini çekmek için
            packageDict['Homepage'] = sidebar_section['href']




        except:
            packageDict['Homepage'] = ''
        try :

            paragraphs = soup.find_all('p')


            i = 0
            for links in paragraphs:

                for perLink in links.find_all('strong'):
                    findHeaders += perLink

                    if(findHeaders[findAuthor] == 'Author:'):
                        for author in links.find_all('a',href=True):
                            packageDict['Author'] = author


                    else :
                        findAuthor += 1



        except :
            packageDict['Author'] = ''

        self._writeData(packageDict)

    def _packageNotFound(self):
        self.sonuc.setText("Package not Found !")
        return

    def _setInstructıonPage(self):
        self.listItems.addItem("<INSTALL>")
        return

   # def _findHomepage(self,href):
    #    import re
     #   return href and  re.compile(self.searchLine.text().strip()).search(href)

    def _installClicked(self):
        instructionText = """Install from PyPI 

                             If you don't know where to get the package from, then most likely you'll want to search the Python Package Index. 
                             Start by entering the name of the package in the search box above and pressing ENTER.


Install from requirements file

Click here to locate requirements.txt file and install the packages specified in it.

Install from local file

Click here to locate and install the package file (usually with .whl, .tar.gz or .zip extension).

Upgrade or uninstall

Start by selecting the package from the left.
"""
        self.sonuc.setText(instructionText)

    # if(q.text()==self.listItems.item(0)) :

    def _writeData(self, packageDict):

 
        self.sonuc.setText(f"{str(packageDict['name']).upper()}")
        self.sonuc.append("\n")
        self.sonuc.append(f"Latest stable version : {packageDict['version']} ")
        self.sonuc.append(f"Summary :{packageDict['details']} ")
        self.sonuc.append(f"Homepage : {packageDict['Homepage']}  ")
        self.sonuc.append(f"PyPI page :{packageDict['PyPI page']} ")
        self.sonuc.append(f"Author : {packageDict['Author']} ")
        return
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())