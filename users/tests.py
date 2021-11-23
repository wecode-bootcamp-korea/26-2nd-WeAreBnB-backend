import json
import jwt

from django.test     import TestCase, Client, TransactionTestCase
from unittest.mock   import patch, MagicMock
from config.settings  import SECRET_KEY, ALGORITHM
from datetime        import datetime, timedelta
from freezegun       import freeze_time

from users.models          import User
from reviews.models        import Review
from rooms.models          import Option, Room, RoomImage, RoomLocation, RoomOption, RoomType
from reservations.models   import Reservation

class SignUpTest(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            id               = 1,
            email            = 'mjb@gmail.com',
            password         = '1q2w3e4r!',
            name             = '민정',
            phone            = '111-1111-1111',
            profile_image_url = '',
            social_id        = '',
            social_type      = '',
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
            id               = 1,
            email            = 'minjbak@naver.com',
            password         = '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            name             = '민정',
            phone            = '111-1111-1111',
            profile_image_url = '',
            social_id        = '',
            social_type      = '',
        )
        
    def tearDown(self):
        User.objects.all().delete()
    
    @freeze_time('2019-01-02')
    def test_sign_in_success(self):
        client = Client()
        user   = {
            'id'      : 1,
            'email'   : 'minjbak@naver.com',
            'password': '12q23w34e45r!'
        }
        
        response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')
        access_token = jwt.encode({'user_id': 1, 'exp': datetime.strptime('2019-01-02', '%Y-%m-%d') + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
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

class KakaoLoginTest(TransactionTestCase):
    reset_sequences = True
    def setUp(self):
        User.objects.create(
            id        = 1,
            name      = '박민정',
            email     = 'angelmin00@naver.com',
            social_id = 1997422419
        )

    def tearDown(self):
        User.objects.all().delete()
    
    @freeze_time('2019-01-02')
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
        access_token        = jwt.encode({'user_id': 2, 'exp': datetime.strptime('2019-01-02', '%Y-%m-%d') + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS',
                'access_token' : access_token
            }
        )
    
    @freeze_time('2019-01-02')
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
        access_token        = jwt.encode({'user_id': 1, 'exp': datetime.strptime('2019-01-02', '%Y-%m-%d') + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
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
        
class MyPageDetailTest(TestCase):
    @freeze_time('2021-11-18')
    def setUp(self):
        User.objects.bulk_create([
            User(
                id         = 1,
                email      = 'ezsv@gmail.com',
                password   = '1q2w3e4r!',
                name       = '이지은',
                phone      = '010-1111-2222',
                created_at = '2021-11-18'
            ),
            User(
                id         = 2,
                email      = 'hwa@gmail.com',
                password   = '1q2w3e4r!',
                name       = '한화연',
                phone      = '010-2222-3333',
                created_at = '2021-11-18'
            ),
            User(
                id         = 3,
                email      = 'minjeong@gmail.com',
                password   = '1q2w3e4r!',
                name       = '박민정',
                phone      = '010-7777-8888',
                created_at = '2021-11-18'
            )
        ])

        RoomType.objects.bulk_create(
            [
            RoomType(
                id   = 1,
                name = '집 전체'
            ),
            RoomType(
                id   = 2,
                name = '개인실'
            ),
            RoomType(
                id   = 3,
                name = '호텔 객실'
            )
        ])

        RoomLocation.objects.bulk_create([
            RoomLocation(
                id        = 1,
                country   = '한국',
                city      = '서울시',
                address   = '한국 서울시 강남구 청담동 11-5',
                latitude  = 37.521927,
                longitude = 127.046626
            ),
            RoomLocation(
                id        = 2,
                country   = '한국',
                city      = '서울시',
                address   = '한국 서울시 강남구 삼성1동 62-9',
                latitude  = 37.517173,
                longitude = 127.054316
            ),
            RoomLocation(
                id        = 3,
                country   = '한국',
                city      = '서울시',
                address   = '한국 서울시 강남구 청담동 99-22',
                latitude  = 37.526105,
                longitude = 127.045747
            )
        ])

        Room.objects.bulk_create([
            Room(
                id           = 1,
                location_id  = 1,
                host_user_id = 1,
                room_type_id = 1,
                title        = '#방구석영화관2#햇살가득 #방구석캠핑 #무료주차,',
                description  = '✔ 도보 2분거리 편의점. 3분거리 먹자골목에 위치!!',
                price        = 98200,
                max_guest    = 4,
                bedroom      = 1,
                bed          = 1,
                bath         = 1,
                created_at   = '2021-11-18',
            ),
            Room(
                id           = 2,
                location_id  = 2,
                host_user_id = 2,
                room_type_id = 2,
                title        = '[OPEN SALE] #SLOW #REST',
                description  = '넓고 깨끗한 공간에서 힐링시간되세요.',
                price        = 109753,
                max_guest    = 3,
                bedroom      = 1,
                bed          = 1,
                bath         = 1,
                created_at   = '2021-11-18',
            ),
            Room(
                id           = 3,
                location_id  = 3,
                host_user_id = 3,
                room_type_id = 3,
                title        = 'L7 Standard Double',
                description  = '귀여운 고양이 두 마리와 기억에 남을 하루를 만드세요♡',
                price        = 75000,
                max_guest    = 2,
                bedroom      = 1,
                bed          = 1,
                bath         = 1,
                created_at   = '2021-11-18',
            )
        ])

        Option.objects.bulk_create([
            Option(
                id        = 1,
                name      = '무선 인터넷',
                image_url = 'https://cdn-icons-png.flaticon.com/512/93/93158.png'
            ),
            Option(
                id        = 2,
                name      = '주방',
                image_url = 'https://cdn-icons-png.flaticon.com/512/963/963883.png'
            ),
            Option(
                id        = 3,
                name      = '헤어드라이어',
                image_url = 'https://cdn-icons.flaticon.com/png/512/3792/premium/3792440.png?token=exp=1637221536~hmac=1808076463d4f922657b285200a923b5'
            )
        ])

        RoomOption.objects.bulk_create([
            RoomOption(
                id        = 1,
                room_id   = 1,
                option_id = 1
            ),
            RoomOption(
                id        = 2,
                room_id   = 2,
                option_id = 2
            ),
            RoomOption(
                id        = 3,
                room_id   = 3,
                option_id = 3
            )
        ])

        RoomImage.objects.bulk_create([
            RoomImage(
                id        = 1,
                room_id   = 1,
                image_url = 'https://cdn.pixabay.com/photo/2016/11/18/17/20/living-room-1835923_960_720.jpg'
            ),
            RoomImage(
                id        = 2,
                room_id   = 2,
                image_url = 'https://cdn.pixabay.com/photo/2017/09/09/18/25/living-room-2732939_960_720.jpg'
            ),
            RoomImage(
                id        = 3,
                room_id   = 3,
                image_url = 'https://cdn.pixabay.com/photo/2015/10/20/18/57/furniture-998265_960_720.jpg'
            )
        ])

        Reservation.objects.bulk_create([
            Reservation(
                id               = 1,
                reservation_code = '00000001',
                room_id          = 1,
                user_id          = 1,
                check_in         = '2021-11-01',
                check_out        = '2021-11-03',
                days             = 2,
                adult            = 3,
                children         = 0,
                created_at       = '2021-11-18'
            ),
            Reservation(
                id               = 2,
                reservation_code = '00000002',
                room_id          = 2,
                user_id          = 1,
                check_in         = '2021-10-10',
                check_out        = '2021-10-14',
                days             = 4,
                adult            = 2,
                children         = 0,
                created_at       = '2021-11-18'
            ),
            Reservation(
                id               = 3,
                reservation_code = '00000003',
                room_id          = 3,
                user_id          = 1,
                check_in         = '2021-10-22',
                check_out        = '2021-10-24',
                days             = 2,
                adult            = 2,
                children         = 0,
                created_at       = '2021-11-18'
            )
        ])

        Review.objects.bulk_create([
            Review(
                id         = 1,
                room_id    = 1,
                user_id    = 1,
                title      = '생각보다 따뜻하고 만족',
                content    = '생각보다 따뜻하고 만족',
                rating     = 5,
                created_at = '2021-11-18'
            ),
            Review(
                id         = 2,
                room_id    = 2,
                user_id    = 1,
                title      = '음...',
                content    = '음...',
                rating     = 3,
                created_at = '2021-11-18'
            ),
            Review(
                id         = 3,
                room_id    = 3,
                user_id    = 1,
                title      = '좋아요',
                content    = '좋아요',
                rating     = 4,
                created_at = '2021-11-18'
            )
        ])

    def tearDown(self):
        User.objects.all().delete()
        RoomType.objects.all().delete()
        RoomLocation.objects.all().delete()
        Room.objects.all().delete()
        Option.objects.all().delete()
        RoomOption.objects.all().delete()
        RoomImage.objects.all().delete()
        Reservation.objects.all().delete()
        Review.objects.all().delete()
        
    def test_mypage_detail_view_get_success(self):
        client = Client()
        self.maxDiff = None
        access_token = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        headers = {'HTTP_Authorization': access_token}
        response = client.get('/users/mypage', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'results': {
                'reservations':[
                    {
                    'reservation_id': 1,
                    'address'       : '한국 서울시 강남구 청담동 11-5',
                    'title'         : '#방구석영화관2#햇살가득 #방구석캠핑 #무료주차,',
                    'image_url'     : 'https://cdn.pixabay.com/photo/2016/11/18/17/20/living-room-1835923_960_720.jpg',
                    'check_in'      : '2021-11-01',
                    'check_out'     : '2021-11-03'
                    },
                    {
                        'reservation_id': 2,
                        'address'       : '한국 서울시 강남구 삼성1동 62-9',
                        'title'         : '[OPEN SALE] #SLOW #REST',
                        'image_url'     : 'https://cdn.pixabay.com/photo/2017/09/09/18/25/living-room-2732939_960_720.jpg',
                        'check_in'      : '2021-10-10',
                        'check_out'     : '2021-10-14'
                    },
                    {
                        'reservation_id': 3,
                        'address'       : '한국 서울시 강남구 청담동 99-22',
                        'title'         : 'L7 Standard Double',
                        'image_url'     : 'https://cdn.pixabay.com/photo/2015/10/20/18/57/furniture-998265_960_720.jpg',
                        'check_in'      : '2021-10-22',
                        'check_out'     : '2021-10-24'
                    }
                ],
                'reviews': [
                    {
                        'review_id': 1,
                        'user_name': '이지은',
                        'room': '#방구석영화관2#햇살가득 #방구석캠핑 #무료주차,',
                        'title': '생각보다 따뜻하고 만족',
                        'content': '생각보다 따뜻하고 만족',
                        'created_at': '2021-11-18T00:00:00'
                    },
                    {
                        'review_id': 2,
                        'user_name': '이지은',
                        'room': '[OPEN SALE] #SLOW #REST',
                        'title': '음...',
                        'content': '음...',
                        'created_at': '2021-11-18T00:00:00'
                    },
                    {
                        'review_id': 3,
                        'user_name': '이지은',
                        'room': 'L7 Standard Double',
                        'title': '좋아요',
                        'content': '좋아요',
                        'created_at': '2021-11-18T00:00:00'
                    }
                ],
                'room_title_list': [
                    '#방구석영화관2#햇살가득 #방구석캠핑 #무료주차,',
                    '[OPEN SALE] #SLOW #REST',
                    'L7 Standard Double'
                ],
                'profile_image_url': None
            }
        })