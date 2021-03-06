import csv
import re
from pprint import pprint

def setCleanSomething():
    a = open("518_Taipei.csv").read()
    a = a.split("\n")
    a[0] =  a[0].replace("：","")
    open("518_Taipei_clean.csv","w").write("\n".join(a))


def setSectionname(d):
    d['address'] = d['上班地點']
    if re.match(r"台北市\w+區", d['上班地點']):
        dis =  re.findall(r"台北市(\w+?)區{1}", d['上班地點'])[0]
        d['section_name'] = dis
        d['region_name'] = '台北市'
    else:
        pprint(d)

def setMap(d):
    dic = {"lng":"NA","lat":"NA"}
    if d['Map'].find(',')!=-1:
        mapstr = d['Map'].split(',')
        dic['lat'] = mapstr[0]
        dic['lng'] = mapstr[1]
    d.update(dic)

def setTitle(d):
    title = d['URL']
    if re.match(r"http://www.518.com.tw/.*?-台北市", d['URL']):
        t = re.findall(r"http://www.518.com.tw/(.*?)-台北市", d['URL'])[0]
        d['title'] = t
    else:
        print(d['URL'])
    

def setMoney(d):
    money = d['薪資待遇']

    money = money.replace(',','')
    dic = {}
    for i in ["hourlow","hourhigh","daylow","dayhigh","monthlow","monthhigh"]:
        dic[i] = "NA"

    if re.match(r"日薪 NTD \d+至\d+元",money):
        fmoney = re.findall(r"日薪 NTD (\d+)至(\d+)元",money)[0]
        dic["daylow"] = fmoney[0]
        dic["dayhigh"] = fmoney[1]
    elif re.match(r"時薪 NTD \d+至\d+元",money):
        fmoney = re.findall(r"時薪 NTD (\d+)至(\d+)元",money)[0]
        dic["hourlow"] = fmoney[0]
        dic["hourhigh"] = fmoney[1]
    elif re.match(r"月薪 NTD \d+至\d+元",money):
        fmoney = re.findall(r"月薪 NTD (\d+)至(\d+)元",money)[0]
        dic["monthlow"] = fmoney[0]
        dic["monthhigh"] = fmoney[1]
    elif re.match(r"NTD \d+~\d+元",money):
        fmoney = re.findall(r"NTD (\d+)~(\d+)元",money)[0]
        dic["monthlow"] = fmoney[0]
        dic["monthhigh"] = fmoney[1]
    elif re.match(r"時薪 NTD \d+元以上",money):
        fmoney = re.findall(r"時薪 NTD (\d+)元以上",money)[0]
        dic["hourlow"] = fmoney
        dic["hourhigh"] = "+"
    elif re.match(r"日薪 NTD \d+元以上",money):
        fmoney = re.findall(r"日薪 NTD (\d+)元以上",money)[0]
        dic["daylow"] = fmoney
        dic["dayhigh"] = "+"
    elif re.match(r"月薪 NTD \d+元以上",money):
        fmoney = re.findall(r"月薪 NTD (\d+)元以上",money)[0]
        dic["monthlow"] = fmoney
        dic["monthhigh"] = "+"
    elif re.match(r"日薪 NTD \d+元以下",money):
        fmoney = re.findall(r"日薪 NTD (\d+)元以下",money)[0]
        dic["daylow"] = "+"
        dic["dayhigh"] = fmoney
    else:
        #re.match(r"週薪 NTD \d+元以上",money) or re.match(r"年薪 NTD \d+至\d+元",money): # few
        if money not in ["依公司規定","面議"]:
            print(money)
    d.update(dic)


#header
fieldnames = ['title','URL','address', 'section_name', 'region_name','lng','lat',"hourlow","hourhigh","daylow","dayhigh","monthlow","monthhigh","薪資待遇"]

writer = csv.DictWriter(open("518_Taipei_ok.csv","w"), fieldnames=fieldnames)
writer.writeheader()


#main
setCleanSomething()
csvdata = csv.DictReader(open("518_Taipei_clean.csv"))

for i in csvdata:
    setTitle(i)
    setSectionname(i)
    setMap(i)
    setMoney(i)
    newdata = { key:i[key] for key in fieldnames }
    writer.writerow(newdata)

exit()
#show 
csvdata = csv.DictReader(open("518_Taipei_ok.csv"))
num = 0 
for i in csvdata:
    pprint(i)
    num += 1
    if num>5:
        break
