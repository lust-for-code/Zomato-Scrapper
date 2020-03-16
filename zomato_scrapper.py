import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url='https://www.zomato.com/bangalore/south-bangalore-restaurants?page='
pages=[1,3,4,5,6]
records=[]
res_id=0
for page in pages:
    res=requests.get(url+str(page), headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    restaurants = soup.find_all("div",attrs={"class": "pos-relative clearfix"})
    for i in range(len(restaurants)):
        res_id+=1
        res_area=restaurants[i].find("a",attrs={'class':'ln24 search-page-text mr10 zblack search_result_subzone left'}).text
        res_type= restaurants[i].find("div",attrs={"class": "res-snippet-small-establishment mt5"}).text.rstrip()
        x=restaurants[i].contents[1].find_all("a")
        cnt=0
        for i in res_type:
            if i==',':
                cnt+=1
        res_name=x[cnt+2].text.rstrip()
        records.append((res_id,res_name, res_area, res_type))
    df=pd.DataFrame(records, columns=['res_id','res_name', 'res_area', 'res_type'])
df.to_json('output.json', orient='records', lines=True)
df.to_csv('zomatoRestaurants.csv',index=False) 
#df