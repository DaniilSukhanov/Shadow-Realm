class Player():
	def __init__(self, health, money, name):
		self.health = health
		self.money = money
		self.name = name

	class Inventory():
		def __init__(self, inv):
			self.inv = []
