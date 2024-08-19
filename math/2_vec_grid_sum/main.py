import random
import json
import math
import os
import shutil

from image_gen import generate_svg  # Убедитесь, что у вас есть эта функция в image_gen.py

# Функция для очистки папок
def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def on_segment(p, q, r):
    """Проверка, лежит ли точка q на отрезке pr"""
    if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
        return True
    return False

def orientation(p, q, r):
    """Вычисление ориентации для упорядочения троек (p, q, r).
    Функция возвращает следующие значения:
    0 -> p, q и r коллинеарны
    1 -> часовая стрелка
    2 -> против часовой стрелки
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def vectors_intersect(p1, q1, p2, q2):
    """Функция для проверки пересечения двух отрезков (p1, q1) и (p2, q2)"""
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def vector_length(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def are_parallel(a1, a2, b1, b2):
    return a1 * b2 == a2 * b1

def min_distance_between_vectors(v1, v2):
    """Функция для вычисления минимального расстояния между концами двух векторов"""
    (x1, y1, x2, y2) = v1
    (x3, y3, x4, y4) = v2
    distances = [
        vector_length(x1, y1, x3, y3),
        vector_length(x1, y1, x4, y4),
        vector_length(x2, y2, x3, y3),
        vector_length(x2, y2, x4, y4)
    ]
    return min(distances)

def generate_unique_tasks(limit=1000):
    tasks = []
    unique_coordinates = set()
    patterns = [
        "На координатной плоскости изображены векторы a→ и b→, координатами которых являются целые числа. Найдите длину вектора {k1}a→ + {k2}b→.",
        "Векторы a→ и b→ заданы координатами. Найдите длину вектора {k1}a→ + {k2}b→.",
        "Определите длину вектора {k1}a→ + {k2}b→, если координаты векторов a→ и b→ заданы.",
        "Найдите длину вектора {k1}a→ + {k2}b→, если даны координаты векторов a→ и b→.",
        "Векторы a→ и b→ заданы своими координатами. Найдите длину вектора {k1}a→ + {k2}b→."
    ]

    patternsHTML = [
        "<p>На координатной плоскости изображены векторы <math><mover><mi>a</mi><mo>&rarr;</mo></mover></math> и <math><mover><mi>b</mi><mo>&rarr;</mo></mover></math> , координатами которых являются целые числа. Найдите длину вектора <math><mover><mi>{k1}a</mi><mo>&rarr;</mo></mover></math>  + {k2}<math><mover><mi>b</mi><mo>&rarr;</mo></mover>.</math></p>",
        "<p>Векторы <math><mover><mi>a</mi><mo>&rarr;</mo></mover></math> и <math><mover><mi>b</mi><mo>&rarr;</mo></mover></math> заданы координатами. Найдите длину вектора <math><mover><mi>{k1}a</mi><mo>&rarr;</mo></mover></math>+ {k2}<math><mover><mi>b</mi><mo>&rarr;</mo></mover></math>.</p></body>",
        "<p>Определите длину вектора <math><mover><mi>{k1}a</mi><mo>&rarr;</mo></mover></math> + {k2}<math><mover><mi>b</mi><mo>&rarr;</mo></mover></math>, если координаты векторов <math><mover><mi>a</mi><mo>&rarr;</mo></mover></math> и <math><mover><mi>b</mi><mo>&rarr;</mo></mover></math> заданы.</p>",
        "<p>Найдите длину вектора <math><mover><mi>{k1}a</mi><mo>&rarr;</mo></mover></math> + {k2}<math><mover><mi>b</mi><mo>&rarr;</mo></mover></math>, если даны координаты векторов <math><mover><mi>a</mi><mo>&rarr;</mo></mover></math> и <math><mover><mi>b</mi><mo>&rarr;</mo></mover></math>.</p>",
        "<p>Векторы <math><mover><mi>a</mi><mo>&rarr;</mo></mover></math> и <math><mover><mi>b</mi><mo>&rarr;</mo></mover></math> заданы своими координатами. Найдите длину вектора <math><mover><mi>{k1}a</mi><mo>&rarr;</mo></mover></math> + {k2}<math><mover><mi>b</mi><mo>&rarr;</mo></mover></math>.</p></body>"
    ]

    while len(tasks) < limit:
        x1, y1 = random.randint(-1, 7), random.randint(-1, 7)
        x2, y2 = random.randint(-1, 7), random.randint(-1, 7)
        x3, y3 = random.randint(-1, 7), random.randint(-1, 7)
        x4, y4 = random.randint(-1, 7), random.randint(-1, 7)

        if (x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4):
            continue

        if (x1 == x3 and y1 == y3) or (x2 == x4 and y2 == y4):
            continue

        if vectors_intersect((x1, y1), (x2, y2), (x3, y3), (x4, y4)):
            continue

        a1, a2 = x2 - x1, y2 - y1
        b1, b2 = x4 - x3, y4 - y3

        if are_parallel(a1, a2, b1, b2):
            continue

        len_a = vector_length(x1, y1, x2, y2)
        len_b = vector_length(x3, y3, x4, y4)

        if len_a < 2 or len_b < 2 or len_a == len_b:
            continue

        if min_distance_between_vectors((x1, y1, x2, y2), (x3, y3, x4, y4)) < 2:
            continue

        coordinates = (x1, y1, x2, y2, x3, y3, x4, y4)
        if coordinates in unique_coordinates:
            continue

        unique_coordinates.add(coordinates)

        k1, k2 = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

        vector_sum_x = k1 * a1 + k2 * b1
        vector_sum_y = k1 * a2 + k2 * b2

        sum_vector_length = math.sqrt(vector_sum_x ** 2 + vector_sum_y ** 2)

        if not sum_vector_length.is_integer():
            continue

        # Проверка, что вектор не выходит за сетку
        if not (-2 <= vector_sum_x <= 8 and -2 <= vector_sum_y <= 8):
            continue

        # Выбираем случайный паттерн
        pattern = random.choice(patterns)
        patternHTML = random.choice(patternsHTML)

        task_text = pattern.format(k1=k1, k2=k2)
        task_html = patternHTML.format(k1=k1, k2=k2)

        # Определение сложности
        difficulty = "easy" if sum_vector_length <= 10 else ("medium" if sum_vector_length <= 20 else "hard")

        # Генерация UID
        uid = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10))

        # Заполнение JSON
        task = {
            "task_num": 2,
            "task_subject": "math",
            "task_types": ["7.5 Координаты и векторы"],
            "task_images": [f"{uid}.svg"],
            "uid": uid,
            "task_text": task_text,
            "task_html": task_html,
            "task_solution": f"Длина вектора {k1}a→ + {k2}b→ вычисляется по формуле √(({k1}a1 + {k2}b1)^2 + ({k1}a2 + {k2}b2)^2). Подставляем значения: √(({vector_sum_x})^2 + ({vector_sum_y})^2) = {sum_vector_length}.",
            "task_hints": ["Используйте формулу длины вектора sqrt(x^2 + y^2)."],
            "answer_type": "short",
            "task_group_key": "vec_grid_sum",
            "difficulty": difficulty,
            "fipi_uid": "579B74",
            "answer": str(sum_vector_length),
            "coordinates": (x1, y1, x2, y2, x3, y3, x4, y4)  # Сохраняем координаты для генерации SVG позже
        }

        tasks.append(task)

    return tasks

def select_tasks(tasks, limit=40):
    easy_tasks = [task for task in tasks if task['difficulty'] == 'easy']
    medium_tasks = [task for task in tasks if task['difficulty'] == 'medium']
    hard_tasks = [task for task in tasks if task['difficulty'] == 'hard']

    random.shuffle(easy_tasks)
    random.shuffle(medium_tasks)
    random.shuffle(hard_tasks)

    selected_tasks = (
            easy_tasks[:int(limit * 0.5)] +
            medium_tasks[:int(limit * 0.3)] +
            hard_tasks[:int(limit * 0.2)]
    )

    random.shuffle(selected_tasks)

    return selected_tasks

# Очистка папок перед генерацией
clear_directory('images')
clear_directory('htmls')

# Генерация уникальных задач
generated_tasks = generate_unique_tasks(limit=1000)

# Выборка задач в нужных пропорциях
selected_tasks = select_tasks(generated_tasks, limit=40)

# Генерация SVG для выбранных задач и сохранение их в папку images
for task in selected_tasks:
    x1, y1, x2, y2, x3, y3, x4, y4 = task["coordinates"]
    vectors = [(x1, y1, x2, y2, "a"), (x3, y3, x4, y4, "b")]
    svg_string = generate_svg([-2, 8], [-2, 8], vectors, f"images/{task['uid']}.svg")
    task["task_images_svg"] = [svg_string]

# Сохранение выбранных задач в JSON
with open("tasks.json", "w", encoding="utf-8") as file:
    json.dump(selected_tasks, file, ensure_ascii=False, indent=4)

# Генерация HTML файлов для выбранных задач
for i, task in enumerate(selected_tasks):
    prev_uid = selected_tasks[i-1]['uid'] if i > 0 else selected_tasks[-1]['uid']
    next_uid = selected_tasks[i+1]['uid'] if i < len(selected_tasks)-1 else selected_tasks[0]['uid']
    html_content = f"""
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Task {i+1}</title>
    </head>
    <body>
        {task['task_html']}
        <br>
        <img src="../images/{task['task_images'][0]}" alt="task image">
        <br>
        <a href="{prev_uid}.html">Previous Task</a>
        <a href="{next_uid}.html">Next Task</a>
    </body>
    </html>
    """
    html_filename = f"htmls/{task['uid']}.html"
    with open(html_filename, "w", encoding="utf-8") as file:
        file.write(html_content)

# Печать нескольких примеров задач
for task in selected_tasks[:5]:  # Выведем первые 5 задач для примера
    print(json.dumps(task, ensure_ascii=False, indent=4))
    print("<br>")
