import secrets
import hmac
import hashlib
import sys
from typing import List, Tuple, Dict
from prettytable import PrettyTable
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

class Dice:
    def __init__(self, values: List[int]):
        if len(values) != 6:
            raise ValueError("Each die must have exactly 6 values")
        if not all(isinstance(x, int) for x in values):
            raise ValueError("All dice values must be integers")
        self.values = values

    def __str__(self):
        return ','.join(map(str, self.values))


class FairRandomGenerator:
    @staticmethod
    def generate_hmac_key() -> bytes:
        """Generate a cryptographically secure random key of 256 bits"""
        return secrets.token_bytes(32)  # 256 bits as required

    @staticmethod
    def generate_random_number(range_start: int, range_end: int) -> Tuple[int, bytes, str]:
        """
        Generate a provably fair random number using HMAC.
        Returns the number, key used, and HMAC value.
        """
        key = FairRandomGenerator.generate_hmac_key()
        # Use secrets.randbelow for uniform distribution
        number = secrets.randbelow(range_end - range_start + 1) + range_start
        # Use SHA3-256 for HMAC calculation
        hmac_value = hmac.new(key, str(number).encode(), hashlib.sha3_256).hexdigest()
        return number, key, hmac_value


class Game:
    def __init__(self, dice_list: List[Dice]):
        if len(dice_list) < 3:
            raise ValueError("At least 3 dice configurations are required")
        self.dice_list = dice_list
        self.used_dice_index = None

    def display_title(self):
        print(f"\n{Fore.CYAN}=== Non-Transitive Dice Game ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Prove the fairness of random selection!{Style.RESET_ALL}\n")

    def play(self):
        self.display_title()
        print("Let's determine who makes the first move.")
        first_player, key, hmac_value = self.determine_first_player()
        print(f"I selected a random value in the range 0..1 (HMAC={hmac_value})")
        user_guess = self.get_user_guess()
        print(f"My selection: {first_player} (KEY={key.hex()})")

        if user_guess == first_player:
            print(f"{Fore.GREEN}You guessed correctly! You make the first move.{Style.RESET_ALL}")
            user_roll = self.user_turn()
            computer_roll = self.computer_turn(exclude=self.used_dice_index)
        else:
            print(f"{Fore.BLUE}I make the first move and choose the dice.{Style.RESET_ALL}")
            computer_roll = self.computer_turn()
            user_roll = self.user_turn(exclude=self.used_dice_index)

        self.determine_winner(user_roll, computer_roll)

    def determine_first_player(self) -> Tuple[int, bytes, str]:
        return FairRandomGenerator.generate_random_number(0, 1)

    def get_user_guess(self) -> int:
        print("\nTry to guess my selection:")
        print("0 - I selected 0")
        print("1 - I selected 1")
        print("? - help")
        print("x - exit")
        
        while True:
            user_input = input(f"{Fore.YELLOW}Your selection: {Style.RESET_ALL}").strip().lower()
            if user_input == "0":
                return 0
            elif user_input == "1":
                return 1
            elif user_input == "?":
                self.display_help_table()
            elif user_input == "x":
                print("Thanks for playing!")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")

    def user_turn(self, exclude: int = None) -> int:
        print("\nChoose your dice:")
        self.display_dice_options(exclude)
        
        dice_index = self.get_user_dice_choice(exclude)
        self.used_dice_index = dice_index
        selected_dice = self.dice_list[dice_index]
        
        # Generate provably fair random number for user's throw
        roll, key, hmac_value = FairRandomGenerator.generate_random_number(0, 5)
        selected_value = selected_dice.values[roll]
        
        print(f"\nI selected a random value in the range 0..5 (HMAC={hmac_value})")
        print(f"Generated value: {roll} (KEY={key.hex()})")
        print(f"{Fore.GREEN}Your throw is {selected_value}{Style.RESET_ALL}")
        
        return selected_value

    def computer_turn(self, exclude: int = None) -> int:
        print("\nIt's time for my throw.")
        available_indices = [i for i in range(len(self.dice_list)) if i != exclude]
        computer_choice = secrets.choice(available_indices)
        self.used_dice_index = computer_choice
        selected_dice = self.dice_list[computer_choice]
        
        print(f"I choose dice {computer_choice + 1}: {selected_dice}")
        
        # Generate provably fair random number for computer's throw
        roll, key, hmac_value = FairRandomGenerator.generate_random_number(0, 5)
        selected_value = selected_dice.values[roll]
        
        print(f"I selected a random value in the range 0..5 (HMAC={hmac_value})")
        print(f"Generated value: {roll} (KEY={key.hex()})")
        print(f"{Fore.BLUE}My throw is {selected_value}{Style.RESET_ALL}")
        
        return selected_value

    def display_dice_options(self, exclude: int = None):
        for i, dice in enumerate(self.dice_list):
            if exclude is not None and i == exclude:
                continue
            print(f"{i + 1} - {dice}")
        print("? - help")
        print("x - exit")

    def get_user_dice_choice(self, exclude: int = None) -> int:
        while True:
            user_input = input(f"{Fore.YELLOW}Your selection: {Style.RESET_ALL}").strip().lower()
            if user_input == "x":
                print("Thanks for playing!")
                sys.exit(0)
            elif user_input == "?":
                self.display_help_table()
                continue
            
            try:
                choice = int(user_input) - 1
                if exclude is not None and choice == exclude:
                    print(f"{Fore.RED}You cannot select the dice already chosen{Style.RESET_ALL}")
                    continue
                if 0 <= choice < len(self.dice_list):
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Enter a number or '?' for help or 'x' to exit.{Style.RESET_ALL}")

    def determine_winner(self, user_roll: int, computer_roll: int):
        print(f"\n{Fore.CYAN}Final Results:{Style.RESET_ALL}")
        if user_roll > computer_roll:
            print(f"{Fore.GREEN}You win ({user_roll} > {computer_roll})!{Style.RESET_ALL}")
        elif user_roll < computer_roll:
            print(f"{Fore.RED}I win ({computer_roll} > {user_roll})!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}It's a tie ({user_roll} = {computer_roll})!{Style.RESET_ALL}")

    def display_help_table(self):
        table = PrettyTable()
        table.field_names = [f"{Fore.CYAN}User Dice v{Style.RESET_ALL}"] + [
            f"{Fore.YELLOW}Dice {i+1}{Style.RESET_ALL}" for i in range(len(self.dice_list))
        ]
        
        for i, user_dice in enumerate(self.dice_list):
            row = [f"{Fore.GREEN}{user_dice}{Style.RESET_ALL}"]
            for opponent_dice in self.dice_list:
                if user_dice == opponent_dice:
                    prob = "- (0.3333)"
                else:
                    prob = f"{self.calculate_win_probability(user_dice, opponent_dice):.4f}"
                row.append(prob)
            table.add_row(row)
        
        print("\nWinning Probabilities Table:")
        print(table)
        print("\nNote: Probabilities show the chance of the row dice winning against the column dice")

    @staticmethod
    def calculate_win_probability(dice1: Dice, dice2: Dice) -> float:
        wins = sum(1 for v1 in dice1.values for v2 in dice2.values if v1 > v2)
        total = len(dice1.values) * len(dice2.values)
        return wins / total


def parse_dice_configurations(args: List[str]) -> List[Dice]:
    """Parse command line arguments into dice configurations"""
    if len(args) < 3:
        raise ValueError("At least 3 dice configurations are required")
    
    dice_list = []
    for arg in args:
        try:
            values = [int(x) for x in arg.split(",")]
            dice_list.append(Dice(values))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid dice configuration '{arg}': {e}")
    return dice_list


def main():
    if len(sys.argv) < 4:
        print(f"{Fore.RED}Error: You must provide at least 3 dice configurations.{Style.RESET_ALL}")
        print("Example usage: python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
        sys.exit(1)

    try:
        dice_list = parse_dice_configurations(sys.argv[1:])
        game = Game(dice_list)
        
        while True:
            print(f"\n{Fore.CYAN}Main Menu:{Style.RESET_ALL}")
            print("1 - Start Game")
            print("2 - Help")
            print("x - Exit")
            
            user_input = input(f"{Fore.YELLOW}Your selection: {Style.RESET_ALL}").strip().lower()
            if user_input == "1":
                game.play()
            elif user_input == "2":
                game.display_help_table()
            elif user_input == "x":
                print("Thanks for playing!")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid selection. Try again.{Style.RESET_ALL}")
                
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()