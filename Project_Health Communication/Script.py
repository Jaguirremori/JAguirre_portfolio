#!/usr/bin/env python
# coding: utf-8

# # Analyzing and Visualizing Communication Skills of Doctors and Nurses as Evaluated by Hospital Patients
# 
# Everyday, many people are interacting with healthcare professionals. Health informatics is extremely important in these interactions. The distribution, clarity, and response of health information influences both health professionals and patients and how they take action in their health related behaviors. In order for patients to take the best actions possible to understand and improve their health, healthcare professionals have to be effective communicators as they are one of the main sources to relay important health information.
# 
# ### The Dataset
# 
# This dataset is provided by the Centers for Medicare and Medicaid Services. It contains a list of hospital ratings for the Hospital Consumer Assessment of Healthcare Providers and Systems (HCAHPS).
# 
# Lets Begin!

# In[31]:


#Import the packages we need

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Read in the dataset
hp_communication = pd.read_csv("Patient_survey__HCAHPS__-_Hospital.csv")


# In[3]:


hp_communication.info()


# It looks like we have a lot of columns! Many of which seems to be strings. There are 455,328 rows in our dataset, but not every column is filled out for every row. There are many relevant columns to choose from, lets take a further look into our dataset.

# In[4]:


hp_communication.head(3)


# I think the first step in our data preparation is to trim our data by columns that are found relevant for this project. And then we can drop NA rows within that smaller dataset so that any unnecessary trimming can be avoided.
# 
# ### What Columns Should We Keep?
# 
# #### FacilityName, Address, City, State, ZIP Code
# All of these columns provide useful location data that will help us analyze facilities at a high level such as state, down to lower levels such as the zipcodes within a city. This kind of geographic data can easily be used in Tableau to build comprehensive maps and plot individual facilities and the communication skills of healthcare professionals.
# 
# #### HCAHPS Measure ID, HCAHPS Question, HCAHPS Answer Percent
# These columns give us information on the survey questions. HCAHPS Measure ID correlates to a specific question being asked, HCAHPS Question is the statement/question being asked, and HCAHPS Answer Percent is the percentage of respondents that agree with that specific statement. It seems that a statement regarding communication effectiveness would be asked up to four times. Where you could agree with whether the statement "always" "sometimes or never" happens.
# 
# #### Number of completed surveys
# 
# This is important so that we can analyze the distribution of survey responses received for a question, this will help us identify any observations where lack of responses may influence the result too much.
# 
# Now that we have our columns of interest, lets subset and clean this dataset.
# 

# In[5]:


#subset
relevant_columns = ["Facility Name","Address", "City", "State", "ZIP Code", 
                    "HCAHPS Measure ID", "HCAHPS Question", "HCAHPS Answer Percent",
                   "Number of Completed Surveys"]
hp_comm_clean = hp_communication[relevant_columns]

#monitor the number of rows dropped
rows_before = len(hp_comm_clean.index)
hp_comm_clean = hp_comm_clean.dropna()
rows_after = len(hp_comm_clean.index)
print("Before dropping NA values we had", rows_before, 
      " rows. We now have ", rows_after, "rows. The difference is "
      , rows_before - rows_after)


# Because all of our relevant columns had 0 null values, no rows were dropped during the df.dropna() method was used. If we were to use this method prior to subsetting, we could expect a lot of rows being removed if no conditions were entered.

# ### Renaming our columns
# 
# Our column titles contain spaces and capital letters, which can make it difficult to write code about. Lets change our column titles to snake case.

# In[6]:


#replace capital letters with lower case lowers 
df_columns_clean = []
for i in hp_comm_clean.columns:
    i = i.replace(" ", "_")
    i = i.lower()
    df_columns_clean.append(i)

hp_comm_clean.columns = df_columns_clean
print(hp_comm_clean.columns)


# This will make our code much easier to work on as we wont have to worry about capitalization and spacing
# 
# ### Lets take a look at our new dataset

# In[7]:


hp_comm_clean.head(4)


# It seems more cleaning is needed! Our df.dropna() method did not catch any "Not Applicable" entries to the hcahps_answer_percent row. It appears that star rating and linear mean value questions give this row a value of "Not Applicable" Lets fix this.

# In[8]:


