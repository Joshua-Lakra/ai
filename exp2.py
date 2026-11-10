
import ollama
import ast
import re

# Dataset
real_code_dataset = [
"""def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",

"""def bubble_sort(arr):
    for i in range(len(arr)-1):
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",

"""def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
    return arr""",

"""def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",

"""def bubble_sort(arr):
    for i in range(len(arr)-1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",

"""def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr""",

"""def bubble_sort(arr):
    for i in range(1, len(arr)):
        for j in range(len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",

"""def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(1, n-i):
            if arr[j-1] > arr[j]:
                arr[j-1], arr[j] = arr[j], arr[j-1]
    return arr""",

"""def bubble_sort(arr):
    n = len(arr)
    i = 0
    while i < n:
        j = 0
        while j < n-i-1:
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            j += 1
        i += 1
    return arr""",

"""def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr"""
]


# Generate Code
prompt = """# Write ONLY a Python function named bubble_sort(arr).
# Sort in ascending order using Bubble Sort.
# Return the sorted list.

def bubble_sort(arr):
"""

response = ollama.generate(
    model="codegemma:2b",
    prompt=prompt,
    options={
        "temperature": 0,
        "num_predict": 150,
        "stop": ["# Write", "def insertion_sort", "def selection_sort"]
    }
)

code = "def bubble_sort(arr):\n" + response["response"]

# Extract the generated function
try:
    tree = ast.parse(code)
    code = ast.get_source_segment(
        code, tree.body[0]
    )
except:
    code = ""

print("GENERATED CODE")
print(code)


# Test Cases
tests = [
    ([5, 3, 8, 4, 2], [2, 3, 4, 5, 8]),
    ([10, 1, 7, 3], [1, 3, 7, 10]),
    ([5, 5, 2, 1], [1, 2, 5, 5]),
    ([9, 8, 7, 6], [6, 7, 8, 9]),
    ([1], [1]),
    ([], [])
]


# Discriminator
def discriminator(code):

    try:
        ast.parse(code)
        syntax = True
    except:
        syntax = False

    if not syntax:
        return 0, 0, 0, 0

    namespace = {}

    try:
        exec(code, namespace)
        function = namespace["bubble_sort"]

        passed = 0

        for data, expected in tests:
            if function(data.copy()) == expected:
                passed += 1

        functional = passed == len(tests)

    except:
        functional = False

    algorithm = (
        "for" in code or "while" in code
    ) and "if" in code and ">" in code and "sorted(" not in code and ".sort(" not in code

    tokens = set(re.findall(r"[a-zA-Z_]+", code.lower()))

    similarity = 0

    for real_code in real_code_dataset:
        real_tokens = set(re.findall(r"[a-zA-Z_]+", real_code.lower()))

        if tokens | real_tokens:
            score = len(tokens & real_tokens) / len(tokens | real_tokens)
            similarity = max(similarity, score)

    similarity = round(similarity * 100, 2)

    final_score = 20 + functional * 40 + algorithm * 20 + similarity * 0.20

    return functional, algorithm, similarity, round(final_score, 2)


# Final Result
if code:
    functional, algorithm, similarity, score = discriminator(code)

    print("\nDISCRIMINATOR RESULT")
    print("Syntax: True")
    print("Functional:", functional)
    print("Algorithm:", algorithm)
    print("Similarity:", similarity, "%")
    print("Final Score:", score, "/ 100")

    print("RESULT:", "ACCEPTED" if score >= 80 else "REJECTED")

else:
    print("Code generation failed. Please run again.")
