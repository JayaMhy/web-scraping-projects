from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import sys
 


def get_job_detail(job):
    title = job.select_one('.profile').text.strip()
    company_name = job.select_one('.company_name').text.strip()
    duration = job.select('.item_body')[1].text.strip()
    last_date = job.select_one('.apply_by').select_one(".item_body").text.strip().replace("'", "")
    page_url = "https://internshala.com" + job.a['href']  
    try:
        stipend = job.select_one('.stipend').text.strip()
    except AttributeError :
        stipend = 'NA'
    today = datetime.today().strftime('%d-%m-%Y')
    row = (title, company_name, stipend, duration, last_date, today , page_url)
    
    return row


def start_scraping(keyword='scraping') :
    rows = []
    page = 1
    #extract the job data
    while True:
        url = f'https://internshala.com/internships/keywords-{keyword}/page-{page}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.select('.individual_internship')
        for job in jobs :
            row = get_job_detail(job)
            rows.append(row)
        page_number = soup.select_one('#pageNumber').text
        total_pages = soup.select_one('#total_pages').text
        if page_number == total_pages:
            break
        print("On page:", page_number, "Pages remaining:" , total_pages)
        page = page + 1

    #save the job data to csv file
    with open(keyword+'.csv', 'w', newline='', encoding='utf-8') as f :
        writer = csv.writer(f)
        writer.writerow(['Job title', 'Company', 'Stipend', 'Duration', 'Last date', 'Extract date', 'Job listing url'])
        writer.writerows(rows)

    print('Done!')

if __name__ == "__main__":
    # total arguments
    n = len(sys.argv)
    if n==2:
        keyword = sys.argv[1]
        start_scraping(keyword)
    else:
        start_scraping()