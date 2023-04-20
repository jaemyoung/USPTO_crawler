# USPTO_crawler 

## 1. USPTO의 API를 활용한 Patents 검색

- 특정 특허번호를 알고있을 때, USPTO에서 제공하는 다양한 특허 정보를 검색하는 방법
    - input : patents numbers
    - output : USPTO에서 제공하는 patents attribution 정보(CPC, IPC, cited by,,,)
    - 현재 버전에서는 2021년 12월 31일 전에 등록된 특허들만 검색

### 사용법

1. 찾고자 하는 특허번호를 구해 pat_num에 저장
    - google patent, kipris …등
2. 원하는 특허 정보를 선택하여 patent_crawling 함수 안 attribution 변수에 대입
    - ex) attribution =["patent_number","cpc_subgroup_id","cited_patent_number",…]
        
        #USPTO API document를 참고하여 attribution 선택
        
        [API Endpoints](https://patentsview.org/apis/api-endpoints)
        
3. pat_num을 patent_crawling에 대입하여 나온 결과값을 DataFrame으로 변환 후 Excel로 저장
 

## 2. Cited_patents 추가하기

- patents가 인용한 patents들의 정보를 찾기 위한 방법
    - input : cited_patent_number
    - output : cited_patent_number와 patents_number를 합쳐 바꿔 1번 방법 실행

### 사용법

1. 1번을 실행했을 때, 얻은 output에서 cited_patents만 추출하여 cited_num에 저장
2. Json 형태의 dictionary 문자열에서 cited_patent_number만 cited_num_list에 저장
3. cited_num_list의 중복을 제거한 후 patents_number를 합쳐 1번방법을 동일 수행
