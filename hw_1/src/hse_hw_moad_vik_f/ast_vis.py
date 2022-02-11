import ast
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from networkx.drawing.nx_pydot import graphviz_layout


class AST2IMG(ast.NodeVisitor):
    def __init__(self):
        self.g = nx.DiGraph()
        self.stack = []
        self.cl = defaultdict(int)
        self.labels, self.colors = dict(), dict()

    def add(self, node, label, color):
        class_name = node.__class__.__name__
        self.cl[class_name] += 1
        node_name = f"{class_name}_{self.cl[class_name]}"
        if len(self.stack) > 0:
            p_name = self.stack[- 1]
            self.g.add_edge(p_name, node_name)
        self.g.add_node(node_name)
        self.stack += [node_name]
        self.labels[node_name], self.colors[node_name] = label, color
        super(self.__class__, self).generic_visit(node)
        self.stack.pop()
        
    def generic_visit(self, node):
        label = node.__class__.__name__
        self.add(node, label, "skyblue")
        
    def visit_Name(self, node):
        label = f"{node.__class__.__name__}\nid: {node.id}"
        self.add(node, label, "sandybrown")

    def visit_FunctionDef(self, node):
        label = f"{node.__class__.__name__}\nname: {node.name}"
        self.add(node, label, "tomato")
    
    def visit_arg(self, node):
        label = f"{node.__class__.__name__}\nname: {node.arg}"
        self.add(node, label, "gold")
        
    def visit_Constant(self, node):
        label = f"{node.__class__.__name__}\nvalue: {node.value}"
        self.add(node, label, "yellowgreen")

    def draw(self, path):
        plt.figure(figsize=(25, 10))
        layout = graphviz_layout(self.g, prog="dot")
        nx.draw(self.g, layout, node_color=[self.colors[y] for y in self.g.nodes()],
                node_size=[220 * len(x) for x in self.g.nodes()], labels=self.labels)
        plt.savefig(path)


if __name__ == "__main__":
    decor = AST2IMG()
    with open("fib.py", "r") as file:
        scr = file.read()
    decor.visit(ast.parse(scr))
    decor.draw("artifacts/ast_fib.png")
    