import numpy as np
import math, time
from typing import TypeVar
from app.utils.user_utils import *

from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)

def check(data, key):
        if data.get(key) is not None:
                if data[key] !={}:
                        return float(data[key]["answer_weight"])
        return 1

def get_education_score(user: user_account_type):
        user_info =  user.user_info
        work_activite_weight = check(data = user_info[0]["formData"], key = "curOccupation")
        education_weight = check(user_info[0]["formData"]["education"], key = "master")
        education_grand_weight = check(data = user_info[0]["formData"], key = "educationGrant")
        olimp_highest_weight = check(data = user_info[2]["formData"], key = "highestOlympiad")
        olimp_rank_weight = check(data = user_info[2]["formData"], key = "rankOlympiad")
        max_bachelor_weight = 1
        max_master_weight = 1
        max_phd_weight = 1
        userdata = user_info[1]["formData"]["EducationScore"]
        bachelor_weight_list = []
        master_weight_list = []
        phd_weight_list = []
        for edu in userdata:
                if edu.get("bachelor") is not None:
                        if edu["bachelor"] != {}:
                                bachelor_weight = get_bachelor_weight(edu)
                                bachelor_weight_list.append(bachelor_weight)
                if edu.get("master") is not None:
                        if edu["master"] != {}:
                                master_weight = get_master_weight(edu)
                                master_weight_list.append(master_weight)
                                
                if edu.get("phd") is not None:
                        if edu["phd"] != {}:
                                phd_weight = get_phd_weight(edu)
                                phd_weight_list.append(phd_weight)                           
        if bachelor_weight_list!=[]:
                max_bachelor_weight = max(bachelor_weight_list)
        if  master_weight_list != []:
                max_master_weight = max(master_weight_list)
        if phd_weight_list != []:
                max_phd_weight = max(master_weight_list)
        education_degree_weight = np.round(max_bachelor_weight*max_master_weight*max_phd_weight,3)
        total_education_weight = work_activite_weight*education_weight*(education_grand_weight*education_degree_weight*olimp_highest_weight*olimp_rank_weight)**(1/3)
        total_education_weight = np.round(total_education_weight,7)
        
        return total_education_weight
        
        


def get_experience_score(user: user_account_type):
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
                                        difference = calculate_date_difference(data)

                        finnly_date = difference.days/365.25
                        finnly_date_weight = get_date_weight(finnly_date=finnly_date)
                        experiance_score = max_working_form_weight*profession_degree_weight* finnly_date_weight
                else:
                        max_working_form_weight = userdata[0]["workingActivityForm"]["answer_weight"]
                        profession_degree_weight = userdata[0]["degreeOfProfes"]["answer_weight"]
                        difference = calculate_date_difference(userdata[0])
                        finnly_date = difference.days/365.25
                        finnly_date_weight = get_date_weight(finnly_date=finnly_date)
                        experiance_score = max_working_form_weight*profession_degree_weight* finnly_date_weight

                return experiance_score
        return experiance_score


def get_skills_score(user):

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

def get_language_score(user):

        userdata = user.user_info[5]["formData"]["languageSkills"]
        total_language_weight = 1
        if len(userdata) > 0:
                for data in userdata:
                        total_language_weight *= data['answer_weight']
                return total_language_weight
        
        return total_language_weight

