# tests/test_outline_manager.py

import os
import pytest
from vpn_interface.outline_manager import (
    create_outline_access_key,
    delete_outline_access_key,
    get_outline_access_keys,
    rename_outline_access_key,
    extract_access_key_id
)

# Настройка тестовых данных
TEST_KEY_NAME = "TestDevice"
RENAMED_KEY_NAME = "RenamedTestDevice"

#OUTLINE_API_URL="https://195.201.111.36:43180"
#OUTLINE_CERT_SHA256="DA276C3627E3899F741634E689CE975C917C864834515313DCD77D65A54D4B5F"

@pytest.fixture(scope="module")
def setup_outline():
    # Проверка наличия необходимых переменных окружения
    #print(os.getenv("OUTLINE_API_URL"))
    #print(os.getenv("OUTLINE_CERT_SHA256"))
    assert os.getenv("OUTLINE_API_URL"), "OUTLINE_API_URL не установлена"
    assert os.getenv("OUTLINE_CERT_SHA256"), "OUTLINE_CERT_SHA256 не установлена"

def test_create_outline_access_key(setup_outline):
    access_url = create_outline_access_key(TEST_KEY_NAME)
    assert access_url, "Не удалось создать ключ доступа Outline"
    print(f"Созданный accessUrl: {access_url}")

def test_get_outline_access_keys(setup_outline):
    keys = get_outline_access_keys()
    assert isinstance(keys, list), "get_outline_access_keys должна возвращать список"
    print(f"Полученные ключи: {[key.name for key in keys]}")

def test_rename_outline_access_key(setup_outline):
    keys = get_outline_access_keys()
    target_key = next((key for key in keys if key.name == TEST_KEY_NAME), None)
    assert target_key, "Целевой ключ для переименования не найден"
    success = rename_outline_access_key(target_key.key_id, RENAMED_KEY_NAME)
    assert success, "Не удалось переименовать ключ доступа Outline"
    # Проверка, что ключ переименован
    keys = get_outline_access_keys()
    renamed_key = next((key for key in keys if key.name == RENAMED_KEY_NAME), None)
    assert renamed_key, "Ключ не был переименован"
    print(f"Ключ переименован в: {renamed_key.name}")

def test_delete_outline_access_key(setup_outline):
    keys = get_outline_access_keys()
    target_key = next((key for key in keys if key.name == RENAMED_KEY_NAME), None)
    assert target_key, "Целевой ключ для удаления не найден"
    success = delete_outline_access_key(target_key.key_id)
    assert success, "Не удалось удалить ключ доступа Outline"
    # Проверка, что ключ удален
    keys = get_outline_access_keys()
    deleted_key = next((key for key in keys if key.name == RENAMED_KEY_NAME), None)
    assert not deleted_key, "Ключ не был удален"
    print(f"Ключ {RENAMED_KEY_NAME} успешно удален")
