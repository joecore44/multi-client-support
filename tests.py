#!/usr/bin/env python
from datetime import datetime, timedelta
import re
import unittest
from app import create_app, db
from app.models import User, Post, TrainerProfile, CustomerProfile, BillingPlan, CustomerSubscription
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Multi Client Support System' in response.get_data(
            as_text=True))

    def test_customer_profile(self):
        user = User(username='john', email='john@example.com')
        db.session.add(user)
        db.session.commit()
        john = User.query.filter_by(username='john').first()
        
        customer = CustomerProfile(user=john)
        customer.first_name = 'Test'
        customer.last_name = 'Tester'
        customer.phone_number = '9099987979'
        customer.branding_image = 'path.to/image.jpg'

        db.session.add(customer)
        db.session.commit()
    
        new_user = CustomerProfile.query.filter_by(user=john).first()
        
        self.assertEqual(new_user.first_name, 'Test')
        self.assertEqual(new_user.last_name, 'Tester')
        self.assertEqual(new_user.phone_number, '9099987979')
        self.assertEqual(new_user.branding_image, 'path.to/image.jpg')


    def test_trainer_profile(self):
        user = User(username='jordann', email='jordann@corenutritionpv.com')
        db.session.add(user)
        db.session.commit()
        jordann = User.query.filter_by(username='jordann').first()

        trainer = jordann.trainer_profiles.first()
        trainer.first_name = 'Testtt'
        trainer.last_name = 'Testerrr'
        trainer.phone_number = '4994994999'
        trainer.branding_image = 'path.to/images.jpg'
        
        db.session.add(trainer)
        db.session.commit()

        new_jordann = User.query.filter_by(username='jordann').first()
        self.assertEqual(new_jordann.first_name, 'Testtt')
        self.assertEqual(new_jordann.last_name, 'Testerrr')
        self.assertEqual(new_jordann.phone_number, '4994994999')
        self.assertEqual(new_jordann.branding_image, 'path.to/images.jpg')

    def test_billing_plans(self):
        user = User(username='jordann', email='john@corenutritionpv.com')
        db.session.add(user)
        db.session.commit()
        jordann = User.query.filter_by(username='jordann').first()

    def test_customer_subscription(self):
        user = User(username='jordann', email='jordannjohn@corenutritionpv.com')
        db.session.add(user)
        db.session.commit()
        jordann = User.query.filter_by(username='jordann').first()

      



    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))


    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

    


if __name__ == '__main__':
    unittest.main(verbosity=2)
