import socket #for socket
import threading
import DatabaseController
import time
from datetime import date, datetime, timedelta


#default port for socket
PORT = 5050

#client and server can connect without on a same machine
SERVER = socket.gethostbyname(socket.gethostname()) #server for local host

# SERVER = "139.162.55.220" #host online
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "LOGIN"
REGISTER_MESSAGE = "REGISTER"
EXIST_USER = "EXIST USER"
LOGIN_SUCCESSFUL = "LOGIN SUCCESSFUL"
LOGIN_FAIL = "LOGIN FAIL"
REGISTER_SUCCESSFUL = "REGISTER SUCCESFULL"
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#Read File for login
datanew = {} #gan du lieu tu def readFile len global cho cac ham khac
userNameListglobal = [] #gan du lieu tu def readFile len global cho cac ham khac
passWordListglobal = [] #gan du lieu tu def readFile len global cho cac ham khac

def readFile():
    loginSignup = open("userList.txt", "r") #open database.txt, mode read

    #tach username va password
    userNameList = [] 
    passWordList = []

    #tung acc trong file, split , username, password-> list de truy cap, zip lai do dict() chi nhan 1 bien, ep kieu ve dict 
    for i in loginSignup:
        username, password = i.split(",")
        password = password.strip()
        userNameList.append(username)
        passWordList.append(password)
    data = dict(zip(userNameList, passWordList))

    #xu ly file xong gan len bien global
    global datanew, userNameListglobal, passWordListglobal
    datanew = data
    userNameListglobal = userNameList
    passWordListglobal = passWordList
    #print(datanew)

#daemon thread luon chay o background, doc file real time 
read_Thread = threading.Thread(target=readFile, daemon=True)
read_Thread.start()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)        
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == LOGIN_MESSAGE:
                    login(conn)
                elif msg == REGISTER_MESSAGE:
                    register(conn)
                elif msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"{addr} disconnected")
                    conn.close()
    except:
        print(f"[{addr}] disconnected")
        conn.close()

       
def login(conn):        
    try:
        global login_name
        
        name_length = conn.recv(HEADER).decode(FORMAT)
        if name_length:
            name_length = int(name_length)
            login_name = conn.recv(name_length).decode(FORMAT)
            
        pass_length = conn.recv(HEADER).decode(FORMAT)
        if pass_length:
            pass_length = int(pass_length)
            password = conn.recv(pass_length).decode(FORMAT)  
        
        if datanew[login_name] == password: #check value cua key trong database vs input client
            conn.send(LOGIN_SUCCESSFUL.encode(FORMAT))
            weather(conn)
        else:
            conn.send(LOGIN_FAIL.encode(FORMAT))
            print(f"[{login_name}] disconnected")
            conn.close()
    except:
        print(f"[{login_name}] disconnected")
        conn.close()
    
def register(conn):
    try:
        name_length = conn.recv(HEADER).decode(FORMAT)
        if name_length:
            name_length = int(name_length)
            name = conn.recv(name_length).decode(FORMAT)
            
        pass_length = conn.recv(HEADER).decode(FORMAT)
        if pass_length:
            pass_length = int(pass_length)
            password = conn.recv(pass_length).decode(FORMAT)  
        
        if name in userNameListglobal:
            conn.send(EXIST_USER.encode(FORMAT))
            print(f"[{login_name}] disconnected")
            conn.close()
        else:
            loginSignup = open("userList.txt", "a") #open database.txt, mode append 
            loginSignup.write(name+","+password+"\n")
            userNameListglobal.append(name) #append list username+passwordGlobal
            passWordListglobal.append(password) 
            loginSignup.close() #dong file de commit viet file. 
                                        #Neu khong dong file thi sau khi het func file moi duoc append -> Loi endless loop signup 

            global datanew
            datanew=dict(zip(userNameListglobal,passWordListglobal)) #data moi sau client signup
            conn.send(REGISTER_SUCCESSFUL.encode(FORMAT)) 
    except:
        print(f"[{login_name}] disconnected")
        conn.close()
        
def weather(conn):
    try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(HEADER).decode(FORMAT)
            
        if msg == IN_APP:
            conn.send(login_name.encode(FORMAT))
            message_length = conn.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = conn.recv(HEADER).decode(FORMAT)
                
                if message == ALL_CITIES:
                    all_cities(conn)
                elif message == ONE_CITY:
                    one_city(conn)
                elif message == ADMIN:
                    admin(conn)
    except:
        print(f"[{login_name}] disconnected")
        conn.close()
        
#Lay ngay thang thoi gian chay code
today = date.today()

