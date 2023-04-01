class Item():

	class Arrmor():
		def __init__(self, absorption, name):
			self.absorption = absorption
			self.name = name

	arrmor1 = Arrmor(0.95, "учебная броня")
	arrmor2 = Arrmor(0.9, "легкая броня")
	arrmor3 = Arrmor(0.75, "средняя броня")
	arrmor4 = Arrmor(0.5, "тяжелая броня")
	arrmor5 = Arrmor(0.25, "броня богов")

	class Weapon():
		def __init__(self, damage, name):
			self.damage = damage
			self.name = name

	weapon1 = Weapon(1, "палка")
	weapon2 = Weapon(3, "меч")
	weapon3 = Weapon(6, "топор")
	weapon4 = Weapon(9, "боевой топор")
	weapon5 = Weapon(15, "плазменный клинок")

	class Heal():
		def __init__(self, healing, name):
			self.healing = healing
			self.name = name

	heal1 = Heal(1, "подорожник")
	heal2 = Heal(5, "зелье здоровья")
	heal3 = Heal(10, "звездочка")