test_data  = [{"name":"umumi-suallar","formData":{"firstName":"a","lastName":"a","workExp":"1","curOccupation":{"id":4,"answer":"Çalışıram"},"education":{"id":10,"answer":"Peşə təhsili"},"educationGrant":{"id":14,"answer":"Əlaçı"}}},
              {"name":"orta-texniki-ve-ali-tehsil-suallari","formData":{"vocationalScore":"3","bachelorsScore":"","masterScore":"","phdScore":""}},
              {"name":"olimpiada-suallar","formData":{"wonOlympics":"0","subjectOlympiad":{"id":21,"answer":"Tarix"},"highestOlympiad":{"id":28,"answer":"Rayon"},"rankOlympiad":{"id":32,"answer":"2-ci yer (Gümüş medal)"}}},
              {"name":"dil-bilikleri-substage","formData":{"haveLanguageSkills":"0","languageSkills":["İngilis dili","Rus dili"],"enlangCert":"2","engLevel":"4","ruLevel":"1"}},
              {"name":"elave-dil-bilikleri-substage","formData":{"langs":[{"addLang":{"id":133,"answer":"İspan dili"},"levelLang":"B2 (Orta)","haveCertLang":"Xeyr"},{"addLang":{"id":135,"answer":"Yapon dili"},"levelLang":"B2 (Orta)","haveCertLang":"Bəli","certLang":"ead"}]}},
              {"name":"xususi-bacariqlar-substage","formData":{"haveSpecialSkills":"0","specialSkills":["Musiqi","Rəqs"],"levelSkill":"","certSkill":"","Musiqi":"0","Rəqs":"1"}},
              {"name":"xususi-bacariqlar-sertifikat-substage","formData":{"musiqiCertifcate":"asdas","rəqsCertifcate":"asdasdas"}},
              {
                "name": "idman-substage",
                "formData": {
                        "sport": {"answer": "Bəli", "weight": 0},
                        "whichSport": ["Futbol", "Güləş", "Basketbol", "Atletika"],
                        "professionals": [
                                {"whichScore": {"answer": "Respublika", "weight": 0.03},"whichPlace": {"answer": "2-ci yer", "weight": 0.2},"name": "Futbol","level": {"answer": "Peşəkar", "weight": 0.03},},
                                {"whichScore": {"answer": "Rayon", "weight": 1},"whichPlace": {"answer": "1-ci yer", "weight": 0.1},"name": "Atletika","level": {"answer": "Peşəkar", "weight": 0.03},},
                                ],
                                
                        "amateurs": [
                                {"level": {"answer": "Həvəskar", "weight": 0.3}, "name": "Güləş"},
                                {"level": {"answer": "Həvəskar", "weight": 0.3}, "name": "Basketbol"},
                                ],
                        },
                },
              {"name":"is-tecrubesi-substage","formData":{"experiences":[{"haveExperience":"0","company":"as","profession":"asd","workingActivityForm":{"id":225,"answer":"Fiziki əmək"},"degreeOfProfes":{"id":231,"answer":"Mütəxəssis"},"startDate":"2023-07-19","endDate":"2023-07-14","currentWorking":False},{"company":"asda","profession":"saxc","workingActivityForm":{"id":226,"answer":"Sənət"},"degreeOfProfes":{"id":231,"answer":"Mütəxəssis"},"startDate":"2023-06-29","endDate":"","currentWorking":True}]}},
              {"name":"proqram-bilikleri-substage",
               "formData":{
                       'design': [
                                { 'answer': "Canva", 'weight': None, 'level': { 'answer': 'Junior', 'weight': None } },
                                {'answer': "Photoshop",'weight': None,'level': { 'answer': 'Middle', 'weight': None }},
                                ],
                        'msOffice': [
                                { 'answer': "Word", 'weight': 1, 'level': { 'answer': "Middle", 'weight': 0.5 } },
                                {'answer': "Excel", 'weight': 0.2, 'level': { 'answer': "Junior", 'weight': 0.7 },},
                                {'answer': "PowerPoint",'weight': 0.4,'level': { 'answer': "Senior", 'weight': 0.3 },},
                                ],
                        'programs': [
                                {'answer': "Python",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "Java",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "Kotlin",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "C/C++",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "C#",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "SQL",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "Javascript",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "Swift",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                {'answer': "HTML/CSS",'weight': None,'level': { 'answer': "Middle", 'weight': None },},
                                ],
                        'others': [
                                {'answer': "Blender",'weight': None,'level': { 'answer': "Junior", 'weight': None },},
                                ],
                                }
                }
        ]

def get_sport_skills_score(user):
    userdata = test_data[7]["formData"]

    if userdata != {}:
        pesekar_score = 1
        heveskar_score = 1

        for sport in userdata["professionals"]:
            if userdata["professionals"] != []:
                # name = sport['name']
                level_weight = sport['level']['weight']
                score_weight = sport['whichScore']['weight']
                place_weight = sport['whichPlace']['weight']
                pesekar_score *= place_weight * score_weight * level_weight
        # print("pesekar score: ", pesekar_score)
        # print("\n")

        heveskar_score = 1
        for sport in userdata["amateurs"]:
            if userdata["amateurs"] != []:
                heveskar_score *= sport['level']['weight']
        # print("heveskar score: ", heveskar_score)
        # print("\n")
        
        if pesekar_score * heveskar_score != 1:
            sport_score = pesekar_score * heveskar_score
            return sport_score


# get score weights for "proqram-bilikleri-substage"
def get_programming_skills_score(user):

        # userdata = user.user_info[9]["formData"]
        userdata = test_data[9]["formData"]

        result = {
                'msOfficeScore':1,
                'designScore':1,
                'programsScore':1,
                'othersScore':1,
        }

        # Calculating officeScore
        word_score = 0
        excel_score = 0
        pp_score = 0
        if userdata['msOffice'] and userdata['msOffice'] != [] and userdata['msOffice'] != 0 and userdata['msOffice'] != '0':
                for answer in userdata['msOffice']:
                        if answer['answer'] == 'Word':
                                word_score = answer['weight'] * answer['level']['weight']
                        if answer['answer'] == 'Excel':
                                excel_score = answer['weight'] * answer['level']['weight']
                        if answer['answer'] == 'PowerPoint':
                                pp_score = answer['weight'] * answer['level']['weight']

                weight_list = {
                        'Excel' : excel_score,
                        'Word' : word_score,
                        "PowerPoint" : pp_score,
                }
                for value in weight_list.values():
                        if value != 0:
                                result['msOfficeScore'] *= value

        else:
                result["msOfficeScore"] = 0
        
        # print("msOfficeScore",result["msOfficeScore"])
        
        # Calculating Scores of design,programs, others categories       
        level_scores_mapping = {
                "programs": {"Junior": {1:0.3, 2:0.2, 3:0.1, 4:0.05}, 'Middle': {1:0.05, 2:0.03, 3:0.01, 4:0.005}, 'Senior' : {1:0.005, 2:0.003, 3:0.001, 4:0.0005}},
                "design": {"Junior": {1:0.4, 2:0.3, 3:0.2, 4:0.1}, 'Middle': {1:0.1, 2:0.05, 3:0.01, 4:0.005}, 'Senior' : {1:0.01, 2:0.005, 3:0.001, 4:0.0005}},
                "others": {"Junior": {1:0.4, 2:0.3, 3:0.2, 4:0.1}, 'Middle': {1:0.1, 2:0.05, 3:0.01, 4:0.005}, 'Senior' : {1:0.01, 2:0.005, 3:0.001, 4:0.0005}}
                # "msOffice": {"Junior": {1:0.1,2:0.2,3:0.3,4:0.4}, 'Middle': {1:0.1,2:0.2,3:0.3,4:0.4}, 'Senior' : {1:0.1,2:0.2,3:0.3,4:0.4}},
        }

        # count of each level in 3 other categories
        lst = {
                'design' : [0,0,0],
                'programs' : [0,0,0],
                'others' : [0,0,0]
        }

        if userdata['design'] != [] !='' !=0:
                for data in userdata['design']:
                        if data['level']['answer'] == 'Junior':
                                lst['design'][0] += 1
                        if data['level']['answer'] == 'Middle':
                                lst['design'][1] += 1
                        if data['level']['answer'] == 'Senior':
                                lst['design'][2] += 1

        if userdata['programs'] != []:
                for data in userdata['programs']:
                        if data['level']['answer'] == 'Junior':
                                lst['programs'][0] += 1
                        if data['level']['answer'] == 'Middle':
                                lst['programs'][1] += 1
                        if data['level']['answer'] == 'Senior':
                                lst['programs'][2] += 1

        if userdata['others'] != []:
                for data in userdata['others']:
                        if data['level']['answer'] == 'Junior':
                                lst['others'][0] += 1
                        if data['level']['answer'] == 'Middle':
                                lst['others'][1] += 1
                        if data['level']['answer'] == 'Senior':
                                lst['others'][2] += 1

        levels = ['Junior', 'Middle', 'Senior']
        for i, level in enumerate(levels):
                #designScore
                if lst['design'] != [0,0,0]:
                        count = lst['design'][i]
                        if count != 0:
                                if count > 4:
                                        level_score = level_scores_mapping['design'][level].get(4)
                                        result['designScore'] *= level_score
                                elif count <=4:
                                        level_score = level_scores_mapping['design'][level].get(count)
                                        result['designScore'] *= level_score
                else:
                        result['designScore'] = 0

                # programsScore
                if lst['programs'] != [0,0,0]:
                        count = lst['programs'][i]
                        if count != 0:
                                if count > 4:
                                        level_score = level_scores_mapping['programs'][level].get(4)
                                        result['programsScore'] *= level_score
                                elif count <=4:
                                        level_score = level_scores_mapping['programs'][level].get(count)
                                        result['programsScore'] *= level_score
                else:
                        result['programsScore'] = 0

                #othersScore
                if lst['others'] != [0,0,0]:
                        count = lst['others'][i]
                        if count != 0:
                                if count > 4:
                                        level_score = level_scores_mapping['others'][level].get(4)
                                        result['othersScore'] *= level_score
                                elif count <=4:
                                        level_score = level_scores_mapping['others'][level].get(count)
                                        result['othersScore'] *= level_score
                else:
                        result['othersScore'] = 0
        
        # find multiplication of all category scores except minimum one
        category_scores = []
        for category in userdata:
                # max 4 decimal points 
                result[f'{category}Score'] = round(result[f'{category}Score'], 4)
                category_score = result[f'{category}Score']
                category_scores.append(category_score)
                # print(f'{category}Score:', category_score)
                # calculating overall programming skills score
        print(category_scores) 
        # Check if all category scores are the same
        # calculate overall programming skills score
        if len(set(category_scores)) == 1:
                print(f"All category scores are the same. min is {min(category_scores)}")
        else:
                # print("Category scores are different.")
                # deleting minimum category score
                
                # print('index',category_scores.index(min(category_scores)))
                minimum_score = min(category_scores)
                category_scores.remove(minimum_score)
                programming_skills_score = 1
                a=0
                if category_scores != []:        
                        for score in category_scores:
                                if 0.5 < score <= 1:
                                        programming_skills_score *= 0.9
                                        a+=1
                                        # print(programming_skills_score)

                                elif 0.3 < score <= 0.5:
                                        programming_skills_score *= 0.8
                                
                                elif 0.1 < score <= 0.3:
                                        programming_skills_score *= 0.7

                                elif 0.01 < score <= 0.1:
                                        programming_skills_score *= 0.5

                                elif 0.001 < score <= 0.01:
                                        programming_skills_score *= 0.3
                                elif 0.0001 < score <= 0.001:
                                        programming_skills_score *= 0.2

                                else:
                                        programming_skills_score *= 0.1
                                
                        programming_skills_score *= minimum_score
                        
                else:
                        programming_skills_score = 0
                        
        return programming_skills_score 
        
