# Task 1: Програма для виводу всіх простих чисел, які розташовані між числами a та b, які задає користувач (не обов'язково a<b)

def is_prime(a, b):
    if a > b:
        a, b = b, a

    for i in range(a, b + 1):
        if i > 1:
            for j in range(2, int(i ** 0.5) + 1):
                if i % j == 0:
                    break
            else:
                print(i)