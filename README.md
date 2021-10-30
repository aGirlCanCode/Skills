# University-Curriculum-JDSkills

Project to compare university syllabus with the most in-demand job skills

We use two datasets for the purpose of our project – (i) LinkedIn Dataset - job descriptions from the latest vacant job postings on LinkedIn and (ii) CS Course Dataset - course objectives from the Computer Science curriculum. 
For (i), we use LinkedIn as it is one of the most popular job portals in India and has more than sufficient data for the purpose of our study. We scrape jobs limited to the region of India. The organization of the scraped data into documents is done in two ways keeping different end goals in mind:

1) Based on defined job roles: Each document in the corpus will have a collection of job descriptions based on the computer science relevant job role, like ‘Data      Scientist’, ‘Network Engineer’, ‘Software Engineer’, ‘Hardware Engineer’ etc. irrespective of the company. For e.g., all ‘Data Scientist’ job vacancies from        different companies will be collected in the same document. Using this method, we can analyze the top skills for any desired job role. 
1) Based on the group of companies (further subdivided into A) service and B) product company groups): Each group of companies will have a defined list based on the    company category in university job placements. Each document in the corpus will have a collection of job descriptions based on the overarching company groups        irrespective of the job role. For e.g., the product company group includes companies like ‘Amazon’ and ‘Cisco’, and the service company group includes companies    like ‘Deloitte’ and ‘Honeywell’. These companies were selected and segregated based on the university placement record. Using this method, we can analyze the top    skills for any desired group of companies.

For each of the above 1), 2A) and 2B), we have used LDA and BerTopic for topic modelling on the JD dataset. 

Similarly, LDA and BerTopic topic modelling is applied to syllabus data from 2018 and 2014 to evaluate the curriculum evaluation. 

We use the syllabus data to make predictions on the 1), 2A), 2B) LDA and BerTopic trained models to see what topics this unseen data falls into. The HTML files generated from the Colab have the dynamic Plotly images which help in comparing the gaps in the syllabus & JD Topic models. 

The data is not included in this repository. It will be published along with the research paper soon.  

