import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag

import re
import nltk

from gensim import corpora, models, matutils
from gensim.models.coherencemodel import CoherenceModel

from skills.data_preprocess.data.inputs import *


def get_jd_dataframe(jd_dict):
    jd_df = pd.DataFrame(jd_dict, index=[0]).transpose()
    jd_df.columns = ['description']
    jd_df = jd_df.sort_index()
    return jd_df


def my_tokenizer(text):
    return re.split("\\s+",text)


def pos_filter(text):
    '''Given a string of text, tokenize the text and pull out only the nouns and adjectives'''
    is_noun_or_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
    tokenized = my_tokenizer(text)
    all_nouns_adj = [word for (word, pos) in pos_tag(tokenized) if is_noun_or_adj(pos)] 
    return ' '.join(all_nouns_adj)


def clean_text(text):
    my_punctuation = '!"$%&\'()*,-./:;\\\<=>?[\\]^_`{|}~•@–'
    my_stopwords = []
    f = open('../../skills/data_preprocess/data/inputs/StopWords.pickle', 'rb')
    my_stopwords = pickle.load(f)
    f.close()
    text = text.lower()
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('…', '', text)
    text = re.sub('['+my_punctuation +']+', ' ', text)
    text_list = [word for word in text.split(' ')
                            if word not in my_stopwords] # remove stopwords
    text = ' '.join(text_list)
    return text


round1 = lambda x: clean_text(x)


def data_clean(df):
    post_pos_filter_data = pd.DataFrame(df.description.apply(pos_filter))
    data_clean = pd.DataFrame(post_pos_filter_data.description.apply(round1))
    return data_clean



def data_transform(df, jd):
    if jd == True:
        cv = CountVectorizer(tokenizer=my_tokenizer, ngram_range=(1,2), max_df=0.90, min_df=0.10)
    else: #most of syllabus terms are unique, so don't need max and min IDF
        cv = CountVectorizer(tokenizer=my_tokenizer, ngram_range=(1,2))
    data_cv = cv.fit_transform(df.description)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = df.index
    return data_dtm, cv


def run_data_transform_pipeline(df, jd):
    cleaned_df = data_clean(df)
    data_dtm, cv = data_transform(cleaned_df, jd)
    return data_dtm, cv


def get_syl_list_2018():
    subs = []
    syllabus_2018 = []
    f = open('../../skills/data_preprocess/data/inputs/Syllabus18.pickle', 'rb')
    subs = pickle.load(f)
    f.close()
    for des in subs:
        des = des.replace('.',',')
        sentences = des.split(".") 
        while '' in sentences:
            sentences.remove('')
        syllabus_2018.extend(sentences)  
    return syllabus_2018


def get_syl_list_2014():
    df = pd.read_excel("../../skills/data_preprocess/data/inputs/Paragraphsyllabus2014.xlsx", sheet_name='Sheet1', usecols="E")
    temp = df.values.tolist()
    syllabus_2014 = []
    for arr in temp:
        syllabus_2014.append(''.join(arr))
    return syllabus_2014


def prepare_syl_for_lda(syllabus, dictionary):
    syllabus_tokens = my_tokenizer(syllabus)
    syl_bow = dictionary.doc2bow(syllabus_tokens)
    return syl_bow


def transform_syllabus_to_lda_model(model, dictionary, year):
    if year == '2018':
        syllabus_list = get_syl_list_2018()
    if year == '2014':
        syllabus_list = get_syl_list_2014()
    result_syl_jd = {}
    for syl in syllabus_list:
        syl_bow = prepare_syl_for_lda(syl, dictionary)
        doc_topics = (model.get_document_topics(syl_bow))
        doc_topics.sort(key = lambda x:x[1], reverse=True)
        top_topics = {i[0] : i[1] for i in doc_topics[:3]}
        result_syl_jd[syl] = top_topics
    return result_syl_jd
