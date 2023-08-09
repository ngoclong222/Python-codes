default_number = 2
user_number = int(input('Enter your number: '))
matches = default_number == user_number
# To compare two values, we use "==". To assign a value to a variable, we use "=".
print(f"Here is the result: {matches}.")

and_operator = user_number > 10 and user_number < 20
# In "and" operator, if the 1st value is false, return the 1st one.
# If the 1st one is true, return the 2nd one.
print(and_operator)

or_operator = user_number < 10 or user_number < 20
# In "or" operator, if the 1st value is true, return the 1st one.
# If the 1st one is false, return the 2nd one.
print(or_operator)

default_greeting = "there"
name = input("Enter your name (optinal): ")
user_name = name or default_greeting
print(f"Hello, {user_name}!")

print("bool(0) returns:", bool(0))
print("bool(non-zero numbers) return:", bool(2))
print("bool('empty string') returns:", bool(""))
print("bool('non-empty strings') return:", bool("Much"))
print("bool(empty list) returns:", bool([]))
print("bool(non-empty lists) return:", bool([2, 4, 6]))
