# BLACKJACK GAME --- To be played in the terminal window ---
import random

class BlackJack:
	"""Model a player vs dealer (1 vs 1) BlackJack game"""
	def __init__(self, name, player_money, dealer_money, current_pot=0.00):
		"""Initialise the game's attributes"""
		self.player_name = name
		self.dealer_balance = dealer_money 
		self.player_balance = player_money
		self.current_pot = current_pot
		
		# Set each players intial hand to have a nominal value of 0
		self.dealers_hand = 0
		self.players_hand = 0
		self.cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 
		8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11]

	def opening_message(self):
		"""Display the dealer's welcome message to the players"""
		print(f"Welcome to the game, {name.title()}. I am the dealer.\n" 
		"I will equal the amount you place into the pot for each hand. Good Luck!\n")

	def deal_players_inital_hand(self):
		"""Deal the player's initial hand"""
		random.shuffle(self.cards)
		card1 = self.cards.pop(random.randrange(len(self.cards)))
		card2 = self.cards.pop(random.randrange(len(self.cards)))	
		self.players_hand += (card1 + card2) 
		print(f"Your hand: {self.players_hand}")

	def deal_dealers_initial_hand(self):
		"""Deal the dealers' initial hand"""
		random.shuffle(self.cards)
		card3 = self.cards.pop(random.randrange(len(self.cards)))
		card4 = self.cards.pop(random.randrange(len(self.cards)))	
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

		self.current_pot = self.current_pot + stake*2
		print(f"\nCURRENT POT: £{self.current_pot}")
		print(f"\nPlayer Current Balance: {self.player_balance}")
		print(f"Dealer Current Balance: {self.dealer_balance}")


	def stick_twist(self):
		twist = True
		while twist:
			decision = input("Would you like to stick or twist?: ")
			if decision == 'stick':
				twist = False
				print(f"\nYou have stuck on {self.players_hand}")
			elif decision == 'twist':
				additional_card = self.cards.pop(random.randrange(len(self.cards)))
				self.players_hand += additional_card
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
		
			if (22 > self.dealers_hand >= 15) and (self.dealers_hand >= self.players_hand):
				print(f"\nThe dealer has stuck on: {self.dealers_hand}")
				break

			elif (self.dealers_hand < 14) or (self.dealers_hand < self.players_hand):
				extra_card = self.cards.pop(random.randrange(len(self.cards)))
				self.dealers_hand += extra_card
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


	def reset_or_continue_game(self):
		"""Reset the nominal values of the hands and the current pot (as long as the last hand was won)"""
		self.dealers_hand = 0
		self.players_hand = 0
		print("\nThe hands have been reset")
		if self.last_hand_outcome == 'draw':
			self.current_pot = self.current_pot	
		else:
			self.current_pot = 0.0

		play_on = input("Would you like to continue playing(y/n)? ")
		if play_on == 'n':
			exit()
		elif play_on == 'y':
			new_game = BlackJack(name, self.player_balance, self.dealer_balance, self.current_pot)




# Introductory phase of the game
name = input("Please enter your name: ")
print(f"Welcome, {name.title()}")
player_money = input("How much money would you like to deposit into your games account: £")
player_money = float(player_money)
if player_money < 0:
	print("You can't enter a negative amount of money.")
else:
	print(f"£{player_money} has been deposited into your account.")
# Set the dealers money equal to the players money (at the beginning of the game) 
dealer_money = player_money

opening_question = input(f"\n{name}, would you like to play BlackJack vs the Dealer(y/n): ")
if opening_question == 'n':
		exit() 
elif opening_question == 'y':
		game = BlackJack(name, player_money, dealer_money)
		game.opening_message()
while True:
	game.deal_players_inital_hand()
	game.deal_dealers_initial_hand()
	game.stake_and_fill_pot()
	game.stick_twist()	
	game.simulate_dealer_playing()
	game.result()
	game.new_balances()
	game.reset_or_continue_game()


