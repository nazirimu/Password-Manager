from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import random
import pyperclip
import json


# ------------------------- SEARCH PASSWORD -------------------------------#
def search():

    website = website_box.get()

    try:
        # open the password keeper to read the data
        with open("password_keeper.json", "r") as data_file:
            # Reading the data to obtain user and password
            data = json.load(data_file)
            user = data[website]["email"]
            password = data[website]["password"]
    except KeyError or FileNotFoundError:
        # Executed if the file is not found or information about it has not been saved.
        message = "There is no information saved for this website."
    else:
        message = f"Username/email: {user}\nPassword: {password}"
    finally:
        messagebox.showinfo(title=f"{website}", message=message)


# ------------------------- PASSWORD GENERATOR-------------------------------#
def random_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_box.insert(0, f"{password}")
    pyperclip.copy(password)


# ------------------------- SAVE PASSWORD -----------------------------------#
def add_pass():
    # Obtaining the details from the entry boxes
    website = website_box.get()
    user = email_box.get()
    password = password_box.get()
    new_entry = {
        website: {
            "email": user,
            "password": password
        }
    }

    # Checking for empty fields
    if len(website) <= 0 or len(user) <= 0 or len(password) <= 0:
        messagebox.showinfo(title="Alert", message="Please insert information in the missing fields")
    else:
        # Verifying information
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"Entered details: \nEmail/username: {user} \nPassword: {password}"
                                               f"\nClick ok to save:")

        if is_ok:
            # NOTE:SECTION INTENTIONALLY WASNT REFACTORED TO BE SHORTER TO BE USED AS A LEARNING REFERENCE FOR JSON

            try:
                # open the password keeper to read the data
                with open("password_keeper.json", "r") as data_file:
                    # Reading the old data
                    data = json.load(data_file)

            except FileNotFoundError:
                # This block is executed if the file is not found.
                with open("password_keeper.json", "w") as data_file:
                    # Update the data
                    json.dump(new_entry, data_file, indent=4)

            else:
                # This block is run if the try block is executed.

                data.update(new_entry)
                # open the password keeper to write the new data
                with open("password_keeper.json", "w") as data_file:
                    # writing the new data
                    json.dump(data, data_file, indent=4)

            finally:
                # Clearing the entries from GUI
                website_box.delete(0, END)
                email_box.delete(0, END)
                password_box.delete(0, END)


# ------------------------- UI SET UP ---------------------------------------#
# Setting up the window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Setting up the Logo
canvas = Canvas(width=200, height=189)
lock_img = ImageTk.PhotoImage(Image.open("logo.png"))
canvas.create_image(100, 95, image=lock_img)
canvas.grid(row=0, column=1)

# WEBSITE
# # # website_label
website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)

# # # website_box
website_box = Entry(width=27)
website_box.focus()
website_box.grid(row=1, column=1, )

# # # search button
search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2)

# EMAIL
# # # email_label
email_label = Label(text="Email/Username: ")
email_label.grid(row=2, column=0)

# # # email_box
email_box = Entry(width=35)
email_box.grid(row=2, column=1, columnspan=2)

# PASSWORD
# # # password_label
password_label = Label(text="Password ")
password_label.grid(row=3, column=0)

# # # password_box
password_box = Entry(width=27)
password_box.grid(row=3, column=1)

# # # Password generator button
password_gen_button = Button(text="Generate", command=random_pass)
password_gen_button.grid(row=3, column=2)

# ADD
# # # add button
add_button = Button(text="Add", width=36, command=add_pass)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
