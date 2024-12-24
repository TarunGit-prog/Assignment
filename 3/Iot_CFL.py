# Context-Free Grammar (CFG) for a Custom IoT Scripting Language
# The language is designed to control IoT devices with simple commands.

# Grammar Rules:
# <program>       ::= <statement> | <statement> <program>
# <statement>     ::= <device_command>
# <device_command>::= 'TURN' <device> <state>
#                    | 'SET' <device> 'TO' <value>
# <device>        ::= 'LIGHT' | 'FAN' | 'THERMOSTAT'
# <state>         ::= 'ON' | 'OFF'
# <value>         ::= <number>
# <number>        ::= <digit> | <digit> <number>
# <digit>         ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

# Example Programs:
# 1. TURN LIGHT ON
# 2. SET THERMOSTAT TO 22
# 3. TURN FAN OFF

# Implementation of a simple parser and interpreter
import re

class IoTScriptingLanguageParser:
    def __init__(self):
        self.device_states = {}

    def parse_program(self, program):
        statements = program.strip().split('\n')
        for statement in statements:
            if statement.strip():
                try:
                    self.parse_statement(statement.strip())
                except ValueError as e:
                    print(f"Error: {e}")

    def parse_statement(self, statement):
        if statement.startswith("TURN"):
            match = re.match(r"TURN (LIGHT|FAN|THERMOSTAT) (ON|OFF)", statement)
            if match:
                device, state = match.groups()
                self.device_states[device] = state
                print(f"{device} turned {state}")
            else:
                raise ValueError(f"Invalid TURN command: {statement}")
        elif statement.startswith("SET"):
            match = re.match(r"SET (LIGHT|FAN|THERMOSTAT) TO (\d+)", statement)
            if match:
                device, value = match.groups()
                self.device_states[device] = int(value)
                print(f"{device} set to {value}")
            else:
                raise ValueError(f"Invalid SET command: {statement}")
        else:
            raise ValueError(f"Invalid statement: {statement}")

# Sample usage
if __name__ == "__main__":
    parser = IoTScriptingLanguageParser()

    try:
        print("Enter your IoT commands below (end with an empty line):")
        user_program = ""
        while True:
            try:
                line = input()
                if line.strip() == "":
                    break
                user_program += line + "\n"
            except EOFError:
                break

        print("\nParsing and executing program:\n")
        parser.parse_program(user_program)

        print("\nDevice States:")
        for device, state in parser.device_states.items():
            print(f"{device}: {state}")
    except OSError as e:
        print(f"Error: Unable to read input. Ensure the environment supports interactive input. ({e})")