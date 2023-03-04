#This is a Python program that uses the tkinter library to create a graphical user interface for unblocking Twitter users. The program uses the Selenium library to automate the process of unblocking users.
#The program starts by importing the necessary libraries, including tkinter, filedialog, and selenium. It then defines a class called "TwitterUnblockTool", which creates the GUI elements and defines the functions for interacting with Twitter. The GUI elements include buttons for starting the browser, browsing for a file containing the list of blocked user IDs, and unblocking users.
#When the "Start Browser" button is clicked, the program uses the Firefox browser to navigate to the Twitter login page. When the "Browse Blocked User IDs" button is clicked, a file dialog opens to allow the user to select a file containing the list of blocked user IDs. When the "Unblock Users" button is clicked, the program reads the user IDs from the selected file, navigates to the Twitter page for each user, clicks the "Blocked" button, waits for the confirmation prompt to appear, and then clicks the "Unblock" button. The program also includes an option to set the frequency at which users are unblocked.
#Finally, the program includes a main section that creates an instance of the "TwitterUnblockTool" class and starts the GUI event loop using the tkinter "mainloop()" function.

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

    def unblock_users(self):
        # Read the blocked user IDs from the selected file
        with open(self.blocked_file_path, "r") as f:
            blocked_user_ids = f.readlines()
        print(f"Blocked user IDs: {blocked_user_ids}")

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