#Create a boolean matrix of rows where "Not Applicable" is not a value, then inject into dataset to clean
hp_comm_clean = hp_comm_clean[hp_comm_clean["hcahps_answer_percent"]!= "Not Applicable"]
hp_comm_clean = hp_comm_clean[hp_comm_clean["hcahps_answer_percent"]!= "Not Available"]


hp_comm_clean.head(4)


# ## A Deeper Explanation of The Kind of Questions We Are Looking At
# 
# ![Screenshot_2020-06-27%20HCAHPS%20V12%200%20Appendix%20A%20-%20HCAHPS%20Mail%20Survey%20Materials%20%28English%29%20-%20click-here-to-view-or-download-the%5B...%5D.png](attachment:Screenshot_2020-06-27%20HCAHPS%20V12%200%20Appendix%20A%20-%20HCAHPS%20Mail%20Survey%20Materials%20%28English%29%20-%20click-here-to-view-or-download-the%5B...%5D.png)
# 
# Here is an example of the kind of questions we are looking at from the HCAHPS survey. Respondents are to select one option. Each response of every question has a specific hcahps_measure_id and hcahps_question. The hcahps_answer_percent means the percentage of respondents that selected that specific option. 
# 
# Lets look at our third row of our data frame

# In[9]:


hp_comm_clean.iloc[2]


# This is our example question in use. This row is specific to the percentage respondents that answered "Usually" to our example question above. What this means is: Out of our 389 responses to this question at Dekalb Regional Medical Center, 17 percent of our respondents felt that doctors "Usually" listen to them during their hospital stay.
# 
# If you add up the percentages of all the answer options, it should add up to 100 percent.
# 
# Because this dataframe and project seem to be heavily reliant on the hcahps_id variable, we have to make sure we understand the values contained within them.

# In[10]:


id_values = hp_comm_clean["hcahps_measure_id"].value_counts()
print(id_values)


# Here we see that we have 72 different unique ids. It will be important to create a function where we can efficiently capture the response ranges for each question we aim to examine. Before that, lets determine the level we want to analyze the data. I think it would be a good idea to start at a general national level, then focus on my state of Maryland.
# 
# Lets group our dataframe by state so we can compare scores accross the country. After that, lets extract Maryland data so that we can look at that at a zipcode level later.

# In[15]:


hp_grouped = hp_comm_clean.groupby("state")
hp_md = hp_grouped.get_group("MD")
hp_md.head()


# ### Extracting and Analyzing our First Question: How often did Doctors listen to Hospital Patients?
# 
# Lets use the question we have an image of and analyze how hospital patients evaluate their doctor's listening skills across the 50 States. The id for patients who said "Always" is "H_DOCTOR_LISTEN_A_P"

# In[66]:


#change hcahps_answer_percent to int
hp_comm_clean["hcahps_answer_percent"] = hp_comm_clean["hcahps_answer_percent"].astype(int)

#First: Lets extract all rows with the relevant id

hp_doctor_listen_always = hp_comm_clean[hp_comm_clean["hcahps_measure_id"]=="H_DOCTOR_LISTEN_A_P"]

#Pivot Table with state as index
hp_doc_listen_always_pv = hp_doctor_listen_always.pivot_table(values = "hcahps_answer_percent", 
                                                                index = "state", 
                                                                margins = True,
                                                               aggfunc = np.mean)

hp_doc_listen_always_pv.plot(kind = "barh", 
                             figsize = (6,10), 
                             title = "Average Percantage of Hospital Patients That Feel Their Doctor 'Always' Listens To Them",
                            legend = False)
#Code Below to export into Tableau
#hp_doc_listen_always_pv.to_csv("hp_doc_listen_usually.csv")


# Here is one visualization representing our chosen metric to analyze. But it is difficult to find any patterns with this kind of visualization. Because of that, I loaded the data into Tableau and made an interactive map that will help visualize the data in a cleaner format.
# ![Sheet%201.png](attachment:Sheet%201.png)
# 
# Here we can see patterns a bit more clearly. The first thing that was noticed was that states in the southwest region of states in the mainland United States tend to have a less percentage of hospital patients say that their doctor "Always" is a good listener. This could be due to a multitude of reasons and should be further analyzed at various levels per state (e.g. do hospitals in a lower median income or education completion area get rated lower in communication than those in wealthier areas with a higher education completion rate). 
# 
