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
        # Clean up the database after each test
        with SessionLocal() as session:
            # Use text function to explicitly declare the SQL statement as text
            session.execute(text("DELETE FROM moderator;"))

    def test_delete_user(self):
        # Create a test user in the database
        test_user = Moderator(email="testh11@example.com", nom="John", prenom="Doe", hashed_password="hashed_password")
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



if __name__ == '__main__':
    unittest.main()
