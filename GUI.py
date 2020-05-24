from tkinter import *
import database
from client import *
import threading


class Gui:
    """gui class - the class that create the GUI in this project
    and handle all the things in front of the client handler"""

    def __init__(self):
        self.client = Client()  # create client object
        self.account_screen = Tk()
        self.ok = False
        # create the account screen of the gui
        self.main_account_screen()
        self.txt = None
        self.chat_entry = None
        self.chat_screen = None
        self.try_again_screen = None
        self.username_login_text_box = None
        self.password_login_text_box = None
        self.username_check = None
        self.password_check = None
        self.login_screen = None
        self.username = None
        self.password = None
        self.password_text_box = None
        self.username_text_box = None
        self.sign_up_screen = None
        self.listbox = None
        self.build = False
        self.value = ""
        self.now_chat = "broadcast"
        self.list_connected = []
        self.dict_name_messages = {}
        self.my_name = ""
        self.client_name_label = None

    def rcv_message(self):
        """
        thread's function that wait to receive message
        """
        while not self.build:
            pass
        while True:
            rcv_msg = self.client.rcv_message()
            print(rcv_msg)
            self.handle_msg(rcv_msg)

    def handle_msg(self, rcv_msg):
        """
        function that handle the gui with the messages that she gets
        """
        to_whom = ""
        if "*" in rcv_msg:  # * - insert to the list box the name of the clients
            self.listbox_insert(rcv_msg.split("*")[0])
        elif "%" in rcv_msg:  # % - gets the name of the client from the login or sign_up in client handler
            self.my_name = rcv_msg.split("%")[0]
            self.client_name_label['text'] = self.my_name
        elif "&" in rcv_msg:  # & - private message
            to_whom = rcv_msg.split("&")[0]
            rcv_msg = rcv_msg.split("&")[1]
            if to_whom in self.dict_name_messages:  # create or add to the dictionary - (key= name) (value = msg)
                self.dict_name_messages[to_whom].append(rcv_msg)
            else:
                self.dict_name_messages.update({to_whom: [rcv_msg]})
        else:  # broadcast messages
            to_whom = "broadcast"
            if "broadcast" in self.dict_name_messages:  # create or add to the dictionary -
                # (key= broadcast) (value = msg)
                self.dict_name_messages["broadcast"].append(rcv_msg)
            else:
                self.dict_name_messages.update({"broadcast": [rcv_msg]})
        if to_whom == self.now_chat:  # If the client is on the sender's name in LISTBOX and he receive a message
            # then the straight message will be written to the screen
            self.txt.configure(state='normal')
            self.txt.insert(END, rcv_msg + '\n')
            self.txt.configure(state='disabled')

    def sign_up(self):
        """create the sign_up screen"""
        self.sign_up_screen = Toplevel(self.account_screen)
        self.sign_up_screen.title("sign_up")
        self.sign_up_screen.geometry("300x250")
        Label(self.sign_up_screen, text="").pack()
        username_lable = Label(self.sign_up_screen, text="Username")
        username_lable.pack()
        self.username = StringVar()
        self.password = StringVar()
        self.username_text_box = Entry(self.sign_up_screen, textvariable=self.username)
        self.username_text_box.pack()
        password_lable = Label(self.sign_up_screen, text="Password")
        password_lable.pack()
        self.password_text_box = Entry(self.sign_up_screen, textvariable=self.password, show='*')
        self.password_text_box.pack()
        Label(self.sign_up_screen, text="").pack()
        Button(self.sign_up_screen, text="sign_up", width=10, height=1, bg="navy", fg="white",
               command=self.sign_up_check).pack()

    def login(self):
        """create the login screen"""
        self.login_screen = Toplevel(self.account_screen)
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")
        Label(self.login_screen, text="").pack()
        self.username_check = StringVar()
        self.password_check = StringVar()
        Label(self.login_screen, text="Username").pack()
        self.username_login_text_box = Entry(self.login_screen, textvariable=self.username_check)
        self.username_login_text_box.pack()
        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Password").pack()
        self.password_login_text_box = Entry(self.login_screen, textvariable=self.password_check, show='*')
        self.password_login_text_box.pack()
        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Login", width=10, height=1, bg="navy", fg="white",
               command=self.login_check).pack()

    def sign_up_check(self):
        """check with the client handler that the username not in use"""
        username_info = self.username.get()
        password_info = self.password.get()
        if self.username.get() == '' or self.password.get() == '':
            self.try_again()
        else:
            self.client.send_message(username_info + "#" + password_info)
            rcv_msg = self.client.rcv_message()
            print(rcv_msg)
            self.username_text_box.delete(0, END)
            self.password_text_box.delete(0, END)
            if "use" in rcv_msg:
                self.try_again()
            else:
                self.ok = True
                self.account_screen.destroy()

    def login_check(self):
        """check with the client handler that the username and the password are okay"""
        username1 = self.username_check.get()
        password1 = self.password_check.get()
        if self.username_check.get() == '' or self.password_check.get() == '':
            self.try_again()
        else:
            self.client.send_message(username1 + " " + password1)
            rcv_msg = self.client.rcv_message()
            print(rcv_msg)
            self.username_login_text_box.delete(0, END)
            self.password_login_text_box.delete(0, END)
            if "wrong" in rcv_msg:
                self.try_again()
            else:
                self.ok = True
                self.account_screen.destroy()

    def try_again(self):
        """create try again screen if there is a problem in sign_up or login"""
        self.try_again_screen = Tk()  # make try_again_screen
        self.try_again_screen.title("TRY AGAIN")
        self.try_again_screen.geometry("150x100")
        Label(self.try_again_screen, text="try again").pack()
        Button(self.try_again_screen, text="OK", command=self.delete_try_again).pack()

    def delete_try_again(self):
        self.try_again_screen.destroy()

    def listbox_insert(self, name):
        """insert to the listbox"""
        self.list_connected.append(name)
        self.listbox.insert(END, name)

    def click_listbox(self, event):
        """handle if click on listbox"""
        widget = event.widget
        selection = widget.curselection()
        self.value = widget.get(selection[0])
        print(self.value)
        self.now_chat = self.value
        self.txt.configure(state='normal')  # delete the messages if click on name in list box
        self.txt.delete('1.0', END)
        self.txt.configure(state='disabled')
        self.handle_chat()

    def handle_chat(self):
        """insert the text of the name that clicked in the listbox"""
        for key in self.dict_name_messages:
            if key == self.now_chat:
                self.txt.configure(state='normal')
                self.txt.delete('1.0', END)
                for msg in self.dict_name_messages[key]:
                    self.txt.insert(END, msg + '\n')
                self.txt.configure(state='disabled')

    def chat(self):
        """create the chat screen"""
        rcv_thread = threading.Thread(target=self.rcv_message)
        rcv_thread.start()
        self.chat_screen = Tk()
        self.chat_screen.geometry("500x400")
        self.chat_screen.title("chat")
        self.client_name_label = Label(text=self.my_name, bg="navy", width="400", height="1", font=("Ariel", 20),
                                       fg="white")
        self.client_name_label.pack()
        Label(text="Chat", bg="navy", width="400", height="1", font=("Calibri", 13)).pack()
        self.listbox = Listbox(self.chat_screen)
        self.listbox.insert(END, "broadcast")
        self.listbox.pack(side=RIGHT, fill=Y)
        self.listbox.bind("<Double-Button-1>", self.click_listbox)
        self.chat_entry = Entry(self.chat_screen, bd=6, bg="navy", fg="white")
        self.chat_entry.pack(side=BOTTOM)
        self.chat_entry.bind("<Return>", self.send_message)
        text_frm = Frame(self.chat_screen, width=450, height=300)
        text_frm.pack(fill="both", expand=False)
        text_frm.grid_propagate(False)
        text_frm.grid_rowconfigure(0, weight=1)
        text_frm.grid_columnconfigure(0, weight=1)
        self.txt = Text(text_frm, borderwidth=3, relief="sunken", bg='dark slate gray')
        self.txt.config(font=("Calibri", 13), undo=True, wrap='word', state='disabled')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scroll_bar = Scrollbar(text_frm, command=self.txt.yview)
        scroll_bar.grid(row=0, column=1, sticky='nsew')
        self.txt['y' + 'scroll' + 'command'] = scroll_bar.set
        self.build = True
        self.chat_screen.mainloop()

    def send_message(self, event):
        """send message with protocol to the server"""
        if self.now_chat == "broadcast":
            self.client.send_message(self.chat_entry.get())
        else:  # the protocol of private messages
            self.client.send_message(self.now_chat + "&" + self.my_name + "&:" + self.chat_entry.get())
        self.chat_entry.delete(0, END)

    def main_account_screen(self):
        """create the account screen"""
        self.account_screen.geometry("500x400")
        self.account_screen.title("sign_up/Login")
        Label(text="Welcome to my chat", bg="navy", width="400", height="2", fg="white", font=("Calibri", 13)).pack()
        Label(text="", width="400", height="2").pack()
        Button(text="Login", height="3", width="35", command=self.login).pack()
        Label(text="", width="400", height="2").pack()
        Button(text="sign_up", height="3", width="35", command=self.sign_up).pack()
        self.account_screen.mainloop()
        if self.ok is False:
            quit()


if __name__ == "__main__":
    g1 = Gui()
    g1.chat()
