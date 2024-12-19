class TuringMachine:
    def __init__(self, tape):
        self.tape = list(tape)  # Convert tape input to list for easy modification
        self.head = 0           # Head starts at the first cell
        self.state = 'q0'       # Initial state
        self.balance = 0        # Bank account balance

    def step(self):
        """Execute a single step of the Turing Machine."""
        symbol = self.tape[self.head] if self.head < len(self.tape) else '_'

        # State transitions
        if self.state == 'q0':
            if symbol == 'D':  # Deposit
                self.state = 'q1'
                self.head += 1
            elif symbol == 'W':  # Withdraw
                self.state = 'q2'
                self.head += 1
            elif symbol == 'B':  # Balance Inquiry
                self.state = 'q3'
                self.head += 1
            elif symbol == '_':  # End of tape
                self.state = 'qh'
            else:
                self.state = 'qe'  # Error state
        elif self.state == 'q1':  # Handle deposit
            amount = self._read_number()
            if amount is not None:
                self.balance += amount
                self.state = 'q4'
        elif self.state == 'q2':  # Handle withdrawal
            amount = self._read_number()
            if amount is not None:
                if self.balance >= amount:
                    self.balance -= amount
                    self.state = 'q4'
                else:
                    self.state = 'qe'  # Error: Insufficient funds
        elif self.state == 'q3':  # Output balance
            print(f"Balance: ${self.balance}")
            self.state = 'q4'
        elif self.state == 'q4':  # Move to next operation
            if symbol == '#':
                self.head += 1
                self.state = 'q0'
            elif symbol == '_':
                self.state = 'qh'  # Halt
        elif self.state == 'qe':  # Error state
            print("Error occurred.")
            self.state = 'qh'

    def _read_number(self):
        """Read a number from the tape."""
        number = ''
        while self.head < len(self.tape) and self.tape[self.head].isdigit():
            number += self.tape[self.head]
            self.head += 1
        return int(number) if number else None

    def run(self):
        """Run the Turing Machine until it halts."""
        while self.state != 'qh':
            self.step()


# Example Input Tape
tape = "D100#W50#B?#D200#W50#B?_"

# Initialize and Run Turing Machine
tm = TuringMachine(tape)
tm.run()
