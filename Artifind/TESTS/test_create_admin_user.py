import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base, Admin, Moderator, users
from moderator import CreateUserRequest
import bcrypt

DATABASE_URL = "mysql+mysqlconnector://root:ah123//12ah@localhost/test_db"  
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
class TestCreateAdminUser(unittest.TestCase):
    def setUp(self):
        # Créer les tables dans la base de données de test
        Base.metadata.create_all(bind=engine)
        self.test_client = TestClient(app)
        self.db = TestingSessionLocal()

    def tearDown(self):
        # Supprimer les tables de la base de données de test
        Base.metadata.drop_all(bind=engine)

        self.db.close()

    def test_create_admin_user(self):
        # Données de test
        create_user_request = CreateUserRequest(
    email="tesnt9vnb9@example.com",
    nom="Test",
    prenom="User",
    password="testpassword",
)


        # Appel à la fonction de création de l'administrateur
        response = self.test_client.post("/moderator/admin/create_user", json=create_user_request.dict())
        print("Request JSON:", create_user_request.dict())
        print("Response JSON:", response.json())

        print(response)
        print('tttttttttttttttttttttttttttttttttttttttttt')
        print(create_user_request.dict())
        print(response.json())

        # Vérifier que la réponse est un code HTTP 201 (Created)
        self.assertEqual(response.status_code, 201)




if __name__ == '__main__':
    unittest.main()
        

