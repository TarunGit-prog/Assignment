class Interpreter:
    def _init_(self):
        self.symbol_table = {}

    def execute(self, node):
        if not isinstance(node, dict) or "type" not in node:
            raise TypeError(f"Invalid node: {node}")

        if node["type"] == "declaration":
            self.symbol_table[node["id"]] = self.evaluate(node["expression"])
        elif node["type"] == "assignment":
            self.symbol_table[node["id"]] = self.evaluate(node["expression"])
        elif node["type"] == "conditional":
            condition = self.evaluate(node["condition"])
            if condition:
                self.execute_block(node["if_block"]["statements"])  # Access 'statements' directly
            elif "else_block" in node:
                self.execute_block(node["else_block"]["statements"])  # Access 'statements' directly
        elif node["type"] == "loop":
            while self.evaluate(node["condition"]):
                self.execute_block(node["block"]["statements"])  # Access 'statements' directly
        elif node["type"] == "write":
            actuator = node["actuator"]
            value = self.evaluate(node["value"])
            print(f"Actuating {actuator}: {value}")
        elif node["type"] == "block":
            self.execute_block(node["statements"])  # Correctly accessing 'statements'
        else:
            raise ValueError(f"Unknown node type: {node['type']}")

    def evaluate(self, expression):
        if expression["type"] == "num":
            return expression["value"]
        elif expression["type"] == "id":
            if expression["id"] not in self.symbol_table:
                raise NameError(f"Undefined variable: {expression['id']}")
            return self.symbol_table[expression["id"]]
        elif expression["type"] == "binary":
            left = self.evaluate(expression["left"])
            right = self.evaluate(expression["right"])
            operator = expression["operator"]
            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                return left / right
            elif operator == ">":
                return left > right
            elif operator == "<":
                return left < right
            elif operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == ">=":
                return left >= right
            elif operator == "<=":
                return left <= right
            else:
                raise ValueError(f"Unknown operator: {operator}")
        elif expression["type"] == "str":  # Handle string literals
            return expression["value"]
        else:
            raise TypeError(f"Invalid expression: {expression}")

    def execute_block(self, statements):
        if not isinstance(statements, list):  # Check if the statements are a list
            raise TypeError(f"Block statements should be a list: {statements}")
        for stmt in statements:
            self.execute(stmt)


# Example Parse Tree for the IoT Program
parse_tree = {
    "type": "conditional",
    "condition": {
        "type": "binary",
        "left": {"type": "id", "id": "temp"},
        "operator": ">",
        "right": {"type": "num", "value": 30}
    },
    "if_block": {
        "type": "block",
        "statements": [
            {"type": "write", "actuator": "fan", "value": {"type": "str", "value": "on"}}
        ]
    },
    "else_block": {
        "type": "block",
        "statements": [
            {"type": "write", "actuator": "fan", "value": {"type": "str", "value": "off"}}
        ]
    }
}

# Example Usage
interpreter = Interpreter()
interpreter.symbol_table = {"temp": 35}  # Simulate sensor reading
interpreter.execute(parse_tree)