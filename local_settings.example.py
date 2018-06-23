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
