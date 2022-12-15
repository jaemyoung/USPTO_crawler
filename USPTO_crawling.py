#%% package
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
import requests
from datetime import datetime
import copy
import itertools
from collections import Counter

#%% crawling function
def patent_crawling(pat_nums):
    # USPTO API 주소
    url_post = 'https://api.patentsview.org/patents/query' 
    # API 항목(필요에 따라 수정)
    condition = '&f=["patent_number","cpc_subgroup_id","ipc_subgroup","patent_date", "patent_type","assignee_id","assignee_organization", "patent_title", "patent_abstract","cited_patent_number", "citedby_patent_number", "citedby_patent_date"]'

    pt_dict_list=[]
    st = time.time()
    for n, i in enumerate(tqdm(pat_nums)):
        q1 = '?q={"patent_number":'
        q2 = '}'
        q = q1 + '"' + i + '"' + q2    
        t_data = q + condition
        t_post = requests.get(url_post + t_data)
    
        while '500' in str(t_post):
            t_post = requests.get(url_post + t_data)
        try:
            t_json = t_post.json()
        except:
            continue
        
        try:
            pt_dict_list.extend(t_json['patents'])
        except TypeError:
            pass
    return pt_dict_list

#%% 특허 추출
pat_num = pd.read_excel('C:/Users/user/Documents/GitHub/USPTO_crawling/data/search_data/[작업중] TI, AB (virtual world, environment, reality) (4,099개).xlsx')
pat_nums = [i.split('-')[1] for i in pat_num['id']]

# 함수 실행 후 dataframe으로 변환 후 데이터 저장
patent_df = pd.DataFrame(patent_crawling(pat_nums))
patent_df1 = patent_df[patent_df["patent_type"]=='utility'] # fiitering utility

# excel 파일로 저장 
patent_df.to_excel('C:/Users/user/Documents/GitHub/USPTO_crawling/data/ouput_data/백춘삼 박사님/patents_3608.xlsx', encoding='utf8', index=False)


#%% cited 관계 특허 추출 
pat_num = pd.read_excel('C:/Users/user/Documents/GitHub/USPTO_crawling/data/ouput_data/patent_1155(+cited_patents).xlsx')
cited_num = pat_num["cited_patents"].apply(eval) # object -> dict 형 변환
cited_num_list = []
for cited_dic in cited_num:
    for cited_dic_number in cited_dic:
        cited_num_list.append(cited_dic_number["cited_patent_number"])
        
cited_nums = list(set(cited_num_list)) # 특허 중복제거 13297 -> 6853

#%% total patant(pat_nums + cited_nums) 추출
total_nums = pat_nums + cited_nums
total_nums = list(filter(None,total_nums)) # None값 제거

# 함수 실행 후 dataframe으로 변환 후 데이터 저장
total_patent_df = pd.DataFrame(patent_crawling(total_nums[:10]))
total_patent_df = total_patent_df[total_patent_df["patent_type"]=='utility'] # fiitering utility

# excel 파일로 저장 
total_patent_df.to_excel('C:/Users/user/Documents/GitHub/USPTO_crawling/data/ouput_data/patent_7972.xlsx', encoding='utf8', index=False)

#%% FC 승인된지 5년이내 FC 수
'''def AAFC(util_patent):
    all_fp_list = []

    for p in tqdm(util_patent):
        p_year = int(p['patent_date'].split('-')[0]) # 타겟 특허의 승인연도
        fp_list = []

        for fp in p['citedby_patents']:
            try:
                fp_year = int(fp['citedby_patent_date'].split('-')[0]) # 타겟특허의 fc들의 승인연도
                # 타겟특허가 승인된지 5년 이내 forward citation 횟수
                if p_year+5 >= fp_year:
                    fp_list.append(fp['citedby_patent_number'])
                else:
                    pass
            # 오류 예외처리
            except AttributeError:
                pass
            except TypeError:
                pass

        all_fp_list.append(fp_list)
    # all_fp_list는 이중리스트의 형태이므로 각 원소리스트의 길이를 구하면서 flatten 진행
    all_fp_list_length = [len(p) for p in all_fp_list]
    return all_fp_list_length

aafc = AAFC(util_patent)
patent = first_patent_df.assign(AAFC = aafc)
'''





