def all_cities(conn):
    db_connection = DatabaseController.connect()
    details = DatabaseController.show_weather(db_connection, today)
    print(details)
    weather_info = ""
    for detail in details:
        weather_info += "Th??nh ph???: %s \t\t  Th???i ti???t: %s \t\t  Nhi???t ?????: %s \n" %(detail[0], detail[2], detail[3])
        weather_info += "---------------------------------------------------------------------------------------------- \n"
        
    conn.send(weather_info.encode(FORMAT))
    
    db_connection.close()
    weather(conn)

def one_city(conn):
    db_connection = DatabaseController.connect()
    city_list = ""
    cities = DatabaseController.show_cities(db_connection)
    i = len(cities)
    for city in cities:
        city_list += "%s" %(city)
        i = i - 1
        if i == 0:
            break
        else:
            city_list += ","
        
    conn.send(city_list.encode(FORMAT))
    
    global city_name
    city_name_length = conn.recv(HEADER).decode(FORMAT)
    if city_name_length:
        city_name_length = int(city_name_length)
        city_name = conn.recv(HEADER).decode(FORMAT)
        
    details = DatabaseController.show_weather_in_next_7_days(db_connection, city_name)
    weather_info = ""
    
    if (len(details) == 0):
        weather_info += "Kh??ng c?? th??ng tin th???i ti???t cho 7 ng??y t???i cho T???nh/Th??nh ph??? %s" %(city_name)
    else:
        for detail in details:
            weather_info += "Th??nh ph???: %s \t Ng??y: %s \t  Th???i ti???t: %s \t  Nhi???t ?????: %s \n" %(detail[0], detail[1], detail[2], detail[3])
            weather_info += "---------------------------------------------------------------------------------------------- \n"
        
    conn.send(weather_info.encode(FORMAT))
            
    db_connection.close()
    weather(conn)

def get_list_city():
    db_connection = DatabaseController.connect()
    return DatabaseController.show_cities(db_connection)

def get_date_list(city_name):
    db_connection = DatabaseController.connect()
    return DatabaseController.show_dates(db_connection, city_name)

def get_cities_in_date(date):
    db_connection = DatabaseController.connect()
    return DatabaseController.show_cities_in_date(db_connection, date)

def get_next_7_days(city_name):
    db_connection = DatabaseController.connect()
    return DatabaseController.show_next_7_dates_for_city(db_connection, city_name)

ADMIN_DASHBOARD = """
B???NG ??I???U KHI???N:
1. Th??m th??ng tin th???i ti???t m???i cho th??nh ph???
2. C???p nh???t th??ng tin th???i ti???t theo ng??y cho th??nh ph???
3. C???p nh???t th??ng tin th???i ti???t cho 7 ng??y g???n nh???t cho th??nh ph???
4. Tho??t
M???i ch???n ch???c n??ng v???i s??? t????ng ???ng: 
""" 

def admin(conn):
    connected = True
    try:
        while connected:
            try:
                conn.send(ADMIN_DASHBOARD.encode(FORMAT))
                
                admin_input_length = conn.recv(HEADER).decode(FORMAT)
                if admin_input_length:
                    admin_input_length = int(admin_input_length)
                    admin_input = conn.recv(HEADER).decode(FORMAT)
                    
                while admin_input != "4":
                    if admin_input == "1":
                        function_1(conn)
                        admin(conn)
                        return
                    elif admin_input == "2":
                        function_2(conn)
                        admin(conn)
                        return
                    elif admin_input == "3":
                        function_3(conn)
                        admin(conn)
                        return
                    else:
                        conn.send(INVALID.encode(FORMAT))
                        admin(conn)
                        return
                print("DONE DASHBOARD")
                print("Client closed")
                connected = False
            except:
                print("Client closed")
                break
    except:
        connected = False
        
    conn.close()
    
