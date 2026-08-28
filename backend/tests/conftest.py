import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User, UserRole
from app.models.scope import Scope
from app.core.security import get_password_hash, create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_admin_user(db_session):
    user = User(
        username="testadmin",
        email="admin@test.local",
        hashed_password=get_password_hash("AdminPass123!"),
        role=UserRole.ADMIN
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_admin_user):
    token = create_access_token({"sub": test_admin_user.username, "role": test_admin_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_scope(db_session):
    scope = Scope(
        name="Test Authorized Lab Scope",
        description="Synthetic Scope for PyTest Suite",
        allowed_targets="10.0.0.0/24, 192.168.1.100, localhost, demo.lab",
        allowed_ports="22,80,443,3389",
        allowed_protocols="ssh,http,https,rdp"
    )
    db_session.add(scope)
    db_session.commit()
    db_session.refresh(scope)
    return scope
