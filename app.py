#This program is a GUI tool for unblocking Twitter users in bulk using Selenium. It imports tkinter, filedialog, selenium, and time modules. 
#It defines a class called TwitterUnblockTool that has methods for starting the browser, browsing for a file containing a list of blocked user IDs, 
#and unblocking the users. The class also has XPaths for the block and unblock buttons. The GUI elements include buttons for starting the browser, 
#browsing for a file, and unblocking users, labels for displaying the unblock frequency, total unblocks, and total IDs to unblock. 
#The program uses Firefox browser and Geckodriver location for launching the browser. The user selects the file containing the list of blocked user IDs, 
#and the program reads and loops through the file to unblock each user. The program displays the total number of IDs unblocked in the GUI and closes the 
#browser window.

import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class TwitterUnblockTool:
    # XPaths for the block and unblock buttons
    block_button_xpath = "//span[contains(text(), 'Blockiert')]"
    unblock_button_xpath = "//span[contains(text(), 'Entblocken')]"

    def __init__(self, master):
        self.master = master
        master.title("Twitter Unblock Tool")

        # Variables
        self.browser = None
        self.blocked_file_path = ""
        self.unblock_frequency = tk.StringVar(value="1")
        self.total_unblocks = tk.StringVar(value="0")

        # GUI Elements
        self.start_browser_button = tk.Button(master, text="Start Browser", command=self.start_browser)
        self.browse_button = tk.Button(master, text="Browse Blocked User IDs", command=self.browse_blocked_user_ids)
        self.unblock_button = tk.Button(master, text="Unblock Users", command=self.unblock_users, state="disabled")
        self.unblock_frequency_label = tk.Label(master, text="Unblock Frequency (seconds):")
        self.unblock_frequency_entry = tk.Entry(master, textvariable=self.unblock_frequency)
        self.total_unblocks_label = tk.Label(master, text="Total IDs Unblocked:")
        self.total_unblocks_entry = tk.Entry(master, textvariable=self.total_unblocks, state="readonly")
        self.total_ids_label = tk.Label(master, text="Total IDs to unblock: 0")

        # Layout
        self.start_browser_button.grid(row=0, column=0, padx=5, pady=5)
        self.browse_button.grid(row=1, column=0, padx=5, pady=5)
        self.unblock_frequency_label.grid(row=2, column=0, padx=5, pady=5)
        self.unblock_frequency_entry.grid(row=2, column=1, padx=5, pady=5)
        self.unblock_button.grid(row=3, column=0, padx=5, pady=5)
        self.total_unblocks_label.grid(row=4, column=0, padx=5, pady=5)
        self.total_unblocks_entry.grid(row=4, column=1, padx=5, pady=5)
        self.total_ids_label.grid(row=5, column=0, padx=5, pady=5)

    def start_browser(self):
        # Set Firefox binary path and Geckodriver location
        options = webdriver.FirefoxOptions()
        options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
        service = Service('geckodriver.exe')

        # Launch Firefox and go to Twitter
        self.browser = webdriver.Firefox(service=service, options=options)
        self.browser.get('https://twitter.com/login')

        # Enable the unblock button
        self.unblock_button.config(state="normal")

    def browse_blocked_user_ids(self):
        self.blocked_file_path = filedialog.askopenfilename(title="Select Blocked User IDs File")
        print(f"Selected file path: {self.blocked_file_path}")

        # Read the number of blocked user IDs from the selected file
        with open(self.blocked_file_path, "r") as f:
            blocked_user_ids = [line.strip() for line in f.readlines()]

        # Update the total_ids_label with the number of blocked user IDs
        total_blocked_user_ids = len(blocked_user_ids)
        self.total_ids_label.config(text=f"Total IDs to unblock: {total_blocked_user_ids}")

    def unblock_users(self):
        # Disable the unblock button
        self.unblock_button.config(state="disabled")

        # Read the blocked user IDs from the selected file
        with open(self.blocked_file_path, "r") as f:
            blocked_user_ids = [line.strip() for line in f.readlines()]

        # Total number of IDs to unblock
        total_ids_to_unblock = len(blocked_user_ids)
        # Loop through the blocked user IDs and unblock each user
        for user_id in blocked_user_ids:
            # Go to the user's Twitter page
            url = f"https://twitter.com/i/user/{user_id}"
            self.browser.get(url)
            time.sleep(1)

            # Click the "Blocked" button
            try:
                blocked_button = self.browser.find_element(By.XPATH, self.block_button_xpath)
                blocked_button.click()
                print(f"Clicked on Blockiert button for user https://twitter.com/i/user/{user_id}")
            except:
                print(f"Unable to find Blockiert button for user https://twitter.com/i/user/{user_id}")
                continue

            # Wait for the confirmation prompt to appear
            time.sleep(1)

            # Click the "Unblock" button
            try:
                unblock_button = self.browser.find_element(By.XPATH, self.unblock_button_xpath)
                unblock_button.click()
                print(f"Clicked on Unblock button for user https://twitter.com/i/user/{user_id}")
            except:
                print(f"Unable to find Unblock button for user https://twitter.com/i/user/{user_id}")
                continue

            # Wait before unblocking the next user
            time.sleep(int(self.unblock_frequency.get()))

        # Show the total number of IDs unblocked in the GUI
        self.total_unblocks.set(str(total_ids_to_unblock))

        # Close the browser window
        self.browser.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TwitterUnblockTool(root)
    root.mainloop()
