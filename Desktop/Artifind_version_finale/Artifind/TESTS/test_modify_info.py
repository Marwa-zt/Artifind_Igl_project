import unittest
from sqlalchemy import text
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_db
from database import SessionLocal, engine
from models import Base, Moderator
from urllib.parse import quote
class TestModifyUser(unittest.TestCase):

    def setUp(self):
        # Create test client and make it accessible to test methods
        self.client = TestClient(app)
        # Bind an engine to the metadata of the Base class, which the database models use
        Base.metadata.create_all(bind=engine)

    
    def test_modify_user(self):
        # Create a test user in the database
        test_user = Moderator(email="up94b0mr@example.com", nom="John", prenom="Doe", hashed_password="hashed_password")
        db = SessionLocal()
        db.add(test_user)
        db.commit()
        
        modified_user_data = {
        "email": "up94b0mr@example.com",
        "nom": "NewLastName",
        "prenom": "NewFirstName",
        "password": "new_secure_password",
        }

        # Make a request to delete the user

        response = self.client.put(f"/moderator/modify-user/{test_user.email}", json=modified_user_data)
        # Check if the response is successful (HTTP 200 OK)
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()

