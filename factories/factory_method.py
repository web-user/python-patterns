from math import sin, cos


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@staticmethod
	def new_cartesian_point(x, y):
		return Point(x, y)

	@staticmethod
	def new_polar_point(rho, theta):
		return Point(rho * sin(theta), rho * cos(theta))

	def __str__(self):
		return f'x: {self.x}, y: {self.y}'


if __name__ == '__main__':
	p = Point(2, 3)
	p2 = Point.new_polar_point(1,2)

	print(p, p2)