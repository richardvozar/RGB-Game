import tkinter as tk
from PIL import ImageColor
from random import randint


"""
TODO:
	- mode-ok elkeszitese (easy, medium, hard)
		- easy: csak 64-esével lehet tippelni (0, 63, 127, 191, 255)
		- medium: csak 32-esével
		- hard: csak 16-osával
		- expert: az összes
	- scoreboard elkeszitese (.txt alapu maybe?)
	- pontszamok kerekitese (maybe?)
	- esztetikumot varazsolni a feluletre
	- minden tip utan mutassa, hogy hogy nez ki az a szin amire tippelt, ahhoz kepest, ami volt valojaban
"""




# converting color codes
def hex_to_rgb(hex):
	return ImageColor.getcolor(hex, 'RGB')

def rgb_to_hex(rgb):
	return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])




# GLOBAL GAME VARIABLE
# todo !!! --> if True, ne tudjon új játékot indítani!!
INGAME = False


# main menu
class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()

		# configure the main window
		self.title('RGB Game')
		self.geometry('500x500+500+200')

		# title at the top
		self.label_title = tk.Label(self, text='RGB Game', font=('italic', 18))
		self.label_title.place(x=180, y=10)

		# entry for the name
		self.entry_name_text = tk.Label(self, text='Name', font=('italic', 11))
		self.entry_name_text.place(x=80, y=50)
		self.entry_name = tk.Entry(self, width=40)
		self.entry_name.place(x=130, y=53)

		# button start game
		self.button_start_game = tk.Button(self, text='START GAME', font=('italic', 15), command=self.start_game)
		self.button_start_game.place(x=180, y=80)

		# listbox for the difficulty
		self.difficulty_text = tk.Label(self, text='Difficulty', font=('italic', 14))
		self.difficulty_text.place(x=180, y=150)
		
		self.difficulties = ['EASY', 'MEDIUM', 'HARD', 'IMPOSSIBLE']
		self.listbox_difficulty = tk.Listbox(self, height=len(self.difficulties), width=11, font=('italic', 13), selectbackground='darkgreen')
		for i in range(len(self.difficulties)):
			self.listbox_difficulty.insert(i, self.difficulties[i])
		self.listbox_difficulty.activate(0)
		self.listbox_difficulty.place(x=180, y=180)

		# button scoreboard
		self.button_scoreboard = tk.Button(self, text='SCOREBOARD', font=('italic', 15))
		self.button_scoreboard.place(x=180, y=330)

		# button exit game
		self.button_exit_game = tk.Button(self, text='EXIT GAME', font=('italic', 15), command=self.quit)
		self.button_exit_game.place(x=180, y=400)

		# TEST BUTTON
		self.test_button = tk.Button(self, text='TEST', command=self.test_btn)
		self.test_button.place(x=200, y=450)

	# METHOTDS
	def test_btn(self):
		selection = self.listbox_difficulty.curselection()
		try:
			idx = selection[0]
		except:
			idx = 0
		value = self.listbox_difficulty.get(idx)

		return idx


	def start_game(self):
		# 0: easy, 1: medium, 2: hard, 3: impossible
		mode = self.test_btn()

		if mode == 0:
			game = GameWindowEasy(self.entry_name.get())
		elif mode == 1:
			game = GameWindowMedium(self.entry_name.get())
		elif mode == 2:
			game = GameWindowHard(self.entry_name.get())
		elif mode == 3:
			game = GameWindowImpossible(self.entry_name.get())
		else:
			print('wat')




# game window
class GameWindowImpossible(tk.Tk):
	def __init__(self, name, mode):
		super().__init__()

		self.name = name

		self.guesses = {} # for saving the guesses
		self.scores = {} # for saving the differences
		self.score = 0
		self.round = 1
		self.color_to_guess = [randint(0, 255), randint(0, 255), randint(0, 255)]
		#print(f'first round: {self.color_to_guess}')

		# configure the window
		self.title('RGB Game')
		self.geometry('500x500+500+200')

		# title at the top
		self.label_title = tk.Label(self, text=f'Round {self.round}', font=('italic', 18))
		self.label_title.place(x=180, y=10)

		# canvas for the color
		self.canvas = tk.Canvas(self, width=300, height=300, bg=f'{rgb_to_hex(self.color_to_guess)}')
		self.canvas.place(x=100, y=50)

		#-- labels and entries --#
		
		# RED
		self.label_red = tk.Label(self, text='RED', font=('italic', 15))
		self.label_red.place(x=100, y=360)
		self.entry_red = tk.Entry(self, width=10)
		self.entry_red.place(x=90, y=390)
		# GREEN
		self.label_green = tk.Label(self, text='GREEN', font=('italic', 15))
		self.label_green.place(x=200, y=360)
		self.entry_green = tk.Entry(self, width=10)
		self.entry_green.place(x=205, y=390)
		# BLUE
		self.label_blue = tk.Label(self, text='BLUE', font=('italic', 15))
		self.label_blue.place(x=330, y=360)
		self.entry_blue = tk.Entry(self, width=10)
		self.entry_blue.place(x=330, y=390)

		# button ACCEPT
		self.button_accept = tk.Button(self, text='ACCEPT', font=('italic', 17), command=self.next_round)
		self.button_accept.place(x=180, y=430)


	def next_round(self):

		# saving the scores
		self.guesses[self.round] = [self.color_to_guess, [int(self.entry_red.get()), int(self.entry_green.get()), int(self.entry_blue.get())]]

		self.scores[self.round] = [ abs(self.color_to_guess[0] - self.guesses[self.round][1][0]),
									abs(self.color_to_guess[1] - self.guesses[self.round][1][1]),
									abs(self.color_to_guess[2] - self.guesses[self.round][1][2])]

		print(f'Round: {self.round}\nColor: {self.color_to_guess}\nGuess: {self.guesses[self.round][1]}\nDiff: {self.scores[self.round]}')


		# show the player the color he/she guessed
		scw = ShowingColorsWindow(self.color_to_guess, self.guesses[self.round][1], self.scores[self.round])


		# check if the round equals to 10
		if self.round == 10:
			
			self.destroy()

			diffs = 0

			for s in self.scores.values():
				diffs += sum(s)

			self.score = 10 * 256 * 3 - diffs

			end_score_window = EndScoreWindow(self.name, self.score)
			return


		# configuring the next round
		self.entry_red.delete(0, 'end')
		self.entry_blue.delete(0, 'end')
		self.entry_green.delete(0, 'end')
		

		self.round += 1
		self.color_to_guess = [randint(0, 255), randint(0, 255), randint(0, 255)]

		#print(f'{self.color_to_guess}')

		self.label_title.configure(text=f'Round {self.round}')
		self.canvas.configure(bg=f'{rgb_to_hex(self.color_to_guess)}')






