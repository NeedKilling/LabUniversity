import ast
import io
import keyword
import re
import tokenize
from typing import Any, Dict, List, Tuple
import json


def split_words(name: str) -> List[str]:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
    s = re.sub(r"[_\W]+", " ", s)
    return [w for w in s.split() if w]


def is_snake_case(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-z0-9_]*", name)) and not name.isupper()


def is_upper_case(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Z0-9_]*", name))


def is_camel_case(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-zA-Z0-9]*", name)) and any(
        c.isupper() for c in name
    )


def is_pascal_case(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][a-zA-Z0-9]*", name)) and any(
        c.islower() for c in name
    )


def json_print(data):
    return json.dumps(data, ensure_ascii=False, indent=4, default=str)


#1
def check_naming_style(names: List[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for name in names:
        if is_upper_case(name):
            style = "UPPER_CASE"
        elif is_snake_case(name):
            style = "snake_case"
        elif is_camel_case(name):
            style = "camelCase"
        elif is_pascal_case(name):
            style = "PascalCase"
        else:
            style = "unknown"
        result[name] = style
    return result


#2
def is_valid_python_identifier(name: str, kind: str) -> bool:
    if not name.isidentifier() or keyword.iskeyword(name):
        return False
    if kind in ("variable", "function"):
        return is_snake_case(name)
    if kind == "class":
        return is_pascal_case(name)
    if kind == "constant":
        return is_upper_case(name)
    return False

#3
def to_pep8_name(name: str, kind: str) -> str:
    words = split_words(name)
    if kind in ("variable", "function"):
        return "_".join(w.lower() for w in words)
    if kind == "class":
        return "".join(w.capitalize() for w in words)
    if kind == "constant":
        return "_".join(w.upper() for w in words)
    return name




#4
def check_indentation(code: str, indent_size: int = 4) -> List[str]:
    errors: List[str] = []
    for i, line in enumerate(code.splitlines(), 1):
        if not line.strip():
            continue
        leading = line[: len(line) - len(line.lstrip())]
        if "\t" in leading and " " in leading:
            errors.append("Строка %d: смешаны табы и пробелы" % i)
        # elif "\t" in leading:
        #     continue
        else:
            if len(leading) % indent_size != 0:
                errors.append(
                    "Строка %d: отступ %d не кратен %d"
                    % (i, len(leading), indent_size)
                )
    return errors


#5
def find_magic_numbers(code: str) -> List[Tuple[int, int]]:
    magic: List[Tuple[int, int]] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok in tokens:
            if tok.type == tokenize.NUMBER:
                try:
                    value = int(tok.string, 0)
                except ValueError:
                    continue
                if value not in (0, 1, -1):
                    magic.append((tok.start[0], value))
    except tokenize.TokenError:
        pass
    return magic
#6
def extract_module_structure(code: str) -> Dict[str, List[str]]:
    tree = ast.parse(code)
    imports: List[str] = []
    constants: List[str] = []
    functions: List[str] = []
    classes: List[str] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and is_upper_case(target.id):
                    constants.append(target.id)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {
        "imports": imports,
        "constants": constants,
        "functions": functions,
        "classes": classes,
    }

#7
def check_docstrings(code: str) -> Dict[str, bool]:
    tree = ast.parse(code)
    result: Dict[str, bool] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result[node.name] = ast.get_docstring(node) is not None
    return result


#8
def generate_module_template(
    module_name: str, functions: List[str], classes: List[str]
) -> str:
    lines = [
        '"""Модуль %s."""' % module_name,
        "",
        "from typing import Any, Dict, List",
        "",
        '__version__ = "0.1.0"',
        "",
    ]
    for func in functions:
        lines.append("def %s() -> None:" % func)
        lines.append('    """Описание функции %s."""' % func)
        lines.append("    pass")
        lines.append("")
    for cls in classes:
        lines.append("class %s:" % cls)
        lines.append('    """Описание класса %s."""' % cls)
        lines.append("    pass")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"



#9
def add_main_guard(code: str, main_function: str = "main") -> str:
    if '__name__ == "__main__"' in code:
        return code
    guard = '\n\nif __name__ == "__main__":\n    %s()\n' % main_function
    return code.rstrip() + guard


#10
def line_length_stats(code: str, max_length: int = 79) -> Dict[str, Any]:
    lines = code.splitlines()
    total = len(lines)
    if total == 0:
        return {
            "total_lines": 0,
            "lines_over_max": 0,
            "max_line_length": 0,
            "average_line_length": 0.0,
        }
    lengths = [len(line) for line in lines]
    return {
        "total_lines": total,
        "lines_over_max": sum(1 for length in lengths if length > max_length),
        "max_line_length": max(lengths),
        "average_line_length": sum(lengths) / total,
    }


#11
def check_imports_order(code: str) -> List[str]:
    tree = ast.parse(code)
    errors: List[str] = []
    seen_non_import = False

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if seen_non_import:
                errors.append(
                    "Строка %d: импорт после определений" % node.lineno
                )
        elif (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            continue
        else:
            seen_non_import = True
    return errors


#12
def max_nesting_level(code: str) -> int:
    max_level = 0
    for line in code.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        level = indent // 4 + 1
        if level > max_level:
            max_level = level
    return max_level


#13
def fix_spaces_around_operators(line: str) -> str:
    comment = ""
    if "#" in line:
        code_part, comment = line.split("#", 1)
        comment = "#" + comment
    else:
        code_part = line

    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code_part).readline))
    except tokenize.TokenError:
        return line

    result: List[str] = []
    operators = {
        "=", "==", "!=", "<", ">", "<=", ">=",
        "+", "-", "*", "/", "//", "%", "**",
        "+=", "-=", "*=", "/=", "//=", "%=", "**=",
        "&", "|", "^", "<<", ">>",
    }

    for tok in tokens:
        if tok.type == tokenize.STRING:
            result.append(tok.string)
        elif tok.type == tokenize.OP and tok.string in operators:
            result.append(" %s " % tok.string)
        elif tok.type in (
            tokenize.NEWLINE,
            tokenize.NL,
            tokenize.ENDMARKER,
            tokenize.INDENT,
            tokenize.DEDENT,
        ):
            continue
        else:
            result.append(tok.string)

    new_code = "".join(result)
    new_code = re.sub(r" +", " ", new_code).strip()
    new_code = re.sub(r"\s+([,.:)\]])", r"\1", new_code)
    new_code = re.sub(r"([(\[{])\s+", r"\1", new_code)
    return new_code + comment





