# Vandyshev-21-K-AS1 Protected Workstation Audit Service

**Отчет по дисциплине "Технология проектирования автоматизированных систем в защищенном исполнении"**

> Тема работы: разработка и деплой веб-сервиса для аудита защищенности рабочих станций.

## Паспорт работы

| Параметр       | Значение                                      |
|----------------|-----------------------------------------------|
| Проект         | `vandyshev-protected-workstation-audit-service` |
| Репозиторий    | `vandyshev-21-k-as1-protected-workstation-audit` |
| Исполнитель    | Вандышев Р.Ю.                    |
| Группа         | 21-К-АС1                                           |
| Дата           | 21.06.2026                                    |
| GitHub         | https://github.com/Sh1rok/vandyshev-21-k-as1-protected-workstation-audit |

![Репозиторий](screenshots/01-github-repository.png)

## 1. Цель работы
Демонстрация полного DevOps-цикла: FastAPI → Docker → Yandex Cloud (Terraform) → Kubernetes.

## 2. Структура репозитория
![Структура проекта](screenshots/02-project-tree.png)

## 3. Описание API
## Описание API

| Метод | Путь | Назначение |
|-------|------|------------|
| GET   | `/`  | Главная страница сервиса |
| GET   | `/health` | Проверка состояния приложения |
| GET   | `/workstations` | Список всех рабочих станций |
| GET   | `/workstations?department=...` | Фильтрация по подразделению |
| GET   | `/workstation/{hostname}` | Поиск рабочей станции по имени |
| GET   | `/audit-ready` | Список станций, готовых к защищенному контуру |
## 4. Локальный запуск без Docker
1) Создание виртуального окружения
```bash
python -m venv venv
```
2) Активация
```bash
venv\Scripts\activate
```
3) Установка зависимостей
```bash
pip install -r requirements.txt
```
4) Запуск сервиса
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Проверка через:
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/workstations
curl http://127.0.0.1:8000/audit-ready
```
Swagger UI будет доступен по адресу:
```bash
http://127.0.0.1:8000/docs
```
![Swagger](sreenshots/03-swagger-ui.png)
