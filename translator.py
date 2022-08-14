import csv
import os
from pathlib import Path

def translate(raw_list, orginal_site , target_translation="TRUE_NAME"):
    """translate raw site rips to TRUE_NAMEs 
    orginal_site = MOBAFIRE // METASRC // TRUE_NAME
    target_translation = MOBAFIRE // METASRC // TRUE_NAME
    raw_list = untranslated runes
    returns array of translated runes
    """
    print("TRANSLATING")
    result = []
    with open('runes-site-translation.csv') as f:
        DictReader_obj = csv.DictReader(f)

        for item in raw_list:
            print(f"Evaluating: {item}")
            for row in DictReader_obj:
                if item == row[orginal_site]:
                    print("raw: " + item + " == " + row[target_translation])
                    result.append(row[target_translation])
                    f.seek(0) #seeks back to the start when found to search next
                    break #breaks current loop to search next item
    return result
                        


def translate_folder(folder_Name, orignal_site, target_translation):
    """
    folder_name = dir of untranslated files
    orginal_site = MOBAFIRE // METASRC // TRUE_NAME
    target_translation = MOBAFIRE // METASRC // TRUE_NAME
    """
    
    folder_path = Path.cwd() / "saves" / folder_Name
    file_names = os.listdir(folder_path)
    
    for file in file_names:
        print(f"TRANSLATING FILE:{file}")
        with open( (folder_path / file) ) as f:
            lines = [line.rstrip('\n') for line in f]
        f.close()
        #last line is a link
        url = lines[-1] #save url information
        lines.remove(lines[-1])

        
        translated_lines = translate(lines, orignal_site, target_translation)
        translated_lines.append(url) #adds url back on the lastline
        file = open( (folder_path / file),"w")
        for translated_line in translated_lines:
            file.write(translated_line + "\n")
        file.close()

def translate_file(file_path, orignal_site, target_translation):
    """
    file_path = path to file
    orginal_site = MOBAFIRE // METASRC // TRUE_NAME
    target_translation = MOBAFIRE // METASRC // TRUE_NAME
    """
    with open( file_path ) as f:
            lines = [line.rstrip('\n') for line in f]
            f.close()
            #last line is a link
            url = lines[-1] #save url information
            lines.remove(lines[-1])

            
            translated_lines = translate(lines, orignal_site, target_translation)
            translated_lines.append(url) #adds url back on the lastline
            file = open( file_path,"w")
            for translated_line in translated_lines:
                file.write(translated_line + "\n")
            file.close()
