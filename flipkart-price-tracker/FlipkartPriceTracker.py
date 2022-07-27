import requests
from bs4 import BeautifulSoup
import smtplib

url = 'https://www.flipkart.com/addyvero-regular-fit-women-black-trousers/p/itmdfe8b3d718721?pid=TROFPJ8BPR86ND36&lid=LSTTROFPJ8BPR86ND364AVUD3&marketplace=FLIPKART&srno=s_1_4&otracker=AS_QueryStore_OrganicAutoSuggest_1_14_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_14_sc_na_na&fm=SEARCH&iid=8a0ec7ec-2fec-4879-97be-b445703c4c20.TROFPJ8BPR86ND36.SEARCH&ppt=sp&ppn=sp&ssid=bm2qcg8iio0000001611163337081&qH=f1e93bc2177ea407'

headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

def check_price():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.select_one(".B_NuCI").get_text()
    price = soup.select_one("._30jeq3").get_text()
    f_price = float(price[1:])

    print(title)
    print(price)

    if(f_price < 450) :
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('xyz@gmail.com', 'xyxulbeujggkspgh')
    subject = 'Rani! flipkart price fell down, go grab it!'
    body = 'Check the flipkart link \n https://www.flipkart.com/addyvero-regular-fit-women-black-trousers/p/itmdfe8b3d718721?pid=TROFPJ8BPR86ND36&lid=LSTTROFPJ8BPR86ND364AVUD3&marketplace=FLIPKART&srno=s_1_4&otracker=AS_QueryStore_OrganicAutoSuggest_1_14_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_14_sc_na_na&fm=SEARCH&iid=8a0ec7ec-2fec-4879-97be-b445703c4c20.TROFPJ8BPR86ND36.SEARCH&ppt=sp&ppn=sp&ssid=bm2qcg8iio0000001611163337081&qH=f1e93bc2177ea407'
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail('xyz@gmail.com', 'abc@gmail.com', msg)
    print('RANI EMAIL HAS BEEN SENT!')
    server.quit()
check_price()