def function_1(conn):
    conn.send(FUNCTION_1.encode(FORMAT))
    city_name_length = conn.recv(HEADER).decode(FORMAT)
    if city_name_length:
        city_name_length = int(city_name_length)
        city_name = conn.recv(city_name_length).decode(FORMAT)
        
    date_length = conn.recv(HEADER).decode(FORMAT)
    if date_length:
        date_length = int(date_length)
        date = conn.recv(date_length).decode(FORMAT)
        
    weather_length = conn.recv(HEADER).decode(FORMAT)
    if weather_length:
        weather_length = int(weather_length)
        weather = conn.recv(weather_length).decode(FORMAT)
        
    temp_length = conn.recv(HEADER).decode(FORMAT)
    if temp_length:
        temp_length = int(temp_length)
        temp = conn.recv(temp_length).decode(FORMAT)
    
    #ki???m tra ng??y nh???p v??o c?? ????ng ?????nh d???ng kh??ng    
    try:
        check_day = datetime.strptime(date, '%Y-%m-%d')
    except:
        conn.send(INVALID.encode(FORMAT))
        return
    
    #ki???m tra city c?? trong list city    
    cities = get_list_city()
    compare_city = ""    
    for city in cities:
        if city_name == city[0]:
            compare_city = "equal"
            break
        else:
            compare_city = "not equal"
    
    #ki???m tra ng??y c?? trong list date                    
    dates = get_date_list(city_name)
    compare_date = ""    
    for in_day in dates:
        print("in_day: ", in_day)
        print("in_day[0]: ", in_day[0])
        if date == in_day[0]:
            compare_date = "equal"
            break
        else:
            compare_date = "not equal"
    
    #th???a m??n kh??ng t???n t???i tp v?? ng??y
    if (compare_city == "not equal" and (compare_date == "not equal" or compare_date == "")):    
        db_connection = DatabaseController.connect()    
        DatabaseController.insert_weather(db_connection, city_name, date, weather, temp)
        
        details = DatabaseController.show_weather_in_day(db_connection, city_name, date)
        #ki???m tra c???p nh???t th??nh c??ng
        if len(details) != 0:
            conn.send(ADD_NEW_SUCCESSFULL.encode(FORMAT))
            weather_info = ""
            for detail in details:
                weather_info += "T???nh/Th??nh ph???: %s \n Ng??y: %s \n Th???i ti???t: %s \n Nhi???t ?????: %s" %(detail[0], detail[1], detail[2], detail[3])
            
            conn.send(weather_info.encode(FORMAT))
        else:
            conn.send(ADD_NEW_FAIL.encode(FORMAT))
    else:
        conn.send(DUPLICATE.encode(FORMAT))
        
    time.sleep(0.5)
    return
  
def function_2(conn):
    conn.send(FUNCTION_2.encode(FORMAT))
     
    date_length = conn.recv(HEADER).decode(FORMAT)
    if date_length:
        date_length = int(date_length)
        date = conn.recv(date_length).decode(FORMAT)
     
    #ki???m tra ng??y ????ng ?????nh d???ng   
    try:
        in_day = datetime.strptime(date, '%Y-%m-%d')
    except:
        conn.send(INVALID.encode(FORMAT))
        return
    
    #l???y danh s??ch tp c?? th??ng tin trong ng??y ????
    cities = get_cities_in_date(date)
    num_cities = len(cities)
    
    #n???u danh s??ch = 0, kh??ng t???n t???i tp n??o ????? update
    if num_cities == 0:
        conn.send(EMPTY.encode(FORMAT))
        return
    
    #g???i danh s??ch tp sang client
    city_list = ""
    for city in cities:
        city_list += "%s" %(city)
        num_cities = num_cities - 1
        if num_cities == 0:
            break
        else:
            city_list += ","
    conn.send(city_list.encode(FORMAT))
    
    #c???p nh???t th???i ti???t v?? nhi???t ????? cho t???ng th??nh ph??? trong danh s??ch
    for city in cities:
        weather_length = conn.recv(HEADER).decode(FORMAT)
        if weather_length:
            weather_length = int(weather_length)
            weather = conn.recv(weather_length).decode(FORMAT)
            print(weather)
            
        temp_length = conn.recv(HEADER).decode(FORMAT)
        if temp_length:
            temp_length = int(temp_length)
            temp = conn.recv(temp_length).decode(FORMAT)
            print(temp)
           
        db_connection = DatabaseController.connect()
        DatabaseController.update_weather_in_time(db_connection, weather, temp, city[0], date)
    
    conn.send(SUCCESSFULL.encode(FORMAT))   
    time.sleep(0.5)
    return
        
