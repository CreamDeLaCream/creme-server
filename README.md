# creme-server
# 옥자가 왜 그럴까

- [옥자가 왜 그럴까 데모 영상](https://www.youtube.com/watch?v=0QK0s1OaOs0)

## 1. 프로젝트 소개

- 반려 강아지 이미지 기반 감정분석 서비스

### 기술 스택

<div>
<img alt="Django" src ="https://img.shields.io/badge/Django-092E20.svg?&style=for-the-badge&logo=Javascript&logoColor=black"/>
<img alt="Poetry" src ="https://img.shields.io/badge/Poetry-60A5FA.svg?&style=for-the-badge&logo=React&logoColor=black"/>
<img alt="SQLite" src ="https://img.shields.io/badge/SQLite-003B57.svg?&style=for-the-badge&logo=Axios&logoColor=white"/>
<img alt="Amazon EC2" src ="https://img.shields.io/badge/Amazon EC2-FF9900.svg?&style=for-the-badge&logo=GitLab&logoColor=white"/>
<img alt="GitLab" src ="https://img.shields.io/badge/GitLab-FCA121.svg?&style=for-the-badge&logo=GitLab&logoColor=white"/>
<img alt="GitHub" src ="https://img.shields.io/badge/GitHub-181717.svg?&style=for-the-badge&logo=GitHub&logoColor=white"/>
</div>

## 2. 프로젝트 기획 의도

- 양육 가구 비율이 점점 늘어나면서 대한민국 1/3의 인구가 반려동물을 키우고 있다.

- 반려인이 증가함으로 더는 인간에 의한 사육으로 그치는 애완동물이 아니라, 함께 소통하고 감정을 공유하며 교감한다는 의미로 '반려동물'이라 표현을 한다.

- 반려동물에 대한 관심도가 높아지고 반려동물 사업이 활성화되고 있다.

- 하지만 라이프스타일에 따라 반려동물과의 교감에 신경을 쓰지 못하는 반려인들 또한 증가하고 있다.

- 우리 집 강아지가 현재 어떤 감정을 가지고 있을까?

- 내가 생각하는 강아지의 감정과 실제 강아지의 감정이 동일할까?

- 반려인들의 이러한 궁금증을 해소하고, 충분한 교감을 형성하기 위해, 반려동물의 감정 상태를 분석해 반려동물의 삶의 질을 높여주는 것이 이 서비스의 주된 목적이다.

### 옥왜까의 페르소나, 최서연(28세, 직장인)씨의 고민

- 일을 시작하면서 갑자기 바빠진 초년생
- 반려견과 함께하는 시간이 줄어 지속적인 교감이 어려운 반려인
- 바빠진 반려인과 정서적으로 멀어진 강아지 옥자를 설정
- 옥자의 감정이 궁금하고, 더 잘해주고 싶은 최서연
- 반려인 최서연과 강아지 옥자와의 관계 회복을 위한 프로젝트

**최서연씨와 같이 반려동물과 지속된 교감이 어려운 반려인을 위한 감정 분석 솔루션 서비스**

## 3. 프로젝트 구성도

- [와이어프레임](https://whimsical.com/AwiTidpMrywD4x61UwXLg7)

## 4. 서비스 주요 기능 설명

### 주요 기능

- 메인 페이지

  - 사진 촬영을 통한 강아지 감정 분석

- 분석 페이지

  - 분석이 이루어지는 동안 반려인이 생각하는 강아지 감정, 홀로 보낸 시간, 산책 횟수, 간식 횟수 체크

- 결과 페이지

  - 퍼센티지로 강아지의 감정 표현
  - 반려인과 반려견의 궁합 확인
  - 강아지가 느끼는 감정에 따른 솔루션 제공 (놀이, 관심, 산책, 간식)
  - 솔루션에 대한 디테일한 팁 제공
  - 검사 결과 URL로 공유, SNS 공유 (카카오)
  - 좋아요 체크 (회원 전용)
  - 반려인이 검사 결과에 대해 기록하는 기능 (회원 전용)

### 서브 기능

- 마이펫 페이지 (회원 전용)

  - 내 반려견 추가 / 관리
  - 반려인의 라이프스타일 등록
  - 강아지 감정 상태 기간별 데이터 제공
  - 저장된 분석 결과를 감정별로 분류하여 반려인이 원하는 감정에 맞게 기록을 선택하는 기능

## 5. 프로젝트 팀원 역할 분담

| 이름   | 담당 업무                          |
| ------ | ---------------------------------- |
| 곽진영 | 프론트엔드                    |
| 김지하 | 인공지능                     |
| 김혜원 | 프론트엔드/UIUX |
| 양영광 | 백엔드                             |
| 현소영 | 인공지능                           |
| 홍리경 | 팀장/백엔드                        |
