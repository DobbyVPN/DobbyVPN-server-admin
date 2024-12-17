# Outline Admin Interface

**Outline Admin Interface** предоставляет удобный интерфейс для управления ключами Outline VPN. Приложение обладает интуитивно понятным терминальным интерфейсом, созданным с помощью библиотеки Textual.

## Возможности

- Просмотр всех ключей Outline VPN
- Добавление новых ключей
- Удаление существующих ключей
- Переименование ключей
- Обновление ключей с сервера Outline
- Управление переменными окружения через `.env` файл

## Установка

### Предварительные требования

- Python 3.8 или выше
- pip

### Шаги установки

1. **Клонируйте репозиторий или скачайте архив с исходным кодом:**

   ```bash
   git clone https://github.com/xaeliudzyh/Outline-Admin-TUI.git
   
2. **Перейдите в директорию проекта**
    ```bash
   cd Outline-Admin-TUI
   
3. **Установите зависимости**
    ```bash
    pip install -r requirements.txt

4. **После успешной установки зависимостей, запустите приложение командой**
    ```bash
   python main.py