import os
import sys
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics import mean_absolute_error
from datetime import date 

sys.path.append(os.path.join('../../'))
import settings

def generate_utility_matrix():
    df_jobs = pd.read_csv(os.path.join(settings.PATH_DATA_RAW, 'structured_skills_dataset.csv'))
    
    df_jobs.set_index('Title', inplace=True)
    df_jobs = df_jobs.unstack().reset_index(name='skills')
    df_jobs.drop(columns='level_0', inplace=True)
    
    df_jobs['count']=1
    df_jobs = df_jobs.pivot(index='Title', columns='skills', values='count').fillna(0)
    
    return df_jobs


def get_rec_str(top_10, list_skill, skillsDict, finalDF, num_recs):
    fin_str = "Below are the top <strong>{} recommendations</strong> and skills you need for them: <br>".format(num_recs)
    for each in top_10:
        df = finalDF.loc[each].values
        indices = [{v: k for k, v in skillsDict.items()}[i] for i, x in enumerate(df) if x == 1]
        req_skills = list(set(indices) - set(list_skill))
        
        if not req_skills:
            fin_str = fin_str + each + ", You don't need any extra skills!<br>" 
        else:
            fin_str = fin_str + each + ", You need the following extra skills: {}".format(str(req_skills)) + "<br>"
            
    return fin_str


# Finds best jobs/roles and additional skills required for the role    
def findJobs(ll , skills_list, finalDF , skills_ndx_dict, num_recs=10) :
    d = dict() 
    # assert len(ll) == 49 , "Length of input not correct !! " 
    for i , j  in finalDF.iterrows() : 
        mae = mean_absolute_error(j.values , ll)
        d[i] = mae 
    s = pd.Series(d) 
    top_10 = list(s.sort_values(ascending = True).iloc[:num_recs].keys())
    del(s)
    return get_rec_str(top_10, skills_list, skills_ndx_dict, finalDF, num_recs)


def createSkillDict(finalDF) : 
    skills_ndx_dict = dict()
    cnt = 0 
    for i in finalDF.columns : 
        skills_ndx_dict[i] = cnt  
        cnt+=1 
    return skills_ndx_dict 


def create_map(list_skills, finalDF, skillsDict):
    list_vals = [0]*finalDF.shape[1]
    for each in list_skills:
        list_vals[skillsDict[each]] = 1
    return list_vals


def generate_recs(list_skills, num_recs):
    finalDF = generate_utility_matrix()
    skillsDict = createSkillDict(finalDF) 
    return findJobs(create_map(list_skills, finalDF, skillsDict), list_skills, finalDF, skillsDict, num_recs)


def get_all_skills():
    finalDF = generate_utility_matrix()
    return list(finalDF.columns)