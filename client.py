import socket
from tkinter import *
import tkinter
from tkcalendar import *
from datetime import date, timedelta
import time
from tkinter import messagebox

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
# server for local host
SERVER = socket.gethostbyname(socket.gethostname())

#server for online host
# SERVER = "139.162.55.220"

ADDR = (SERVER, PORT)

#DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "LOGIN"
REGISTER_MESSAGE = "REGISTER"
REGISTER_SUCCESSFUL = "REGISTER SUCCESFULL"
EXIST_USER = "EXIST USER"
LOGIN_SUCCESSFUL = "LOGIN SUCCESSFUL"
LOGIN_FAIL = "LOGIN FAIL"
IN_APP = "IN APP"
ADMIN = "admin"

ALL_CITIES = "ALL CITIES"
ONE_CITY = "ONE CITY"
INVALID = "INVALID"
FUNCTION_1 = "FUNCTION_1"
FUNCTION_2 = "FUNCTION_2"
FUNCTION_3 = "FUNCTION_3"

ADD_NEW_SUCCESSFULL= "ADD_NEW_SUCCESSFULL"
ADD_NEW_FAIL = "ADD_NEW_FAIL"
DUPLICATE = "DUPLICATE"
EMPTY = "EMPTY"
SUCCESSFULL = "SUCCESSFULL"

today = date.today()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
def receive():
    return client.recv(8192).decode(FORMAT)

def login_verify():
    try:
        send(LOGIN_MESSAGE)
        
        username_login = login_username.get()
        send(username_login)
        
        password_login = login_password.get()
        send(password_login)
        
        login_username_entry.delete(0, END)
        login_password_entry.delete(0, END)
        
        received_msg = receive()
        
        if received_msg == LOGIN_FAIL:
            Label(login_screen, text = "Login Failed, due to security, shut down in 3s", fg = "red" ,font = ("calibri", 10)).pack()
            login_screen.after(3000, login_screen.destroy)
            welcome_screen.after(3000, welcome_screen.destroy)
            client.close()
        elif received_msg == LOGIN_SUCCESSFUL:
            weather_app_home()
            login_screen.destroy()
        else:
            Label(login_screen, text = "Login Failed, due to security, shut down in 3s", fg = "red" ,font = ("calibri", 10)).pack()
            login_screen.after(3000, login_screen.destroy)
            welcome_screen.after(3000, welcome_screen.destroy)
            client.close()
    except:
        # send(DISCONNECT_MESSAGE)
        Label(login_screen, text = "Server Closed, program will close after 3s", fg = "red" ,font = ("calibri", 10)).pack()
        welcome_screen.after(3000, welcome_screen.destroy)
        client.close()

def login():
    global login_screen
    global login_username
    global login_password
    global login_username_entry
    global login_password_entry
    
    login_username = StringVar()
    login_password = StringVar()
    
    login_screen = Toplevel(welcome_screen)
    login_screen.title("???ng d???ng th???i ti???t - ????ng nh???p")
    login_screen.geometry("350x300")
    Label(login_screen, text = "M???i nh???p c??c th??ng tin b??n d?????i").pack()
    Label(login_screen, text = "").pack()
    
    Label(login_screen, text = "T??n ????ng nh???p * ").pack()
    login_username_entry = Entry(login_screen, textvariable = login_username)
    login_username_entry.pack()
        
    Label(login_screen, text = "M???t kh???u * ").pack()
    login_password_entry = Entry(login_screen, textvariable = login_password)
    login_password_entry.pack()
    
    Label(login_screen, text = "").pack()
    Button(login_screen, text = "????ng nh???p", width = 10, height = 1, command = login_verify).pack()