#14
def analyze_comments(code: str) -> Dict[str, Any]:
    total_lines = len(code.splitlines())
    total_comments = 0
    docstring_lines = 0

    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                total_comments += 1
    except tokenize.TokenError:
        pass

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module),
            ):
                doc = ast.get_docstring(node)
                if doc:
                    docstring_lines += len(doc.splitlines())
    except SyntaxError:
        pass

    comment_ratio = total_comments / total_lines if total_lines else 0.0
    return {
        "total_comments": total_comments,
        "docstring_lines": docstring_lines,
        "comment_ratio": comment_ratio,
    }


#15
def find_long_functions(
    code: str, max_lines: int = 50
) -> List[Tuple[str, int]]:
    tree = ast.parse(code)
    result: List[Tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.body:
            start = node.body[0].lineno
            end = node.body[-1].end_lineno
            length = end - start + 1
            if length > max_lines:
                result.append((node.name, length))
    return result


#16
def normalize_blank_lines_between_functions(code: str) -> str:
    lines = code.splitlines()
    result: List[str] = []
    for line in lines:
        if line.startswith("def ") or line.startswith("class "):
            while result and result[-1].strip() == "":
                result.pop()
            if result:
                result.append("")
                result.append("")
        result.append(line)
    return "\n".join(result)


#17
def simple_linter(code: str) -> List[str]:
    errors: List[str] = []
    lines = code.splitlines()

    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        leading = line[: len(line) - len(line.lstrip())]
        if "\t" in leading and " " in leading:
            errors.append("Строка %d: смешаны табы и пробелы" % i)
        elif " " in leading and len(leading) % 4 != 0:
            errors.append("Строка %d: отступ не кратен 4" % i)

    for i, line in enumerate(lines, 1):
        if len(line) > 79:
            errors.append("Строка %d: длина %d > 79" % (i, len(line)))

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    errors.append(
                        "Строка %d: функция %s без docstring"
                        % (node.lineno, node.name)
                    )
                if not is_snake_case(node.name):
                    errors.append(
                        "Строка %d: имя функции %s не snake_case"
                        % (node.lineno, node.name)
                    )
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    errors.append(
                        "Строка %d: класс %s без docstring"
                        % (node.lineno, node.name)
                    )
    except SyntaxError:
        errors.append("Синтаксическая ошибка при разборе кода")

    for line_no, value in find_magic_numbers(code):
        errors.append("Строка %d: магическое число %s" % (line_no, value))

    return errors


#18
def style_report(code: str, module_name: str) -> str:
    structure = extract_module_structure(code)
    docstrings = check_docstrings(code)
    stats = line_length_stats(code)
    magic = find_magic_numbers(code)

    total_doc = sum(1 for v in docstrings.values() if v)
    total_defs = len(docstrings)
    coverage = (total_doc / total_defs * 100) if total_defs else 0.0

    lines = [
        "Module: %s" % module_name,
        "Total lines: %d" % stats["total_lines"],
        "Functions: %d" % len(structure["functions"]),
        "Classes: %d" % len(structure["classes"]),
        "Docstring coverage: %.1f%%" % coverage,
        "Lines over 79 chars: %d" % stats["lines_over_max"],
        "Magic numbers found: %d" % len(magic),
    ]
    return "\n".join(lines)


#19
def refactor_bad_code(code: str) -> str:
    lines = code.splitlines()
    result: List[str] = ['"""Отрефакторенный модуль."""', ""]
    constants: Dict[str, int] = {}

    for line in lines:
        match = re.match(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
        if match:
            old_name = match.group(1)
            new_name = to_pep8_name(old_name, "function")
            line = line.replace(old_name, new_name, 1)
            result.append(line)
            result.append('    """Описание функции %s."""' % new_name)
            continue

        def repl(match_obj: re.Match) -> str:
            val = int(match_obj.group())
            if val not in (0, 1, -1):
                const_name = "CONST_%d" % val
                constants[const_name] = val
                return const_name
            return match_obj.group()

        line = re.sub(r"\b\d+\b", repl, line)
        result.append(line)

    if constants:
        const_lines = ["%s = %d" % (name, val) for name, val in constants.items()]
        result = result[:2] + const_lines + [""] + result[2:]

    return "\n".join(result)


#20
def compare_module_versions(old_code: str, new_code: str) -> Dict[str, Any]:
    old_struct = extract_module_structure(old_code)
    new_struct = extract_module_structure(new_code)
    old_docs = check_docstrings(old_code)
    new_docs = check_docstrings(new_code)

    def coverage(docs: Dict[str, bool]) -> float:
        total = len(docs)
        if total == 0:
            return 0.0
        return sum(1 for v in docs.values() if v) / total * 100

    return {
        "added_functions": list(
            set(new_struct["functions"]) - set(old_struct["functions"])
        ),
        "removed_functions": list(
            set(old_struct["functions"]) - set(new_struct["functions"])
        ),
        "added_classes": list(
            set(new_struct["classes"]) - set(old_struct["classes"])
        ),
        "removed_classes": list(
            set(old_struct["classes"]) - set(new_struct["classes"])
        ),
        "docstring_coverage_old": coverage(old_docs),
        "docstring_coverage_new": coverage(new_docs),
    }


if __name__ == "__main__":
    print("ЗАДАНИЕ 1")
    names = ["my_var", "myVar", "MyVar", "MAX_SIZE", "Bad-Name"]
    print(json_print(check_naming_style(names)))
    print()

    print("ЗАДАНИЕ 2")
    print(is_valid_python_identifier("my_var", "variable"))
    print(is_valid_python_identifier("MyClass", "class"))
    print(is_valid_python_identifier("MAX_SIZE", "constant"))
    print()

    print("ЗАДАНИЕ 3")
    print(to_pep8_name("UserName", "variable"))
    print(to_pep8_name("MAX_SIZE", "function"))
    print(to_pep8_name("user_name", "class"))
    print()

    print("ЗАДАНИЕ 4")
    bad_indent_code = "def f():\n  x = 1\n    y = 2\n\tz = 3\n"
    print(json_print(check_indentation(bad_indent_code)))
    print()

    print("ЗАДАНИЕ 5")
    magic_code = "x = 100\n# comment 200\ny = 1\nz = -1\ns = '300'\n"
    print(find_magic_numbers(magic_code))
    print()

    print("ЗАДАНИЕ 6")
    module_code = (
        '"""Модуль пример."""\n\n'
        "import os\nfrom sys import argv\n\n"
        "MAX_SIZE = 100\n\n"
        "def foo():\n    pass\n\n"
        "class Bar:\n    pass\n"
    )
    print(json_print(extract_module_structure(module_code)))
    print()

    print("ЗАДАНИЕ 7")
    doc_code = (
        'def foo():\n    """Docstring."""\n    pass\n\n'
        "class Bar:\n    pass\n"
    )
    print(json_print(check_docstrings(doc_code)))
    print()

    print("ЗАДАНИЕ 8")
    print(generate_module_template("my_module", ["foo", "bar"], ["Baz"]))
    print()

    print("ЗАДАНИЕ 9")
    base_code = "def main():\n    pass\n"
    print(add_main_guard(base_code))
    print()

    print("ЗАДАНИЕ 10")
    stats_code = "line1\nline2 is longer than 79 chars..." + "x" * 80 + "\n"
    print(json_print(line_length_stats(stats_code)))
    print()

    print("ЗАДАНИЕ 11")
    bad_imports = "def f():\n    pass\n\nimport os\n"
    print(check_imports_order(bad_imports))
    print()

    print("ЗАДАНИЕ 12")
    nested_code = (
        "def f():\n    if x:\n        for i in range(10):\n            pass\n"
    )
    print(max_nesting_level(nested_code))
    print()

    print("ЗАДАНИЕ 13")
    print(fix_spaces_around_operators("x=a+b"))
    print(fix_spaces_around_operators("if x==1: # comment"))
    print()

    print("ЗАДАНИЕ 14")
    comment_code = (
        '"""Docstring."""\n# Comment line\nx = 1  # inline comment\n'
    )
    print(json_print(analyze_comments(comment_code)))
    print()

    print("ЗАДАНИЕ 15")
    long_func = "def f():\n" + "    x = 1\n" * 60
    print(find_long_functions(long_func, max_lines=50))
    print()

    print("ЗАДАНИЕ 16")
    blank_code = "def a():\n    pass\n\n\n\ndef b():\n    pass\n"
    print(normalize_blank_lines_between_functions(blank_code))
    print()

    print("ЗАДАНИЕ 17")
    lint_code = "def BadName():\n    x = 100\n    return x\n"
    print(json_print(simple_linter(lint_code)))
    print()

    print("ЗАДАНИЕ 18")
    report_code = (
        '"""Модуль пример."""\n\n'
        "MAX_SIZE = 100\n\n"
        'def foo():\n    """Docstring."""\n    pass\n\n'
        "class Bar:\n    pass\n"
    )
    print(style_report(report_code, "example"))
    print()

    print("ЗАДАНИЕ 19")
    bad_code = "def BadName():\n    x = 100\n    return x\n"
    print(refactor_bad_code(bad_code))
    print()

    print("ЗАДАНИЕ 20")
    old_code = "def foo():\n    pass\n"
    new_code = (
        'def foo():\n    """Doc."""\n    pass\n\n'
        "def bar():\n    pass\n"
    )
    print(json_print(compare_module_versions(old_code, new_code)))