import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base, Admin, Moderator, users
from moderator import CreateUserRequest
import bcrypt

DATABASE_URL = "mysql+mysqlconnector://marwa:12345678@localhost/test_db"  
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
    email="testlmm@example.com",
    nom="Test",
    prenom="User",
    password="testpassword",
)


        # Appel à la fonction de création de l'administrateur
        response = self.test_client.post("/moderator/admin/create_user", json=create_user_request.dict())
       

        # Vérifier que la réponse est un code HTTP 201 (Created)
        self.assertEqual(response.status_code, 201)
   

    def test_create_admin_user_existing_email(self):
        # Données de test avec email déjà enregistré dans la base de données
        create_user_request = CreateUserRequest(
            email="test@example.com",
            nom="Test",
            prenom="User",
            password="testpassword",
        )

        # Ajouter un utilisateur avec le même email dans la base de données
        existing_user = Moderator(
            email="testlmm@example.com",
            nom="Test",
            prenom="User",
            hashed_password=bcrypt.hashpw("testpassword".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )
        self.db.add(existing_user)
        self.db.commit()

        # Appel à la fonction de création de l'administrateur
        response = self.test_client.post("/moderator/admin/create_user", json=create_user_request.dict())

        # Vérifier que la réponse est un code HTTP 400 (Bad Request)
        self.assertEqual(response.status_code, 400)




if __name__ == '__main__':
    unittest.main()
        

