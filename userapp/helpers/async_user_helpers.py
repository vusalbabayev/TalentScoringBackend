from typing import TypeVar
from datetime import datetime
import numpy as np
import math, time
from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)

async def get_date_weight(finnly_date):
        if 0 <= finnly_date < 1:
                finnly_date_weight = 0.9
        elif 1 <= finnly_date < 3:
                finnly_date_weight = 0.7
        elif 3 <= finnly_date < 5:
                finnly_date_weight = 0.5
        elif 5 <= finnly_date <10:
                finnly_date_weight = 0.3
        elif 10 <= finnly_date <20:
                finnly_date_weight = 0.1
        elif 20 <= finnly_date:
                finnly_date_weight = 0.01

        return finnly_date_weight

async def calculate_date_difference(data):
        if data["endDate"] == "":
                current_date = datetime.now()
                start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
                difference = current_date - start_date
        else:
                start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
                end_date = datetime.strptime(data["endDate"], "%Y-%m-%d")
                difference = end_date - start_date
        return difference


async def get_education_score(user: user_account_type):
        tehsil_score = 0
        
        education= user.user_info[0]["formData"]["education"]
        occupation_weight = user.user_info[0]["formData"]["curOccupation"]["answer_weight"]
        grade_weight = user.user_info[0]["formData"]["educationGrant"]["answer_weight"]
        if user.user_info[2]["formData"]["wonOlympics"] == "1":
                olympiad_status_weight = user.user_info[2]["formData"]["highestOlympiad"]["answer_weight"]
                olympiad_rank_weight = user.user_info[2]["formData"]["rankOlympiad"]["answer_weight"]
        else:
                olympiad_status_weight=1
                olympiad_rank_weight = 1
        if len(education) ==3:
                education_weight = education[0]["bachelor"]["answer_weight"]*education[1]["master"]["answer_weight"]*education[2]["phd"]["answer_weight"]
                education_score = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]*user.user_info[1]["formData"]["masterScore"]["answer_weight"]*user.user_info[1]["formData"]["phdScore"]["answer_weight"]
        elif len(education) ==2:
                education_weight = education[0]["bachelor"]["answer_weight"]*education[1]["master"]["answer_weight"]
                education_score = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]*user.user_info[1]["formData"]["masterScore"]["answer_weight"]
        elif len(education) ==1:
                education_weight = education[0]["bachelor"]["answer_weight"]
                education_score = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]
    
        tehsil_score = (
            np.exp(
                np.log(occupation_weight)
                + np.log(education_weight)
                + (1/3) * np.log(grade_weight * education_score * olympiad_status_weight * olympiad_rank_weight)
            )
        ) * 100        
        tehsil_score = np.round(tehsil_score,8)
        return tehsil_score


async def get_experience_score(user: user_account_type):
        userdata = user.user_info[3]["formData"]["experiences"]
        experiance_score = 1
        if len(userdata)>0:
                workingform = {"Fiziki əmək":1, "Sənət":2, "Ali ixtisas":3, "Sahibkar":4}
                max_working_form_weight = 0
                profession_degree_weight = 0
                if len(userdata)>1:
                        max = 0
                        for data in userdata:
                                if workingform[data["workingActivityForm"]["answer"]]>max:
                                        max = workingform[data["workingActivityForm"]["answer"]]
                                        max_working_form_weight = data["workingActivityForm"]["answer_weight"]
                                        profession_degree_weight = data["degreeOfProfes"]["answer_weight"]
                                        difference = await calculate_date_difference(data)

                        finnly_date = difference.days/365.25
                        finnly_date_weight = await get_date_weight(finnly_date=finnly_date)
                        experiance_score = max_working_form_weight*profession_degree_weight* finnly_date_weight
                else:
                        max_working_form_weight = userdata[0]["workingActivityForm"]["answer_weight"]
                        profession_degree_weight = userdata[0]["degreeOfProfes"]["answer_weight"]
                        difference = await calculate_date_difference(userdata[0])
                        finnly_date = difference.days/365.25
                        finnly_date_weight = await get_date_weight(finnly_date=finnly_date)
                        experiance_score = max_working_form_weight*profession_degree_weight* finnly_date_weight

                return experiance_score
        return experiance_score


async def get_skills_score(user):

        userdata = user.user_info[4]["formData"]["specialSkills"]
        lst=[]
        heveskar_count = 0
        pesekar_count = 0

        for data in userdata:
                lst.append(data['talent_level'])
                if data['talent_level'] == 'heveskar':
                        heveskar_answer_weight = data['answer_weight']
                elif data['talent_level'] == 'pesekar':
                        pesekar_answer_weight = data['answer_weight']

        for value in lst:
                if value=='heveskar':
                        heveskar_count += 1
                elif value=='pesekar':
                        pesekar_count += 1

        formula_result = (heveskar_count**heveskar_answer_weight) * (pesekar_count**pesekar_answer_weight)
        return formula_result

async def get_language_score(user):

        userdata = user.user_info[5]["formData"]["languageSkills"]
        total_language_weight = 1
        if len(userdata) > 0:
                for data in userdata:
                        total_language_weight *= data['answer_weight']
                return total_language_weight
        
        return total_language_weight