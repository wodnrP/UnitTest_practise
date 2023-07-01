# TDD 기초 : UnitTest 적용 연습 프로젝트입니다.

해당 프로젝트는 Swagger_practise를 copy하여 일부 변경한 프로젝트입니다.

---

**Requirements**
```
Install Python3.8

$ python3 -m venv ./{your venv name}    가상환경 생성
$ source {your venv name}/bin/activate  가상환경 실행
```
**Installation**
```
$ git clone https://github.com/wodnrP/Swagger_practise.git
$ pip install -r requirements.txt       프로젝트 패키지 설치 
```

**.env file create**
- 프로젝트 폴더와 같은 위치에 .env file 생성
- https://djecrety.ir/ 에서 django secret_key 생성 후 .env file에 작성
```
DEBUG=...   
SECRET_KEY=...
```

**static setting**
- 프로젝트 폴더와 같은 위치에 static 디렉토리 생성
- static 디렉토리 하위에 css, image, js 디렉토리 생성
- 이후 다음과 같은 코드 실행
```
$ python3 manage.py collectstatic
```

**Migration**
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

**TEST RUN**
- practise app 전체 테스트 실행
```
$ python3 manage.py test
```
- 부분 실행 : TESTCASE CLASS 기준
```
$ python3 manage.py test <앱 이름>.<테스트 파일 이름>.<Class이름>
$ python3 manage.py test practise.tests.SignupTest
```
- 부분 실행 : test 함수 기준
```
$ python3 manage.py test <앱 이름>.<테스트 파일 이름>.<Class이름>.<test함수이름>
$ python3 manage.py test practise.tests.SignupTest.test_signup_post_success
```
