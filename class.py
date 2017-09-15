class Test:

	def __init__(self, num):
		self.num = num; # このクラスが持つnum関数に引数を格納
	def print_num(self):
		print('引数で渡された数字は{}です。'.format(self.num)) # {}にself.numを格納


class Test2(Test): # Testクラスを継承

	def print_test2_info(self):
		print('このクラスはTestクラスを継承しています')
		super().print_num() # 親クラスのprint_num()を呼び出す




test = Test2(10) # インスタンスを作成、ここで渡された引数が__init__のnumに渡される
test.print_test2_info()