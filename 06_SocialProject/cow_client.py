
import cmd
import threading
import time
import readline
import socket

class cow_client(cmd.Cmd):

    prompt = "mymy >> "

    def __init__(self):
        super().__init__()
        self.socket = socket.socket()
        self.socket.connect(("0.0.0.0", 1337))
        self.timer = threading.Thread(target=self.read_from_server, args=())
        self.timer.start()
        self.rn = 1
        self.cn = 2
        self.request = {}
        self.complition = {}

    def request_num(self):
        self.rn += 2
        return self.rn

    def complition_num(self):
        self.cn += 2
        return self.cn

    def do_who(self, arg):
        """List of users"""
        num = self.request_num()
        self.request[num] = None
        self.write_to_server("who\n", num)

        while self.request[num] == None:
            pass
        if self.request[num] != "":
            print(self.request[num])

    def do_cows(self, arg):
        """List of available names"""
        num = self.request_num()
        self.request[num] = None
        self.write_to_server("cows\n", num)

        while self.request[num] == None:
            pass
        if self.request[num]:
            print(self.request[num])

    def do_login(self, arg):
        """Log in"""
        num = self.request_num()
        self.request[num] = None
        self.write_to_server("login " + arg + "\n", num)

        while self.request[num] == None:
            pass
        if self.request[num]:
            print(self.request[num])


    def complete_login(self, text, line, begidx, endidx):
        num = self.complition_num()
        self.complition[num] = None
        self.write_to_server("cows\n", num)
        
        while self.complition[num] == None:
            pass

        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = self.complition[num].split()
        return [c for c in complition if c.startswith(text)]

    def do_say(self, arg):
        """Write to a specific user"""
        self.write_to_server("say " + arg + "\n", self.request_num())

    def complete_say(self, text, line, begidx, endidx):
        num = self.complition_num()
        self.complition[num] = None
        self.write_to_server("who\n", num)
        
        while self.complition[num] == None:
            pass

        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = self.complition[num].split()
        return [c for c in complition if c.startswith(text)]

    def do_yield(self, arg):
        """Write to all users"""
        self.write_to_server("yield " + arg + "\n", self.request_num())

    def do_quit(self, arg):
        """Log out"""
        num = self.request_num()
        self.request[num] = None
        self.write_to_server("quit\n", num)

        while self.request[num] == None:
            pass
        if self.request[num] != "":
            print(self.request[num])


    def do_exit(self, arg):
        """Exit program"""
        self.timer.do_run = False
        self.do_quit("")
        self.socket.close()
        print()
        return 1

    def do_EOF(self, arg):
        """Exit program"""
        print()
        self.timer.do_run = False
        self.do_quit("")
        self.socket.close()
        print()
        return 1


    def write_to_server(self, data, num):
        self.socket.send((str(num) + " " + data).encode())

    
    def read_from_server(self):
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            data = self.socket.recv(1024).decode()
            data_num = data.split()[0]
            data = data[len(data_num):].strip()
            data_num = int(data_num)
            if data_num in self.complition and self.complition[data_num] == None:
                self.complition[data_num] = data
            elif data_num in self.request and self.request[data_num] == None:
                self.request[data_num] = data
            else:
                print(f"\n{data}\n{self.prompt}{readline.get_line_buffer()}", end="", flush=True)


if __name__ == "__main__":
    cow_client().cmdloop()
