from caching import cacheForLRU
from flask import Flask,request
from bs4 import BeautifulSoup
import sys,requests,json

app = Flask(__name__)
cache = cacheForLRU()

def scrapeLink(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
    try:
        response = requests.get(url, headers={'User-Agent': user_agent}, verify=False, timeout=(15, 20))
        soup = BeautifulSoup(response.text,'html5lib')
        return soup
    except Exception:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        return None

def getStockCode(stockCode):
    try:
        soup = scrapeLink('https://finance.yahoo.com/quote/'+str(stockCode)+'/history?p='+str(stockCode))
        if soup:
            mainTable = soup.find('div',class_='Pb(10px) Ovx(a) W(100%)')
            if mainTable: 
                subTable = soup.find('table',class_='W(100%) M(0)').find('tbody').findAll('tr')[0].findAll('td')[-2]
                if subTable: return subTable.find('span').text
        return None
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),e)
        return None
    
def extractStockCurrentPrice(stockCode):
    closingPrice = cache.get(stockCode)
    if closingPrice!=-1:
        return {'Source':'From Caching','stockCode':stockCode,'closingPrice':closingPrice}
    else:
        closingPrice = getStockCode(stockCode)
        cache.put(stockCode, closingPrice)
        return {'Source':'New Record','stockCode':stockCode,'closingPrice':closingPrice}

@app.route('/')
def start():
    return 'API Successfully Created'

@app.route('/getData',methods=['POST'])
def processData():
    if 'stockCode' in request.json:
        stockCode = request.json["stockCode"]
        data = extractStockCurrentPrice(stockCode)
        result['stockDetails'],result['currentCache'] = data,cache.cache
        return json.dumps([result])
    else:
        return 'Please Provide Stock Code Details'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='7005')
