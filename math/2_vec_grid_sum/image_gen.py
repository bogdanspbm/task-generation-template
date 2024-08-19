from lxml import etree

def generate_svg(grid_x, grid_y, vectors, output_file):
    scale = 100  # масштабирование координат

    # Создаем корневой элемент SVG с инвертированным viewBox
    svg = etree.Element("svg", width="500", height="500", viewBox=f"{grid_x[0] * scale} {-grid_y[1] * scale} {scale * (grid_x[1] - grid_x[0])} {scale * (grid_y[1] - grid_y[0])}", xmlns="http://www.w3.org/2000/svg")

    # Создаем элементы сетки
    for x in range(grid_x[0], grid_x[1] + 1):
        line = etree.Element("line", x1=str(x * scale), y1=str(-grid_y[0] * scale), x2=str(x * scale), y2=str(-grid_y[1] * scale), stroke="#464646", **{"stroke-width": "1"})
        svg.append(line)
    for y in range(grid_y[0], grid_y[1] + 1):
        line = etree.Element("line", x1=str(grid_x[0] * scale), y1=str(-y * scale), x2=str(grid_x[1] * scale), y2=str(-y * scale), stroke="#464646", **{"stroke-width": "1"})
        svg.append(line)

    # Создаем оси
    x_axis = etree.Element("line", x1=str(grid_x[0] * scale), y1="0", x2=str(grid_x[1] * scale), y2="0", stroke="black", **{"stroke-width": "2"})
    y_axis = etree.Element("line", x1="0", y1=str(-grid_y[0] * scale), x2="0", y2=str(-grid_y[1] * scale), stroke="black", **{"stroke-width": "2"})
    svg.append(x_axis)
    svg.append(y_axis)

    # Добавляем метки для осей
    # Метка для начала координат
    zero_text = etree.Element(
        "text",
        x="-42",
        y="52",
        fill="#242424",
        **{"font-family": "Arial"},
        **{"font-weight": "600"},
        **{"font-size": "48"}
    )
    zero_text.text = "0"
    svg.append(zero_text)

    # Метка для координаты 1 на оси абсцисс
    x1_text = etree.Element(
        "text",
        x=str(scale - 12),
        y="52",
        fill="#242424",
        **{"font-family": "Arial"},
        **{"font-weight": "600"},
        **{"font-size": "48"}
    )
    x1_text.text = "1"
    svg.append(x1_text)

    # Метка для координаты 1 на оси ординат
    y1_text = etree.Element(
        "text",
        x="-42",
        y=str(-scale + 20),
        fill="#242424",
        **{"font-family": "Arial"},
        **{"font-weight": "600"},
        **{"font-size": "48"}
    )
    y1_text.text = "1"
    svg.append(y1_text)

    # Создаем маркер для стрелок
    defs = etree.Element("defs")
    marker = etree.Element("marker", id="arrow", markerWidth="5", markerHeight="5", refX="4", refY="2.5", orient="auto")
    path = etree.Element("path", d="M0,0 L5,2.5 L0,5 Z", fill="#9254de")
    marker.append(path)
    defs.append(marker)
    svg.append(defs)

    # Создаем векторы
    for vector in vectors:
        start_x, start_y, end_x, end_y, label = vector
        line = etree.Element(
            "line",
            x1=str(start_x * scale),
            y1=str(-start_y * scale),
            x2=str(end_x * scale),
            y2=str(-end_y * scale),
            stroke="#9254de",
            **{"stroke-width": "8"},
            **{"marker-end": "url(#arrow)"},
            **{"aria-description": label}
        )
        svg.append(line)

        # Определяем середину вектора
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # Вычисляем перпендикулярный вектор
        dx = end_x - start_x
        dy = end_y - start_y
        length = (dx**2 + dy**2)**0.5
        if length == 0:
            continue
        perp_dx = -dy / length
        perp_dy = dx / length

        # Определяем смещение для метки
        offset = 0.32  # расстояние в масштабных единицах
        label_x = mid_x + perp_dx * offset
        label_y = mid_y + perp_dy * offset

        # Добавляем метки для векторов
        text = etree.Element(
            "text",
            x=str(label_x * scale - 28),
            y=str(-label_y * scale + 15),
            fill="#242424",
            **{"font-family": "Arial"},
            **{"font-weight": "600"},
            **{"font-size": "48"}
        )
        text.text = label
        svg.append(text)

        # Добавляем стрелочку над меткой вектора
        arrow_line = etree.Element(
            "line",
            x1=str(label_x * scale - 30),
            y1=str(-label_y * scale - 25),
            x2=str(label_x * scale),
            y2=str(-label_y * scale - 25),
            stroke="#242424",
            **{"stroke-width": "3"}
        )
        svg.append(arrow_line)

        arrow_head_left = etree.Element(
            "line",
            x1=str(label_x * scale),
            y1=str(-label_y * scale - 24),
            x2=str(label_x * scale - 5),
            y2=str(-label_y * scale - 30),
            stroke="#242424",
            **{"stroke-width": "3"}
        )
        svg.append(arrow_head_left)

        arrow_head_right = etree.Element(
            "line",
            x1=str(label_x * scale),
            y1=str(-label_y * scale - 26),
            x2=str(label_x * scale - 5),
            y2=str(-label_y * scale - 20),
            stroke="#242424",
            **{"stroke-width": "3"}
        )
        svg.append(arrow_head_right)

    # Запись в файл
    tree = etree.ElementTree(svg)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return etree.tostring(svg, pretty_print=True).decode('utf-8')

