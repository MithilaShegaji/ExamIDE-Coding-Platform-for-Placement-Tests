import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-super-secret-key-that-no-one-knows'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:qwer@localhost/ExamIDE_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Judge0 API Configuration
JUDGE0_API_HOST = "judge0-ce.p.rapidapi.com"
JUDGE0_API_KEY = "6dfdfbada2msh8f832febcf6b9e0p14c372jsn22b5f4a30709" 