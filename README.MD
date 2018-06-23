# Project: Ajou Arxiv

아주대학교 사회과학대학교의 ***1인1기1작*** 교육과정을 위한 학습 지원 웹 서비스 입니다.



## Install Environment and Dependencies

- 파이썬 버전은 <code>3.6</code> 을 기준으로 작성되었습니다.
- 간단한 환경 설정을 위해 최신 버전의 <code>Anaconda</code>를 설치하여 사용하길 권장합니다.
- 본 프로젝트를 위한 가상환경을 생성 및 활성화 한 후 아래의 과정을 진행하세요.
- 가상환경에서 <code>requirements.txt</code>를 사용해 필요한 의존 라이브러리들을 모두 설치할 수 있습니다.
```bash
(YourVirtualEnv) ProjectPath> pip install --upgrade pip
(YourVirtualEnv) ProjectPath> pip install -r requirements.txt
```
- 이후에는 데이터베이스 환경을 마이그레이션 합니다.
```bash
(YourVirtualEnv) ProjectPath> python manage.py makemigrations
(YourVirtualEnv) ProjectPath> python manage.py migrate
```
- 아래의 명령어로 관리자 전용 아이디를 생성할 수 있습니다.
```bash
(YourVirtualEnv) ProjectPath> python manage.py createsuperuser
```
- <code>manage.py</code>와 같은 폴더에 <code>local_settings.py</code> 파일을 생성한 이후 아래와 같이 설정해주세요.
```python
# -*- coding: utf-8 -*-
"""
서버 디버깅 모드 설정
"""
IS_DEBUG_MODE = True

"""
서버 접속을 위한 기본 설정 
"""
BASE_HOST = 'your.site.com:8000'
BASE_PROTOCOL = 'http'
BASE_URL = BASE_PROTOCOL + "://" + BASE_HOST

"""
서버 보안 설정
"""
SECRET_KEY = 'YOUR SECRET KEY HERE'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

"""
이메일 인증 및 회원가입을 허락할 도메인 목록
"""
ALLOWED_EMAIL_DOMAIN = [
    'ajou.ac.kr'
]

"""
메일 인증을 위해 사용할 메일서버 계정 정보
"""
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hello@gmail.com'
EMAIL_HOST_PASSWORD = 'gmail_password'
EMAIL_PORT = 587
EMAIL_DISPLAYED_NAME = '아주대학교 1인1기1작 교육과정'

"""
DISQUS 댓글 기능 사용을 위한 계정정보
"""
DISQUS_WEBSITE_SHORTNAME = 'YOUR SHORT NAME HERE'

```
- 아래의 명령어로 서버를 실행할 수 있습니다.
```bash
(YourVirtualEnv) ProjectPath> python manage.py runserver 0.0.0.0:8000
```

## Contacts
###Developer
```json
{
  "name" : "Dongyi Kim",
  "email": "dykim@codingmonster.net",
  "phone": "(+82) 010-2040-4457",
}
```
###Designer
```json
{
  "name" : "Juhyun Lee",
  "email": "Juhyunlee.uxui@gmail.com",
}
```