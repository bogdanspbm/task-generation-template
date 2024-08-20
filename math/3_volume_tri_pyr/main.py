import random
import json
import os
import shutil
from lxml import etree
from image_gen import generate_svg
from generate_html_files import generate_html_files
from itertools import combinations



def generate_volume_tasks(limit=1000):
    tasks = []

    base_area_range = list(range(1, 101))
    height_range = list(range(1, 101))

    base_labels_sets = [
        ["A", "B", "C"], ["X", "Y", "Z"], ["L", "M", "N"], ["P", "Q", "R"], ["G", "H", "I"]
    ]

    task_patterns = [
        "Найдите объём многогранника, вершинами которого являются вершины {vertices} правильной треугольной призмы {base_labels}, площадь основания которой равна {base_area}, а боковое ребро равно {height}.",
        "Вычислите объём многогранника, образованного вершинами {vertices} правильной треугольной призмы {base_labels}, с площадью основания {base_area} и высотой {height}.",
        "Определите объём многогранника с вершинами {vertices} правильной треугольной призмы {base_labels}, если площадь основания равна {base_area}, а боковое ребро равно {height}.",
        "Рассчитайте объём многогранника, имеющего вершины {vertices} правильной треугольной призмы {base_labels}, при площади основания {base_area} и высоте {height}.",
        "Найдите объём многогранника, образованного вершинами {vertices} правильной треугольной призмы {base_labels}, при площади основания {base_area} и боковом ребре {height}."
    ]

    task_patterns_html = [
        "<p>Найдите объём многогранника, вершинами которого являются вершины {vertices} правильной треугольной призмы {base_labels}, площадь основания которой равна {base_area}, а боковое ребро равно {height}.</p>",
        "<p>Вычислите объём многогранника, образованного вершинами {vertices} правильной треугольной призмы {base_labels}, с площадью основания {base_area} и высотой {height}.</p>",
        "<p>Определите объём многогранника с вершинами {vertices} правильной треугольной призмы {base_labels}, если площадь основания равна {base_area}, а боковое ребро равно {height}.</p>",
        "<p>Рассчитайте объём многогранника, имеющего вершины {vertices} правильной треугольной призмы {base_labels}, при площади основания {base_area} и высоте {height}.</p>",
        "<p>Найдите объём многогранника, образованного вершинами {vertices} правильной треугольной призмы {base_labels}, при площади основания {base_area} и боковом ребре {height}.</p>"
    ]

    for base_area in base_area_range:
        for height in height_range:
            volume = base_area * height
            if volume % 3 != 0:  # Проверка, что объем является натуральным числом
                continue
            volume = volume // 3

            base_labels = random.choice(base_labels_sets)
            top_labels = [label + "1" for label in base_labels]

            if random.choice([True, False]):
                random_top_label = random.choice(top_labels)
                vertex_set = [base_labels[0], base_labels[1], base_labels[2], random_top_label]
            else:
                random_base_label = random.choice(base_labels)
                vertex_set = [top_labels[0], top_labels[1], top_labels[2], random_base_label]

            formatted_base_labels = "".join(base_labels) + "".join(top_labels)

            task_text = random.choice(task_patterns).format(vertices=", ".join(vertex_set), base_labels=formatted_base_labels, base_area=base_area, height=height)
            task_html = random.choice(task_patterns_html).format(vertices=", ".join(vertex_set), base_labels=formatted_base_labels, base_area=base_area, height=height)

            uid = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10))

            connections = set(combinations(vertex_set, 2))

            svg_content = generate_svg(base_labels, top_labels, connections)

            task = {
                "task_num": 3,
                "task_subject": "math",
                "task_types": ["7.3 Многогранники"],
                "task_images": [f"{uid}.svg"],
                "task_images_svg": [svg_content],
                "uid": uid,
                "task_text": task_text,
                "task_html": task_html,
                "task_solution": f"Объём многогранника вычисляется по формуле V = S * h / 3. Подставляем значения: V = {base_area} * {height} / 3 = {volume}.",
                "task_hints": ["Используйте формулу объёма пирамиды V = S * h / 3."],
                "answer_type": "short",
                "task_group_key": "volume_tri_pyr",
                "task_group_label": "Объем пирамиты в треугольной трапеции",
                "difficulty": "medium",
                "fipi_uid": "BE03FA",
                "task_answer": str(volume),
                "base_area": base_area,
                "height": height,
                "vertices": ", ".join(vertex_set),
                "base_labels": formatted_base_labels
            }

            tasks.append(task)
            if len(tasks) >= limit:
                return tasks

    return tasks

def select_tasks(tasks, limit=40):
    random.shuffle(tasks)
    return tasks[:limit]


# Генерация уникальных задач
generated_tasks = generate_volume_tasks(limit=1000)

# Выборка задач
selected_tasks = select_tasks(generated_tasks, limit=40)

# Сохранение выбранных задач в JSON
with open("tasks.json", "w", encoding="utf-8") as file:
    json.dump(selected_tasks, file, ensure_ascii=False, indent=4)

generate_html_files(selected_tasks)

# Печать нескольких примеров задач
for task in selected_tasks[:5]:
    print(json.dumps(task, ensure_ascii=False, indent=4))
    print("<br>")
