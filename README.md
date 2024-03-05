# Python University Data Scraper

## Introduction

This Python script is designed for educational purposes and is intended to fetch and process data related to universities in Turkey based on specific codes provided by the Council of Higher Education (YÖK). Please note that commercial use is strictly prohibited, and the accuracy and currency of the data should be verified through official YÖK sources.

## Required Libraries

Make sure you have the following libraries installed in your Python environment:
- requests
- BeautifulSoup
- tqdm
- pandas

You can install them using pip:

```bash
pip install requests beautifulsoup4 tqdm pandas
```

## Usage

To run the script, ensure you have Python installed on your system along with the required libraries specified above. Then, execute the following command in your terminal:

```bash
python main.py 2023 all
```

## Results
The script generates an Excel file containing the data processed from YÖK. You can find the file named `university_data_<year>_<uni_type>.xlsx`, where `<year>` and `<uni_type>` correspond to the year and type of universities specified in the command line arguments.

Additionally, you can visualize the data using tools like Excel or matplotlib to gain insights into the distribution of students across different cities and university types.

## Additional Information

By modifying the department codes, you can obtain various insights such as the number of students who went to the top 5 big cities in Turkey, students who attended private universities, or those who attended the same university as they graduated from high school.

## Results Example

![Number of Students Going to University by Province](number_of_students_going_to_universtiy_by_province.png)

## Additional Data

You can find additional data in the Excel file linked below:

- [University Data Excel File](university_data_2023_all.xlsx)

## Author

This script was coded by ___Faruk Avcı.___









