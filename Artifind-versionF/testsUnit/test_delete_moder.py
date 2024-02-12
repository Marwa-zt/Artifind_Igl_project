import unittest
from sqlalchemy import text
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_db
from database import SessionLocal, engine
from models import Base, Moderator

class TestDeleteUser(unittest.TestCase):

    def setUp(self):
        # Create test client and make it accessible to test methods
        self.client = TestClient(app)
        # Bind an engine to the metadata of the Base class, which the database models use
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        with SessionLocal() as session:
            # Use text function to explicitly declare the SQL statement as text
            session.execute(text("DELETE FROM moderator;"))

    def test_delete_user(self):
        # Create a test user in the database
        test_user = Moderator(email="test411@example.com", nom="John", prenom="Doe", hashed_password="hashed_password")
        db = SessionLocal()
        db.add(test_user)
        db.commit()

        # Get the user id
        user_id = test_user.id

        # Check if the user exists before deletion
        self.assertIsNotNone(db.query(Moderator).get(user_id))

        # Make a request to delete the user
        response = self.client.delete(f"/moderator/delete-user/{test_user.email}")

        # Check if the response is successful (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        db.refresh(test_user)
        # Check if the user is deleted from the database
        #self.assertIsNone(db.query(Moderator).get(user_id))

    def test_delete_nonexistent_user(self):
        # Attempt to delete a user that doesn't exist
        response = self.client.delete("/moderator/delete-user/nonexistent@example.com")

        # Check if the response status code is 404
        self.assertEqual(response.status_code, 404)

    
if __name__ == '__main__':
    unittest.main()