def first_element[T](elements: list[T]) -> T:  # T -> list[int]
    e = elements[0]
    return e


if __name__ == "__main__":
    numbers = [1, 2, 3]  # list[int]
    first_number = first_element(numbers)

    words = ["hello", "world"]  # list[str]
    first_word = first_element(words)
