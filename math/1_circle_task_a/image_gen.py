from lxml import etree
import math


def getVectorFromPoints(pointA, pointB):
    return (pointA[0] - pointB[0], pointA[1] - pointB[1])

def sumVecs(pointA, pointB):
    return (pointA[0] + pointB[0], pointA[1] + pointB[1])

def scaleVector(vector, scale):
   return (vector[0] * scale, vector[1] * scale)

def getVectorNormal(pointA):
    return math.sqrt(pointA[1] ** 2 + pointA[0] ** 2)

def normalizeVec(vector, scale = 1):
    return (vector[0] * scale / getVectorNormal(vector), vector[1] * scale / getVectorNormal(vector))

def generate_svg_string(points, segments, arcs):
    # Create the SVG root element
    svg = etree.Element('svg', xmlns="http://www.w3.org/2000/svg", width="500", height="500", **{"viewBox": "0 0 500 500"})

    labelOffset = 15
    dotRadius = "2"

    pointsCoords = {};

    # Draw a circle
    center_point = next((point for point in points if len(point) == 1), None)
    if center_point:
        circle = etree.SubElement(svg, 'circle', cx="250", cy="250", r="200", stroke="#242424", fill="none", **{"stroke-width": "2px"})
        pointsCoords[center_point] = (250,250)
        etree.SubElement(svg, 'circle', cx=str(250), cy=str(250), r=dotRadius, fill="#242424")
        etree.SubElement(svg, 'text', x=str(250 + labelOffset), y=str(250 - labelOffset),
                         fill="#242424",
                         **{"font-family": "Arial"},
                         **{"font-weight": "600"},
                         **{"text-anchor": "middle"},
                         **{"font-size": "18"}).text = center_point
        ox, oy = 250, 250

    # Draw points on the circle
    for point in points:
        if len(point) == 3:
            name, angle, _ = point
            angle_rad = math.radians(angle)
            x = ox + 200 * math.cos(angle_rad)
            y = oy - 200 * math.sin(angle_rad)  # SVG y-axis goes down, hence subtraction
            etree.SubElement(svg, 'circle', cx=str(x), cy=str(y), r=dotRadius, fill="#242424")

            xDirection = (x - 250) / 250
            yDirection = (y - 250) / 250

            if yDirection > 0:
                yDirection *= 2

            pointsCoords[name] = (x,y)

            etree.SubElement(svg, 'text', x=str(x + xDirection * labelOffset), y=str(y + yDirection * labelOffset),
                             fill="#242424",
                             **{"font-family": "Arial"},
                             **{"font-weight": "600"},
                             **{"text-anchor": "middle"},
                             **{"font-size": "18"}).text = name

    # Draw segments
    for segment in segments:
        p1_name, p2_name = segment
        p1 = next((point for point in points if point[0] == p1_name), None)
        p2 = next((point for point in points if point[0] == p2_name), None)

        if p1 and p2:
            if len(p1) == 3:
                angle1_rad = math.radians(p1[1])
                x1 = ox + 200 * math.cos(angle1_rad)
                y1 = oy - 200 * math.sin(angle1_rad)
            else:
                x1, y1 = ox, oy

            if len(p2) == 3:
                angle2_rad = math.radians(p2[1])
                x2 = ox + 200 * math.cos(angle2_rad)
                y2 = oy - 200 * math.sin(angle2_rad)
            else:
                x2, y2 = ox, oy

            etree.SubElement(svg, 'line', x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), stroke="#464646", **{"stroke-width": "2px"})

    for arc in arcs:
        centerCoords = pointsCoords[arc[1]]
        leftCoords =  pointsCoords[arc[0]]
        rightCoords =  pointsCoords[arc[2]]

        # Calculate the control point for the arc
        leftVec = normalizeVec(getVectorFromPoints(leftCoords, centerCoords), labelOffset * 2)
        rightVec = normalizeVec(getVectorFromPoints(rightCoords, centerCoords), labelOffset * 2)

        pointA = sumVecs(centerCoords, leftVec)
        pointB = sumVecs(centerCoords, rightVec)
        control_point = scaleVector(sumVecs(pointA, rightVec), 1)

        # Create a curved path
        path_data = f"M {pointA[0]},{pointA[1]} Q {control_point[0]},{control_point[1]} {pointB[0]},{pointB[1]}"
        etree.SubElement(svg, 'path', d=path_data, stroke="#725DFF", fill="none", **{"stroke-width": "2px"})


    # Convert the SVG tree to a string
    svg_string = etree.tostring(svg, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')

    with open('image.svg', 'w') as f:
        f.write(svg_string)

    return svg_string


# Example usage:
points = [
    ('O'),  # Center of the circle
    ('A', 270, 5),  # Point on the circumference at 270 degrees
    ('B', 0, 5),  # Point on the circumference at 0 degrees
    ('C', 60, 5),  # Point on the circumference at 60 degrees
    ('D', 180, 5)  # Point on the circumference at 180 degrees
]

segments = [
    ('O', 'A'),
    ('O', 'B'),
    ('O', 'C'),
    ('O', 'D'),
    ('B', 'C'),
]

arcs = [
    ('C', 'B', 'O')
]

svg_string = generate_svg_string(points, segments, arcs)
