def pair(head, tail):
    def inner(func):
        return func(head, tail)
    return inner


def head(lst):
    if lst is None:
        print("Ошибка: у пустого списка нет головы")
        return None

    def getHead(h, t):
        return h

    return lst(getHead)


def tail(lst):
    if lst is None:
        print("Ошибка: у пустого списка нет хвоста")
        return None

    def getTail(h, t):
        return t

    return lst(getTail)


def makeList(*args):
    def build(index):
        if index == len(args):
            return None
        return pair(args[index], build(index + 1))

    return build(0)


def listToString(lst):
    def elementsToString(node):
        if node is None:
            return ""
        rest = tail(node)
        if rest is None:
            return str(head(node))
        return str(head(node)) + ", " + elementsToString(rest)

    return "[" + elementsToString(lst) + "]"


def listRange(low, high):
    if low > high:
        return None
    return pair(low, listRange(low + 1, high))


def foldl(func, lst, acc):
    if lst is None:
        return acc
    return foldl(func, tail(lst), func(acc, head(lst)))


def listSum(lst):
    def add(acc, value):
        return acc + value

    return foldl(add, lst, 0)


def fact(n):
    if n < 0:
        print("Ошибка: факториал отрицательного числа не определён")
        return None

    def multiply(acc, value):
        return acc * value

    return foldl(multiply, listRange(1, n), 1)


def listToPy(lst):
    def addElement(acc, value):
        return acc + [value]

    return foldl(addElement, lst, [])


def listReverse(lst):
    def prepend(acc, value):
        return pair(value, acc)

    return foldl(prepend, lst, None)


def foldr(func, lst, acc):
    if lst is None:
        return acc
    return func(head(lst), foldr(func, tail(lst), acc))


def listMap(func, lst):
    def mapElement(value, acc):
        return pair(func(value), acc)

    return foldr(mapElement, lst, None)


def listFilter(pred, lst):
    def filterElement(value, acc):
        if pred(value):
            return pair(value, acc)
        return acc

    return foldr(filterElement, lst, None)


def sumOddSquares(lst):
    def square(value):
        return value * value

    def isOdd(value):
        return value % 2 != 0

    return listSum(listMap(square, listFilter(isOdd, lst)))


def listConcat(lst1, lst2):
    return foldr(pair, lst1, lst2)


def listReplace(lst, index, value):
    if index < 0 or lst is None:
        print("Ошибка: индекс вне границ списка")
        return None
    if index == 0:
        return pair(value, tail(lst))

    newTail = listReplace(tail(lst), index - 1, value)
    if newTail is None:
        return None
    return pair(head(lst), newTail)


if __name__ == "__main__":
    def subtract(left, right):
        return left - right

    def square(value):
        return value * value

    def isOdd(value):
        return value % 2 != 0

    numbers = makeList(1, 2, 3, 4, 5)
    print("Список:", listToString(numbers))
    print("Голова:", head(numbers))
    print("Хвост:", listToString(tail(numbers)))
    print("Диапазон:", listToString(listRange(3, 7)))
    print("Сумма:", listSum(numbers))
    print("Факториал 5:", fact(5))
    print("Список Python:", listToPy(numbers))
    print("Разворот:", listToString(listReverse(numbers)))
    print("Свёртка слева:", foldl(subtract, numbers, 0))
    print("Свёртка справа:", foldr(subtract, numbers, 0))
    print("Квадраты:", listToString(listMap(square, numbers)))
    print("Нечётные:", listToString(listFilter(isOdd, numbers)))
    print("Сумма квадратов нечётных:", sumOddSquares(numbers))
    print("Объединение:", listToString(listConcat(numbers, makeList(6, 7))))
    print("Замена:", listToString(listReplace(numbers, 2, 99)))
