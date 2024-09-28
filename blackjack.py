import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_WIDTH, CARD_HEIGHT = 73, 98
BACKGROUND_COLOR = (0, 128, 0)  # Green for the table
FONT_COLOR = (255, 255, 255)
RESULT_COLOR_WIN = (0, 255, 0)  # Green for win
RESULT_COLOR_LOSE = (255, 0, 0)  # Red for lose
RESULT_COLOR_TIE = (255, 255, 0)  # Yellow for tie

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = pygame.transform.scale(pygame.image.load(f'cards/{rank}{suit}.png'), (CARD_WIDTH, CARD_HEIGHT))

    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

# Deck class
class Deck:
    suits = ['H', 'D', 'C', 'S']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def score(self):
        total = sum(card.value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == 'A')
        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1
        return total

# AI Player class
class AIPlayer(Player):
    def make_decision(self, game):
        if self.score() < 17:
            self.add_card(game.deck.deal_card())
            return f"{self.name} hits."
        else:
            return f"{self.name} stands."

# Game class
class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.dealer_hand = []
        self.current_player_index = 0
        self.game_over = False
        self.message = "Press 'H' to hit or 'S' to stand."
        self.result_message = ""

    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.deal_card())
            self.dealer_hand.append(self.deck.deal_card())

    def reset_game(self):
        self.deck = Deck()
        for player in self.players:
            player.hand = []
        self.dealer_hand = []
        self.current_player_index = 0
        self.game_over = False
        self.message = "Press 'H' to hit or 'S' to stand."
        self.result_message = ""

    def display(self, screen):
        screen.fill(BACKGROUND_COLOR)
        y_offset = 50
        
        # Display players' hands
        for player in self.players:
            hand_score = player.score()
            hand_str = f"{player.name}: {hand_score}"
            text = font.render(hand_str, True, FONT_COLOR)
            screen.blit(text, (50, y_offset))
            for i, card in enumerate(player.hand):
                screen.blit(card.image, (50 + i * (CARD_WIDTH + 10), y_offset + 30))
            y_offset += 150

        # Display dealer's hand
        dealer_score = sum(card.value() for card in self.dealer_hand) - self.dealer_hand[1].value()  # Hide second card
        dealer_str = f"Dealer: {dealer_score if len(self.dealer_hand) > 1 else '?' }"
        text = font.render(dealer_str, True, FONT_COLOR)
        screen.blit(text, (WIDTH - 200, 50))
        for i, card in enumerate(self.dealer_hand):
            screen.blit(card.image, (WIDTH - 200 + i * (CARD_WIDTH + 10), 80))

        # Display messages
        message_text = font.render(self.message, True, FONT_COLOR)
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT - 120))

        if self.game_over:
            result_text = font.render(self.result_message, True, FONT_COLOR)
            if "win" in self.result_message.lower():
                result_text = font.render(self.result_message, True, RESULT_COLOR_WIN)
            elif "lose" in self.result_message.lower():
                result_text = font.render(self.result_message, True, RESULT_COLOR_LOSE)
            else:
                result_text = font.render(self.result_message, True, RESULT_COLOR_TIE)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT - 80))

# Main function
def main():
    global font
    font = pygame.font.Font(None, 36)

    human_player = Player("You")
    ai_player1 = AIPlayer("AI Bot 1")
    ai_player2 = AIPlayer("AI Bot 2")
    players = [human_player, ai_player1, ai_player2]

    game = Game(players)
    game.deal_initial_cards()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blackjack")

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_h:  # Hit
                    human_player.add_card(game.deck.deal_card())
                    if human_player.score() > 21:
                        game.result_message = "You bust! Dealer wins."
                        game.game_over = True
                elif event.key == pygame.K_s:  # Stand
                    game.message = "AI is playing..."
                    for i in range(1, len(players)):  # AI plays
                        ai_player = players[i]
                        action = ai_player.make_decision(game)
                        game.message += f" {action}"
                    dealer_score = sum(card.value() for card in game.dealer_hand)
                    human_score = human_player.score()
                    if dealer_score > 21 or human_score > dealer_score:
                        game.result_message = "You win!"
                    elif dealer_score == human_score:
                        game.result_message = "It's a tie!"
                    else:
                        game.result_message = "Dealer wins!"
                    game.game_over = True

        # Render the game state
        game.display(screen)
        pygame.display.flip()
        clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()
