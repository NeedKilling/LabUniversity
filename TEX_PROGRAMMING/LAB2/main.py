def convert_types(data):
    result = []
    for item in data:
        if isinstance(item, str):
            try:
                converted_item = int(item)
            except ValueError:
                try:
                    converted_item = float(item)
                except ValueError:
                    converted_item = item
        else:
            converted_item = str(item)
        result.append(converted_item)
    return result


def swap_values(a, b):
    a, b = b, a
    return a, b


def bool_transform(value):
    if value:
        return True
    else:
        return False


def compound_operations(a, b):
    results = []

    value = a
    value += b
    results.append(value)

    value = a
    value -= b
    results.append(value)

    value = a
    value *= b
    results.append(value)

    value = a
    value /= b
    results.append(value)

    value = a
    value //= b
    results.append(value)

    value = a
    value %= b
    results.append(value)

    value = a
    value **= b
    results.append(value)
    return results


def check_type(value, expected_type):
    actual_type = type(value).__name__
    if actual_type == expected_type:
        return True
    else:
        return False


def logical_and(a, b, c):
    if a:
        if b:
            if c:
                return True
    return False


def logical_or(a, b, c):
    if a:
        return True
    if b:
        return True
    if c:
        return True
    return False


def is_between(value, low, high):
    if value >= low and value <= high:
        return True
    else:
        return False


def print_even_numbers(n):
    for number in range(1, n + 1):
        if number % 2 == 0:
            print(number)


def countdown_while(n):
    number = n
    while number >= 1:
        print(number)
        number -= 1


def skip_multiples(n, multiple):
    if multiple == 0:
        raise ZeroDivisionError("Делитель не может быть равен нулю")
    for number in range(1, n + 1):
        if number % multiple == 0:
            continue
        print(number)


