import os
import tkinter as tk
from PIL import Image, ImageTk
import json

#changes the directory
os.chdir("C:/Users/socio/OneDrive/Documents/Python projects/Clicker game")

class Wobble:
    def __init__(self, root):
        self.root = root
        self.points, self.points_per_click, self.upgrade_level = self.load_game()

        self.root.title("Wobble Clicker")




        # Load custom button images
        self.click_button_image = Image.open("Crystal.png")
        self.upgrade_button_image = Image.open("Crystal 2.png")

        #resizes the images

        #Converts Images to objects
        self.click_button_photo = ImageTk.PhotoImage(self.click_button_image)
        self.upgrade_button_photo = ImageTk.PhotoImage(self.upgrade_button_image)




        self.points_label = tk.Label(root, text=f"Points: {self.points}")
        self.points_label.pack(pady=10)
        #the new point button
        self.click_button = tk.Button(root, image=self.click_button_photo, command=self.add_points)
        self.click_button.pack(pady=10)
        #the new upgrade buttons
        self.upgrade_button = tk.Button(root, text=f"Upgrade (Cost: {self.calculate_upgrade_cost()} points)", command=self.buy_upgrade)
        self.upgrade_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Game", command=self.save_game)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(root, text="Load Game", command=self.load_game_ui)
        self.load_button.pack(side=tk.RIGHT, padx=5)

    def add_points(self):
        self.points += self.points_per_click
        self.update_points_label()

    def buy_upgrade(self):
        upgrade_cost = self.calculate_upgrade_cost()
        if self.points >= upgrade_cost:
            self.points -= upgrade_cost
            self.points_per_click += 1
            self.upgrade_level += 1
            self.update_upgrade_button_text()
            self.update_points_label()
        else:
            print("Not enough points to buy upgrade.")

    def calculate_upgrade_cost(self):
        return int(10 ** (0.7 * self.upgrade_level *0.6))

    def update_upgrade_button_text(self):
        self.upgrade_button.config(text=f"Upgrade (Cost: {self.calculate_upgrade_cost()} points)")

    def update_points_label(self):
        self.points_label.config(text=f"Points: {self.points}")

    def save_game(self):
        game_state = {
            "points": self.points,
            "points_per_click": self.points_per_click,
            "upgrade_level": self.upgrade_level
        }
        with open("savegame.json", "w") as file:
            json.dump(game_state, file)
        print("Game saved.")

    def load_game(self):
        try:
            with open("savegame.json", "r") as file:
                game_state = json.load(file)
                points = game_state["points"]
                points_per_click = game_state["points_per_click"]
                upgrade_level = game_state.get("upgrade_level", 0)  # Default to 0 if upgrade_level is not present
                print("Game loaded.")
                return points, points_per_click, upgrade_level
        except FileNotFoundError:
            print("No save file found.")
            return 0, 1, 0

    def load_game_ui(self):
        self.points, self.points_per_click, self.upgrade_level = self.load_game()
        self.update_upgrade_button_text()
        self.update_points_label()

if __name__ == "__main__":
    root = tk.Tk()
    game = Wobble(root)
    root.mainloop()
