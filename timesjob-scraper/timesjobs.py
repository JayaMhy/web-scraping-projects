from bs4 import BeautifulSoup
import requests
import time

familiar_skill = []
familiar_skill = input('Put skill that you are familiar with >').split(",")
print("Filtering {}".format(familiar_skill))

def find_jobs() :
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text , 'lxml')
    jobs = soup.find_all('li' , class_ = 'clearfix job-bx wht-shd-bx')
    for index,job in enumerate(jobs) :
        published_date = job.find('span', class_ = 'sim-posted').span.text
        if 'few' in published_date :
            company_name = job.find('h3' , class_ = 'joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']
            for skill in familiar_skill :
                if skill in skills :
                    with open("posts/{}.txt".format(index), 'w') as f :
                        f.write("Company name: {}\n".format(company_name.strip()))
                        f.write("Required Skills: {}\n".format(skills.strip()))
                        f.write("More info: {}\n".format(more_info))
                    print("File saved : {}".format(index))

if __name__ == "__main__" :
    while True :
        find_jobs()
        time_wait = 10
        print("Waiting {} minutes...".format(time_wait))
        time.sleep(time_wait*60)