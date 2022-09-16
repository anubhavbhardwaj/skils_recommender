import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics import mean_absolute_error
from datetime import date 


def getSkills(x , unique_skills):
    l = list()
    for i in str(x).split():
        if i in unique_skills: 
            l.append(i)
    if len(l)== 0:
        return None
    l = list(set(l))
    return l

# Merging both basic qualifications and preferred qualifications
def merge(x) : 
    if x['BASIC QUALIFICATIONS'] == None and x['PREFERRED QUALIFICATIONS'] != None : 
        return x['PREFERRED QUALIFICATIONS']
    elif x['BASIC QUALIFICATIONS'] != None and x['PREFERRED QUALIFICATIONS'] == None : 
        return x['BASIC QUALIFICATIONS']
    elif x['BASIC QUALIFICATIONS'] == None and x['PREFERRED QUALIFICATIONS'] == None :
        return None 
    return x['BASIC QUALIFICATIONS'] + x['PREFERRED QUALIFICATIONS']


def load_data() : 
    amazon = pd.read_csv('./data/amazon_jobs_dataset.csv')
    skills  = pd.read_csv('./data/skills.csv' , dtype = str) 

    skills = skills.unstack(level = 0 ).dropna().reset_index()[0]
    l = list()
    for i in skills.values  : 
        for j in i.split(';') :
            l.append(j) 
    unique_skills = list(set(l))

    amazon['BASIC QUALIFICATIONS'] = amazon['BASIC QUALIFICATIONS'].apply(lambda x : getSkills(x , unique_skills) )
    amazon['PREFERRED QUALIFICATIONS'] = amazon['PREFERRED QUALIFICATIONS'].apply(lambda x : getSkills(x , unique_skills))
    amazon['Posting_date'] = pd.to_datetime(amazon['Posting_date'])
    amazon.drop('Unnamed: 0' , axis = 1 , inplace = True)

    amazon['QUALIFICATIONS'] = amazon.apply(merge , axis = 1)
    amazon.drop(['BASIC QUALIFICATIONS' , 'PREFERRED QUALIFICATIONS'] ,axis = 1 , inplace = True )
    amazon.dropna(inplace= True)

    amazon = amazon.loc[ : , ['Title' , 'QUALIFICATIONS' , 'Posting_date']]
    cnt =0 
    for i in amazon.iterrows():
        for j in i[1]['QUALIFICATIONS']:
            amazon.loc[cnt,j] = 1
        cnt+=1
    
    amazon.fillna(0 , inplace = True)
    amazon = amazon[amazon.Title != 0]
    amazon.drop('QUALIFICATIONS' , axis =1 , inplace = True )

    hashmap= {} 
    
    for i , j in amazon.groupby('Title') : 
        hashmap[i] = j.sort_values(by = 'Posting_date' , ascending= False).iloc[0,2:]

    #     Dataframe for skills corresponding to each role 
    finalDF = pd.DataFrame(hashmap).T

    return finalDF

# Calculates skill difference between input skills and closest jobs 
def skilldiff(top_10 , ll  ,finalDF , skills_ndx_dict  ): 
    add = dict()
    for i in top_10 :
        cnt = 0 
        l = list()
        for j in finalDF.loc[i] : 
            if j == 1 and ll[cnt]!=1 : 
                l.append(skills_ndx_dict[cnt])
            cnt+=1 
        add[i] = l
    return add
        
# Finds best jobs/roles and additional skills required for the role    
def findJobs(ll , finalDF , skills_ndx_dict) :
    d = dict() 
    # assert len(ll) == 49 , "Length of input not correct !! " 
    for i , j  in finalDF.iterrows() : 
        mae = mean_absolute_error(j.values , ll)
        d[i] = mae 
    s = pd.Series(d) 
    top_10 = list(s.sort_values(ascending = True).iloc[:10].keys())
    del(s)
    return skilldiff(top_10 , ll  , finalDF=finalDF , skills_ndx_dict = skills_ndx_dict) 


# finalDF = load_data() 

def createSkillDict(finalDF) : 
    skills_ndx_dict = dict()
    cnt = 0 
    for i in finalDF.columns : 
        skills_ndx_dict[cnt] = i  
        cnt+=1 
    return skills_ndx_dict 


finalDF= load_data() 
skillsDict = createSkillDict(finalDF) 

# Extract an example for checking results 
ex = list()
for i , j  in finalDF.iterrows() : 
    ex = j.values
    break

t = findJobs(ex , finalDF , skillsDict) 

print(t)
