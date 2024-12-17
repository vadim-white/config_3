import re
import sys
import toml

def remove_multiline_comments(toml_text):
    """Удаляет многострочные комментарии из текста TOML."""
    multiline_comment_pattern = re.compile(r'#\|.*?\|#', re.DOTALL)
    return re.sub(multiline_comment_pattern, '', toml_text)

def evaluate_expression(expression, constants):
    """Вычисляет константное выражение в постфиксной форме."""
    tokens = expression.split()
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in constants:
            stack.append(constants[token])
        elif token == '+':
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif token == '-':
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif token == 'print()':
            print("Print output:", stack[-1])
        else:
            print(f"Unknown token in expression: {token}")
            sys.exit(1)
    return stack[0] if stack else None

def parse_toml_to_custom_lang(toml_data):
    """Преобразует TOML-данные в учебный конфигурационный язык."""
    output_lines = []
    constants = {}

    def process_value(value):
        if isinstance(value, list):
            return "'( " + " ".join(map(str, value)) + " )"
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            return str(value)

    for key, value in toml_data.items():
        if isinstance(value, list):
            # Обработка массивов
            output_lines.append(f"{key} = {process_value(value)}")
        elif isinstance(value, str) and value.startswith(".[") and value.endswith("]."):
            # Обработка постфиксных выражений
            expression = value[2:-2]  # Обрезаем '.[' и '].'
            result = evaluate_expression(expression, constants)
            constants[key] = result
            output_lines.append(f"set {key} = {result}")
        else:
            # Обработка простых значений
            constants[key] = value
            output_lines.append(f"set {key} = {process_value(value)}")

    return "\n".join(output_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file.toml>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as f:
            toml_text = f.read()
            toml_text = remove_multiline_comments(toml_text)  # Удаляем многострочные комментарии

            # Заменяем выражения в постфиксной форме на строковые выражения
            toml_text = re.sub(r'\.\[.*?\]\.', lambda m: f'"{m.group(0)}"', toml_text)

            toml_data = toml.loads(toml_text)  # Загружаем данные после очистки
    except Exception as e:
        print(f"Error reading TOML file: {e}")
        sys.exit(1)

    output = parse_toml_to_custom_lang(toml_data)
    print(output)
