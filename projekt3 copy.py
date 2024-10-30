"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jakub Macíček

email: macicekjakub@gmail.com

discord: 
"""

import requests  # Knihovna pro stahování obsahu webových stránek
from bs4 import BeautifulSoup  # Knihovna pro parsování HTML kódu
import pandas as pd  # Knihovna pro práci s daty a ukládání do CSV
import sys  # Knihovna pro ukončení programu při chybě

# Funkce pro načtení vstupních argumentů
def parse_arguments():
    """
    Tato funkce zpracovává argumenty předané skriptu z příkazového řádku.
    Očekává dva argumenty:
    1. URL adresa územního celku, odkud budou stahována data.
    2. Název výstupního CSV souboru, kam budou uloženy výsledky.
    
    Pokud nejsou argumenty správně zadány, program se ukončí a vypíše chybovou zprávu.
    """
    #args = [str(sys.argv[1]),sys.argv[2]]
    
    #arg1 = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"#praha
    #arg1 = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"#prostejov
    arg1 = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7101"
    #arg2 = sys.argv[2]
    arg2 = "vysledky.csv"
    args = [arg1,arg2]
    # Ověříme, že URL začíná správným odkazem
    if "https://www.volby.cz" in arg1[20]:
        print("Chyba: Zadejte platný odkaz na web volby.cz.")
        sys.exit(1)  # Program ukončíme, pokud URL není správné
    return args
# Funkce pro stažení HTML obsahu stránky
def download_page(url):
    """
    Tato funkce přijímá URL odkaz, stahuje obsah stránky pomocí requests
    a následně vrací strukturovaný HTML obsah pomocí BeautifulSoup.
    Pokud je chyba při stahování stránky, program se ukončí.
    """
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Chyba při načítání stránky: {url}")
        sys.exit(1)  # Pokud stránku nelze načíst, program ukončíme

    # Vrátíme načtený a zparsovaný HTML obsah
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Funkce pro extrakci dat z tabulky výsledků
def extract_results(url):
    """
    Tato funkce přijímá HTML obsah stránky, hledá tabulku s výsledky voleb
    a extrahuje data o jednotlivých obcích a výsledcích hlasování.
    Vrací seznam dat, kde každý prvek obsahuje informace o jedné obci.
    """
    # Stáhneme HTML stránku pomocí daného URL
    soup = download_page(url)
    data_do_souboru = []
    
    # Hledáme první tabulku na stránce (předpokládáme, že obsahuje volební výsledky)
    tables = soup.find_all('table')
    is_header = False
    if not tables:
        print("Chyba: Tabulka s výsledky nebyla nalezena.")
        sys.exit(1)  # Ukončíme program, pokud tabulka neexistuje

    # Najdeme všechny řádky tabulky (vynecháme první dva řádky, pokud jsou to hlavičky)
    
    for i in range(3):
        
        table = tables[i]
        rows = table.find_all('tr')
        
        countrer = 0
        # Pro každý řádek tabulky extrahujeme data
        for row in rows:
            data = []
            if countrer < 2:
                countrer += 1
                continue
            
            
            # Získáme všechny sloupce z řádku
            columns = row.find_all('td')
            code, name = extract_obec(columns)
            if name == "-":
                break
            data.append(code),data.append(name)
            link_to_second = columns[2].find('a')['href']
            second_page = download_page("https://www.volby.cz/pls/ps2017nss/" + link_to_second)
            votes = [0] * 28
            if not(is_final_page(second_page)):
                tables_links = second_page.find('table').find_all('tr')[1:]
                table_links = tables_links[0].find_all('a')
                
                for link2 in table_links:
                    link3 = link2['href']
                    third_page = download_page("https://www.volby.cz/pls/ps2017nss/" + link3)
                    votes = list(map(lambda a, b: a + b, votes, extract_votes(third_page,"third")))
                for v in votes:
                    data.append(v)
                """if not(is_header):
                    header = headerf(third_page)
                    is_header = True
                    data_do_souboru.insert(0,header)"""
                
            else:
                votes = extract_votes(second_page,"second")
                """if not(is_header):
                    header = headerf(second_page)
                    is_header = True
                    data_do_souboru.insert(0,header)"""
                for v in votes:
                    data.append(v)
                
            data_do_souboru.append(data)
        if not(is_header):
                    header = headerf(third_page)
                    is_header = True
                    data_do_souboru.insert(0,header)
    return data_do_souboru

def is_final_page(page):
    identificator = page.find('table').find('tr').find('th').text.strip()
    if  identificator == "Okrsek":
        return False
    return True
def extract_obec(columns):
    obec_code = columns[0].text.strip()  
    obec_name = columns[1].text.strip()
    return (obec_code,obec_name)
def final_page(second_page):
    tables_links = second_page.find('table').find_all('tr')[1:]
    table_links = tables_links[0].find_all('a')
    for link2 in table_links:
        link3 = link2['href']
        third_page = download_page("https://www.volby.cz/pls/ps2017nss/" + link3)
        extract_votes(third_page,"third")
def headerf(page):
    table = page.find_all('table')
    partys = []
    header_star = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    for i in range(2):
        i += 1
        for party in table[i].find_all('tr')[2:]:
            columns_partys = party.find_all('td')
            strana = columns_partys[1].text.strip()
            partys.append(strana)
    partys.pop()
    for i in range(5):
        i = -i
        partys.insert(0,header_star[i])
    return partys

def extract_votes(page,number):
    a = 0
    b = 2
    data = []
    if number == "third":
        a = -3
        b = 1
    table = page.find_all('table')
    columns = (table[0].find_all('tr')[b:])[0].find_all('td')
    voters = columns[3+a].text.strip().replace('\xa0', '') # Počet voličů v seznamu
    Vydané_obálky = columns[4+a].text.strip().replace('\xa0', '') # Počet vydaných obálek
    valid_voters = columns[7+a].text.strip().replace('\xa0', '') # Počet platných hlasu
    data.append(int(Vydané_obálky)),data.append(int(voters)),data.append(int(valid_voters))
    
    for i in range(2):
        i = i + 1
        for party in table[i].find_all('tr')[2:]:
            columns_partys = party.find_all('td')
            data.append(int(columns_partys[2].text.strip().replace("-","0")))
    data.pop()
    return data
# Funkce pro uložení dat do CSV5
def save_to_csv(data, output_file):
    """
    Tato funkce přijímá extrahovaná data (seznam obcí a jejich volebních výsledků),
    název výstupního souboru a hlavičku (názvy sloupců) a ukládá data do CSV souboru
    pomocí knihovny pandas.
    """
    header = data[0]
    data.pop(0)
    #print(len(header))
    #print(len(data[2]))
    df = pd.DataFrame(data,columns=header)  # Vytvoříme DataFrame s danými daty a hlavičkou
    df.to_csv(output_file, index=False)  # Uložíme DataFrame do CSV souboru
    print(f"Výsledky byly úspěšně uloženy do {output_file}")  # Vypíšeme potvrzení o uložení

# Hlavní funkce programu
def main():
    """
    Hlavní funkce programu, která řídí celý průběh:
    1. Načte argumenty z příkazového řádku.
    2. Stáhne obsah stránky podle zadaného URL.
    3. Extrahuje data z tabulky s volebními výsledky.
    4. Uloží výsledky do CSV souboru podle zadaného názvu.
    """
    args = parse_arguments()  # Načteme argumenty (URL a výstupní soubor)
    
    # Extrahujeme data o volebních výsledcích z načtené stránky
    data = extract_results(args[0])
    
    # Definujeme hlavičku CSV souboru (sloupce), kde každý název odpovídá správné informaci
    
    # Uložíme výsledky do CSV souboru

    save_to_csv(data, args[1])

# Spustíme hlavní funkci programu
if __name__ == "__main__":
    main()
