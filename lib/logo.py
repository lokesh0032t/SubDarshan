import time
import colorama
def logo():
   

    

    with open('lib/info.txt', 'r', encoding='cp1252') as f:
        for i in f:
            g = i.strip()
            print(f"{colorama.Fore.LIGHTCYAN_EX}{g}{colorama.Style.RESET_ALL}")
            time.sleep(.05) 


        
        print("Starting...........")