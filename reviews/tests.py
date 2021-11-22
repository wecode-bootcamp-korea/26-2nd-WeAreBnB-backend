import json

from django.test    import TestCase, Client

from users.models   import User
from rooms.models   import Room, RoomLocation, RoomType
from reviews.models import Review

class ReservationTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = Client()

        User.objects.create(
            id       = 1,
            email    = 'minjbak@naver.com',
            password = '$2b$12$FCUz7aU5O.PbJOc73iGgYuGtNnkFpR2mjrWkcK3/SF4Oqy6r4Hmgi',
            name     = '민정',
            phone    = '111-1111-1111',
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
                room_id    = 2,
                user_id    = 1,
                title      = '좋아요',
                content    = '좋아요',
                rating     = 4,
                created_at = '2021-11-18'
            )
        ])

    def tearDown(self):
        User.objects.all().delete()
        Room.objects.all().delete()
        RoomLocation.objects.all().delete()
        RoomType.objects.all().delete()
        Review.objects.all().delete()

    def test_success_reviews_view_get_method(self):
        response = self.client.get('/reviews/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'results' : {
                'review_info'      : [{
                        'username'       : '민정',
                        'user_profile'   : None,
                        'title'          : '생각보다 따뜻하고 만족',
                        'content'        : '생각보다 따뜻하고 만족',
                        'rating'         : 5,
                        'date'           : '2021/11'
                        }],
                        'average_rating' : 5.0,
                        'review_count'   : 1
                    }
                }
            )