import requests
from bs4 import BeautifulSoup
import sys
from tqdm import tqdm
import pandas as pd
class YokApi:
    def __init__(self, year, uni_type):  
        self.year = year
        self.uni_type = uni_type
        self.uni_codes = [] # refers to all department codes
        self.priv_uni_codes = []  # refers to private university department codes for example # 1054
        self.state_uni_codes = [] # refers to state university department codes for example # 2079

        self.code_and_city = {} # keeps which university in which city for example # 1054 : "İstanbul"  
        self.count_and_city = {} # keeps which city has how many students went to university for example # "İstanbul" : 80506
        self.own_city_count = {}
        self.get_uni_codes()
        self.get_city_codes()
        self.get_uni_data()

    def get_uni_codes(self):
        file_path = f'all_deparments_codes{self.year}.txt'
        with open(file_path, "r") as f:
            for line in f.readlines():
                line = line.rstrip("\n")
                if line.startswith(("1", "2")):
                    self.uni_codes.append(int(line))
                    if line.startswith("1"):
                        self.state_uni_codes.append(int(line))
                    else:   
                        self.priv_uni_codes.append(int(line))

    def get_city_codes(self):
        file_path = "code_and_city.txt"
        with open(file_path, "r") as f:
            for line in f.readlines():
                temp_list = line.split(" ")
                if len(temp_list) == 2:
                    self.code_and_city[int(temp_list[0].strip(":"))] = self.turkish_to_english(temp_list[1].strip().lower())

    def turkish_to_english(self, text):
        turkish = "çÇğĞıİöÖşŞüÜ"
        english = "cCgGiIoOsSuU"
        table = str.maketrans(turkish, english)
        return text.translate(table)

    def get_uni_data(self):
        if self.uni_type == "state":
            uni_list = self.state_uni_codes
        elif self.uni_type == "private":
            uni_list = self.priv_uni_codes
        else:
            uni_list = self.uni_codes

        with tqdm(total=len(uni_list), desc="Fetching Data") as pbar:
            
            for code in uni_list:
                if self.year == 2023:
                    url = f'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1020c.php?y={code}&t=1'
                else:
                    url = f'https://yokatlas.yok.gov.tr/{self.year}/content/lisans-dynamic/1020c.php?y={code}'
                try:
                    response = requests.get(url)
                    current_uni_city = self.code_and_city[int(code/100000)]
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        veriler = []
                        rows = soup.find_all('tr')

                        for row in rows[1:]:
                            columns = row.find_all('td')
                            if len(columns) >= 3:
                                veri1 = columns[0].text.strip()
                                veri2 = int(columns[1].text.strip())
                                veriler.append([veri1, veri2])

                        for liste in veriler[1:]:
                            sehir = self.turkish_to_english(liste[0]).lower()
                            deger = liste[1]
                            
                            if sehir == current_uni_city:
                                if sehir in self.own_city_count:
                                    self.own_city_count[sehir] += deger
                                else:
                                    self.own_city_count[sehir] = deger
                            
                            if sehir in self.count_and_city:
                                self.count_and_city[sehir] += deger
                            else:
                                self.count_and_city[sehir.lower()] = deger
                            

                            

                    else:
                        print(f"Failed to fetch data for code {code}, Status Code: {response.status_code}")
                except Exception as e:
                    print(f"Error processing code {code}: {str(e)}")
                pbar.update(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <year: 2019 to 2023> <uni_type: all, private, state>")
        sys.exit(1)
    
    year = int(sys.argv[1])
    uni_type = sys.argv[2]

    if year not in range(2019, 2024) or uni_type not in ["all", "private", "state"]:
        print("Usage: python main.py <year: 2019 to 2023> <uni_type: all, private, state>")
        sys.exit(1)
    
    yok = YokApi(year, uni_type)

    df = pd.DataFrame(yok.count_and_city.items(), columns=['City', 'Student Count'])
    excel_file = f'university_data_{year}_{uni_type}.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Data exported to {excel_file}")

if __name__=="__main__":
    main()
