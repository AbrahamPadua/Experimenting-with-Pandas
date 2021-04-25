import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# Constants
PAYSCALE_ENDPOINT = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
NO_OF_PAGES = 34

# Creating the Columns
Ranks, Majors, Early_Career, Degree_Type, Mid_Career, Meaning = [], [], [], [], [], []

for page_num in range(1, NO_OF_PAGES):
    # Getting the Data
    url = PAYSCALE_ENDPOINT + f"/page/{page_num}"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Adding the Data to the Columns
    Ranks += [rank.getText()[5:]
              for rank in soup.select("tr.data-table__row > td:nth-child(1)")]
    Majors += [major.getText()[6:]
               for major in soup.select("tr.data-table__row > td:nth-child(2)")]
    Degree_Type += [degree.getText()[12:]
                    for degree in soup.select("tr.data-table__row > td:nth-child(3)")]
    Early_Career += [salary.getText()[17:]
                     for salary in soup.select("tr.data-table__row > td:nth-child(4)")]
    Mid_Career += [salary.getText()[15:]
                   for salary in soup.select("tr.data-table__row > td:nth-child(5)")]
    Meaning += [meaning.getText()[15:]
                for meaning in soup.select("tr.data-table__row > td:nth-child(6)")]

# Turning the Columns into CSV
dataframe = pd.DataFrame(list(zip(Ranks, Majors, Degree_Type, Early_Career, Mid_Career, Meaning)), columns=[
    "Rank", "Major", "Degree Type", "Early Career Salary", "Mid-Career Salary", "Meaning"])
dataframe.to_csv("Data.csv", index=False)
