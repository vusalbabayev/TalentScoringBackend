#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import textwrap
from fpdf import FPDF


# In[2]:


df = pd.read_excel('sample_df.xlsx')


# In[3]:


import openai
openai.api_key = "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"


# ## Define CV Generator Function

# In[4]:


def generate_cv_content(i = 17, dataframe = df, save_pdf = True, pdf_file_name = 'sample_CV.pdf', print_response = True, 
                       temperature = 0.7):
    
    ######################
    ##  Create Prompt   ##
    ######################
    
    prompt = ''
    prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
    prompt += f"I have education level of {df.iloc[i].level}. "
    to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
    prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
    prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
    prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
    prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
    prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
                            language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

    prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

    prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


    prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
    prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")
    
    ################################
    ##  Assign test system info   ##
    ################################
    testing_system_info = '''
                        Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                        Having average grades in high school means having different grades - A, B, C, D, etc.
                        DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                        Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                        Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                        Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                        Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                        Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 40-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-40   is considered bad and it means that the person has failed.

                        PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 30-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-30   is considered bad and it means that the person has failed.'''


    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"""You are a helpful AI tool which can create CV based on the user data. User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                            The response you give will be written into pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                            """},
            {"role": "user", "content": "Please create CV based on the information of the user. Add some extra explanations and summaries as needed. Indicate the e summary on the top."},

        ],
        temperature = temperature,
    )

    
    print(response.choices[0].message.content)
    
    
    ################################
    ##      Save to PDF file      ##
    ################################
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 5 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='P', unit = 'mm', format = 'A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Arial', size = fontsize_pt)
    splitted = response.choices[0].message.content.split('\n')
    for line in splitted:
        lines = textwrap.wrap(line, width_text)
        if len(lines) == 0:
            pdf.ln()
        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)
    pdf.output(pdf_file_name, 'F')
    
    return response.choices[0].message.content


# ## Use Function

# In[50]:


cv_content = generate_cv_content()


# ## Generate Summary Generator

# In[111]:


def generate_cv_summary(i = 17, dataframe = df, save_pdf = True, pdf_file_name = 'sample_CV.pdf', print_response = True, 
                       temperature = 0.7):
    
    ######################
    ##  Create Prompt   ##
    ######################
    
    prompt = ''
    prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
    prompt += f"I have education level of {df.iloc[i].level}. "
    to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
    prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
    prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
    prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
    prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
    prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
                            language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

    prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

    prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


    prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
    prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")
    
    ################################
    ##  Assign test system info   ##
    ################################
    testing_system_info = '''
                        Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                        Having average grades in high school means having different grades - A, B, C, D, etc.
                        DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                        Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                        Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                        Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                        Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                        Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 40-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-40   is considered bad and it means that the person has failed.

                        PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 30-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-30   is considered bad and it means that the person has failed.'''


    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"""You are a helpful AI tool which can create only summary part of CV professionally. User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                            The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                            """},
            {"role": "user", "content": """Please create me a short summary (max 100 words) part for the CV based on the information of me professionally and in a formal way. 
                                         Add some extra explanations as needed. Do not indicate something like 'Summary:' etc. The response  will be automatically written to CV.
                                         Write it in first personal singular"""},

        ],
        temperature = temperature,
        # max_tokens = 100
    )

    
    print(response.choices[0].message.content)    
    return response.choices[0].message.content


# In[112]:


sample_summary = generate_cv_summary()


# In[86]:


len(sample_summary.split())


# In[87]:


print(sample_summary.replace('\n\n', '\n'))


# ## Job experience details

# In[113]:


def generate_summary_job_experience(i = 17, dataframe = df, job_no = 1,
                       temperature = 0.7):
    
    ######################
    ##  Create Prompt   ##
    ######################
    
    prompt = ''
    prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
    prompt += f"I have education level of {df.iloc[i].level}. "
    to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
    prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
    prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
    prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
    prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
    prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
                            language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

    prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

    prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


    prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
    prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")
    
    ################################
    ##  Assign test system info   ##
    ################################
    testing_system_info = '''
                        Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                        Having average grades in high school means having different grades - A, B, C, D, etc.
                        DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                        Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                        Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                        Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                        Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                        Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 40-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-40   is considered bad and it means that the person has failed.

                        PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 30-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-30   is considered bad and it means that the person has failed.'''


    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"""You are a helpful AI tool which can create summary and details part of job experience parts of CV professionally. 
                                            User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                            The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                            """},
            {"role": "user", "content": f"""Please create me a short summary (max 100 words) part of my job experience {job_no} based on the information of me professionally and in a formal way. 
                                         Add some extra explanations as needed. Do not indicate something like 'Summary:' etc. The response  will be automatically written to CV.
                                         Use bullet points as needed. Do not indicate job name, positions, date range, only some info about job.
                                         """},
               ],
        temperature = temperature,
        # max_tokens = 100
    )

    # response.choices[0].message.content
    
    print(response.choices[0].message.content)    
    return response.choices[0].message.content


# In[114]:


job_experience1 = generate_summary_job_experience()


# In[ ]:





# In[ ]:





# ## Job title

# In[5]:


df.iloc[17].desired_job


# In[12]:


def generate_job_title(i = 17, dataframe = df, temperature = 0.7):
    
    ######################
    ##  Create Prompt   ##
    ######################
    
    prompt = ''
    prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
    prompt += f"I have education level of {df.iloc[i].level}. "
    to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
    prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
    prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
    prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
    prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
    prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
                            language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

    prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

    prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


    prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
    prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")
    
    ################################
    ##  Assign test system info   ##
    ################################
    testing_system_info = '''
                        Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                        Having average grades in high school means having different grades - A, B, C, D, etc.
                        DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                        Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                        Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                        Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                        Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                        Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 40-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-40   is considered bad and it means that the person has failed.

                        PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                        Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                        Score range of 50-80  is considered good and only 10-15% of students can score this.
                        Score range of 30-50  is considered normal and only 20-25% of students can score this.
                        Score range of 0-30   is considered bad and it means that the person has failed.'''


    # Example OpenAI Python library request
    desired_job_vacancy = df.iloc[i].desired_job
    x = '' if desired_job_vacancy else "I want to apply for the position: " + desired_job_vacancy
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"""You are a helpful AI tool which can create Job Title of people (such as 'Manager', 'Data Scientist') for CV professionally.
                                            The user may give extra prompt such as 'I want to apply for this job', etc.
                                            User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                            The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                            """},
            {"role": "user", "content": f"""Please create me a Job title for me based on the information of me professionally and in a formal way. {x}
                                         The response  will be automatically written to CV. Do not indicate things like 'Job title:' or date ranges, company name, etc.
                                         """},
            # {"role": "assistant", "content": "Who's there?"},
            # {"role": "user", "content": "Orange."},
        ],
        temperature = temperature,
        # max_tokens = 100
    )

    # response.choices[0].message.content
    
    print(response.choices[0].message.content)    
    return response.choices[0].message.content


# In[13]:


sample_job_title = generate_job_title()


# In[14]:


sample_job_title

