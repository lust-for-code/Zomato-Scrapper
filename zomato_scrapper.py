#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url='https://www.zomato.com/bangalore/south-bangalore-restaurants?page='

#extracting information from the pages
pages=[1,2,3,4,5,6]

records=[]
res_id=0
ress=[]

for page in pages:

    #extracting the content of the url
    res=requests.get(url+str(page), headers=headers)

    #parsing the content by beautifulsoup
    soup = BeautifulSoup(res.text, 'html.parser')

    #extracting all restaurants
    restaurants = soup.find_all("div",attrs={"class": "pos-relative clearfix"})
    
    for i in range(len(restaurants)):
        #extracting restaurant id
        res_id+=1

        #extracting restaurant area
        res_area=restaurants[i].find("a",attrs={'class':'ln24 search-page-text mr10 zblack search_result_subzone left'}).text
        
        #extracting restaurant type
        res=restaurants[i].find_all("a",attrs={"class": "zdark ttupper fontsize6"})
        res_type=''
        
        for inn in res:
            res_type+=(inn.text+',')
        
        res_type=res_type[:-1]
        
        x=restaurants[i].contents[1].find_all("a")
        cnt=0
        for ind in res_type:
            if ind==',':
                cnt+=1
        res_name=x[cnt+2].text.rstrip()
        
        ##extracting rating of restaurant
        rating_pattern= r"rating-popup rating-for-(\d+)[\w -]+(\d)"
        ress = re.search(rating_pattern, str(restaurants[i]))
        if ress is not None:
            rating=float(restaurants[i].find("div", attrs={"class": "rating-popup rating-for-"+ress[1]+" res-rating-nf right level-"+ress[2]+" bold"}).text)
        else:
            rating=None

        #extracting voting of restaurant
        voting_pattern= r"rating-votes-div-(\d+)[\w ->]+\>(\d+)"
        vote_obj =re.search(voting_pattern, str(restaurants[i]))
        if vote_obj is not None:
            voting=vote_obj[2]
        else:
            voting=None
        
        #compiling all the tuples for exactly 80 restaurants
        if res_id<=80:
            records.append((res_id,res_name, res_area, res_type, rating, voting))

#dataframe
df=pd.DataFrame(records, columns=['res_id','res_name', 'res_area', 'res_type', 'rating', 'voting'])

#exporting to json format
df.to_json('output.json', orient='records', lines=True)

#exporting to csv format
df.to_csv('zomato_restaurants.csv',index=False)
