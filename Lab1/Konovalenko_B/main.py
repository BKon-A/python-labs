from task1_prime import is_prime;
from task2_fibonacci import fib;

def main():

    try:
        a = int(input("Enter a: "))
        b = int(input("Enter b: "))
        if (a or b) <= 1:
            raise BufferError
    except BufferError:
        print("Please, enter a number greater than 1!")
        return
    except ValueError:
        print("Please, enter a number!")
        return
    
    print(f"\nPrime numbers between {a} and {b}:")
    is_prime(a, b)
    
    try:
        k = int(input("\nEnter k: "))
        if k < 0:
            raise ValueError
    except ValueError:
        print("Please, enter a positive number!")
        return
    
    print(f"The first {k} Fibonacci numbers are:")
    print(fib(k))

if __name__ == "__main__":
    main()