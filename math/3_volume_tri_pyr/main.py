import random
import json
import os
import shutil
from lxml import etree
from itertools import combinations

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def generate_svg(base_labels, top_labels, connections):
    points = {
        base_labels[0]: (50, 150), base_labels[1]: (190, 140), base_labels[2]: (70, 220),
        top_labels[0]: (50, 50), top_labels[1]: (190, 40), top_labels[2]: (70, 120)
    }

    label_offsets = {
        base_labels[0]: (-12, 8), base_labels[1]: (8, 8), base_labels[2]: (-12, 8),
        top_labels[0]: (-12, -8), top_labels[1]: (8, -8), top_labels[2]: (-12, -8)
    }

    svg = etree.Element('svg', xmlns="http://www.w3.org/2000/svg", width="250", height="250",  **{"viewBox": "0 0 250 250"})

    dashed_connections = [(base_labels[0], top_labels[0]), (base_labels[1], top_labels[1]), (base_labels[2], top_labels[2])]
    drawn_edges = set()

    for start, end in dashed_connections:
        if start in points and end in points:
            etree.SubElement(svg, 'line', x1=str(points[start][0]), y1=str(points[start][1]),
                             x2=str(points[end][0]), y2=str(points[end][1]),
                             stroke="#646464", stroke_dasharray="5,5")
            drawn_edges.add((start, end))
            drawn_edges.add((end, start))

    for start, end in [(base_labels[0], base_labels[1]), (base_labels[1], base_labels[2]),
                       (base_labels[2], base_labels[0]),
                       (top_labels[0], top_labels[1]), (top_labels[1], top_labels[2]), (top_labels[2], top_labels[0])]:
        if (start, end) not in drawn_edges and (end, start) not in drawn_edges:
            etree.SubElement(svg, 'line', x1=str(points[start][0]), y1=str(points[start][1]),
                             x2=str(points[end][0]), y2=str(points[end][1]),
                             stroke="#646464")

    def is_triangle(p1, p2, p3):
        return ((p1, p2) in connections or (p2, p1) in connections) and \
            ((p2, p3) in connections or (p3, p2) in connections) and \
            ((p3, p1) in connections or (p1, p3) in connections)

    triangles = []
    for combo in combinations(points.keys(), 3):
        if is_triangle(combo[0], combo[1], combo[2]):
            triangles.append(combo)

    for triangle in triangles:
        polygon_points = " ".join([f"{points[point][0]},{points[point][1]}" for point in triangle])
        etree.SubElement(svg, 'polygon', points=polygon_points, fill="#9254de", fill_opacity="0.05")

    for connection in connections:
        start, end = connection
        if start in points and end in points:
            etree.SubElement(svg, 'line', x1=str(points[start][0]), y1=str(points[start][1]),
                             x2=str(points[end][0]), y2=str(points[end][1]), stroke="#9254de", stroke_width="2")

    for label, point in points.items():
        offset_x, offset_y = label_offsets.get(label, (0, 0))
        text = etree.SubElement(svg, 'text', x=str(point[0] + offset_x), y=str(point[1] + offset_y), fill="#242424",
                                font_family="Arial", font_weight="bold", font_size="14")
        text.text = label

    return etree.tostring(svg, pretty_print=True).decode().replace('stroke_dasharray', 'stroke-dasharray').replace(
        "stroke_width", "stroke-width").replace('font_family', 'font-family').replace("font_size", "font-size").replace(
        "font_weight", "font-weight").replace("fill_opacity", "fill-opacity")

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
            svg_filename = f"images/{uid}.svg"
            with open(svg_filename, "w") as file:
                file.write(svg_content)

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

# Очистка папок перед генерацией
clear_directory('images')
clear_directory('htmls')

# Генерация уникальных задач
generated_tasks = generate_volume_tasks(limit=1000)

# Выборка задач
selected_tasks = select_tasks(generated_tasks, limit=40)

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
for task in selected_tasks[:5]:
    print(json.dumps(task, ensure_ascii=False, indent=4))
    print("<br>")
