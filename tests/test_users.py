import unittest
from index import create_app
from flask_login import login_user, current_user
from unittest.mock import patch, MagicMock
from connectors.mysql_connector import engine, sessionmaker
from models.user import User
from models.product import Product
from index import app
import json

class TestLoginFeature(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

        with self.app.application.app_context():
            with self.engine.connect() as connection:
                self.Session.configure(bind=connection)
                session = self.Session()

                # Create a test user
                dummy_pass = 'dummypassword'
                test_user = User(name='Test User', email='unittest@dummy.com', password=dummy_pass, role='Admin')
                test_user.set_password(dummy_pass)
                session.add(test_user)
                session.commit()
                session.close()


    def tearDown(self):

        with self.app.application.app_context():
            with self.engine.connect() as connection:
                self.Session.configure(bind=connection)
                session = self.Session()

                # Delete the test user from the database
                test_user = session.query(User).filter(User.email=="unittest@dummy.com").first()
                if test_user:
                    session.delete(test_user)

                # Delete inserted product data from the DB
                test_product = session.query(Product).filter(Product.name=="test product").first()
                if test_product:
                    session.delete(test_product)

                session.commit()
                session.close()

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def login_user(self):
        response = self.app.post('/login', data=dict(
            email='unittest@dummy.com',
            password='dummypassword'
        ), follow_redirects=True)

        return response

    def test_login_user(self):
        # Log in the test user
        response = self.login_user()

        # Assert successful login
        self.assertEqual(response.status_code, 200) 
        
    # Function for accessing authorized domain
    def test_authorized_endpoint(self):
        self.login_user()

        # Check GET /product access
        response = self.app.get('/review')
        self.assertEqual(response.status_code, 200) 

        # Check GET /login access

    # Function for checking unauthorized domain
    def test_unauthorized_endpoint(self):
        # Check GET /product access
        response = self.app.get('/review')
        self.assertEqual(response.status_code, 403) 

        self.login_user()
        response = self.app.get('/review')
        self.assertEqual(response.status_code, 200) 

    # Function for checking unauthorized domain
    def test_product_insert(self):

        request_body = dict(
            rating=5,
            description='test review'
        )

        # Check POST /product access
        response = self.app.post('/review', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 403) 

        self.login_user()
        response = self.app.post('/review', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200) 


if __name__ == '__main__':
    unittest.main()