import os

def generate_html_files(tasks, output_folder='html'):
    # Удаляем все файлы в папке html
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        for file_name in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    # Генерируем HTML файлы
    for i, task in enumerate(tasks):
        task_html = task['task_html']
        task_images_svg = task['task_images_svg'][0]  # Берем первую картинку, если их несколько

        # Формируем ссылки на предыдущую и следующую задачи
        prev_link = ''
        next_link = ''
        if i > 0:
            prev_uid = tasks[i-1]['uid']
            prev_link = f'<a href="{prev_uid}.html">Previous Task</a>'
        if i < len(tasks) - 1:
            next_uid = tasks[i+1]['uid']
            next_link = f'<a href="{next_uid}.html">Next Task</a>'

        # Создаем HTML-контент
        html_content = f'''
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Task {task["uid"]}</title>
        </head>
        <body>
            {task_html}
            <div>{task_images_svg}</div>
            <div>
                {prev_link} | {next_link}
            </div>
        </body>
        </html>
        '''

        # Записываем HTML файл
        file_name = os.path.join(output_folder, f'{task["uid"]}.html')
        with open(file_name, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

