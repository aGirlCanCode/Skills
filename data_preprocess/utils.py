import glob, os
import pickle
import sys
import nltk
from data import *


def load_filters():
    product_filter_start_idx = product_filter_end_idx = product_filter_skip_idx = service_filter_skip_idx = {}
    f = open('filters/ProductFilterStartx.pickle', 'rb')
    product_filter_start_idx = pickle.load(f)
    f.close()
    f1 = open('filters/ProductFilterEndx.pickle', 'rb')
    product_filter_end_idx = pickle.load(f1)
    f1.close()
    f2 = open('filters/ProductFilterSkipx.pickle', 'rb')
    product_filter_skip_idx = pickle.load(f2)
    f2.close()
    f3 = open('filters/ServiceFilterSkipx.pickle', 'rb')
    service_filter_skip_idx = pickle.load(f3)
    f3.close()
    return product_filter_start_idx , product_filter_end_idx , product_filter_skip_idx, service_filter_skip_idx



def input_file_preprocess(company, filename):
    desc = ""
    product_filter_start_idx , product_filter_end_idx , product_filter_skip_idx, service_filter_skip_idx = load_filters()

    if (company not in product_filter_start_idx) and (company not in product_filter_skip_idx) and (company not in service_filter_skip_idx):
        return "", False

    with open(filename, 'r') as f:
        i = 0
        lines = f.readlines()
        while (i < len(lines)-1):
            if company in product_filter_start_idx:
                start_substring = product_filter_start_idx[company]
                end_substring = product_filter_end_idx[company]
                if lines[i].startswith(start_substring):
                    while(1):
                        i += 1
                        if(lines[i].startswith(end_substring) or (i == len(lines) - 1)):
                            break
                        desc += str(lines[i])
            if company in product_filter_skip_idx:
                start_substring = product_filter_skip_idx[company]
                while(1):
                    if i == len(lines) - 1:
                        break
                    i += 1
                    if lines[i].startswith(start_substring):
                        continue
                    desc += str(lines[i])
            if company in service_filter_skip_idx:
                start_substring = service_filter_skip_idx[company]
                while(1):
                    if i == len(lines) - 1:
                        break
                    i += 1
                    if lines[i].startswith(start_substring):
                        continue
                    desc += str(lines[i])
            i += 1
    f.close()
    return desc, True


def get_updated_jd():
    product_company_jd = {}
    service_company_jd = {}
    role_jd = {}
    desc = {}
    all_companies = []
    found = False

    f = open('data/inputs/ProductCompanies.pickle', 'rb') #get the list of product company names
    product = pickle.load(f)
    f.close()

    for filename in glob.glob('data/company/*.pickle'):
        with open(os.path.join(os.getcwd(), filename), 'rb') as fl:
            company = (filename.split('/')[2]).split('.')[0]
            all_companies.append(company.lower())
            job_roles_desc = pickle.load(fl)
            for key, val in job_roles_desc.items():
                text_file = ""
                desc[key] = ""
                for idx in range(len(val)):
                    desc[key] += val[idx]
                text_file = 'data/company/' + key + company + ".txt"
                '''f = open(text_file, 'w')
                f.write(str(desc[key]))
                f.close()'''
                upd_desc, found = input_file_preprocess(company, text_file)
                if found == False:
                    upd_desc = desc[key]
                if key not in role_jd:
                    role_jd[key] = ""
                role_jd[key]+= upd_desc
                if company.lower() in product:
                    if company not in product_company_jd:
                        product_company_jd[company] = ""
                    product_company_jd[company]+= upd_desc
                else:
                    if company not in service_company_jd:
                        service_company_jd[company] = ""
                    service_company_jd[company]+= upd_desc
        fl.close()

    #Pickle JD Dicts for later use
    f1 = open('data/inputs/ProductCompanyJD.pickle', 'wb')
    pickle.dump(product_company_jd, f1)
    f1.close()
    f2 = open('data/inputs/JobRoleJD.pickle', 'wb')
    pickle.dump(role_jd, f2)
    f2.close()
    f3 = open('data/inputs/ServiceCompanyJD.pickle', 'wb')
    pickle.dump(service_company_jd, f3)
    f3.close()
    f4 = open('data/inputs/AllCompanies.pickle', 'wb')
    pickle.dump(all_companies, f4)
    f4.close()


