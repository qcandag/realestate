import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json

# emlakjet.com web scrapping/data mining project.
"""
Data paths:
    -title: <div class="zlc-title">
    -price: <div class="feature-item feature-price">5.700.000 TL</div>
    -location: <div class="zlc-location">
    -roomnumber&area: <div class="zlc-tags">
"""
header_parma = {
    'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
}

url = "https://www.zingat.com/istanbul-satilik-konut"

get_zingat = requests.get(url, headers=header_parma)
#print(get_zingat.status_code)
zingat_contents = get_zingat.content
zingat_soup = bs(zingat_contents, "lxml")

zingat_price_list = []
zingat_title_list = []
zingat_location_list = []
zingat_room_area_list = []
zingat_room_list = []
zingat_area_list = []
room_zingat_list = []
area_zingat_list = []

def get_data():
    #Get Title
    zingat_title = zingat_soup.find_all("div", attrs={"class":"zlc-title"})


    for title in zingat_title:
        zingat_title_list.append(title.text.strip())
    
    #Get Price
    zingat_price = zingat_soup.find_all("div", attrs={"class":"feature-item feature-price"})
    

    for price in zingat_price:
        zingat_price_list.append(int(price.text.replace("TL","").replace(".","").strip()))
    
    #Get Location
    zingat_location = zingat_soup.find_all("div", attrs={"class":"zlc-location"})
    

    for location in zingat_location:
        zingat_location_list.append(location.text.strip())

    #Get Room Number & Area
    zingat_room_area = zingat_soup.find_all("div", attrs={"class":"zlc-tags"})
    for room_area in zingat_room_area:
        zingat_room_area_list.append(room_area.text.strip().split("\n"))

def get_page():
    for pages in range(2,3):

        page_url = f"https://www.zingat.com/istanbul-satilik-konut?page={pages}"
        get_zingat = requests.get(page_url, headers=header_parma)
        #print(get_zingat.status_code)
        zingat_contents = get_zingat.content
        zingat_soup = bs(zingat_contents, "lxml")

        #Get Title
        zingat_title = zingat_soup.find_all("div", attrs={"class":"zlc-title"})
        for title in zingat_title:
            zingat_title_list.append(title.text.strip())
        
        #Get Price
        zingat_price = zingat_soup.find_all("div", attrs={"class":"feature-item feature-price"})
        for price in zingat_price:
            zingat_price_list.append(int(price.text.replace("TL","").replace(".","").strip()))
        
        #Get Location
        zingat_location = zingat_soup.find_all("div", attrs={"class":"zlc-location"})
        for location in zingat_location:
            zingat_location_list.append(location.text.strip())

        #Get Room Number & Area
        zingat_room_area = zingat_soup.find_all("div", attrs={"class":"zlc-tags"})
        for room_area in zingat_room_area:
            zingat_room_area_list.append(room_area.text.strip().split("\n"))

        list_len = len(zingat_room_area_list)
        
    for index in range(0,list_len):
        zingat_room_list.append(zingat_room_area_list[index][0])
        zingat_area_list.append(zingat_room_area_list[index][1])
        #zingat_area_list.append("None")
    print("Room and Area: ",zingat_room_area_list)


def write_data():
    # Write to data to dataframe
    zingat_data = pd.DataFrame()
    zingat_data["Title"] = zingat_title_list
    zingat_data["Price"] = zingat_price_list
    zingat_data["Location"] = zingat_location_list
    zingat_data["Number of Rooms"] = zingat_room_list
    zingat_data["Area"] = zingat_area_list
    
    zingat_data.to_excel("zingat_data.xlsx", index=False)
    

get_data()
get_page()
write_data()
