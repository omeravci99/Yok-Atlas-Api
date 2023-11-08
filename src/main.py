################################################################################################################################################
#                                                                                                                                              #
#   Bu program eğitim amaçlıdır ve Yükseköğretim Kurulu (YÖK) tarafından sağlanan resmi verilere dayanmaktadır.                                #
#   Ticari amaçlar için kullanılması yasaktır. Verilerin doğruluğunu ve güncelliğini doğrulamak için YÖK resmi kaynaklarına başvurmalısınız.   #
#                                                                                                                                              #
################################################################################################################################################

################################################################################################################################################
#                                                                                                                                              #
#   This program is for educational purposes and relies on official data provided by the Council of Higher Education (YÖK).                    #
#   Commercial use is strictly prohibited. You should consult official YÖK sources to verify the accuracy and currency of the data.            #
#                                                                                                                                              #
################################################################################################################################################

#coded by Ömer Faruk Avcı, faruk.avci@ozu.edu.tr 25.09.2023

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Lists to store university codes, codes of big cities, and counting data
codes = [] # refers to all department codes
code_and_city = {} # store the informaiton for example # "İstanbul" : 453
count_and_city = {} # keeps which university in which city for example # 1054 : "İstanbul"

# Function to fetch and count data for universities
def count():
    for code in tqdm(codes, desc="Fetching Data"):
        url = f'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1020c.php?y={code}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                veriler = []
                rows = soup.find_all('tr')

                # Extract data from the HTML table on the university's page
                for row in rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) >= 3:
                        veri1 = columns[0].text.strip()
                        veri2 = int(columns[1].text.strip())
                        veriler.append([veri1, veri2])

                # Process and count the data for each city
                for liste in veriler[1:]:
                    sehir = turkish_to_english(liste[0]).lower()
                    deger = liste[1]

                    if sehir in count_and_city:
                        count_and_city[sehir] += deger
                    else:
                        count_and_city[sehir.lower()] = deger

            else:
                print(f"Failed to fetch data for code {code}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error processing code {code}: {str(e)}")

# Function to read and parse the mapping of university codes to cities from a file
def code_city():
    try:
        with open("code_and_city.txt", "r") as f:
            for line in f.readlines():
                temp_list = line.split(" ")
                if len(temp_list) == 2:
                    # Handle special case for "Afyon" or "Afyonkarahisar"
                    if  turkish_to_english(temp_list[1].strip().lower()) == "afyon" or turkish_to_english(temp_list[1].strip().lower()) == "afyonkarahisar":
                        temp_list[1] = "afyonkarahisar"
                    # Store the mapping of university code to city
                    code_and_city[int(temp_list[0].strip(":"))] = turkish_to_english(temp_list[1].strip().lower())
    except Exception as e:
        print(f"Error reading 'result.txt': {str(e)}")

# Function to read codes of universities
def codes_of_major():
    with open("all_deprtment_codes.txt", "r") as f:
        for line in f:
            line = line.rstrip("\n")
            # Check if a line starts with "1" or "2" (indicating a major university code) and add it to the list
            if line.startswith(("1", "2")):
                codes.append(int(line))
    return True
# Function to transliterate Turkish characters to English
def turkish_to_english(text):
    turkish_chars = "çÇğĞıİöÖşŞüÜ"
    english_chars = "cCgGiIoOsSuU"
    translation = str.maketrans(turkish_chars, english_chars)
    return text.translate(translation)


# Calling functions to execute the program
def main():
    codes_of_major()     # Read and store codes of major cities'universities
    code_city()          # Read and store the mapping of university codes to cities
    count()              # Fetch and count data for universities


if __name__ == "__main__":
    main()

# Printing the result
print(count_and_city)  # Print the counting data for cities


