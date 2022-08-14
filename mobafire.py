from os import error
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import random
import time


#this works 90% of the time sometimes it gets stuck and cba to fix it atm.
#File "get_league_builds\mobafire.py", line 74, in getBestRunes
#    shards = shard_container.find_all("span")
#AttributeError: 'NoneType' object has no attribute 'find_all'
#https://www.mobafire.com/league-of-legends/build/s12-updated-challenger-ivern-support-guide-587026
#


def getAllChampLinks():
    """returns list of top build url"""
    champBuilds = []
    try:
        page = requests.get("https://www.mobafire.com/league-of-legends/champions")
        soup = BeautifulSoup(page.content, "html.parser")

        championTable = soup.find_all("a", class_="champ-list__item visible")
        print("processing: "+ str(len(championTable)) + " champions")
        
        for champion in championTable:
            #dont spam server
            time.sleep(random.randrange(0,2))
            
            #get champs name
            championName = champion.find("div", class_="champ-list__item__name")
            championName = (championName.find("b")).text
            
            #get their reccomended builds page
            championBuildOptions = "https://www.mobafire.com" + champion['href']
            
            try:
                page2 = requests.get(championBuildOptions)
                soup2 = BeautifulSoup(page2.content, "html.parser")
                topBuild = soup2.find('a',class_="mf-listings__item")
                topBuild = "https://www.mobafire.com" + topBuild['href']

                print(str(championName) +" || " + str(topBuild) )
                champBuilds.append(topBuild)

            except(error):
                print(error)
            
    except(error): 
        print(error)

    return champBuilds


def getBestRunes(url):
    """scrapes runes from given url returns list of un translated runes"""
    result = []
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    rune_container = soup.find("div", class_="new-runes")
    
    #Rune classes
    rune_classes = rune_container.find_all("div", class_="new-runes__title")
    result.append(rune_classes[0].get_text())
    result.append(rune_classes[1].get_text())

    #the rest of the runes
    sub_runes = rune_container.find_all("div", class_="new-runes__item")
    for rune in sub_runes:
        temp = rune.find("span").get_text()
        if temp != "":
            result.append(temp)

    #the shards
    shard_container = rune_container.find("div", class_="new-runes__shards")
    shards = shard_container.find_all("span")
    for shard in shards: 
        result.append(shard["shard-type"])

    return(result)


def getBestRunesAll(urls):
    """calls GetBestRunes on url array saving output to text file"""
    
    #create directoy to save scrapes to
    path = Path.cwd() / "saves" / "mobafire" 
    if path.exists() == False:
        print("Creating folder: saves//mobafire")
        path.mkdir()

    
    for url in urls: 
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        #file name from page
        champion_name_block = soup.find("a", class_ ="champ-tabs__more")
        champion_name_raw = champion_name_block.get_text()
        champion_name_raw2 = champion_name_raw.replace("More ", "")
        champion_name = champion_name_raw2.replace(" Guides","")
        

        #call rune scraper
        runes = getBestRunes(url)

        #create file to store scrape in
        file_path = Path.cwd() / "saves" / "mobafire" / f"{champion_name}_mobafire.txt"
        
        file = open( file_path,"w")
        runes = getBestRunes(url)
        for rune in runes:
            file.write(rune + "\n")
        file.write(url)
        file.close()
        print(f"writting: {champion_name}")
        
        #dely to not spam the site
        time.sleep(random.randrange(0,2))


# file_path = Path.cwd() / "mobafirelinks.txt"

# links = getAllChampLinks()

# file = open( file_path,"w")
# for link in links:
#     file.write(link + "\n")



# print("links saved")

# results = getBestRunes("https://www.mobafire.com/league-of-legends/build/ziannis-challenger-veigar-guide-585002")
# print(results)