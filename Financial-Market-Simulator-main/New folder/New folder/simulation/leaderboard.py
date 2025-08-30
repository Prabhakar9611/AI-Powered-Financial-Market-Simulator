import json
import os

class Leaderboard:
    def __init__(self, leaderboard_file='leaderboard.json'):
        """
        Initialize the leaderboard with data from the leaderboard file.
        
        :param leaderboard_file: Path to the leaderboard JSON file
        """
        self.leaderboard_file = leaderboard_file
        self.leaderboard = self.load_leaderboard()

    def load_leaderboard(self):
        """
        Load existing leaderboard from the file, or create a new one if it doesn't exist.
        
        :return: List of leaderboard entries
        """
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Leaderboard file is corrupt. Starting fresh.")
                return []
        return []

    def update_leaderboard(self, username, total_balance):
        """
        Update the leaderboard with a new user's performance or an update to an existing user's performance.
        
        :param username: User's username
        :param total_balance: User's total portfolio balance
        """
        # Check if username already exists
        for entry in self.leaderboard:
            if entry['username'] == username:
                entry['total_balance'] = max(total_balance, entry['total_balance'])
                break
        else:
            # If username not found, add new entry
            self.leaderboard.append({
                'username': username,
                'total_balance': total_balance
            })

        # Sort leaderboard by total balance in descending order
        self.leaderboard.sort(key=lambda x: x['total_balance'], reverse=True)

        # Keep top 10 entries
        self.leaderboard = self.leaderboard[:10]

        # Save updated leaderboard to file
        self.save_leaderboard()

    def save_leaderboard(self):
        """
        Save the leaderboard to the JSON file.
        """
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.leaderboard, f, indent=4)

    def display_leaderboard(self):
        """
        Display the leaderboard showing the top performers.
        """
        print("\n--- Top Traders Leaderboard ---")
        if not self.leaderboard:
            print("No entries yet!")
            return

        for i, entry in enumerate(self.leaderboard, 1):
            print(f"{i}. {entry['username']}: ${entry['total_balance']:.2f}")

