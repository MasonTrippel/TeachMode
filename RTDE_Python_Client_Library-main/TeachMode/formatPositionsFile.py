import ast
def load_data(filename):
    arrays = []
    with open(filename, "r") as file:
        for line in file:
            # Remove whitespace and trailing commas
            line = line.strip().strip(',')
            if line:
                # Convert string representation of list to actual list
                try:
                    array = ast.literal_eval(line)
                    arrays.append(array)
                except ValueError as e:
                    print(f"Error parsing line: {line}. Error: {e}")
    return arrays

filename = "robot_positions.txt"
arrays = load_data(filename)
print(arrays)