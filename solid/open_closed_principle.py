# software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification

from enum import Enum

class Color(Enum):
	"""
	Generic Color.

	Derive from this class to define color
	"""

	RED = 1
	GREEN = 2
	BLUE = 3


class Size(Enum):
	"""
	Generic Size.

	Derive from this class to define size
	"""

	SMALL = 1
	MEDIUM = 2
	LARGE = 3


class Product:

	def __init__(self, name, color, size):
		self.name = name
		self.color = color
		self.size = size


class ProductFilter:

	def filter_by_color(self, products, color):
		for p in products:
			if p.color == color: yield p


class Specification:
	"""
	This class determines whether a particular element meets a certain criterion
	"""

	def is_satisfied(self, item):
		pass

	def __and__(self, other):
		return AndSpecification(self, other)


class Filter:
	"""
	we will expand the functionality and not modify the existing one
	"""

	def filter(self, items: list, spec):
		"""
		base class method but generic
        Args:
            items: products list
            spec: object

        Returns:
            Nothing.
		"""
		pass


class ColorSpecification(Specification):
	"""
	inherit from the class Specification and implement the functionality
	"""

	def __init__(self, color):
		self.color = color

	def is_satisfied(self, item):
		return item.color == self.color


class SizeSpecification(Specification):
	"""
	Inherit from the class Specification and implement the functionality
	"""

	def __init__(self, size):
		self.size = size

	def is_satisfied(self, item):
		return item.size == self.size


class AndSpecification(Specification):
	"""
	Combinator - a structure that combines other structures
	"""

	def __init__(self, *args):
		self.args = args # specifications

	def is_satisfied(self, item):
		"""
		we check whether the specification is satisfied,
		the product must meet each of the specifications.
		We use a lambda to check if the specification for this particular product meets
		:param item:
		:return:
		"""
		return all(map(
			lambda spec: spec.is_satisfied(item), self.args
		))


class BatterFilter(Filter):
	"""
	Filter implementation, Inherit from the class Filter
	"""

	def filter(self, items, spec):
		"""
		we look at each individual element and check if the element meets the specification requirement
		Args:
			items: products list
			spec: object

		Returns:
			yield item
		"""
		for item in items:
			if spec.is_satisfied(item):
				yield item

if __name__ == '__main__':
	apple = Product('Apple', Color.GREEN, Size.SMALL)
	tree = Product('Tree', Color.GREEN, Size.LARGE)
	house = Product('House', Color.BLUE, Size.LARGE)
	products = [apple, tree, house]
	bf = BatterFilter()

	print('Green products:')
	green = ColorSpecification(Color.GREEN)
	for p in bf.filter(products, green):
		print(f' - {p.name} is green')

	print("Large products:")
	large = SizeSpecification(Size.LARGE)
	for p in bf.filter(products, large):
		print(f' - {p.name} is large')

	print("Large blue items:")
	large_blue = large & ColorSpecification(Color.BLUE)
	for p in bf.filter(products, large_blue):
		print(f' - {p.name} is large and blue')