# end of the game score
class EndScoreWindow(tk.Tk):
	def __init__(self, name, score):
		super().__init__()

		# configure the window
		self.title('RGB Game')
		self.geometry('500x500+500+200')

		self.label_name = tk.Label(self, text=f'{name}', font=('italic', 30))
		self.label_name.place(x=50, y=50)

		self.label_score = tk.Label(self, text='Score:', font=('italic', 30))
		self.label_score.place(x=50, y=150)

		self.label_score_num = tk.Label(self, text=f'{score}', font=('italic', 30))
		self.label_score_num.place(x=200, y=150)

		self.button_destroy = tk.Button(self, text='CLOSE', font=('italic', 17), command=self.destroy)
		self.button_destroy.place(x=200, y=400)

		

# showing the player the original and the guessed color
class ShowingColorsWindow(tk.Tk):
	def __init__(self, original, guessed, difference):
		super().__init__()

		# configure the window
		self.title('RGB Game')
		self.geometry('300x300+500+200')

		# original
		self.label_original = tk.Label(self, text='Original Color', font=('italic', 13))
		self.label_original.place(x=15, y=15)

		self.label_original_r = tk.Label(self, text='R', font=('italic', 13))
		self.label_original_r.place(x=30, y=150)

		self.label_original_g = tk.Label(self, text='G', font=('italic', 13))
		self.label_original_g.place(x=65, y=150)

		self.label_original_b = tk.Label(self, text='B', font=('italic', 13))
		self.label_original_b.place(x=100, y=150)

		self.canvas_original = tk.Canvas(self, width=100, height=100, bg=f'{rgb_to_hex(original)}')
		self.canvas_original.place(x=25, y=50)

		self.og_r_value = tk.Label(self, text=f'{original[0]}', font=('italic', 13))
		self.og_r_value.place(x=26, y=170)

		self.og_g_value = tk.Label(self, text=f'{original[1]}', font=('italic', 13))
		self.og_g_value.place(x=59, y=170)

		self.og_b_value = tk.Label(self, text=f'{original[2]}', font=('italic', 13))
		self.og_b_value.place(x=94, y=170)

		# guessed
		self.label_guessed = tk.Label(self, text='Guessed Color', font=('italic', 13))
		self.label_guessed.place(x=165, y=15)

		self.label_guessed_r = tk.Label(self, text='R', font=('italic', 13))
		self.label_guessed_r.place(x=175, y=150)

		self.label_guessed_g = tk.Label(self, text='G', font=('italic', 13))
		self.label_guessed_g.place(x=210, y=150)

		self.label_guessed_b = tk.Label(self, text='B', font=('italic', 13))
		self.label_guessed_b.place(x=245, y=150)

		self.canvas_guessed = tk.Canvas(self, width=100, height=100, bg=f'{rgb_to_hex(guessed)}')
		self.canvas_guessed.place(x=170, y=50)

		self.gu_r_value = tk.Label(self, text=f'{guessed[0]}', font=('italic', 13))
		self.gu_r_value.place(x=169, y=170)

		self.gu_g_value = tk.Label(self, text=f'{guessed[1]}', font=('italic', 13))
		self.gu_g_value.place(x=204, y=170)

		self.gu_b_value = tk.Label(self, text=f'{guessed[2]}', font=('italic', 13))
		self.gu_b_value.place(x=239, y=170)

		# difference
		self.label_diff = tk.Label(self, text=f'Difference\nR:{difference[0]}    G:{difference[1]}    B:{difference[2]}', font=('italic', 10))
		self.label_diff.place(x=80, y=210)

		# button
		self.button_close = tk.Button(self, text='CLOSE', font=('italic', 13), command=self.destroy)
		self.button_close.place(x=100, y=260)
		
		
	

		







if __name__ == '__main__':
	main_window = MainWindow()
	main_window.mainloop()