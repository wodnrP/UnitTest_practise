from django.test import TestCase
import json
from django.urls import reverse
from django.test import (TestCase, Client, RequestFactory)
from rest_framework.test import APIClient
from .models import User
from rest_framework.authtoken.models import Token
# Create your tests here.

#회원가입 기능 관련 테스트케이스
class SignupTest(TestCase):
    # 테스트에 필요한 객체를 미리 생성
    def setUp(self):
        pass

    # 테스트 과정 중에 생긴 데이터 제거 
    # 다른 테스트와 연관성이 있어도 정확한 테스트 결과를 위해 Clean UP을 진행
    def tearDown(self):
        User.objects.all().delete()
    
    # 회원가입 기능이 성공적으로 동작하는지 테스트
    def test_signup_post_success(self):
        client = Client()

        signup_info = {
            "username" : "signTestUser",
            "password" : "test1234",
            "nickname" : "테스트사용자"
        }
        # json.dumps()로 객체를 json화 시켜줌
        response = client.post(reverse('signup'), json.dumps(signup_info), content_type='application/json')
        
        # assertEqual()로 response 받은 status code가 정상적인지 확인
        self.assertEqual(response.status_code, 201)

# 로그인 기능 관련 테스트케이스
class LoginTest(TestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create(
            username="loginTestUser",
            nickname="로그인테스트사용자"
        )
        self.user.set_password("test0987")
        self.user.save()

    def tearDown(self):
        User.objects.all().delete()

    # 로그인 기능 테스트
    def test_login_post_sucess(self):
        login_info = {
            "username" : "loginTestUser",
            "password" : "test0987"
        }
        response = self.client.post(self.url, data=login_info, format='json')
        self.assertEqual(response.status_code, 201)
    
    # 로그인시 아이디가 틀렸을 경우 에러 테스트
    def test_login_post_invalid_username(self):
        login_info = {
            "username" : "logTestUser",
            "password" : "test0987"
        }
        response = self.client.post(self.url, data=login_info, format='json')
        self.assertEqual(response.status_code, 400)
    
    # 로그인시 비밀번호가 틀렸을 경우 에러 테스트
    def test_login_post_invalid_password(self):
        login_info = {
            "username" : "loginTestUser",
            "password" : "test1234"
        }
        response = self.client.post(self.url, data=login_info, format='json')
        self.assertEqual(response.status_code, 400)

# 로그아웃 테스트 케이스
class LogoutTest(TestCase):
    """
    1. json massage, status=200이 정상적으로 반환되는지 테스트
    2. 리프레시 토큰이 쿠키에서 삭제되었는지 테스트
    """ 
    def test_logout_delete_success(self):
        response = self.client.delete(reverse('logout'), format='json')

        self.assertEqual(response.json(), {'Message' : 'Logout success'} ) # json 메시지 확인
        self.assertEqual(response.status_code, 200)                        # status code 200 확인
        self.assertEqual(response.cookies['refreshToken'].value, "")       # 쿠키에 refreshToken 값 확인 

class UserInfoGetTest(TestCase):
    """
    1. json 객체와 status=200 정상적으로 반환되는지 테스트
    2. 토큰이 없을 경우 TokenErrorException class 호출에 따른 json message와 status=401 반환 테스트
    """
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.maxDiff = None
        
        self.user = User.objects.create(
            id = 1,
            username = "infoTestUser",
            nickname = "GET테스트사용자",
            profile = None
        )
        self.user.set_password('asdf1234')

        self.user.save()
    def tearDown(self):
        User.objects.all().delete()
    
    # 사용자 정보 조회 테스트
    def test_userinfo_success(self):
        login_user = {
            "username" : "infoTestUser",
            "password" : "asdf1234",
        }
        # 사용자 로그인
        login_response = self.client.post(reverse('login'), 
        data=login_user, format='json')
        # 로그인한 사용자의 access_token을 header에 인증
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.json()['access_token']}"
        )
        # 사용자 정보 조회 response
        response = self.client.get(reverse('user-info'), content_type='application/json')
        # response status code 200 검증 
        self.assertEqual(response.status_code, 200)
        # response json 객체 검증
        self.assertEqual(response.json(),{
            'id' : 1,
            'nickname' : 'GET테스트사용자',
            'profile' : None
        })
    
    # 토큰이 없는 경우
    def test_userinfo_nottoken(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {''}"
        )
        response = self.client.get(reverse('user-info'), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), { 'detail' : 'unauthenticated'})

class UserInfoPatchTest(TestCase):
    """
    1. json 객체와 status=200 정상적으로 반환되는지 테스트
    2. json 객체와 status=400 정상적으로 반환되는지 테스트
    3. 토큰이 없을 경우 TokenErrorException class 호출에 따른 json message와 status=401 반환 테스트
    """
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.maxDiff = None
        
        self.user = User.objects.create(
            id = 1,
            username = "infoTestUser",
            nickname = "GET테스트사용자",
            profile = None
        )
        self.user.set_password('asdf1234')

        self.user.save()
    def tearDown(self):
        User.objects.all().delete()
    
    # 사용자 정보 수정 테스트
    def test_userinfo_success(self):
        login_user = {
            "username" : "infoTestUser",
            "password" : "asdf1234",
        }

        login_response = self.client.post(reverse('login'), 
        data=login_user, format='json')

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.json()['access_token']}"
        )

        # 수정할 데이터
        user_update = {
            'nickname' : 'PATCH테스트사용자'
        }

        response = self.client.patch(reverse('user-info'), user_update)
        self.assertEqual(response.status_code, 200)

