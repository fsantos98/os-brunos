from mermaid import Mermaid

# Define your Mermaid diagram
diagram = """
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
"""

# Create a Mermaid object
mermaid = Mermaid(diagram)

# Render the diagram to a file
mermaid.render('output.svg')
