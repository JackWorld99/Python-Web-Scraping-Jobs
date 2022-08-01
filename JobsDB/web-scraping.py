import requests
from bs4 import BeautifulSoup
import pandas as pd

searchTerm = 'fresh+graduate'

def fetch_data(page, searchTerm):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = f'https://sg.jobsdb.com/j?jt=3&l=&p={page}&q={searchTerm}&sp=facet_job_type'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def extract(soup):
    divs = soup.find_all('article', class_ = 'job-card')
    for item in divs:
        title = item.find('h3', class_ = 'job-title').text.strip()
        try:
            company = item.find('span', class_ = 'job-company').text.strip()
        except:
            company = ''
        try:
            pay = item.find('div', class_ = 'content').text.strip()
            if '$' not in pay:
                raise ValueError()

            salary = pay
            char_to_replace = {'$': '',',': '','-':''}
            replaced = salary.translate(str.maketrans(char_to_replace))
            r_space = replaced.strip()
            arr = r_space.split(' ')
            if len(arr)>2 and arr[2].isnumeric():
                expect_pay = arr[2]
            elif arr[0].isnumeric():
                expect_pay = arr[0]
            else:
                expect_pay = '0'
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-abstract').text.strip()
        find_href = item.find('a', class_ ='job-link')['href']
        link = 'https://sg.jobsdb.com' + find_href

        if len(salary) > 0 and int(expect_pay) >= 3200:
            job = {
                'Job Title': title,
                'Company Name': company,
                'Salary (Month)': salary,
                'Link': link,
                'Summary': summary
            }
            joblist.append(job)
    return joblist
 
def output(joblist, searchTerm):
    if len(joblist) > 0:
        df = pd.DataFrame(joblist)
        print(df.head())
        # df.to_json(searchTerm.replace('+', ' ') + ' Job List.json')
        df.to_csv(searchTerm.replace('+', ' ') + ' Job List.csv', index = False)
        print('Saved to CSV')
    else: 
        print("No expected Job match...")
    return

joblist = []

for i in range(1,31):
    print(f'Getting page, {i}')
    soup = fetch_data(i, searchTerm)
    joblist = extract(soup)

output(joblist, searchTerm)

