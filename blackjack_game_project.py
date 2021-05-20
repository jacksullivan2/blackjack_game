# BLACKJACK GAME --- To be played in the terminal window ---
import random
import mysql.connector
import jack_passwords

db = mysql.connector.connect(
	host='localhost',
	user='root',
	password=jack_passwords.mysql_server_password(),
	database='blackjack')

class BlackJack:
	"""Model a player vs dealer (1 vs 1) BlackJack game"""
	def __init__(self, name, player_money, dealer_money, current_pot=0.00):
		"""Initialise the game's attributes"""
		self.player_name = name
		self.dealer_balance = dealer_money 
		self.player_balance = player_money
		self.current_pot = current_pot
		self.last_hand_outcome = ""
		self.player_card_one_ace = False
		self.player_card_two_ace = False
		self.dealer_card_one_ace = False
		self.dealer_card_two_ace = False
		
		# Set each players intial hand to have a nominal value of 0
		self.dealers_hand = 0
		self.players_hand = 0
		self.cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 
		8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
		'A', 'A', 'A', 'A']

	def opening_message(self):
		"""Display the dealer's welcome message to the players, and the rules of the game"""
		print(f"\nWelcome to the game, {name.title()}. I am the dealer.\n" 
		"I will equal the amount you place into the pot for each hand.\n"
		"\nRemember the rules:-\t Highest hand under or equal to 21 wins"
		"-\tYour hand must be atleast 16 to win \n The first to bankrupt the opponent wins. \n Good luck!")


	def deal_players_inital_hand(self):
		"""Deal the player's initial hand"""
		random.shuffle(self.cards)
		card1 = self.cards.pop(random.randrange(len(self.cards)))
		card2 = self.cards.pop(random.randrange(len(self.cards)))	
		
		# Handle for potential Ace in the first card 
		if card1 == 'A':
			print(f"\nYou have been delt: {card1} {card2}")
			ace_choice = input("\nWould you like your first card as a 1 or 11?  ")
			ace_choice1 = int(ace_choice)
			if ace_choice1 == 1:
				card1 = 1
			elif ace_choice1 == 11:
				card1 = 11
				self.player_card_one_ace = True
		# Handle for potential Ace in the second card		
		if card2 == 'A':
			print(f"\nYou have been delt: {card1} {card2}")
			ace_choice2 = input("Would you like your second card as a 1 or 11? ")
			ace_choice2 = int(ace_choice2)
			if ace_choice2 == 1:
				card2 = 1
			elif ace_choice2 == 11:
				card2 = 11
				self.player_card_two_ace = True

		self.players_hand += (card1 + card2) 
		print(f"\n\tYOUR HAND: {self.players_hand}")

	
	def deal_dealers_initial_hand(self):
		"""Deal the dealers' initial hand, and define the dealer's strategy"""
		random.shuffle(self.cards)
		card3 = self.cards.pop(random.randrange(len(self.cards)))
		card4 = self.cards.pop(random.randrange(len(self.cards)))
		# The dealer will interpret their first card as an ace if it gives them a hand of 16-21
		if card3 == 'A' and (5 <= card4 <= 10):
			card3 = 11
			self.dealer_card_one_ace = True

		# The dealer will opt for a 12 in the scenario when she is delt two Ace's	
		elif card3 == 'A' and card4 == 'A':
			card3, card4 = 11, 1
			self.dealer_card_one_ace = True
		# The dealer will choose their Ace to be a one if their other card is a low value.	
		elif card3 == 'A' and (4 >= card4):
			card3 = 1
		# The next two elif block introduces the same logic but factors for the dealer being given an Ace 
		# for her second card.	
		elif card4 == 'A' and (5 <= card3 <= 10):
			card4 = 11
			self.dealer_card_two_ace = True
		elif card4 == 'A' and (4 >= card3):
			card4 = 1

		self.dealers_hand += (card3 + card4) 
		print(f"\tDEALER'S HAND: {self.dealers_hand}\n")


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
		print(f"\n(Player Current Balance: £{self.player_balance})")
		print(f"(Dealer Current Balance: £{self.dealer_balance})")


	def stick_twist(self):
		twist = True
		while twist:
			decision = input("\nWould you like to stick or twist?: ")
			if decision == 'stick':
				twist = False
				print(f"\nYou have stuck on {self.players_hand}")
			elif decision == 'twist':
				additional_card = self.cards.pop(random.randrange(len(self.cards)))
				if additional_card == 'A':
					additional_card = 1
				self.players_hand += additional_card
				print(f"Current hand: {self.players_hand}")
				if self.players_hand > 21:
					
					if self.player_card_one_ace:
						self.players_hand = self.players_hand - 10
						print(f"You adjusted your Ace (11) to Ace (1). Your new hand: {self.players_hand}")
						self.player_card_one_ace = False
						continue
					
					elif self.player_card_two_ace:
						self.players_hand = self.players_hand - 10
						print(f"\nYou adjusted your Ace (11) to Ace (1). Your new hand: {self.players_hand}")
						self.player_card_two_ace = False
						continue

					else:
						print("---BUST---")
						break
	

	def simulate_dealer_playing(self):
		"""Simulate the dealer playing the game in response to the Player's final hand"""
		print("\nThe dealer is now playing")
		while True:
			if self.players_hand > 21 and (21 >= self.dealers_hand >= 16):
				print(f"\nThe dealer has stuck on: {self.dealers_hand}")
				break

			elif self.players_hand > 21 and self.dealers_hand < 16:
				extra_card = self.cards.pop(random.randrange(len(self.cards)))
				if extra_card == 'A':
					extra_card = 1
				self.dealers_hand += extra_card
				print(f"Dealers hand: {self.dealers_hand}")
				continue
		
			elif (21 >= self.players_hand >= 16) and (self.dealers_hand < self.players_hand):
				extra_card = self.cards.pop(random.randrange(len(self.cards)))
				if extra_card == 'A':
					extra_card = 1
				self.dealers_hand += extra_card
				print(f"Dealers hand: {self.dealers_hand}")
				continue

			elif (21 >= self.players_hand >= 16) and (self.dealers_hand == self.players_hand):
				print(f"\nThe dealer has stuck on: {self.dealers_hand}")
				break

			elif (21 >= self.players_hand >= 16) and (self.dealers_hand > self.players_hand):
				if self.dealers_hand > 21:
					if self.dealer_card_one_ace:
						self.dealers_hand = self.dealers_hand - 10 
						print("The dealer has adjusted her Ace from an 11 to a 1. Dealer now playing: " 
							f"{self.dealers_hand}")
						self.dealer_card_one_ace = False
						if self.dealers_hand <= 21:
							continue 

					elif self.dealer_card_two_ace:
						self.dealers_hand = self.dealers_hand - 10
						print("The dealer has adjusted her Ace from an 11 to a 1. Dealer now playing: " 
							f"{self.dealers_hand}")
						self.dealer_card_two_ace = False
						if self.dealers_hand <= 21:
							continue
					else:
						print("THE DEALER HAS BUSTED")
						break
				else:
					print(f"\nThe dealer has stuck on: {self.dealers_hand}")
					break

			
			elif self.dealers_hand > 21:
				if self.dealer_card_one_ace:
					self.dealers_hand = self.dealers_hand - 10 
					print("The dealer has adjusted her Ace from an 11 to a 1. Dealer now playing: " 
						f"{self.dealers_hand}") 
					self.dealer_card_one_ace = False
					if self.dealers_hand <= 21:
							continue
				elif self.dealer_card_two_ace:
						self.dealers_hand = self.dealers_hand - 10
						print("The dealer has adjusted her Ace from an 11 to a 1. Dealer now playing: " 
							f"{self.dealers_hand}")
						self.dealer_card_two_ace = False
						if self.dealers_hand <= 21:
							continue
				else: 
					print("\nTHE DEALER HAS BUSTED")
					break


	def result(self):
		"""State the result of the hand."""
		if (self.players_hand > self.dealers_hand) and (self.players_hand <= 21):
			print("You have won this hand!!!")
			self.player_balance += self.current_pot
			self.last_hand_outcome = 'player win'
		
		elif (self.players_hand <= 21) and (self.dealers_hand > 21):
			print("You have won this hand!!!")
			self.player_balance += self.current_pot
			self.last_hand_outcome = 'player win'

		elif self.players_hand == self.dealers_hand or (self.players_hand > 21 and self.dealers_hand > 21):
			print("This hand was a draw. The pot will roll over")
			self.last_hand_outcome = 'draw' 

		elif (self.players_hand < self.dealers_hand) and (self.dealers_hand <=21):
			print("The dealer won this hand!")
			self.dealer_balance += self.current_pot
			self.last_hand_outcome = 'dealer win'

		elif (self.dealers_hand <= 21) and (self.players_hand > 21):
			print("The dealer won this hand.")
			self.dealer_balance += self.current_pot
			self.last_hand_outcome = 'dealer win'


	def new_balances(self):
		"""State the new current balances."""
		print(f"\nPlayer Balance: {self.player_balance}")
		print(f"Dealer Balance: {self.dealer_balance}")

	def database_store(self):
		"""Store the result of the last hand into a database in my MySQL server"""
		my_cursor = db.cursor()
		query = "INSERT INTO games (player_name, hand_result, current_pot, player_hand, dealer_hand)"
		query += "VALUES (%s, %s, %s, %s, %s)"
		data = (self.player_name, self.last_hand_outcome, self.current_pot, self.players_hand, self.dealers_hand)
		my_cursor.execute(query, data)
		db.commit() 

	def reset_continue_or_finish_game(self):
		"""Reset the nominal values of the hands and the current pot (as long as the last hand was won)"""
		self.dealers_hand = 0
		self.players_hand = 0
		print("\nThe hands have been reset")
		if self.last_hand_outcome == 'draw':
			self.current_pot = self.current_pot	
		else:
			self.current_pot = 0.0
		# Finish the game if either player has to go into a negative balance to play the next hand.	
		if self.player_balance <= 1.99:
			print("---THE DEALER HAS WON THE GAME---")
			exit()
		if self.dealer_balance <= 1.99:
			print("---YOU HAVE WON THE GAME---")
			exit()

		play_on = input("Would you like to continue playing(y/n)? ")
		if play_on == 'n':
			exit()
		elif play_on == 'y':
			new_game = BlackJack(name, self.player_balance, self.dealer_balance, self.current_pot)



##  Introductory phase of the game ## 
name = input("Please enter your name: ")
print(f"Welcome, {name.title()}")
player_money = input("\nHow much money would you like to deposit into your games account: £")

try:
	player_money = float(player_money)
except ValueError:
	print("You need to enter a numerical value when depositing into your games account")
	player_money = input("\nHow much money would you like to deposit into your games account: £")
	player_money = float(player_money)

if player_money < 0:
	print("You can't enter a negative amount of money.")
	player_money = input("How much would you like to deposit into your account: £")
	player_money = float(player_money)

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
	game.database_store()
	game.reset_continue_or_finish_game()

