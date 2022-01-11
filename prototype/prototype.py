# Prototypical - a style in which there is no concept of a class,
# and inheritance is performed by cloning an existing instance of an object - a prototype
import copy


class Address:

	def __init__(self, street_address, city, country):
		self.street_address = street_address
		self.city = city
		self.country = country

	def __str__(self):
		return f'{self.street_address}, {self.city}, {self.country}'


class Person:
	def __init__(self, name, address):
		self.name = name
		self.address = address

	def __str__(self):
		return f'{self.name} lives at {self.address}'


john = Person("John", Address("123 London Road", "London", "UK"))
print(john)
# jane = john
jane = copy.deepcopy(john)
jane.name = "Jane"
jane.address.street_address = "124 London Road"
print(john, '\n', jane)