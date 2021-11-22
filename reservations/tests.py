import json, uuid, jwt

from django.test         import TestCase, Client
from unittest.mock       import patch, MagicMock

from users.models        import User
from rooms.models        import Room, RoomLocation, RoomType
from reservations.models import Reservation
from datetime            import datetime, timedelta
from config.settings     import SECRET_KEY, ALGORITHM

class ReservationTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = Client()

        User.objects.create(
            id                = 1,
            email             = 'minjbak@naver.com',
            password          = '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            name              = '민정',
            phone             = '111-1111-1111',
        )

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
                host_user_id = 1,
                room_type_id = 2,
                title        = '[OPEN SALE] #SLOW #REST',
                description  = '넓고 깨끗한 공간에서 힐링시간되세요.',
                price        = 109753,
                max_guest    = 3,
                bedroom      = 1,
                bed          = 1,
                bath         = 1,
                created_at   = '2021-11-18',
            )
        ])

        Reservation.objects.bulk_create([
            Reservation(
                id               = 1,
                reservation_code = '00002',
                user_id          = 1,
                room_id          = 1,
                check_in         = '2021-11-26',
                check_out        = '2021-11-28',
                days             = 2,
                adult            = 2,
                children         = 0
            )
        ])

    def tearDown(self):
        User.objects.all().delete()
        Room.objects.all().delete()
        Reservation.objects.all().delete()
        RoomLocation.objects.all().delete()
        RoomType.objects.all().delete()

    @patch('reservations.views.uuid.uuid4')
    def test_success_reservation_view_post_method(self, mocked_requests):
        user = {
            'id'       : 1,
            'email'    : 'minjbak@naver.com',
            'password' : '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            'name'     : '민정',
            'phone'    : '111-1111-1111',
        }

        response     = self.client.post('/users/signin', json.dumps(user), content_type='application/json')
        access_token = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
        
        mocked_requests.return_value = '00001'

        class MockResponse:
            def json(self):
                return {
                    'reservation_code' : '00001'
                }

        reservation = {
            'user'      : 1,
            'room'      : 1,
            'check_in'  : '2021-11-25',
            'check_out' : '2021-11-28',
            'adult'     : 3,
            'children'  : 0
        }

        mocked_requests.get = MagicMock(return_value = MockResponse())    
        headers  = {'HTTP_Authorization': access_token}
        response = self.client.post('/reservations', json.dumps(reservation), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'reservation_code': '00001'
            }
        )
    
    def test_success_reservationfix_view_put_method(self):
        user = {
            'id'       : 1,
            'email'    : 'minjbak@naver.com',
            'password' : '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
        }

        response     = self.client.post('/users/signin', json.dumps(user), content_type='application/json')
        access_token = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)

        reservation = {
            'check_in'  : '2021-11-25',
            'check_out' : '2021-11-28',
            'adult'     : 3,
            'children'  : 0
        }

        headers  = {'HTTP_Authorization': access_token}
        response = self.client.put('/reservations/00002', json.dumps(reservation), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS'
            }
        )

    def test_success_reservationfix_view_delete_method(self):
        user = {
            'id'       : 1,
            'email'    : 'minjbak@naver.com',
            'password' : '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            'name'     : '민정',
            'phone'    : '111-1111-1111',
        }

        response     = self.client.post('/users/signin', json.dumps(user), content_type='application/json')
        access_token = jwt.encode({'user_id': 1, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)

        headers  = {'HTTP_Authorization': access_token}
        response = self.client.delete('/reservations/00002', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS'
            }
        )