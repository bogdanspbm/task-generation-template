# Генератор задач

Данный репозиторий содержит пример из нескольких генераторов задач, а также JS-скрипт для удобного дебага и проверки созданных задач.

## Генераторы

Для генерации задач используется Python. Обычно код занимает от 150 до 200 строк, но все зависит от количества переиспользования функций, которые могут повторяться из раза в раз, в новых задачах.

Так в примере /math/1_circle_task_a - функции save_tasks_to_json, generate_html_files, generate_uid, generate_random_letters - можно переиспользовать во всех других задачах. В таком случае размер скрипта, может быть меньше 100 строк. 

## Тестирования 

Для предварительного дебага можно использовать метод generate_html_files, который создает множество HTML файлов для проверки задачи. Для более детального дебага, с целью проверить, что все необходимые поля присутсвуют в JSON и правильно читаются, используйте файл /import/index.html. Подайте сгенерированный tasks.json файл в форму и проверьте что получилось.
