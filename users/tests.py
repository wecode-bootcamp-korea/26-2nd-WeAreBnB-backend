import json
import jwt

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock                  import patch, MagicMock
from datetime                       import datetime, timedelta
from config.settings                import SECRET_KEY, ALGORITHM

from users.models                   import User

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            email             = 'mjb@gmail.com',
            password          = '1q2w3e4r!',
            name              = '민정',
            phone             = '111-1111-1111',
            profile_image_url = '',
            social_id         = '',
            social_type       = '',
        )
    
    def tearDown(self):
        User.objects.all().delete()
        
    def test_sign_up_success(self):
        client = Client()
        user   = {
            'name'    : '민정',
            'email'   : 'migigi@gmail.com',
            'password': '1q2w3e4r!'
        }
        
        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS'
            }
        )
        
    def test_sign_up_key_error(self):
        client = Client()
        user   = {
            'name'    : '민정',
            'password': '1q2w3e4r!'
        }
        
        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'KEY_ERROR'
            }
        )
        
    def test_sign_up_email_not_valid(self):
        client = Client()
        user   = {
            'name'    : '민정',
            'email'   : 'migigi@gmailcom',
            'password': '1q2w3e4r!'
        }
        
        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'EMAIL_NOT_VALID'
            }
        )

    def test_sign_up_password_not_valid(self):
        client = Client()
        user   = {
            'name'    : '민정',
            'email'   : 'mjb@gmail.com',
            'password': '1q2w3e'
        }
        
        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'PASSWORD_NOT_VALID'
            }
        )

class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            email             = 'minjbak@naver.com',
            password          = '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            name              = '민정',
            phone             = '111-1111-1111',
            profile_image_url = '',
            social_id         = '',
            social_type       = '',
        )
        
    def tearDown(self):
        User.objects.all().delete()
        
    def test_sign_in_success(self):
        client = Client()
        user   = {
            'id'      : 1,
            'email'   : 'minjbak@naver.com',
            'password': '12q23w34e45r!'
        }
        
        response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')
        access_token = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS',
                'access_token' : access_token
            }
        )
        
    def test_sign_in_invalid_password(self):
        client = Client()
        user   = {
            'email'   : 'minjbak@naver.com',
            'password': '1q2w3e4'
        }
        
        response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_PASSWORD'
            }
        )
        
    def test_sign_in_invalid_key_error(self):
        client = Client()
        user   = {
            'email'   : 'minjbak@naver.com',
        }
        
        response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'KEY_ERROR'
            }
        )

class KakaoLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            id        = 1,
            name      = '박민정',
            email     = 'angelmin00@naver.com',
            social_id = 1997422419
        )

    def tearDown(self):
        User.objects.all().delete()
        
    @patch('users.views.requests')
    def test_kakao_login_new_user_success(self, mocked_requests):
        client = Client()
        
        class MockResponse:
            def json(self):
                return {
                    "id": 1997422418,
                    "kakao_account": {
                        "profile": {
                        "nickname": "박민"
                        },
                        "email": "angelmin@naver.com"
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockResponse())
        headers             = {'HTTP_Authorization': 'fake_access_token'}
        response            = client.get('/users/kakaologin', **headers)
        access_token        = jwt.encode({'user_id': 2, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS',
                'access_token' : access_token
            }
        )
        
    @patch('users.views.requests')
    def test_kakao_login_existing_user_success(self, mocked_requests):
        client = Client()
        
        class MockResponse:
            def json(self):
                return {
                    "id": 1997422419,
                    "kakao_account": {
                        "profile": {
                        "nickname": "박민정"
                        },
                        "email": "angelmin00@naver.com"
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockResponse())
        headers             = {'HTTP_Authorization': 'fake_access_token'}
        response            = client.get('/users/kakaologin', **headers)
        access_token        = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS',
                'access_token' : access_token
            }
        )
        
    @patch('users.views.requests')
    def test_kakao_login_existing_user_success(self, mocked_requests):
        client = Client()
        
        class MockResponse:
            def json(self):
                return {
                    "id": 1997422419,
                    "kakao_account": {
                        "profile": {
                        "nickname": "박민정"
                        },
                        "email": "angelmin00@naver.com"
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockResponse())
        headers             = {'HTTP_Authorization': 'fake_access_token'}
        response            = client.get('/users/kakaologin', **headers)
        access_token        = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS',
                'access_token' : access_token
            }
        )
        
    @patch('users.views.requests')
    def test_kakao_login_invalid_token(self, mocked_requests):
        client = Client()
        
        class MockResponse:
            def json(self):
                return {
                    "code": -401,
                    "msg": "InvalidTokenException"
                }
        
        mocked_requests.get = MagicMock(return_value = MockResponse())
        headers             = {'HTTP_Authorization': 'fake_access_token'}
        response            = client.get('/users/kakaologin', **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_TOKEN'
            }
        )

class ProfileImageTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            name              = '민정',
            email             = 'minjbak@naver.com',
            password          = '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            phone             = '111-1111-1111'
        )

    def tearDown(self):
        User.objects.all().delete()
        
    @patch('core.utils.FileUpload')
    def test_profile_image_s3_upload_success(self, mocked_file_upload):
        access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MzgyNzQ4MDF9.99xiY7YF4pzIhIU5so8DMHwChfkuKdYRyHYA51azkmk'
        
        class MockedResponse:
            def upload(self):
                return 'https://wearebnbbucket.s3.ap-northeast-2.amazonaws.com/d5620dde-2641-4c86-932f-ffdb1a550b25'
        
        file = SimpleUploadedFile(
            name         = 'test.png',
            content      = b'file_content',
            content_type = 'application/png'
        )
        
        mocked_file_upload.upload = MagicMock(return_value = MockedResponse())
        headers          = {'HTTP_Authorization': access_token, 'format' : 'multipart'}
        body             = {'filename' : file}
        response         = self.client.post('/edit-photo', body, **headers)

        print(response)
        
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})
        self.assertEqual(response.status_code, 200)