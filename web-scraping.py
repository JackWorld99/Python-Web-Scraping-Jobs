import requests
from bs4 import BeautifulSoup
import pandas as pd

searchTerm = 'fresh+graduate'

def fetch_data(page, searchTerm):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = f'https://sg.indeed.com/jobs?q={searchTerm}&l=Singapore&sc=0kf%3Ajt%28fulltime%29%3B&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def extract(soup):
    joblist = []
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('h2', class_ = 'jobTitle').text.strip()
        company = item.find('span', class_ = 'companyName').text.strip()
        try:
            pay = item.find('div', class_ = 'attribute_snippet').text.strip()
            pay.index('$')
            salary = pay
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip()
        find_href = item.find('a', class_ ='jcs-JobTitle')['href']
        link = 'https://sg.indeed.com' + find_href

        job = {
            'Job Title': title,
            'Company Name': company,
            'Salary (Month)': salary,
            'Link': link,
            'Summary': summary
        }
        joblist.append(job)
    return joblist
 
def output (joblist, searchTerm):
    df = pd.DataFrame(joblist)
    print(df.head())
    df.to_csv(searchTerm.replace('+', ' ') + ' Job List.csv', index = False)
    print('Saved to CSV')
    return


for i in range(0,50,10):
    print(f'Getting page, {i}')
    soup = fetch_data(i, searchTerm)
    joblist = extract(soup)

output (joblist, searchTerm)