string_1 = 'Hello "World"!'  # Single quotation mark (SQM) in case there are DQMs in the string
print(string_1)

string_2 = "Hello. It's me"  # Double quotation mark (DQM) in case there are SQMs in the string
print(string_2)

string_3 = "He said that \"He love me\""  # Use backslash \ before a character to remove meaning
print(string_3)

age_1 = '26'
print('You are ' + age_1)  # Print out a string and a variable including another string

age_2 = 26
string_4 = str(age_2)  # Convert data type from number to string, then connect to another string
print("I'm also " + string_4)

height = 162
print(f'Your height is {height}' + ' cm')
# Use f"string + {variable}". Curly braces {} can help format a variable to string type
# We can use f-strings like this: f"""strings""" (That's called multi-line quotation mark)

name_1 = 'Terry'
greeting_1 = 'How are you, {}?'
terry_greeting = greeting_1.format(name_1)
# Format things inside the curly braces of a variable by putting another variable into {}
# If we have multi-curly braces with different values, the program will execute formatting in order
print(terry_greeting)

greeting_2 = 'How do you do, {name_2}?'
# Include a variable name into {}, then format the variable greeting_2 manually as following
bonnie_greeting = greeting_2.format(name_2='Bonnie')
print(bonnie_greeting)

my_name = 'Long'
your_name = input('Enter your name: ')  # Input data from user. Data type is always string
print(f'Hello {your_name}, my name is {my_name}.')

age = int(input('Enter your age: '))  # Use int() to change the data type from string to number
print(f'You have lived for {age * 12} months.')
