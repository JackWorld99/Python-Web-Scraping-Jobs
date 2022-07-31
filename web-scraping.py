import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = 'https://sg.indeed.com/jobs?q=fresh+graduate&l=Singapore&sc=0kf%3Ajt%28fulltime%29%3B&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'cardOutline')
    for item in divs:
        title = item.find('h2', class_ = 'jobTitle').text.strip()
        company = item.find('span', class_ = 'companyName').text.strip()
        try:
            dollar = '$'
            salary_a = item.find('div', class_ = 'attribute_snippet').text.strip()
            salary_a.index(dollar)
            salary = salary_a
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip()

        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)

joblist = []

for i in range(0,50,10):
    print(f'Getting page, {i}')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('joblist.csv')