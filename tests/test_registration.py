# tests/test_registration.py (добавьте или дополните)

from registration import add_user, authenticate_user, get_all_users
import sqlite3
import pytest

# Фикстура для временной БД
@pytest.fixture
def temp_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, 
                       username TEXT UNIQUE, 
                       password TEXT, 
                       email TEXT)''')
    yield conn
    conn.close()

def test_add_user_success(temp_db):
    # Тестируем добавление пользователя
    result = add_user(temp_db, "testuser", "pass123", "test@example.com")
    assert result == True

def test_add_user_duplicate(temp_db):
    add_user(temp_db, "testuser", "pass123", "test@example.com")
    result = add_user(temp_db, "testuser", "pass456", "other@example.com")
    assert result == False

def test_authenticate_user_correct(temp_db):
    add_user(temp_db, "alice", "secret", "alice@example.com")
    result = authenticate_user(temp_db, "alice", "secret")
    assert result == True

def test_authenticate_user_wrong_password(temp_db):
    add_user(temp_db, "bob", "pass", "bob@example.com")
    result = authenticate_user(temp_db, "bob", "wrong")
    assert result == False

def test_authenticate_user_not_exists(temp_db):
    result = authenticate_user(temp_db, "nobody", "pass")
    assert result == False

def test_get_all_users_hides_passwords(temp_db):
    add_user(temp_db, "charlie", "pwd", "charlie@example.com")
    users = get_all_users(temp_db)
    assert len(users) == 1
    assert 'password' not in users[0]  # пароль не должен показываться