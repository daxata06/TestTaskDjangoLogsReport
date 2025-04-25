<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>README — Анализ логов Django</title>
</head>
<body>
  <h1>📝 CLI-приложение для анализа логов Django</h1>

  <h2>📥 Клонирование репозитория</h2>
  <p>Склонируйте проект с GitHub:</p>
  <pre><code>git clone https://github.com/daxata06/TestTaskDjangoLogsReport.git</code></pre>
  <p>Перейдите в директорию проекта:</p>
  <pre><code>cd название-репозитория</code></pre>

  <h2>📦 Установка и запуск</h2>

  <h3>1. 🔧 Создание виртуального окружения</h3>
  <p>Откройте терминал и выполните:</p>
  <pre><code>python -m venv venv</code></pre>

  <p><strong>Активация виртуального окружения:</strong></p>
  <ul>
    <li><strong>Windows:</strong> <code>venv\Scripts\activate</code></li>
    <li><strong>macOS/Linux:</strong> <code>source venv/bin/activate</code></li>
  </ul>

  <h3>2. 🧪 Установка зависимостей</h3>
  <p>Установите <code>pytest</code> (и другие зависимости при необходимости):</p>
  <pre><code>pip install pytest</code></pre>

  <h2>🚀 Использование</h2>
  <p>Для анализа логов и генерации отчёта выполните:</p>
  <pre><code>python main.py путь_к_логу1.log путь_к_логу2.log --report handlers</code></pre>

  <p><strong>Пример:</strong></p>
  <pre><code>python main.py app1.log app2.log --report handlers</code></pre>

  <h2>🧪 Запуск тестов</h2>
  <p>Чтобы запустить все тесты:</p>
  <pre><code>pytest -v</code></pre>

  <p>Чтобы запустить один конкретный тест:</p>
  <pre><code>pytest test_main.py::test_extract_handler_from_message</code></pre>
</body>
</html>