def register_user():
    try:
        send(REGISTER_MESSAGE)
            
        username_register = register_username.get()
        send(username_register)
        
        password_register = register_password.get()
        send(password_register)

        register_username_entry.delete(0, END)
        register_password_entry.delete(0, END)
        
        received_msg = receive()
            
        if received_msg == EXIST_USER:
            Label(register_screen, text = "T??n ????ng nh???p ???? t???n t???i, due to security, shut down in 3s", fg = "red" ,font = ("calibri", 10)).pack()
            register_screen.after(3000, register_screen.destroy)
            welcome_screen.after(3000, welcome_screen.destroy)
            client.close()
        elif received_msg == REGISTER_SUCCESSFUL:
            login()
            register_screen.destroy()
        else:
            Label(register_screen, text = "Failed to login, due to security, shut down in 3s", fg = "red" ,font = ("calibri", 10)).pack()
            register_screen.after(3000, register_screen.destroy)
            welcome_screen.after(3000, welcome_screen.destroy)
            client.close()
    except:
        # send(DISCONNECT_MESSAGE)
        Label(register_screen, text = "Server Closed, program will close after 3s", fg = "red" ,font = ("calibri", 10)).pack()
        welcome_screen.after(3000, welcome_screen.destroy)
        client.close()

def register():
    
    global register_screen
    
    global register_username
    global register_password
    global register_username_entry
    global register_password_entry
    
    register_username = StringVar()
    register_password = StringVar()
    
    register_screen = Toplevel(welcome_screen)
    register_screen.geometry("350x300")
    register_screen.title("???ng d???ng th???i ti???t - ????ng k??")
    Label(register_screen, text = "Nh???p c??c th??ng tin b??n d?????i").pack()
    Label(register_screen, text = "").pack()
    
    Label(register_screen, text = "T??n ????ng nh???p * ").pack()
    register_username_entry = Entry(register_screen, textvariable = register_username)
    register_username_entry.pack()
    
    Label(register_screen, text = "M???t kh???u * ").pack()
    register_password_entry =  Entry(register_screen, textvariable = register_password)
    register_password_entry.pack()
    
    Label(register_screen, text = "").pack()
    Button(register_screen, text = "????ng k??", width = 10, height = 1, command = register_user).pack()

