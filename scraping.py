import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import PatternFill
 
orangeFill = PatternFill(start_color='FFC000',
                   end_color='FFC000',
                   fill_type='solid')
 
blueFill = PatternFill(start_color='00B0F0',
                   end_color='00B0F0',
                   fill_type='solid')
 
wb = Workbook()

del wb['Sheet']

sheet = wb.create_sheet('planilha')

response = requests.get('https://ufu.br/')

if(response.status_code == 200):
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.title.contents)
    
    leftBar = soup.find('ul', class_='sidebar-nav nav-level-0')
    leftBarLines = leftBar.find_all('li', class_='nav-item')

    initCapture = False
    linesWishLeftBar = []
    linksWishLeftBar = []
    for li in leftBarLines:
        if 'Graduação' in li.text.strip():
            initCapture = True

        if initCapture:
            linesWishLeftBar.append(li.text.strip())
            linksWishLeftBar.append(li.a.get('href'))
            linesWishLeftBar

sheet.cell(1,1).value = "Menu Nav"
sheet.cell(1,1).fill = orangeFill
 
sheet['B1'] = "Links"
sheet['B1'].fill = blueFill
 
for i, linha in enumerate(linesWishLeftBar):
    sheet.cell(i+2,1).value = linha
 
for i, link in enumerate(linksWishLeftBar): 
    sheet.cell(i+2,2).value = "https://ufu.br"+link
 
wb.save("UFU_menu_nav.xlsx")