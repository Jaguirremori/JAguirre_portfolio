#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime


# In[3]:


#read in patient data
patients = pd.read_csv("Patient_survey__HCAHPS__-_State.csv")
patients.columns


# In[13]:


#Trim to relevant categories
patientsrelevant =  patients[["State", "HCAHPS Question", "HCAHPS Answer Description", "HCAHPS Answer Percent", "HCAHPS Measure ID"]]
patientsrelevant


# In[5]:


#Finding percentage of patients that believe nurses always or sometimes/never communicated well 
#Always
nursecommalways = patientsrelevant.loc[patientsrelevant["HCAHPS Measure ID"]=="H_COMP_1_A_P"]
nursecommalways = nursecommalways.loc[nursecommalways["HCAHPS Answer Percent"]!="Not Available"]
pd.to_numeric(nursecommalways["HCAHPS Answer Percent"])
nursecommalways.sort_values("HCAHPS Answer Percent", ascending = False)
nursecommalways.head()
nursecommalways["HCAHPS Answer Percent"].mean()


# In[6]:


#Never
nursecommsomenever = patientsrelevant.loc[patientsrelevant["HCAHPS Measure ID"]=="H_COMP_1_SN_P"]
nursecommsomenever = nursecommsomenever.loc[nursecommsomenever["HCAHPS Answer Percent"]!="Not Available"]
pd.to_numeric(nursecommsomenever["HCAHPS Answer Percent"])
nursecommsomenever.sort_values("HCAHPS Answer Percent", ascending = False)
nursecommsomenever.head()
nursecommsomenever["HCAHPS Answer Percent"].mean()


# In[7]:


#Concat and export
nursecommasn = pd.concat([nursecommalways,nursecommsomenever])
nursecommasn.to_csv('nursecomunication.csv', index=False)


# In[8]:


patientsrelevant


# In[9]:


#Finding percentage of patients that believe doctors always or sometimes/never communicated well 
#Always
doccommalways = patientsrelevant.loc[patientsrelevant["HCAHPS Measure ID"]=="H_COMP_2_A_P"]
doccommalways = doccommalways.loc[doccommalways["HCAHPS Answer Percent"]!="Not Available"]
pd.to_numeric(doccommalways["HCAHPS Answer Percent"])
doccommalways.sort_values("HCAHPS Answer Percent", ascending = False)
doccommalways.head()
doccommalways["HCAHPS Answer Percent"].mean()

#Sometimes or Never
doccommsomenever = patientsrelevant.loc[patientsrelevant["HCAHPS Measure ID"]=="H_COMP_2_SN_P"]
doccommsomenever = doccommsomenever.loc[doccommsomenever["HCAHPS Answer Percent"]!="Not Available"]
pd.to_numeric(doccommsomenever["HCAHPS Answer Percent"])
doccommsomenever.sort_values("HCAHPS Answer Percent", ascending = False)
doccommsomenever.head()
doccommsomenever["HCAHPS Answer Percent"].mean()


# In[10]:


#Concat and export
doccommasn = pd.concat([doccommalways,doccommsomenever])
doccommasn.to_csv('doctorcommunication.csv', index=False)


# In[30]:



nursedoctorcomm = pd.concat([doccommasn, nursecommasn])


# In[34]:


nursedoctorcomm.to_csv("nursedoctorcomm.csv", index= False )


# In[15]:


#Create a function that extracts the "sometimes or never" or "always" of a specified ID
def extraction(id1, id2):
    data = patientsrelevant.loc[patientsrelevant["HCAHPS Measure ID"]==id1]
    data = data.loc[data["HCAHPS Answer Percent"]!="Not Available"]
    pd.to_numeric(data["HCAHPS Answer Percent"])
    data.sort_values("HCAHPS Answer Percent", ascending = False)
    data2 = patientsrelevant.loc[patientsrelevant["HCAHPS Measure ID"]==id2]
    data2 = data.loc[data["HCAHPS Answer Percent"]!="Not Available"]
    pd.to_numeric(data2["HCAHPS Answer Percent"])
    data2.sort_values("HCAHPS Answer Percent", ascending = False)
    data_concat = pd.concat([data, data2])
    return data_concat
    


# In[18]:


nurse_explain_skills = extraction("H_NURSE_EXPLAIN_A_P", "H_NURSE_EXPLAIN_SN_P")
nurse_explain_skills


# In[ ]:




