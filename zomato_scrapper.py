#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url='https://www.zomato.com/bangalore/south-bangalore-restaurants?page='

pages=[1,3,4,5,6]
records=[]
restaurant_id=0

#extracting information from the pages
for page in pages:

    #extracting the content of the url
    res=requests.get(url+str(page), headers=headers)

    #parsing the content by beautifulsoup
    soup = BeautifulSoup(res.text, 'html.parser')

    #extracting all restaurants of class 'pos-relative clearfix'
    restaurants = soup.find_all("div",attrs={"class": "pos-relative clearfix"})

    for i in range(len(restaurants)):
        #extracting restaurant id
        restaurant_id+=1  

        #extracting area
        area=restaurants[i].find("a",attrs={'class':'ln24 search-page-text mr10 zblack search_result_subzone left'}).text
        
        #extracting restaurant type
        restaurant_type= restaurants[i].find("div",attrs={"class": "res-snippet-small-establishment mt5"}).text.rstrip()
        
        x=restaurants[i].contents[1].find_all("a")
        cnt=0

        for i in restaurant_type:
            if i==',':
                cnt+=1
        name=x[cnt+2].text.rstrip()
        
        #compiling all the tuples
        records.append((restaurant_id,name, area, restaurant_type))

    #dataframes    
    df=pd.DataFrame(records, columns=['restaurant_id','name', 'area', 'restaurant_type'])

#exporting to json format
df.to_json('output.json', orient='records', lines=True)

#exporting to csv format
df.to_csv('zomato_restaurants.csv',index=False) 

