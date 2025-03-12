# Log File Processor

## Описание проекта
Этот Python-скрипт предназначен для обработки сжатых лог-файлов (`.log.gz`). Он извлекает и фильтрует строки, содержащие определенные подстроки (`IpAppCallControlManager.callEventNotify` и `IpCall.routeReq`), и сохраняет результаты в отдельные файлы в папке `result`.

### Основные функции:
- Автоматически определяет каталог, в котором находятся логи.
- Ищет файлы с расширением `.log.gz`.
- Фильтрует записи по заданным условиям.
- Записывает отфильтрованные данные в текстовые файлы внутри папки `result`.

## Полезность проекта
Этот инструмент может быть полезен:
- **Аналитикам и инженерам** для обработки логов без необходимости вручную просматривать файлы.
- **Администраторам систем** для автоматизированного анализа логов звонков и маршрутизации.
- **Разработчикам ПО**, которым требуется быстро выделять нужные данные из лог-файлов для отладки.

## Структура проекта
Структура проекта должна выглядеть следующим образом:
```
/log_processor/
│   main.py                         # Основной скрипт
│   README.md                       # Документация
│
├── result/                         # Папка с результатами работы
│   ├── 2025-02-01.txt              # Файл с отфильтрованными записями
│
│   RA-2025-02-01-01-00-00.log.gz   # Пример файла лога
```

## Ожидаемый формат лог-файлов
Лог-файлы должны быть в формате `.log.gz` и содержать строки с разделением пробелами. Восьмая позиция строки должна содержать допустимый префикс (`1234400511`, `1234710011`, и т.д.).

## Что искать в логах
Скрипт ищет строки, содержащие:
- `IpAppCallControlManager.callEventNotify`
- `IpCall.routeReq`

При этом фильтрация происходит по условиям:
1. Строка должна содержать хотя бы 7 элементов (целостость данных и успешный звонок).
2. Должен быть найден один из целевых подстрок (`REQUIRED_SUBSTRINGS`).
3. Восьмой элемент должен начинаться с одного из `ALLOWED_PREFIXES`.
4. Связанные записи группируются по идентификатору (`line_for_filter[2]`).

## Как запустить проект
1. Убедитесь, что у вас установлен Python 3.
2. Поместите исполняемый `main.py` в папку с лог-файлами (`.log.gz`).
3. Запустите скрипт:
   ```bash
   python main.py
   ```
4. Результаты обработки появятся в папке `result/`.

## Зависимости
Скрипт не использует внешние библиотеки.

## Автор
Этот проект был создан для использования для телеком компании. Если у вас есть вопросы, предложения или замечания, свяжитесь со мной - `klokovsergey@gmail.com`!

