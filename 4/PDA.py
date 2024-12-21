class PDA: 
    def _init_(self): 
        self.stack = []   
 
    def evaluate(self, expression): 
        print(f"Input Expression: {expression}") 
        self.stack = [] 
        tokens = self._tokenize(expression) 
        result = self._process_tokens(tokens) 
        if self.stack: 
            raise ValueError("Stack is not empty! Invalid expression.") 
        return result
 
    def _tokenize(self, expression): 
        tokens = [] 
        current_num = [] 
        for char in expression: 
            if char.isdigit(): 
                current_num.append(char) 
            else: 
                if current_num: 
                    tokens.append(''.join(current_num)) 
                    current_num = [] 
                if char in "+-*/()": 
                    tokens.append(char) 
        if current_num: 
            tokens.append(''.join(current_num)) 
        return tokens
 
    def _process_tokens(self, tokens): 
        num_stack = [] 
        op_stack = [] 
 
        def precedence(op): 
            if op in ('+', '-'): 
                return 1 
            if op in ('*', '/'): 
                return 2 
            return 0
 
        def apply_operator(): 
            if not op_stack or len(num_stack) < 2:
                raise ValueError("Invalid expression.")
            operator = op_stack.pop() 
            right = num_stack.pop() 
            left = num_stack.pop() 
            if operator == "+": 
                num_stack.append(left + right) 
            elif operator == "-": 
                num_stack.append(left - right) 
            elif operator == "*": 
                num_stack.append(left * right) 
            elif operator == "/": 
                num_stack.append(left / right) 
 
        for token in tokens: 
            if token.isdigit():   
                num_stack.append(int(token)) 
            elif token in "+-*/":   
                while (op_stack and precedence(op_stack[-1]) >= precedence(token)): 
                    apply_operator() 
                op_stack.append(token) 
            elif token == "(":   
                op_stack.append(token) 
            elif token == ")":   
                while op_stack and op_stack[-1] != "(": 
                    apply_operator() 
                if not op_stack or op_stack[-1] != "(": 
                    raise ValueError("Mismatched parentheses")
                op_stack.pop()  # Remove '(' from stack
            else: 
                raise ValueError(f"Invalid token: {token}") 
 
        while op_stack:  
            apply_operator() 
 
        if len(num_stack) != 1:
            raise ValueError("Invalid expression.")
        return num_stack.pop()   
 
pda = PDA()

expression = input("Enter an arithmetic expression: ")
try: 
    result = pda.evaluate(expression) 
    print(f"Result: {result}\n") 
except ValueError as e: 
    print(f"Error: {e}\n")