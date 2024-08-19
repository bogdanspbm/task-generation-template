from lxml import etree
from itertools import combinations

def generate_svg(base_labels, top_labels, connections):
    # Define points for base and top with adjustments
    points = {
        base_labels[0]: (50, 150), base_labels[1]: (190, 140), base_labels[2]: (70, 220),
        top_labels[0]: (50, 50), top_labels[1]: (190, 40), top_labels[2]: (70, 120)
    }

    # Define adjusted positions for labels
    label_offsets = {
        base_labels[0]: (-12, 8), base_labels[1]: (8, 8), base_labels[2]: (-12, 8),
        top_labels[0]: (-12, -8), top_labels[1]: (8, -8), top_labels[2]: (-12, -8)
    }

    # Create SVG root element
    svg = etree.Element('svg', xmlns="http://www.w3.org/2000/svg", width="250", height="250", **{"viewBox": "0 0 250 250"})

    # Draw dashed connections
    dashed_connections = [("A", "A1"), ("B", "B1"), ("C", "C1")]
    drawn_edges = set()

    for start, end in dashed_connections:
        if start in points and end in points:
            etree.SubElement(svg, 'line', x1=str(points[start][0]), y1=str(points[start][1]),
                             x2=str(points[end][0]), y2=str(points[end][1]),
                             stroke="#646464", stroke_dasharray="5,5")
            drawn_edges.add((start, end))
            drawn_edges.add((end, start))

    # Draw solid connections for base and top
    for start, end in [(base_labels[0], base_labels[1]), (base_labels[1], base_labels[2]),
                       (base_labels[2], base_labels[0]),
                       (top_labels[0], top_labels[1]), (top_labels[1], top_labels[2]), (top_labels[2], top_labels[0])]:
        if (start, end) not in drawn_edges and (end, start) not in drawn_edges:
            etree.SubElement(svg, 'line', x1=str(points[start][0]), y1=str(points[start][1]),
                             x2=str(points[end][0]), y2=str(points[end][1]),
                             stroke="#646464", stroke_dasharray="5,5")

    # Function to check if three points form a triangle in the connections
    def is_triangle(p1, p2, p3):
        return ((p1, p2) in connections or (p2, p1) in connections) and \
            ((p2, p3) in connections or (p3, p2) in connections) and \
            ((p3, p1) in connections or (p1, p3) in connections)

    # Find all possible triangles from the connections
    triangles = []
    for combo in combinations(points.keys(), 3):
        if is_triangle(combo[0], combo[1], combo[2]):
            triangles.append(combo)

    # Draw filled polygons for each triangle
    for triangle in triangles:
        polygon_points = " ".join([f"{points[point][0]},{points[point][1]}" for point in triangle])
        etree.SubElement(svg, 'polygon', points=polygon_points, fill="#9254de", fill_opacity="0.05")

    # Draw solid connections from the provided list
    for connection in connections:
        start, end = connection
        if start in points and end in points:
            etree.SubElement(svg, 'line', x1=str(points[start][0]), y1=str(points[start][1]),
                             x2=str(points[end][0]), y2=str(points[end][1]), stroke="#9254de", stroke_width="2")

    # Add labels with offsets
    for label, point in points.items():
        offset_x, offset_y = label_offsets.get(label, (0, 0))
        text = etree.SubElement(svg, 'text', x=str(point[0] + offset_x), y=str(point[1] + offset_y), fill="#242424", font_family="Arial", font_weight="bold",
                                font_size="14")
        text.text = label

    return etree.tostring(svg, pretty_print=True).decode().replace('stroke_dasharray', 'stroke-dasharray').replace(
        "stroke_width", "stroke-width").replace('font_family', 'font-family').replace("font_size", "font-size").replace("font_weight", "font-weight").replace("fill_opacity", "fill-opacity")

# Example usage
base_labels = ["A", "B", "C"]
top_labels = ["A1", "B1", "C1"]
connections = [("A", "B"), ("B", "C"), ("C", "A"), ("A", "C1"), ("B", "C1"), ("C", "C1")]

# Converting the list of connections into a set of tuples for easier checking
connections = set(connections)

svg_content = generate_svg(base_labels, top_labels, connections)

# Save SVG content to a file
with open("image.svg", "w") as file:
    file.write(svg_content)
