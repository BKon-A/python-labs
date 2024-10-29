# Task 2: Створити рекурсивну функцію fib(k), яка повертає список n чисел Фібоначчі. Написати програму яка виводить k чисел
#         Фібоначчі, використовуючи функцію fib(k)

def fib(k):
    if k == 0:
        return []
    elif k == 1:
        return [0]
    elif k == 2:
        return [0, 1]
    else:
        fibs = fib(k - 1)
        fibs.append(fibs[-1] + fibs[-2])
        return fibs