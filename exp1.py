import ollama

name = "vowel_count"
prompt = "Count the number of vowels in a given string"
tests = [("sky",0),("pretty",1),("education",5),("light",1)]

response = ollama.generate(
    model = "qwen2.5-coder:7b",
    prompt = f"Create a python function {name} to {prompt}. Only return the function and do no use any markdown formatting such as ```python```"
)

code = response["response"].strip()
print("Generated Code:")
print(code)


#Testing
namespace = {}

try:
    exec(code,namespace)
    function = namespace[name]
    passed = 0

    for value,expected in tests:
        result = function(value)
        print(f"{value} -> {result} (EXPECTED {expected})")

        if(result == expected):
            print("PASS")
            passed +=1

        else:
            print("FAIL")


    print(f"TEST CASES PASSED: {passed}/{len(tests)}")
    print("Overall Result: ", "CORRECT" if(passed == len(tests)) else "INCORRECT")

except Exception as e:
    print("ERROR", e)