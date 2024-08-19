import random
import math
import string
import json
from collections import defaultdict


def generate_uid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)).upper()


def generate_all_power_equations_tasks():
    tasks = []

    # Варианты формулировок задач
    task_text_variants = [
        "Решите уравнение",
        "Найдите корень уравнения",
        "Определите значение x для уравнения"
    ]

    for a in range(-50, 51):
        for b in range(1, 51):

            if a == 0:
                continue

            if b != 1:
                ab_ratio = a / b
            else:
                ab_ratio = a


            for c in range(-10, 11):
                if c == 0:
                    continue

                for d in range(-10, 11):
                    if d == 0:
                        continue

                    for e in range(-100, 101):

                        if e == 0 or e == 1 or e == -1:
                            continue

                        cx_d_variants = [(c, d), (d, c), (-c, -d)]
                        for cx, dx in cx_d_variants:
                            if cx < 0 and dx < 0:
                                cx, dx = -cx, -dx

                            if ab_ratio.is_integer():
                                equation = f"{int(ab_ratio)}^({cx}x {"+" if dx > 0 else "-"} {abs(dx)}) = {e}"
                            else:
                                equation = f"({a}/{b})^({cx}x {"+" if dx > 0 else "-"} {abs(dx)}) = {e}"

                            try:
                                x_value = (math.log(e) / math.log(ab_ratio) - dx) / cx
                                if x_value.is_integer():
                                    x_value = int(x_value)
                                    stepen = abs(cx * x_value + dx)

                                    difficulty = "hard"

                                    if stepen == 1 or stepen == 0:
                                        continue

                                    if stepen == 2 or stepen == 3 or stepen == 1 or stepen == 0:
                                        if abs(x_value) < 10:
                                            difficulty = "easy"
                                        else:
                                            difficulty = "medium"
                                    elif stepen == 4 or stepen == 5:
                                        if abs(x_value) < 10:
                                            difficulty = "medium"
                                        else:
                                            difficulty = "hard"

                                    # Выбор случайной формулировки задачи
                                    task_text = random.choice(task_text_variants)

                                    # Формирование HTML задачи
                                    if ab_ratio.is_integer():
                                        task_html = f"{task_text}: <math><msup><mn>{int(ab_ratio)}</mn><mrow><mi>{cx}x {"+" if dx > 0 else "-"} {abs(dx)}</mi></mrow></msup><ms>= </ms><mn>{e}</mn></math>."
                                        task_solution =  f"Для решения уравнения {equation} применим логарифм: log_{int(ab_ratio)}({e}) = {cx}x {'+' if dx > 0 else '-'} {abs(dx)}. Решая полученное уравнение, получаем x = (log_{ab_ratio}({e}) {'-' if dx > 0 else '+'} {abs(dx)}) / {cx} = {x_value}."
                                    else:
                                        task_html = f"{task_text}: <math><msup><mrow><ms>(</ms><mfrac><mn>{a}</mn><mn>{b}</mn></mfrac><ms>)</ms></mrow><mrow><mi>{cx}x {"+" if dx > 0 else "-"} {abs(dx)}</mi></mrow></msup><ms>= </ms><mn>{e}</mn></math>."
                                        task_solution =  f"Для решения уравнения {equation} применим логарифм: log_({a}/{b})({e}) = {cx}x {'+' if dx > 0 else '-'} {abs(dx)}. Решая полученное уравнение, получаем x = (log_{ab_ratio}({e}) {'-' if dx > 0 else '+'} {abs(dx)}) / {cx} = {x_value}."

                                    task = {
                                        "task_num": 6,
                                        "task_subject": "math",
                                        "task_types": ["2.1 Целые и дробно-рациональные уравнения",
                                                       "2.4 Показательные и логарифмические уравнения"],
                                        "task_images": [],
                                        "fipi_uid": "4CBD4E",
                                        "task_text": f"{task_text}: {equation}.",
                                        "task_answer": str(x_value),
                                        "task_html": '<p>' + task_html + "</p>",
                                        "task_solution": task_solution,
                                        "task_hints": [
                                            "Используйте логарифмирование для решения показательного уравнения."],
                                        "uid": generate_uid(),
                                        "answer_type": "short",
                                        'task_group_key': "stepen_equation_a",
                                        'task_group_label': "Простейшее степенное уравнение",
                                        "difficulty": difficulty
                                    }

                                    tasks.append(task)

                            except ValueError:
                                continue
                            except ZeroDivisionError:
                                continue

    return tasks


def filter_tasks_by_difficulty(tasks):
    difficulty_buckets = defaultdict(list)
    for task in tasks:
        difficulty_buckets[task['difficulty']].append(task)
    return difficulty_buckets


def sample_tasks(difficulty_buckets, easy_ratio=5, medium_ratio=3, hard_ratio=2):
    easy_tasks = difficulty_buckets['easy']
    medium_tasks = difficulty_buckets['medium']
    hard_tasks = difficulty_buckets['hard']

    print(len(easy_tasks))
    print(len(medium_tasks))
    print(len(hard_tasks))

    total_tasks = 50

    sampled_tasks = []

    sampled_tasks.extend(random.sample(easy_tasks, int(total_tasks * easy_ratio / 10)))
    sampled_tasks.extend(random.sample(medium_tasks, int(total_tasks * medium_ratio / 10)))
    sampled_tasks.extend(random.sample(hard_tasks, int(total_tasks * hard_ratio / 10)))

    return sampled_tasks


# Сохранение задач в файл JSON
def save_tasks_to_json(tasks, filename='tasks.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


# Основная функция для генерации задач, сортировки их и сохранения в файл JSON
def main():
    print("Generating power equation tasks...")
    all_tasks = generate_all_power_equations_tasks()
    print(f"Total tasks generated: {len(all_tasks)}")

    # Фильтрация задач по сложности
    tasks_by_difficulty = filter_tasks_by_difficulty(all_tasks)

    # Выборка задач с заданным распределением 5:3:2
    sampled_tasks = sample_tasks(tasks_by_difficulty)
    print(f"Total tasks sampled: {len(sampled_tasks)}")

    # Сохранение задач в файл JSON
    save_tasks_to_json(sampled_tasks)
    print("Sampled tasks saved to tasks.json.")


if __name__ == "__main__":
    main()
