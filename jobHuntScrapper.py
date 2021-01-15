import requests
from bs4 import BeautifulSoup
from datetime import date
import time

date = date.today().strftime('%d/%m/%Y')
time = time.strftime("%I:%M %p")


def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Safari/537.36'}
    url = f"https://in.indeed.com/jobs?l=Mysore,+Karnataka&sort=date&start={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    print(len(divs))
    for item in divs:
        tittle = item.find('a').text.strip()
        company = item.find('span', class_='company').text.strip()

        try:
            location = item.find('span', class_='location accessible-contrast-color-location').text
            salary = item.find('span', class_='salaryText').text.strip()
        except:
            location = ''.strip()
            salary = ''.strip()
        job_ref_link = item.h2.a['href']
        summary = item.find('div', {'class': 'summary'}).text.replace('\n', '')
        post_date = item.find('span', class_='date').text.strip()

        with open('extractedData\\jobsData.txt', 'a', encoding="utf-8") as f:
            f.write('\n')
            f.write(f'Tittle: {tittle} \n')
            f.write(f'Company: {company} \n')
            f.write(f'Location: {location} \n')
            f.write(f'Salary: {salary} \n')
            f.write(f'Posted: {post_date} \n')
            f.write(f'Scraped_time: {date} {time} \n')
            f.write(f'Ref_link: https://in.indeed.com{job_ref_link} \n')
            f.write(f'summary: {summary} \n')

    return


if __name__ == '__main__':
    print('')
    print('Collecting Data....')
    print('Please wait while The Scrapper collect some jobs for you')
    c = extract(0)
    with open('extractedData\\jobsData.txt', 'r+') as f:
        dataflow = f.read()
        if len(dataflow) != 0:
            f.truncate(0)
    transform(c)
    print('')
    print('scrapping done, please check the text file for scrapped data')
