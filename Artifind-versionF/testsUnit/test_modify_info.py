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
        test_user = Moderator(email="tesntuuu@example.com", nom="John", prenom="Doe", hashed_password="hashed_password")
        db = SessionLocal()
        db.add(test_user)
        db.commit()
        
        modified_user_data = {
        "email": "tesntuuu@example.com",
        "nom": "NewLastName",
        "prenom": "NewFirstName",
        "password": "new_secure_password",
        }

        # Make a request to delete the user

        response = self.client.put(f"/moderator/modify-user/{test_user.email}", json=modified_user_data)
        # Check if the response is successful (HTTP 200 OK)
        assert response.status_code == 200
        db.refresh(test_user)
        # Check if the user information has been modified correctly
        '''
        modified_user = db.query(Moderator).filter(Moderator.email == test_user.email).first()
        self.assertEqual(modified_user.nom, modified_user_data["nom"])
        self.assertEqual(modified_user.prenom, modified_user_data["prenom"])
        '''
        db.close()

        def test_modify_non_existing_user(self):
        # Attempt to modify a user that does not exist in the database
         non_existing_email = "nonexistinng@example.com"

         modified_user_data = {
            "email": non_existing_email,
            "nom": "NewLastName",
            "prenom": "NewFirstName",
            "password": "new_secure_password",
        }

        # Make a request to modify the non-existing user
         response = self.client.put(f"/moderator/modify-user/{quote(non_existing_email)}", json=modified_user_data)

        # Check if the response is HTTP 404 Not Found
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
