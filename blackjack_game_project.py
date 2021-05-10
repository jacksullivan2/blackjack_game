# BLACKJACK GAME --- To be played in the terminal window ---
from random import choice

class BlackJack:
	"""Model a player vs dealer (1 vs 1) BlackJack game"""
	def __init__(self, player_name, money, current_pot=0.00):
		"""Initialise the game's attributes"""
		self.player_name = name
		self.dealer_balance = money 
		self.player_balance = money
		self.current_pot = 0.00
		self.last_hand_outcome = ""
		
		# Set each players intial hand to have a nominal value of 0
		self.dealers_hand = 0
		self.players_hand = 0
		self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11]

	def opening_message(self):
		"""Display the dealer's welcome message to the players"""
		print(f"Welcome to the game, {name.title()}. I am the dealer.\n" 
		"I will equal the amount you place into the pot for each hand. Good Luck!\n")

	def deal_players_inital_hand(self):
		"""Deal the player's initial hand"""
		card1 = choice(self.cards)
		card2 = choice(self.cards)
		self.players_hand += (card1 + card2) 
		print(f"Your hand: {self.players_hand}")

	def deal_dealers_initial_hand(self):
		"""Deal the dealers' initial hand"""
		card3 = choice(self.cards)
		card4 = choice(self.cards)
		self.dealers_hand += (card3 + card4) 
		print(f"Dealer's hand: {self.dealers_hand}")

	def stake_and_fill_pot(self):
		"""Ask how much the player would like to place into the pot for this hand. The dealer will match it. 
			Temporarily remove the the stake from the player and dealer's balance. Fill the pot"""
		stake = input("Place an amount into the pot (minimum £2): £ ")
		stake = float(stake)
		if stake < 2:
			print("You need to place more into the pot")	
		else:
			self.player_balance = self.player_balance - stake
			self.dealer_balance = self.dealer_balance - stake

		self.current_pot = stake*2
		print(f"\nCURRENT POT: £{self.current_pot}")


	def stick_twist(self):
		twist = True
		while twist:
			decision = input("Would you like to stick or twist?: ")
			if decision == 'stick':
				twist = False
				print(f"\nYou have stuck on {self.players_hand}")
			elif decision == 'twist':
				self.players_hand += choice(self.cards)
				print(f"Current hand: {self.players_hand}")
				if self.players_hand > 21:
					print("BUST")
					break
				else:
					continue

	def simulate_dealer_playing(self):
		"""Simulate the dealer playing the game in response to the Player's final hand"""
		print("The dealer is now playing")
		while True:
		
			if (22 > self.dealers_hand >= 15 ) and (self.dealers_hand >= self.players_hand):
				print(f"\nThe dealer has stuck on: {self.dealers_hand}")
				break

			elif (self.dealers_hand < 14) or (self.dealers_hand < self.players_hand):
				self.dealers_hand += choice(self.cards)
				print(f"Dealers hand: {self.dealers_hand}")
				continue
			elif self.dealers_hand > 21:
				print("\nTHE DEALER HAS BUSTED")
				break


	def result(self):
		"""State the result of the hand."""
		if (self.players_hand > self.dealers_hand) and (self.players_hand <= 21):
			print("You have won this hand!!!")
			self.player_balance += self.current_pot
		
		elif (self.players_hand <= 21) and (self.dealers_hand > 21):
			print("You have won this hand!!!")
			self.player_balance += self.current_pot

		elif self.players_hand == self.dealers_hand or (self.players_hand > 21 and self.dealers_hand > 21):
			print("This hand was a draw. The pot will roll over")
			self.last_hand_outcome = 'draw' 

		elif (self.players_hand < self.dealers_hand) and (self.dealers_hand <=21):
			print("The dealer won this hand!")
			self.dealer_balance += self.current_pot

		elif (self.dealers_hand <= 21) and (self.players_hand > 21):
			print("The dealer won this hand.")
			self.dealer_balance += self.current_pot


	def new_balances(self):
		"""State the new current balances."""
		print(f"\nPlayer Balance: {self.player_balance}")
		print(f"Dealer Balance: {self.dealer_balance}")


	def reset(self):
		"""Reset the nominal values of the hands and the current pot (as long as the last hand was won)"""
		self.dealers_hand = 0
		self.players_hand = 0
		print("\nThe hands have been reset")
		if self.last_hand_outcome == 'draw':
			money = self.current_pot
		else:
			self.current_pot = 0.0







# Introductory phase of the game 
name = input("Please enter your username: ")
print(f"Welcome, {name.title()}")
money = input("How much moeny would you like to deposit into your games account: £")
money = float(money)
if money < 0:
	print("You can't withdraw money at this moment.")
else:
	print(f"£{money} has been deposited into your account.")


while True:
	opening_question = input(f"\n{name}, would you like to play BlackJack vs the Dealer(y/n): ")
	if opening_question == 'n':
		break 
	elif opening_question == 'y':
		
		game = BlackJack(name, money)
		game.opening_message()
		game.deal_players_inital_hand()
		game.deal_dealers_initial_hand()
		game.stake_and_fill_pot()
		game.stick_twist()	
		game.simulate_dealer_playing()
		game.result()
		game.new_balances()
		game.reset()