def function_3(conn):
    conn.send(FUNCTION_3.encode(FORMAT))
    
    #l???y danh s??ch tp g???i cho client
    cities = get_list_city()
    num_cities = len(cities)
    city_list = ""
    for city in cities:
        city_list += "%s" %(city)
        num_cities = num_cities - 1
        if num_cities == 0:
            break
        else:
            city_list += ","
    conn.send(city_list.encode(FORMAT))
    
    #nh???n t??n tp t??? client
    city_name_length = conn.recv(HEADER).decode(FORMAT)
    if city_name_length:
        city_name_length = int(city_name_length)
        city_name = conn.recv(city_name_length).decode(FORMAT)    
        
    #so s??nh t??n tp client g???i c?? trong list tp kh??ng    
    compare = ""    
    for city in cities:
        if city_name == city[0]:
            compare = "equal"
            break
        else:
            compare = "not equal"
    
    #n???u kh??ng th?? th??ng b??o client v?? ng???ng nh???p
    if compare == "not equal":
        conn.send(INVALID.encode(FORMAT))
        return
    
    #l???y danh s??ch 7 ng??y ti???p theo cho tp client nh???p v??o
    dates = get_next_7_days(city_name)
    num_dates = len(dates)
    conn.send(str(num_dates).encode(FORMAT))
    
    #n???u tp c?? ????? 7 ng??y, c???p nh???t bth
    if num_dates == 7:    
        for date in dates:
            open_str = "=.=.=.=.= C???p nh???t cho ng??y %s =.=.=.=.=" %(date[0])
            conn.send(open_str.encode(FORMAT))
            
            weather_length = conn.recv(HEADER).decode(FORMAT)
            if weather_length:
                weather_length = int(weather_length)
                weather = conn.recv(weather_length).decode(FORMAT)
                
            temp_length = conn.recv(HEADER).decode(FORMAT)
            if temp_length:
                temp_length = int(temp_length)
                temp = conn.recv(temp_length).decode(FORMAT)

            db_connection = DatabaseController.connect()
            DatabaseController.update_weather_in_time(db_connection, weather, temp, city_name, date[0])
    
    #n???u s??? ng??y tr??? ra < 7
    elif num_dates < 7:
        #n???u s??? ng??y l?? 0, ti???n h??nh th??m m???i
        if num_dates == 0:
            i = 0
            in_day = today
            print(today)
            while i < 7:
                open_str = "=.=.=.=.= C???p nh???t cho ng??y %s =.=.=.=.=" %(in_day)
                conn.send(open_str.encode(FORMAT))
            
                weather_length = conn.recv(HEADER).decode(FORMAT)
                if weather_length:
                    weather_length = int(weather_length)
                    weather = conn.recv(weather_length).decode(FORMAT)
                    
                temp_length = conn.recv(HEADER).decode(FORMAT)
                if temp_length:
                    temp_length = int(temp_length)
                    temp = conn.recv(temp_length).decode(FORMAT)
                    
                db_connection = DatabaseController.connect()
                DatabaseController.insert_weather(db_connection, city_name, in_day, weather, temp)

                in_day = in_day + timedelta(days = 1)
                print(in_day)
                i += 1
                
        else:
            #n???u c?? nh??ng ??t h??n 7 ng??y, c???p nh???t 1 ?????i v???i ng??y ???? c?? trong db v?? th??m m???i ?????i v???i nh???ng ng??y kh??ng c?? 
            for date in dates:
                open_str = "=.=.=.=.= C???p nh???t cho ng??y %s =.=.=.=.=" %(date[0])
                conn.send(open_str.encode(FORMAT))
                
                weather_length = conn.recv(HEADER).decode(FORMAT)
                if weather_length:
                    weather_length = int(weather_length)
                    weather = conn.recv(weather_length).decode(FORMAT)
                    
                temp_length = conn.recv(HEADER).decode(FORMAT)
                if temp_length:
                    temp_length = int(temp_length)
                    temp = conn.recv(temp_length).decode(FORMAT)

                db_connection = DatabaseController.connect()
                DatabaseController.update_weather_in_time(db_connection, weather, temp, city_name, date[0])

            i = num_dates
            in_day = date[num_dates - 1]
            in_day = datetime.strptime(in_day, '%Y-%m-%d')
            print(in_day)
            while i < 7:
                open_str = "=.=.=.=.= C???p nh???t cho ng??y %s =.=.=.=.=" %(in_day)
                conn.send(open_str.encode(FORMAT))
                
                weather_length = conn.recv(HEADER).decode(FORMAT)
                if weather_length:
                    weather_length = int(weather_length)
                    weather = conn.recv(weather_length).decode(FORMAT)
                    
                temp_length = conn.recv(HEADER).decode(FORMAT)
                if temp_length:
                    temp_length = int(temp_length)
                    temp = conn.recv(temp_length).decode(FORMAT)
                    
                db_connection = DatabaseController.connect()
                DatabaseController.insert_weather(db_connection, city_name, in_day, weather, temp)

                in_day = in_day + timedelta(days = 1)
                print(in_day)
                i += 1
    
    conn.send(SUCCESSFULL.encode(FORMAT))  
    time.sleep(0.5)
    return
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
while True:
    start()
