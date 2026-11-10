
import ollama
import ast
import re

# 1. REAL CODE DATASET (10 SAMPLES)

real_code_dataset = [
"""def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
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
    n = len(arr)
    for i in range(n-1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",

"""def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
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
    return arr"""
]


# 2. GENERATE CODE USING CODEGEMMA

def generate_code():

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
            "stop": [
                "# Write",
                "def insertion_sort",
                "def selection_sort"
            ]
        }
    )

    code = "def bubble_sort(arr):\n" + response["response"]

    try:
        tree = ast.parse(code)

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if node.name == "bubble_sort":
                    return ast.get_source_segment(code, node)

        return ""

    except SyntaxError:
        return ""


# 3. CHECK SYNTAX

def check_syntax(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# 4. TEST FUNCTIONALITY

def test_code(code):

    namespace = {}

    tests = [
        ([5, 3, 8, 4, 2], [2, 3, 4, 5, 8]),
        ([10, 1, 7, 3], [1, 3, 7, 10]),
        ([5, 5, 2, 1], [1, 2, 5, 5]),
        ([9, 8, 7, 6], [6, 7, 8, 9]),
        ([1], [1]),
        ([], [])
    ]

    try:
        exec(code, namespace)
        bubble_sort = namespace["bubble_sort"]

        for data, expected in tests:
            if bubble_sort(data.copy()) != expected:
                return False

        return True

    except Exception:
        return False


# 5. CHECK BUBBLE SORT ALGORITHM

def check_algorithm(code):

    code = code.lower()

    return (
        "def bubble_sort" in code
        and ("for" in code or "while" in code)
        and "if" in code
        and ">" in code
        and ".sort(" not in code
        and "sorted(" not in code
    )


# 6. CALCULATE SIMILARITY

def calculate_similarity(code):

    tokens = set(re.findall(r"[a-zA-Z_]+", code.lower()))

    if not tokens:
        return 0

    best = 0

    for real_code in real_code_dataset:

        real_tokens = set(
            re.findall(r"[a-zA-Z_]+", real_code.lower())
        )

        score = len(tokens & real_tokens) / len(tokens | real_tokens)

        best = max(best, score)

    return round(best * 100, 2)


# 7. DISCRIMINATOR

def discriminator(code):

    syntax = check_syntax(code)

    if not syntax:
        return {
            "syntax": False,
            "functional": False,
            "algorithm": False,
            "similarity": 0,
            "score": 0
        }

    functional = test_code(code)
    algorithm = check_algorithm(code)
    similarity = calculate_similarity(code)

    score = (
        20
        + functional * 40
        + algorithm * 20
        + similarity * 0.20
    )

    return {
        "syntax": syntax,
        "functional": functional,
        "algorithm": algorithm,
        "similarity": similarity,
        "score": round(score, 2)
    }


# 8. MAIN PROGRAM

print("CODEGEMMA - BUBBLE SORT GENERATOR")
print("=" * 45)

print("Real Dataset Size:", len(real_code_dataset))

code = generate_code()

if not code:
    print("\nCode generation failed. Please run again.")
    exit()

print("\nGenerated Code:")
print(code)

result = discriminator(code)

print("\nDISCRIMINATOR RESULT")
print("-" * 45)

print("Syntax:", result["syntax"])
print("Functional:", result["functional"])
print("Algorithm:", result["algorithm"])
print("Similarity:", result["similarity"], "%")
print("Final Score:", result["score"], "/ 100")

if result["score"] >= 80:
    print("\nRESULT: ACCEPTED")
else:
    print("\nRESULT: REJECTED")
