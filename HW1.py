print "Subatomic Physics"

x = 1
if x == 1:
	print "X is 1."

int1 = 1
float1 = 1.0
float2 = float(1)
string1 = 'string'
string2 = "string"
string3 = "Double quotes: Don't worry about apostrophes"

one = 1
two = 2
three = one + two

hello = "hello"
world = "world"
helloworld = hello + " " + world

# Multiple assignment:
a,b=3,4

mylist = []
mylist.append(1)
mylist.append(2)
mylist.append(3)
print(mylist[0]) # prints 1
print(mylist[1]) # prints 2
print(mylist[2]) # prints 3

# prints out 1,2,3
for x in mylist:
    print x

# This prints out "Hello, John!"
name = "John"
print "Hello, %s!" % name

# This prints out "John is 23 years old."
name = "John"
age = 23
print "%s is %d years old." % (name, age)

# This prints out: A list: [1, 2, 3]
newlist = [1,2,3]
print "A list: %s" % newlist

# another example
data = ("John", "Doe", 53.44)
format_string = "Hello %s %s.  Your balance is %.2f"

print format_string % data

""" is a multi-line comment.
%s - String (or any object with a string representation, like numbers)
%d - Integers
%f - Floating point numbers
%.<number of digits>f - Floating point numbers with a fixed amount of digits to the right of the dot.
%x/%X - Integers in hex representation (lowercase/uppercase)

"""

astring = "Hello world!"
print len(astring)
print astring.index("o")
print astring.count("l")
print astring[3:7]
print astring.upper()
print astring.lower()
print astring.startswith("Hello")
print astring.endswith("asdfasdfasdf")
afewwords = astring.split(" ")