def weather_app_home():
    try:
        global weather_home_screen

        send(IN_APP)

        login_name = receive()

        if login_name == ADMIN:
            login_screen.destroy()
            send(ADMIN)
            admin()
        else:
            weather_home_screen = Toplevel(welcome_screen)
            weather_home_screen.title("???ng d???ng th???i ti???t")
            weather_home_screen.geometry("400x450")    
            Label(weather_home_screen, text = "Ch??o m???ng " + login_name, bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
            Label(weather_home_screen, text = "Xem th???i ti???t...").pack()
            Label(weather_home_screen, text = "").pack()
            
            Button(weather_home_screen, text = "Nhi???u t???nh th??nh", height = "2", width = "30", command = all_cities).pack()
            
            Label(weather_home_screen, text = "").pack()
            Button(weather_home_screen, text = "M???t t???nh th??nh",height = "2", width = "30", command = one_city).pack()
    except:
        Label(weather_home_screen, text = "Server Closed, program will close after 3s", fg = "red" ,font = ("calibri", 10)).pack()
        welcome_screen.after(3000, welcome_screen.destroy)
        client.close()


        
def all_cities():
    try:
        global all_cities_screen
        
        send(ALL_CITIES)
        weather_home_screen.destroy()
        
        all_cities_screen = Toplevel(welcome_screen)
        all_cities_screen.title("???ng d???ng th???i ti???t - Th??ng tin chung")
        all_cities_screen.geometry("500x550")  
        
        Label(all_cities_screen, text = "").pack()
        Label(all_cities_screen, text = "D??? b??o th???i ti???t ng??y " + str(today)).pack()
        Label(all_cities_screen, text = "").pack()
        Label(all_cities_screen, text = "-----------------------------------------------------------------------------------------------", justify = "left").pack()
        
        weather_info = receive()
        Label(all_cities_screen, text = weather_info, justify = "left").pack()
        weather_app_home()
        print("hello");
    except:
        Label(weather_home_screen, text = "Server Closed, program will close after 3s", fg = "red" ,font = ("calibri", 10)).pack()
        welcome_screen.after(3000, welcome_screen.destroy)
        client.close()
    
def one_city_show():
    try:
        global one_city_show_screen

        one_city_screen.destroy()
        one_city_show_screen = Toplevel(welcome_screen)
        one_city_show_screen.title("???ng d???ng th???i ti???t - Th??ng tin m???t t???nh th??nh")
        one_city_show_screen.geometry("700x550") 
        
        city = city_name.get()
        send(city)
        weather_home_screen.destroy()
        
        Label(one_city_show_screen, text = "").pack()
        Label(one_city_show_screen, text = "D??? b??o th???i ti???t " + city + " 7 ng??y t???i").pack()
        Label(one_city_show_screen, text = "").pack()
        
        weather_info = receive()
        Label(one_city_show_screen, text = weather_info).pack(pady = 10)
        weather_app_home()
    except:
        Label(weather_home_screen, text = "Server Closed, program will close after 3s", fg = "red" ,font = ("calibri", 10)).pack()
        welcome_screen.after(3000, welcome_screen.destroy)
        client.close()
    
def one_city():
    try:
        global one_city_screen
        global city_name
        
        send(ONE_CITY)
        
        one_city_screen = Toplevel(welcome_screen)
        one_city_screen.title("???ng d???ng th???i ti???t - Th??ng tin m???t t???nh th??nh")
        one_city_screen.geometry("350x300")
        
        cities = receive()
        city_list = list(cities.split(","))
        
        Label(one_city_screen, text = "Danh s??ch t???nh th??nh hi???n c?? ").pack()
        city_name = StringVar()
        city_name.set(city_list[0])
        drop = OptionMenu(one_city_screen, city_name, *city_list)
        drop.pack(pady = 10)
        
        Button(one_city_screen, text = "Xem th???i ti???t", width = 10, height = 1, command = one_city_show).pack()
    except:
        Label(weather_home_screen, text = "Server Closed, program will close after 3s", fg = "red" ,font = ("calibri", 10)).pack()
        welcome_screen.after(3000, welcome_screen.destroy)
        client.close()
 
def admin():
    try:
        menu = receive()
        admin_input = input(menu)
        send(admin_input)
        
        if (admin_input == "4"):
            print("Ch????ng tr??nh k???t th??c")
            return
        
        msg = receive()
        if msg == FUNCTION_1:
            function_1()
            admin()
            return
        elif msg == FUNCTION_2:
            function_2()
            admin()
            return
        elif msg == FUNCTION_3:
            function_3()
            admin()
            return
        elif msg == INVALID:
            print("Ch???c n??ng kh??ng t???n t???i")
            admin()
            return  
    except:
        print("****SERVER CLOSED****")
        client.close()
                
def function_1():
    try:
        print("-.-.-.-.-.- Th??m th??ng tin th???i ti???t m???i cho th??nh ph??? -.-.-.-.-.-")
        city_input = input("- Nh???p t??n th??nh ph??? mu???n th??m m???i: ")
        send(city_input)
        
        date_input = input("- Nh???p ng??y mu???n th??m m???i (?????nh d???ng YYYY-MM-DD): ")
        send(date_input)
        
        weather_input = input("- Nh???p th??ng tin th???i ti???t: ")
        send(weather_input)
        
        temp_input = input("- Nhi???t ?????: ") 
        send(temp_input)
        
        msg = receive()
        if msg == ADD_NEW_SUCCESSFULL:
            print("---------TH??M M???I TH??NH C??NG----------")
            print("- Th??ng tin m???i c???p nh???t: ")
            weather_info = receive()
            print(weather_info)
            print("--------------------------------------------------")
            return
        elif msg == INVALID:
            print("****Ng??y nh???p v??o kh??ng ????ng v???i ?????nh d???ng****")
            return
        elif msg == ADD_NEW_FAIL:
            print("****Th??m m???i kh??ng th??nh c??ng****")
            return
        elif msg == DUPLICATE:
            print("****Th??ng tin th???i ti???t cho th??nh ph??? v?? ng??y n??y ???? t???n t???i****")
            return
    except:
        print("****SERVER CLOSED****")
        client.close()
    
def function_2():
    try:
        print("-.-.-.-.-.- C???p nh???t th??ng tin th???i ti???t theo ng??y -.-.-.-.-.-")
        date_input = input("Nh???p ng??y mu???n c???p nh???t th??ng tin (?????nh d???ng YYYY-MM-DD): ")
        send(date_input)
        
        msg = receive()
        if msg == INVALID:
            print("Ng??y nh???p v??o kh??ng ????ng v???i ?????nh d???ng")
            return
        if msg == EMPTY:
            print("****Kh??ng c?? th??ng tin th???i ti???t cho T???nh/Th??nh v??o ng??y t????ng ???ng****")
            return
        
        cities = msg
        city_list = list(cities.split(","))
        
        for city in city_list:
            print("=.=.=.=.= C???p nh???t cho T???nh/Th??nh ph??? %s =.=.=.=.=" %(city))
            weather_input = input("Nh???p th??ng tin th???i ti???t m???i: ")
            send(weather_input)
            
            temp_input = input("Nhi???t ????? m???i: ") 
            send(temp_input)
            
        received_msg = receive()
        if received_msg == SUCCESSFULL:
            print("---------C???P NH???T TH??NH C??NG----------")
            return
    except:
        print("****SERVER CLOSED****")
        client.close()
        

def function_3():
    try:
        print("-.-.-.-.-.- C???p nh???t th??ng tin th???i ti???t theo th??nh ph??? cho 7 ng??y k??? ti???p -.-.-.-.-.-")
        
        cities = receive()
        city_list = list(cities.split(","))
        i = 1
        print("-----Danh s??ch T???nh/Th??nh c?? th??ng tin th???i ti???t trong 7 ng??y t???i-----")
        for city in city_list:
            print("%i. %s" %(i, city))
            i = i + 1
            
        city_input = input("- Nh???p T???nh/Th??nh ph??? mu???n c???p nh???t (y??u c???u nh???p ch??nh x??c nh?? tr??n): ")
        send(city_input)
        
        msg = receive()
        if msg == INVALID:
            print("****Kh??ng t???n t???i T???nh/Th??nh ph???****")
            return
        
        num_dates = int (msg)
        
        if num_dates == 7:
            i = num_dates - 1
            while i >= 0:
                open_str = receive()
                print(open_str)
                
                weather_input = input("- Nh???p th??ng tin th???i ti???t m???i: ")
                send(weather_input)
                
                temp_input = input("- Nhi???t ????? m???i: ") 
                send(temp_input)
                
                i = i - 1
                
        elif num_dates < 7:
            if num_dates == 0:
                i = 0
                while i < 7:
                    open_str = receive()
                    print(open_str)
                    
                    weather_input = input("- Nh???p th??ng tin th???i ti???t m???i: ")
                    send(weather_input)
                    
                    temp_input = input("- Nhi???t ????? m???i: ") 
                    send(temp_input)

                    i += 1
                    
            else:
                i = num_dates - 1
                while i >= 0:
                    open_str = receive()
                    print(open_str)
                    
                    weather_input = input("- Nh???p th??ng tin th???i ti???t m???i: ")
                    send(weather_input)
                    
                    temp_input = input("- Nhi???t ????? m???i: ") 
                    send(temp_input)
                    
                j = num_dates
                while j < 7:
                    open_str = receive()
                    print(open_str)
                    
                    weather_input = input("- Nh???p th??ng tin th???i ti???t m???i: ")
                    send(weather_input)
                    
                    temp_input = input("- Nhi???t ????? m???i: ") 
                    send(temp_input)
                    
                    j += 1
                    
        received_msg = receive()
        
        if received_msg == SUCCESSFULL:
            print("---------C???P NH???T TH??NH C??NG----------")
            return
        
    except:
        print("****SERVER CLOSED****")
        client.close()
        
def main_screen():
    global welcome_screen
    welcome_screen = Tk()
    welcome_screen.geometry("300x250")
    welcome_screen.title("???ng d???ng th???i ti???t")
    Label(text = "Ch??o m???ng b???n", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    
    Label(text = "").pack()
    Button(text = "????ng nh???p", height = "2", width = "30", command = login).pack()
    
    Label(text = "").pack()
    Button(text = "????ng k??",height = "2", width = "30", command = register).pack()
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            welcome_screen.destroy()
            client.send(str.encode("!DISCONNECT"))
            client.close()

    welcome_screen.protocol("WM_DELETE_WINDOW", on_closing)
    welcome_screen.mainloop()


main_screen()
