import json
import re
import mechanicalsoup
import requests
import os

os.environ['GOOGLE_MAPS_API_KEY'] = 'AIzaSyCPRJVtczSvz5xKJKSl-Edi-iFj8yPYkv8'
os.environ['BACK4APP_APP_ID'] = 'tpZ2UGamEjsClSSUiNsJIQZrnBB24rdVxrOjduJ0'
os.environ['BACK4APP_API_KEY'] = '7G1ZyRgPJ4gCp1BGweoMEpdAh65sSYAZEkEri0kk'


def getBrands():
    brandsRes = requests.get(
        'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10000&order=Make&keys=Make',
        headers={'X-Parse-Application-Id': os.getenv('BACK4APP_APP_ID'), 'X-Parse-REST-API-Key': os.getenv('BACK4APP_API_KEY')})
    brands = brandsRes.json()
    uniqBrands = list()
    for i in range(len(brands['results'])):
        if brands['results'][i]['Make'] not in uniqBrands:
            uniqBrands.append(brands['results'][i]['Make'])

    return uniqBrands


def getModels(brand):
    url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=1000&order=Model&keys=Make,Model,Year&order=Model,Year&where=%0A++++++++%7B%0A++++++++++++%22Make%22%3A+%22' + brand + '%22%0A++++++++%7D%0A++++++++'
    modelsRes = requests.get(url, headers={'X-Parse-Application-Id': os.getenv('BACK4APP_APP_ID'), 'X-Parse-REST-API-Key': os.getenv('BACK4APP_API_KEY')})

    return modelsRes


def getTankStation(request):
    region = request.POST.get('region')
    fuel = request.POST.get('fuel')
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('https://www.ceskybenzin.cz/aktualni-ceny-PHM/' + region + '/' + fuel, verify=False)
    page = browser.get_current_page()
    pageResult = page.find_all("table", id='vypis1')
    regResult = re.findall("<td[^>]*>(.*?)<\/td>", str(pageResult))

    result = list(dict())
    i = 0
    while i < len(regResult):
        curResDict = dict()
        curResDict['name'] = regResult[i + 1]
        curResDict['address'] = regResult[i + 2]
        strPrice = regResult[i + 3].replace("Kč", "")
        curResDict['price'] = strPrice
        result.append(curResDict)
        i += 9

    jsonResult = json.dumps(result)
    return jsonResult


def getMapGeometry(request):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    inputStr = str(request.POST.get('inputStr'))
    geoPositions = requests.get(url, params={'key': os.getenv('GOOGLE_MAPS_API_KEY'), 'input': inputStr, 'inputtype': 'textquery', 'fields': 'geometry'})

    return geoPositions
