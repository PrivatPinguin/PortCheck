# takes an ip adress and scan it for open and closed ports
# and attach the results to a file
ERROR_MSG_HELP = "Usage: 'python3 scan_ip_ports.py gui' or python3 scan_ip_ports.py <ip> [ optional:<star_port>, <end_port>, *<file> = <ip>+<file>* ]\n"
ERROR_MSG_00 = "\tError\tInvalid ip adress\n"
ERROR_MSG_01 = "\tError\tStart port is higher than end port\n"
ERROR_MSG_02 = "\tError\tStart port or end port is out of range\n"
FILE_FOOTENER = "_portscan.log"
FILE_IS_OPEN = False

def __stringify_open_port(port):
    return "Port {} is open".format(port)

def __scan_ip_ports_file(ip, port, file):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, port))
        s.close()
        file.write(__stringify_open_port(port) + "\n")
        print(__stringify_open_port(port))
    except:
        # print("Port {} is closed".format(port)) # too fast to print in terminal 
        # file.write("Port {} is closed\n".format(port)) # uncomment to save to file
        pass 

# try create a header string with the date and time and atache ip adress to it else create sting with ip adress
def __create_header_string(ip):
    bs = "\n"
    try:
        import datetime
        time_now = datetime.datetime.now()
        file_header = str(time_now) + "\nIP:\t" + ip + bs
        return file_header, time_now
    except:
        file_header = ip + bs
        return file_header, time_now

# check if ip is valid 
def check_ip(ip):
    """
    checks if ip is reachable and valid
    """
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

# create a funktion that takes passed time and returns a string with the passed time
def __time_difference(time_then):
    time_diff = ""
    try:
        import datetime
        time_now = datetime.datetime.now()
        time_diff =  time_now - time_then
        # prints the time difference in minutes
        return "Time to finish:\n\t{} min\n\t{} sec\n\t{} ms".format(time_diff.seconds//60, time_diff.seconds, time_diff.microseconds)
    except:
        return ("Time to finish:\n\t" + str(time_diff))

# a threaded funktion that takes an ip adress and scan it for open and closed port in a thread saves the results to a file
# a funktion that starts a thread for each port in a range and saves the results to a file
def threaded_scan_file(ip, start_port=1, end_port=65535, file=FILE_FOOTENER):
    """
    PortCheck
    ---------
    Checks the given IP for open Ports - if port is open: logs open ports in file.
    use:
    threaded_scan_file( IP as string | optional: Start-Port | optional: End-Port | optional: Custom-file-name )
    """
    #checkif start_port and end_port are valid
    if end_port.lower() == "max":
        end_port = 65535
    if end_port:      
        if type(end_port) != int:
            end_port = int(end_port)+1
    else:
        end_port = 65535
    if start_port:
        if type(start_port) != int:
            start_port = int(start_port)
    else:
        start_port = 1
    if start_port > end_port:
        return ERROR_MSG_01
    elif start_port < 1 or end_port > 65535:
        return ERROR_MSG_02
    if check_ip(ip):
        file = open(ip + FILE_FOOTENER, "w")
        #opens a new file
        header, time_now= __create_header_string(ip)
        file.write(header)
        print(header)
        for port in range(start_port, end_port): #  65535):
            # chrates a threaded __scan_ip_ports_file function
            t = threading.Thread(target=__scan_ip_ports_file, args=(ip, port, file))
            t.start()
        t.join()
        file.close()
        return __time_difference(time_now)
    else:
        return (ERROR_MSG_HELP + ERROR_MSG_00)
# opens file content
def __open_file(file, ip):
    if not file:
        file = ip + FILE_FOOTENER
        #paste content of file to a sting
    try:
        #read file and print it
        with open(file, "r") as f:
            file = f.read()
        f.close()
        return file
    except:
        return 'Error\treading logfile.'

# create a gui that uses threaded_scan_file function where the user can enter ip adress and scan it for open and closed ports
def gui_show():
    """
    PortCher GUI
    ------------
    opens a GUI to ender IP, Start-/End-Port and Filename
    
    check 'threaded_scan_file(*)' for more information.
    """
    try:
        import tkinter as tk
    except:
        return 'ImportError\tInstall TKinter\n\nLinux\tsudo apt-get install python3-tk\n\nWindows\tpip install python-tk\nor\tpip install python3-tk'
    # create a window
    window = tk.Tk()
    window.title("Port Scanner")
    window.geometry("250x300")
    # create a label
    label = tk.Label(window, text="Enter IP:")
    label.grid(column=0, row=0)
    # create a text box
    ip_box = tk.Entry(window, width=15)
    ip_box.grid(column=1, row=0)
    # create a label
    label = tk.Label(window, text="Start Port:")
    label.grid(column=0, row=1)
    # create a text box
    start_port_box = tk.Entry(window, width=15)
    start_port_box.grid(column=1, row=1)
    # create a label
    label = tk.Label(window, text="End Port:")
    label.grid(column=0, row=2)
    # create a text box
    end_port_box = tk.Entry(window, width=15)
    end_port_box.grid(column=1, row=2)
    # create a label
    label = tk.Label(window, text="File:")
    label.grid(column=0, row=3)
    # create a text box
    file_box = tk.Entry(window, width=15)
    file_box.grid(column=1, row=3)
    # create empty label on the right side with red text 
    #create a var for empty label with text alignment left
    label_result = tk.Label(window, text="", fg="red", anchor="w", justify="left")
    label_result.grid(column=1, row=5)
    # create a button when pressed it gets the result of the file and stores it in label_result
    def __get_result():
        try:
        # show wait animation while scanning
            label_result.config(text="Scanning...")
            window.update()
            scan_text = threaded_scan_file(ip_box.get(), start_port_box.get(), end_port_box.get(), file_box.get())
            result = scan_text + "\n" + __open_file(file_box.get(), ip_box.get())
            label_result.config(text=result)
            window.update()
        except:
            label_result.config(text="Error")
        
    # create a button
    button = tk.Button(window, text="Scan", command=__get_result)
    button.grid(column=1, row=4)
    # start the window
    window.mainloop()

# open the python file as a scirpt and take ip as an argument or start gui
if __name__ == "__main__":
    import sys, socket, threading
    if len(sys.argv) == 0:
        print(ERROR_MSG_HELP + ERROR_MSG_00)
    elif len(sys.argv) == 1:
        gui_show()
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == "gui":
            gui_show()
        else:
            print(threaded_scan_file(sys.argv[1]))
    elif len(sys.argv) == 3:
        print(ERROR_MSG_HELP + ERROR_MSG_02)
    elif len(sys.argv) == 4:
        print(threaded_scan_file(sys.argv[1], sys.argv[2], sys.argv[3]))
    elif len(sys.argv) == 5:
        print(threaded_scan_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print(ERROR_MSG_HELP)
