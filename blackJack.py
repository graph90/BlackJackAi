from langchain_community.llms import Ollama
import random
llm = Ollama(model="llama3.2")
def card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def adjust_for_ace(hand):
    total = sum(hand)
    if total > 21 and 11 in hand:
        hand[hand.index(11)] = 1
    return hand

def basic_blackjack_strategy(player_hand, dealer_upcard):
    player_total = sum(player_hand)
    if player_total <= 11:
        if player_total in [9, 10, 11]:
            if dealer_upcard < 7:
                return "Double Down"
        return "Hit"
    elif 12 <= player_total <= 16:
        if dealer_upcard >= 7:
            return "Hit"
        else:
            return "Stand"
    else:
        return "Stand"

def blackjack_ai(player_hand, dealer_upcard, revealed_cards):
    strategy_move = basic_blackjack_strategy(player_hand, dealer_upcard)
    prompt = (f"Player hand: {player_hand}, Dealer upcard: {dealer_upcard}, "
              f"Revealed cards so far: {revealed_cards}. "
              f"Based on basic blackjack strategy and card counting, what is the best move? "
              f"Recommend whether to Hit, Stand, Double Down, or Split.")
    llm_response = llm.invoke(prompt)
    
    if "Double Down" in strategy_move:
        final_decision = "Double Down"
    elif "Hit" in strategy_move:
        final_decision = "Hit"
    elif "Stand" in strategy_move:
        final_decision = "Stand"
    else:
        final_decision = "Unknown Move"

    formatted_response = (f"--- AI Recommendation ---\n"
                          f"Based on the analysis:\n{llm_response}\n\n"
                          f"**Final Decision:** {final_decision}\n"
                          f"-----------------------")
    
    return formatted_response

def get_valid_card_input(prompt_text):
    while True:
        card = input(prompt_text).upper().strip()
        if card in ['A', 'K', 'Q', 'J'] or (card.isdigit() and 1 <= int(card) <= 10):
            return card_value(card)
        else:
            print("Invalid input! Please enter a valid card (1-10, 'J', 'Q', 'K', 'A').")

def get_valid_yes_no(prompt_text):
    while True:
        choice = input(prompt_text).strip().lower()
        if choice in ["yes", "y", "no", "n"]:
            return choice
        else:
            print("Invalid input! Please enter 'yes/y' or 'no/n'.")

def play_blackjack(revealed_cards):
    print("\nBlackjack Ai")
    
    dealer_upcard = get_valid_card_input("Enter the dealer's upcard (2-11 or 'A' for Ace): ")
    revealed_cards.append(dealer_upcard)
    
    player_hand = []
    for i in range(2):
        card = get_valid_card_input(f"Enter card {i+1} in your hand (1-10, 'J', 'Q', 'K', 'A'): ")
        player_hand.append(card)
        revealed_cards.append(card)

    player_hand = adjust_for_ace(player_hand)

    while True:
        player_hand = adjust_for_ace(player_hand)
        ai_response = blackjack_ai(player_hand, dealer_upcard, revealed_cards)
        print("\nAi's recommendation:")
        print(ai_response)
        
        if "Double Down" in ai_response:
            double_down_choice = get_valid_yes_no("\nDo you want to Double Down? (yes/y or no/n): ")
            if double_down_choice in ["yes", "y"]:
                new_card = get_valid_card_input("Enter the value of the next card you received (1-10, 'J', 'Q', 'K', 'A'): ")
                player_hand.append(card_value(new_card))
                revealed_cards.append(card_value(new_card))
                print(f"\nYou doubled down and received: {new_card}. Your total hand is now: {player_hand}")
                break
            else:
                print("You chose not to double down.")
        elif "Hit" in ai_response:
            hit_choice = get_valid_yes_no("\nDo you want to Hit? (yes/y or no/n): ")
            if hit_choice in ["yes", "y"]:
                new_card = get_valid_card_input("Enter the value of the next card you received (1-10, 'J', 'Q', 'K', 'A'): ")
                player_hand.append(card_value(new_card))
                revealed_cards.append(card_value(new_card))
            else:
                break
        else:
            break

    print("\nRound finished.")

def start_blackjack_game():
    revealed_cards = []
    while True:
        play_blackjack(revealed_cards)
        play_again = get_valid_yes_no("\nAnother round? (yes/y or no/n): ")
        if play_again not in ["yes", "y"]:
            print("Goodbye.")
            break

start_blackjack_game()