def if_elif_else_chain(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"


def abs_value(x):
    if x < 0:
        return -x
    else:
        return x


def binary_representation(n):
    if n == 0:
        return "0"
    number = n
    sign = ""
    if number < 0:
        sign = "-"
        number = -number
    result = ""
    while number > 0:
        remainder = number % 2
        result = str(remainder) + result
        number //= 2
    return sign + result


def custom_round(number, ndigits):
    multiplier = 10 ** ndigits
    scaled_number = number * multiplier
    if scaled_number >= 0:
        rounded_number = int(scaled_number + 0.5)
    else:
        rounded_number = int(scaled_number - 0.5)
    result = rounded_number / multiplier
    return result


def find_max_min(numbers):
    if len(numbers) == 0:
        raise ValueError("Список чисел не должен быть пустым")
    max_value = numbers[0]
    min_value = numbers[0]
    for number in numbers:
        if number > max_value:
            max_value = number
        if number < min_value:
            min_value = number
    return max_value, min_value


def all_true(iterable):
    for item in iterable:
        if not item:
            return False
    return True


def any_true(iterable):
    for item in iterable:
        if item:
            return True
    return False


def custom_enumerate(sequence, start=0):
    result = []
    index = start
    for item in sequence:
        pair = (index, item)
        result.append(pair)
        index += 1
    return result


def custom_filter(func, iterable):
    result = []
    for item in iterable:
        if func(item):
            result.append(item)
    return result


def custom_map(func, iterable):
    result = []
    for item in iterable:
        converted_item = func(item)
        result.append(converted_item)
    return result


def custom_zip(list1, list2):
    result = []
    length = min(len(list1), len(list2))
    for index in range(length):
        pair = (list1[index], list2[index])
        result.append(pair)
    return result


def custom_reversed(sequence):
    result = []
    for index in range(len(sequence) - 1, -1, -1):
        result.append(sequence[index])
    return result


def custom_sorted(iterable, reverse=False):
    result = list(iterable)
    length = len(result)
    for pass_index in range(length - 1):
        swapped = False
        for index in range(length - pass_index - 1):
            if reverse:
                if result[index] < result[index + 1]:
                    result[index], result[index + 1] = (
                        result[index + 1], result[index]
                    )
                    swapped = True
            else:
                if result[index] > result[index + 1]:
                    result[index], result[index + 1] = (
                        result[index + 1], result[index]
                    )
                    swapped = True
        if not swapped:
            break
    return result


def sum_digits(n):
    number = n
    if number < 0:
        number = -number
    result = 0
    while number > 0:
        digit = number % 10
        result += digit
        number //= 10
    return result


def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for character in text:
        if character in vowels:
            count += 1
    return count


def power(base, exp):
    result = 1
    exponent = exp
    if exponent < 0:
        exponent = -exponent
    for step in range(exponent):
        result *= base
    if exp < 0:
        result = 1 / result
    return result


def is_prime(n):
    if n < 2:
        return False
    for divisor in range(2, n):
        if divisor * divisor > n:
            break
        if n % divisor == 0:
            return False
    return True


def factorial(n):
    if n < 0:
        raise ValueError("Факториал определён для неотрицательных чисел")
    result = 1
    for number in range(1, n + 1):
        result *= number
    return result


def fibonacci(n):
    if n < 0:
        raise ValueError("Номер числа Фибоначчи не может быть отрицательным")
    previous = 0
    current = 1
    for step in range(n):
        next_number = previous + current
        previous = current
        current = next_number
    return previous


if __name__ == "__main__":
    print("Задание 1")
    print(convert_types([1, "2", "hello", 3.5]))
    print()

    print("Задание 2")
    print(swap_values(5, 10))
    print()

    print("Задание 3")
    print(bool_transform(5))
    print(bool_transform(0))
    print()

    print("Задание 4")
    print(compound_operations(10, 3))
    print()

    print("Задание 5")
    print(check_type(5, "int"))
    print(check_type("5", "int"))
    print()

    print("Задание 6")
    print(logical_and(True, 5, "x"))
    print(logical_and(True, 0, "x"))
    print()

    print("Задание 7")
    print(logical_or(0, "", False))
    print(logical_or(0, 5, False))
    print()

    print("Задание 8")
    print(is_between(5, 1, 10))
    print(is_between(15, 1, 10))
    print()

    print("Задание 9")
    print_even_numbers(10)
    print()

    print("Задание 10")
    countdown_while(5)
    print()

    print("Задание 11")
    skip_multiples(10, 3)
    print()

    print("Задание 12")
    print(if_elif_else_chain(5))
    print(if_elif_else_chain(-3))
    print(if_elif_else_chain(0))
    print()

    print("Задание 13")
    print(abs_value(-5))
    print(abs_value(3))
    print()

    print("Задание 14")
    print(binary_representation(10))
    print(binary_representation(0))
    print()

    print("Задание 15")
    print(custom_round(3.14159, 2))
    print(custom_round(2.5, 0))
    print()

    print("Задание 16")
    print(find_max_min([3, 7, 1, 9, 2]))
    print()

    print("Задание 17")
    print(all_true([1, 2, 3]))
    print(all_true([1, 0, 3]))
    print()

    print("Задание 18")
    print(any_true([0, "", False]))
    print(any_true([0, 5, False]))
    print()

    print("Задание 19")
    print(custom_enumerate(["a", "b", "c"], start=1))
    print()

    print("Задание 20")
    print(custom_filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))
    print()

    print("Задание 21")
    print(custom_map(lambda x: x * 2, [1, 2, 3]))
    print()

    print("Задание 22")
    print(custom_zip([1, 2, 3], ["a", "b", "c"]))
    print()

    print("Задание 23")
    print(custom_reversed([1, 2, 3, 4]))
    print()

    print("Задание 24")
    print(custom_sorted([3, 1, 4, 1, 5]))
    print(custom_sorted([3, 1, 4], reverse=True))
    print()

    print("Задание 25")
    print(sum_digits(1234))
    print(sum_digits(99))
    print()

    print("Задание 26")
    print(count_vowels("Hello World"))
    print(count_vowels("Python"))
    print()

    print("Задание 27")
    print(power(2, 5))
    print(power(3, 3))
    print()

    print("Задание 28")
    print(is_prime(17))
    print(is_prime(18))
    print()

    print("Задание 29")
    print(factorial(5))
    print(factorial(0))
    print()

    print("Задание 30")
    print(fibonacci(10))
    print(fibonacci(0))
    print(fibonacci(1))
