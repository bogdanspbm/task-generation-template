import random
import json
from image_gen import generate_svg_string
from generate_html_files import generate_html_files
import uuid

def generate_uid():
    """Генерация уникального идентификатора из 10 случайных заглавных букв или цифр."""
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

def generate_random_letters():
    """Генерация 5 уникальных случайных заглавных букв из английского алфавита."""
    return random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 5)

def generateImage(angle_acb, point_labels):
    startAngle = random.randint(0, 360)

    # Используем случайные буквы с маппингом на 'O', 'A', 'B', 'C', 'D'
    points = [
        (point_labels['O']),  # Центр окружности
        (point_labels['A'], startAngle + angle_acb, 5),  # Точка на окружности
        (point_labels['B'], startAngle, 5),  # Точка на окружности
        (point_labels['C'], startAngle + angle_acb + 180, 5),  # Точка на окружности
        (point_labels['D'], startAngle + 180, 5)  # Точка на окружности
    ]

    segments = [
        (point_labels['C'], point_labels['A']),
        (point_labels['C'], point_labels['B']),
        (point_labels['B'], point_labels['D'])
    ]

    arcs = [(point_labels['A'], point_labels['C'], point_labels['B']),
            (point_labels['A'], point_labels['O'], point_labels['D'])]

    return generate_svg_string(points, segments, arcs)

def generate_task():
    """Генерация одной задачи."""
    angle_acb = random.randint(30, 60)  # Случайный угол от 30 до 60 градусов
    angle_aod = 180 - 2 * angle_acb

    # Генерация случайных букв
    random_letters = generate_random_letters()

    # Маппинг случайных букв на 'O', 'A', 'B', 'C', 'D'
    point_labels = {key: value for key, value in zip(['O', 'A', 'B', 'C', 'D'], random_letters)}

    task_text = (
        f"Отрезки {point_labels['A']}{point_labels['C']} и {point_labels['B']}{point_labels['D']} — диаметры окружности с центром {point_labels['O']}. "
        f"Угол {point_labels['A']}{point_labels['C']}{point_labels['B']} равен {angle_acb}°. Найдите величину угла {point_labels['A']}{point_labels['O']}{point_labels['D']}. Ответ дайте в градусах."
    )

    # Пресеты для HTML условия задачи
    html_presets = [
        f"<p>В окружности с центром в точке {point_labels['O']} отрезки {point_labels['A']}{point_labels['C']} и {point_labels['B']}{point_labels['D']} являются диаметрами. Угол <math><mi>{point_labels['A']}{point_labels['C']}{point_labels['B']}</mi></math> равен {angle_acb}°. Найдите угол <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math>. Ответ дайте в градусах.</p>",
        f"<p>Диаметры {point_labels['A']}{point_labels['C']} и {point_labels['B']}{point_labels['D']} пересекаются в центре окружности {point_labels['O']}. Вписанный угол <math><mi>{point_labels['A']}{point_labels['C']}{point_labels['B']}</mi></math> составляет {angle_acb}°. Определите величину центрального угла <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math>. Ответ дайте в градусах.</p>",
        f"<p>В окружности с центром {point_labels['O']} проведены диаметры {point_labels['A']}{point_labels['C']} и {point_labels['B']}{point_labels['D']}. Угол <math><mi>{point_labels['A']}{point_labels['C']}{point_labels['B']}</mi></math>, который является вписанным, равен {angle_acb}°. Найдите угол <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math>, который является центральным. Ответ дайте в градусах.</p>",
        f"<p>Окружность с центром в точке {point_labels['O']} имеет диаметры {point_labels['A']}{point_labels['C']} и {point_labels['B']}{point_labels['D']}. Величина угла <math><mi>{point_labels['A']}{point_labels['C']}{point_labels['B']}</mi></math> составляет {angle_acb}°. Определите величину угла <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math>. Ответ в градусах.</p>",
        f"<p>В окружности с центром в точке {point_labels['O']} отрезки {point_labels['A']}{point_labels['C']} и {point_labels['B']}{point_labels['D']} — это диаметры. Угол <math><mi>{point_labels['A']}{point_labels['C']}{point_labels['B']}</mi></math> равен {angle_acb}°. Найдите угол <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math>. Дайте ответ в градусах.</p>"
    ]

    task_solution = f"<p>Угол <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math> является смежным для угла <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['B']}</mi></math>. В свою очередь угол <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['B']}</mi></math> является центральным углом, опирающимся на туже дугу, что и вписанный угол <math><mi>{point_labels['A']}{point_labels['B']}{point_labels['C']}</mi></math>, а значет он в два раза больше него: <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['B']}</mi></math>=<math><mi>{angle_acb}*2</mi></math>={angle_acb*2}. Теперь остается найти угол <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math> как смежный углу <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['B']}</mi></math>. <math><mi>{point_labels['A']}{point_labels['O']}{point_labels['D']}</mi></math> = <math><mi>180-{angle_acb * 2}</mi></math>={180 - angle_acb * 2}</p>"

    # Выбор случайного пресета
    task_html = random.choice(html_presets)

    task_answer = str(angle_aod)

    hints = [
        f"<p>Центральный угол равен удвоенному вписанному углу, опирающемуся на ту же дугу.</p>",
        f"<p>Используйте свойство, смежных углов. Сумма смежных углов - равняется 180 градусам.</p>",
     ]

    def evaluate_difficulty(angle_acb):
        if angle_acb <= 45:
            return "easy"
        else:
            return "medium"

    difficulty = evaluate_difficulty(angle_acb)

    return {
        "uid": generate_uid(),
        "task_subject": "math",
        "task_text": task_text,
        "task_html": task_html,
        "task_solution": task_solution,
        "task_answer": task_answer,
        "task_images_svg": [generateImage(angle_acb, point_labels)],
        "task_hints": hints,
        "task_group_label": "Поиск центральногго угла, через вписанный и смежный",
        "task_types": ["7.1 Фигуры на плоскости"],
        "task_group_key": "circle_task_a",
        "answer_type": "short",
        "task_num": 1,
        "fipi_uid": "80A34C",
        "difficulty": difficulty
    }

def generate_tasks(num_tasks=1000):
    tasks = [generate_task() for _ in range(num_tasks)]
    return tasks

def save_tasks_to_json(tasks, filename='tasks.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# Генерация 1000 задач
all_tasks = generate_tasks(1000)

# Выбор случайных 40 задач
random_tasks = random.sample(all_tasks, 40)

# Сохранение в файл tasks.json
save_tasks_to_json(random_tasks)
generate_html_files(random_tasks, "htmls")

print("40 задач успешно сгенерированы и сохранены в файл tasks.json")
