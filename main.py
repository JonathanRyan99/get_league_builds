from pathlib import Path
import metasrc
import translator




def main():
    #make output dir
    path = Path.cwd() / "saves" 
    if path.exists() == False:
        print("Creating folder: saves")
        path.mkdir()
    
    options = ["aram_all","urf_all","5v5_all"]
    print(options)


    user_input = input("please select an option: 1-3: ")
    match user_input:

        case "1" | "aram_all":
            print("aram_all")
            print("gathering metasrc ARAM URLS")
            urls = metasrc.getAllChampLinksAram()
            print("scraping build from URLs")
            metasrc.scrapeAllAram(urls)
            print("translating builds")
            translator.translate_folder("metasrcAram","METASRC","TRUE_NAME")

        case "2" | "urf_all":
            print("urf_all")
            print("gathering metasrc URF URLS")
            urls = metasrc.getAllChampLinksURF()
            print("scraping build from URLs")
            metasrc.scrapeAllURF(urls)
            print("translating builds")
            translator.translate_folder("metasrcURF","METASRC","TRUE_NAME")
            
        case "3" | "5v5_all":
            print("5v5")
            print("Collecting metasrc 5v5 urls")
            urls = metasrc.getAllChampLinks5v5()
            print("scraping web pages")
            metasrc.scrapeAll5v5(urls)
            print("translating metasrc5v5 folder")
            translator.translate_folder("metasrc5v5","METASRC","TRUE_NAME")
            
        case _:
            print("input invalid")


    
    
    
     



main()
print("Program Exited")