def save_stopwords():
    my_stopwords = nltk.corpus.stopwords.words('english')

    add_stop_words = ['insights', 'description', 'role', 'degree', 'potential', 'pooling', 'position', 'technology', 'accessibility', 'regard', 'possess', 'employment', 'here', 'communication', 'environment', 'tools', 'teams', 'engineering', 'work', 'experience', 'qualifications', 'world', 'privilege', 'actions', 'eat', 'lessons', 'field', 'years', 'life', 'skills', 'culture', 'team', 'senior', 'objectives', 'modern', 'customers', 'knowledge', 'ability', 'computer', 'understanding', 'opportunity', 'building', 'requirements', 'computer science', 'defining', 'science', 'stakeholders', 'background', 'reliability', 'company', 'levels', 'patterns', 'recommendations', 'projects', 'solution', 'search', 'power', 'future', 'production', 'issues', 'day', 'year', 'reviews,', 'quality', 'e.g.', 'action', 'dynamodb', 'propose', 'feasibility', 'ph.d.', 'passion', 'age', 'mix', 'equivalent', "bachelor's", 'job', 'powerha', 'consultants', 'powerful', 'cash', 'powerplay', 'engineers', 'capital', 'things', 'people', 'firms', 'firm', 'member', 'leverage', 'threats', 'analyst', 'reporting', 'countries', 'portfolio', 'backbone', 'methodologies', 'economy', 'partners', 'economy', 'backbone', 'build', 'business,', 'businesses', 'class', 'companies', 'innovation', 'operations', 'strategy', 'polices', 'workers', 'points', 'geographies', 'gender', 'disabilities', 'policies,', 'employer', 'applicants', "world's", 'positions', 'consideration', 'equal', 'pay', 'full time', 'similar', 'qualified', 'plus', 'difficult', 'platform', 'include', 'lending', 'identifying', 'providing', 'practices', 'vulnerability', 'colour', 'religion', 'sex', 'national', 'origin', 'identity', '·', 'disability', 'ambitious', 'functions', 'preferred', 'bachelor', 'porting', 'positive', 'practical', 'least', 'non internship', 'good', 'responsibilities', 'desirable', 'fast', 'internship', 'users', 'professional', 'pim', 'key', 'googlers', 'billions', 'generation', 'phd', 'mba', 'experiences', 'target', 'internal', 'partner', 'next', 'abuse', 'trust', 'managers', 'mission', 'ads', 'capabilities', 'outstanding', 'millions', 'please', 'passout', 'date', 'towards', 'unique', 'requirement', 'duties', 'judgment', 'minimum', 'needed', 'freedom', 'useful', 'uf0b7', "you'll", 'offer', 'helpful', 'full', 'time', 'class research', 'unit', 'salesforce', 'practitioner', 'graduate', 'services', 'about', 'project', 'candidate', 'application', 'location', 'bengaluru', 'primary', 'secondary', 'educational', 'areas', 'trends', 'technical', 'clients', 'applications', 'value', 'attributes', 'client', 'qualification', 'new', 'others', 'various', 'insurance', 'create', 'delivery', 'best', 'high', 'activities', 'plan', 'contract', 'global', 'responsible', 'bangalore', 'diverse', 'problems', 'bachelors', 'effective', 'incorporate', 'able', 'right', 'place', 'journey', 'problem', 'awareness', 'part', 'alternatives', 'joiners', 'immediate', 'mandatory', 'ctc', 'inmail', 'suraj', 'player', 'play', 'com', 'br', 'andgt', 'mba', 'assistance', 'andlt', 'scope', 'practice', 'group', 'interviews', 'money', 'notice', 'www', 'hiring', 'interested', 'jobs', 'orientation', 'expression', 'jobs', 'legal', 'eligible', 'color', 'sexual', 'merit', 'disclaimer', 'marital status', 'marital', 'discrimination', 'fake', 'orientation status', 'representatives', 'interview', 'pregnancy', 'sexual orientation', 'veteran', 'race color', 'lot', "we’ve", 'roadmaps', 'hire', 'private', 'limited', 'industries', 'mid', 'b tech', 'offices', 'guidelines', 'cities', 'safety', 'directed', 'long', 'term', 'colleagues', 'transfer', 'bs relevant', 'government', 'mind', 'deliver', 'shipping', 'type', 'available', 'talent', 'early' ,'better', 'plants', 'essential', 'everything', 'employees', 'b tech', 'behavior', 'race', 'massive', 'deliveries', 'individual', 'relevant', 'division', 'component', 'ways', 'thinking', 'tax', 'management', 'level', 'proven', 'members', 'skillsandlt', 'andamp', 'scientist', 'peoplesoft', 'guide mentor', 'yrs', 'india', 'chennai', 'tcs', 'desired', 'statements', 'school', 'mba', 'policycenter', 'popular', 'point contact', 'poc', 'hr', 'important', 'coaching', 'employee', 'individuals', 'goals', 'addition', 'hyderabad', 'based', 'familiarity', 'change', 'possibilities', 'junior']

    my_stopwords.extend(add_stop_words)

    f = open('data/inputs/AllCompanies.pickle', 'rb')
    companies = pickle.load(f)
    f.close()

    my_stopwords.extend(companies)

    #Pickle stopwords for later use
    f3 = open('data/inputs/StopWords.pickle', 'wb')
    pickle.dump(my_stopwords, f3)
    f3.close()