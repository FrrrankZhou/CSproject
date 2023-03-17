import random as r
import keyboard
import os
import json
from math import log2
from colorama import *


init(autoreset=True)
side_length: int
score: int
field: list[list[int]]
drawing: str
pool: list[int]


def get_empty() -> list[tuple[int, int]]:  # 记录所有0
	return [(i, j) for j in range(side_length) for i in range(side_length) if field[i][j] == 0]


def output():  # 显示数组
	power: int
	row: list[int]
	print(f"your score: {Style.BRIGHT+Fore.YELLOW+str(score)}")
	print('-' * 16 * side_length)
	for row in field:
		print('|'+'|'.join(['\t\t']*side_length)+"|")
		print('|', end='\t')
		for x in row:
			if x:
				power = round(log2(x))
				print(f'\033[1;4{power//8};3{power%8}m{x}', end='\t|\t')
			else:
				print(x, end='\t|\t')
		print()
		print('|' + '|'.join(['\t\t'] * side_length) + "|")
		print('-'*16*side_length)


def left():  # 按行合并
	row: int
	for row in range(side_length):
		merge(row)


def right():  # 相当于mirror后左移
	row: int
	for row in range(side_length):
		field[row].reverse()
		merge(row)
		field[row].reverse()


def up():  # 相当于转置后再左移
	transpose()
	left()
	transpose()


def down():  # 相当于转置后再右移
	transpose()
	right()
	transpose()


def is_game_over() -> bool:  # 判断游戏是否结束
	zeros: list
	for i in range(side_length):
		for c in range(side_length - 1):
			# 判断是否还可以走
			zeros = get_empty()
			if zeros:
				return False
			# 判断是否还可以相加
			if field[i][c] == field[i][c + 1] or field[c][i] == field[c + 1][i]:
				return False
	return True


def game_over_discriminant():  # 游戏结束的判断与输出
	if is_game_over():
		print(Style.BRIGHT+Fore.RED+"Game Over")
		print(drawing)
		print("press x to stop or press r to restart")


def manipulate(procedure):  # 每一个输入带来的操作
	row: int
	os.system('cls')
	procedure()
	if any(0 in row for row in field):
		gen()
	output()

	game_over_discriminant()


def reset_board():  # 清空当前游戏的数组
	os.system('cls' if os.name in ('nt', 'dos') else 'clear')
	global score  # by ref
	global field  # by ref
	score = 0
	field = [[0 for _ in range(side_length)] for _ in range(side_length)]
	for _ in range(2):
		gen()
	output()


def transpose():  # 矩阵转置
	col: int
	row: int
	for col in range(1, side_length):
		for row in range(col, side_length):
			field[row][col - 1], field[col - 1][row] = field[col - 1][row], field[row][col - 1]


def merge(row: int):  # 合并一行并向左移动
	i: int
	global score  # by ref
	move_zero_to_end(row)  # 左移操作
	for i in range(side_length - 1):
		if field[row][i] == 0:
			break
		if field[row][i] == field[row][i + 1]:
			score += field[row][i]
			field[row][i] += field[row][i]
			field[row].pop(i + 1)
			field[row].append(0)


def move_zero_to_end(row: int):
	# 在有0的情况下左移
	i: int
	for i in range(side_length - 1, -1, -1):
		if field[row][i] == 0:
			field[row].pop(i)
			field[row].append(0)


def gen():  # 随机生成
	zeros: list[tuple[int, int]]
	pos: [int, int]
	num: int
	zeros = get_empty()
	num = 2 ** r.choice(pool)
	pos = r.choice(zeros)
	field[pos[0]][pos[1]] = num


# 读取json，没有就初始化一个
try:
	with open('customizable_data.json', 'r') as f:
		temp = json.load(f)
		pool = temp["possible random result (please write only n in 2^n)"]
		side_length = temp["side length of game board"]
except FileNotFoundError:
	pool = [1, 2]
	side_length = 4
	stack = {"possible random result (please write only n in 2^n)": pool, 'side length of game board': side_length}
	with open('customizable_data.json', 'w') as f:
		json.dump(stack, f, indent=2)
# 初始化
score = 0
field = [[0 for _ in range(side_length)] for _ in range(side_length)]
keyboard.add_hotkey('w', manipulate, [up])
keyboard.add_hotkey('s', manipulate, [down])
keyboard.add_hotkey('a', manipulate, [left])
keyboard.add_hotkey('d', manipulate, [right])
keyboard.add_hotkey('r', reset_board)
print('Welcome to 4096!')
drawing = """
    *!%86*^               . ^~a3ovo*~*.
 -&@@@@@@@@@@$~   . *3#@%o+              a#!v.   .++8@@@@@#@%;
 *#@@@@@@@@@@@@@@$&vo..                       .a&*~#@@@@@@@@@@#@
 n@@@@@@@@@@@@@@@!.                                1#@@@@@@@@@@@@@z
#@@@@@@@@@@@@@@v                                 .  a&#@@@@@@@@@@#-
@@@@@@@@@@@@#;                                      .+@@@@@@@@@@@@%
&@@@@@@@@@@@1                           .             -%@@@@@@@@@@$
 #@@@@@@@@#&*                      *u&&#$61o*           -#@@@@@@@@@3
 6#@@@@@@%.                 -.. . -vua1n;^~*            .$#@@@@@@$
  ..#@@@@!-           .~a6&@@&!v+  *oo+  . .            ..+@@@@#&;
    6##@v          +u#@&661i631u+.+^oi!!#&i*             .*@@#~.
     +3          -oaz^    +n*+-      -ai.                 &*
     .a^          -oo-^1#@@@1-.        .                  .;@
     i!.           ..13^-o^.            .-                  6z
     #^                       .^-        +1!                ;@
     1o                       -1-   .*ono1o+^uz+.             $
   -#-                      +33au%#@@#@!v..  ..*+            8
    1i                      .v;. .-^---. . .    -           .-n#-
 .^#@1                  .*~oo~;-  ..o3$##$&#@*                -@#8.
-&@@@+                  .*~;nvno+.8#&u~o11$@#^                -@@@#;
@@@@@i                    +-+on~~a@#@8av^. +                  ;@#@@@
@@@@@@^                    -+;oo;+.-.      -;-                u@&@@@&
@@@@@@#v .                 -^;;~~;;ou%&$$###!^.              *$@@@@@##.
@@@@@@@@@^                   ^^;~oo;;^.^^++*.              .#@@@@@@@@#;
@@@@@@@@#@6-                    .-++..+++-.               u##@@@@@@@@##
@@@@@@@@@@#@#z                      .                . .3##@@@@@@@@@@@@
@@@@@@@@@@@@@@@#a                                  *i@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@##&3;..                       +1#@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@#8v~~+;on66888&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""
print(drawing)
print('press r to start')
keyboard.wait('x')
