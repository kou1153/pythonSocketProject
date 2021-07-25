from tkinter import *
import os

def login():
    global login_screen
    global login_username
    global login_password
    global login_username_entry
    global login_password_entry
    
    login_username = StringVar()
    login_password = StringVar()
    
    login_screen = Toplevel(welcome_screen)
    login_screen.title("Weather App")
    login_screen.geometry("300x250")
    Label(login_screen, text = "Login here!!!!", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(login_screen, text = "Please enter details below to login").pack()
    Label(login_screen, text = "").pack()
    
    Label(login_screen, text = "Username * ").pack()
    login_username_entry = Entry(login_screen, textvariable = login_username)
    login_username_entry.pack()
        
    Label(login_screen, text = "Password * ").pack()
    login_password_entry = Entry(login_screen, textvariable = login_password)
    login_password_entry.pack()
    
    Label(login_screen, text = "").pack()
    
    Button(login_screen, text="Login").pack()
    # Button(login_screen, text = "Login", width = 10, height = 1, command = login_verify).pack()

def register():
    global register_screen
    
    global username
    global password
    global username_entry
    global password_entry
    
    username = StringVar()
    password = StringVar()
    
    register_screen = Toplevel(welcome_screen)
    register_screen.geometry("300x250")
    register_screen.title("Weather App")
    Label(register_screen, text = "Register here!!!!", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(register_screen, text = "Please enter details below").pack()
    Label(register_screen, text = "").pack()
    
    Label(register_screen, text = "Username * ").pack()
    username_entry = Entry(register_screen, textvariable = username)
    username_entry.pack()
    
    Label(register_screen, text = "Password * ").pack()
    password_entry =  Entry(register_screen, textvariable = password)
    password_entry.pack()
    
    Label(register_screen, text = "").pack()
    Button(register_screen, text="Register").pack()
    # Button(register_screen, text = "Register", width = 10, height = 1, command = register_user).pack()

def main_screen():
    global welcome_screen
    welcome_screen = Tk()
    welcome_screen.geometry("300x250")
    welcome_screen.title("Weather App")
    Label(text = "Welcome here!!!!", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    # Button(text="Login").pack()
    Button(text = "Login", height = "2", width = "30", command = login).pack()
    Label(text = "").pack()
    # Button(text="Register").pack()
    Button(text = "Register",height = "2", width = "30", command = register).pack()

    welcome_screen.mainloop()
    
main_screen()