from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters
import logging, re, os, pickle
import json
  

logging.basicConfig(level = logging.WARN)

job_data = {}
perTitle = {}
titCount = {}
companies = {}        
running = {}

def on_data(data: EventData):
    if running['company'] in data.company.lower():
        desc = data.description.lower()
        if titCount[title] == 100:
            raise Exception("Reached 100")
        if desc not in job_data:
            titCount[running['title']] +=1
            
            job_data[running['title']].append(desc)
            print(data.company.lower()," --- ", data.title.lower())

    else:
        print(running['company']," is not ",data.company.lower())  
           
      
    
def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('Completed a Query')
    
scraper = LinkedinScraper(
    chrome_executable_path="/Users/aproy/chromedriver", # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver) 
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=1.8,  # Slow down the scraper to avoid 'Too many requests (429)' errors
)

scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

job_titles = ["Data Scientist","Software Engineer","Data Analyst", "Business Analyst", "Quality Assurance Engineer", "Front-end Developer", "Network Engineer", "Systems Engineer"]

inputlist = {'Deloitte': 'https://www.linkedin.com/jobs/search/?f_C=1038%2C2575271%2C833228%2C2104609%2C923085%2C305921%2C9414792%2C1521182%2C2675235%2C3219775%2C4787398%2C2261938%2C1333125%2C2449847%2C5399878%2C634399%2C2223417%2C3032502%2C2015111%2C314269%2C3579500%2C3527791%2C786769%2C1176753%2C9390319%2C907951%2C3728669%2C18216%2C41897%2C8810%2C1729712%2C2428303%2C821437%2C2506324%2C2283536%2C2488727%2C2283664%2C67061%2C1176613%2C2936856%2C2481360%2C10056751%2C3311300%2C2290202%2C1721381&f_E=1%2C2%2C3&geoId=102713980&location=India',
             'KPMG':'https://www.linkedin.com/jobs/search/?f_C=2525300%2C476231%2C397575%2C438661%2C1848155%2C1517725%2C2826983%2C2354861%2C9499295%2C1678410%2C1636236%2C2525298%2C2655422%2C2525297%2C1957184%2C3360750%2C295769%2C409624%2C1285645%2C1909506%2C585513%2C2278147%2C2614401%2C319336%2C755110%2C1710123%2C2498775%2C400887%2C2389718%2C2688219%2C844671%2C5372196%2C2135383%2C1079%2C1080%2C1252142%2C335098&f_E=1%2C2%2C3&geoId=102713980&location=India',
             'PWC':'https://www.linkedin.com/jobs/search/?f_C=1044%2C3266802%2C3810745%2C3217589%2C9337226%2C2581218%2C3564656%2C2627310%2C9210507%2C3692336%2C3268473%2C3715440%2C2550006%2C2457780%2C3246816%2C3266850%2C2375025%2C3656175%2C1357453%2C3112821%2C3268526%2C2856948%2C3167442%2C2380807%2C2445697%2C309921%2C3581150%2C3230748%2C18860400%2C3225472%2C10244331%2C3625486%2C1092713%2C9495273%2C2493855&f_E=1%2C2%2C3&geoId=102713980&location=India', 
             'TCS':'https://www.linkedin.com/jobs/search/?f_C=1353&geoId=92000000&location=India',
             'Accenture':'https://www.linkedin.com/jobs/search/?f_C=9215331&f_E=2&geoId=102713980&location=India',
             'Cognizant':'https://www.linkedin.com/jobs/search/?f_C=1680&f_E=2%2C3&geoId=102713980&location=India',
             'HCL':'https://www.linkedin.com/jobs/search/?f_C=1756%2C3665057%2C5254&f_E=1%2C2%2C3&geoId=102713980&location=India',
             'Infosys':'https://www.linkedin.com/jobs/search/?f_C=1283&f_E=1%2C2&geoId=102713980&location=India',
             'Wipro':'https://www.linkedin.com/jobs/search/?f_C=1318%2C9437247&f_E=1%2C2%2C3&geoId=102713980&location=India',
             'Capegemini':'https://www.linkedin.com/jobs/search/?f_C=157240%2C1075%2C1956%2C163711%2C505336&geoId=92000000',
             'Honeywell':'https://www.linkedin.com/jobs/search/?f_C=1344%2C30848%2C2482149%2C3162288%2C49760%2C1789466%2C2344450%2C1610364%2C1379665%2C10152%2C118216%2C2344234%2C1474887%2C10452%2C16406%2C164413&f_E=1%2C2&geoId=102713980&location=India',
             'MindTree':'https://www.linkedin.com/jobs/search/?f_C=4300%2C40955666&f_E=1%2C2%2C3&geoId=102713980&location=India'
}
for key, value in inputlist.items():
    #if input("Do You Want To Continue? [y/n]") == "y":
        job_data = {}
        titCount = {}
        
        companies = {}    
        running['company'] = key.lower()
        
        companies[key] = value
        pickfile = key+".pickle"
        countfile = key+".txt"
            
        for title in job_titles:
            
            job_data[title] = []
            titCount[title] = 0
            running['title'] = title
            
            for job_url in list(companies.values()):
                queries = []
                query = Query(query=title, options=QueryOptions(limit=1000,locations=['India'],filters=QueryFilters(company_jobs_url=job_url)))
                queries.append(query)
                try:
                    scraper.run(queries)
                    print("Queries done")       
                
                except Exception as ex:
                    print(str(ex))    
        
        f = open(pickfile,"wb")
        pickle.dump(job_data,f)
        f.close()    
        
        with open(countfile, 'a') as c:
            c.write(json.dumps(titCount))
    

    