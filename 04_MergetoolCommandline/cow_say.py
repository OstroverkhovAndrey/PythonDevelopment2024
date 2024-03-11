
import cowsay
import cmd
import shlex

class cmd_cowsay(cmd.Cmd):
    """
    Cmd for use cowsay modul
    """

    prompt = "mymy >> "

    def print_error_message(self, error=""):
        print("Error!", error)

    def do_list_cows(self, arg):
        """
        Print list cowfile.

        Usage: list_cows [path]

        Parameters:
            path    : Optional, default - cowpath in python-cowsay.
                      Path to cowfiles.
        """
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) == 1:
            arg = type(cowsay.COW_PEN)(arg[0])
            print(cowsay.list_cows(arg))
        else:
            print(cowsay.list_cows())
    
    def make_cow_arguments_dict(self, arg):
        arg = shlex.split(arg)
        arg_dict = {"-f" : 'default',
                    "-e" : cowsay.Option.eyes,
                    "-T" : cowsay.Option.tongue}
        i = 0
        while i < len(arg)-1:
            if arg[i] in arg_dict.keys():
                arg_dict[arg[i]] = arg[i+1]
                arg.pop(i)
                arg.pop(i)
                i -= 1
            i += 1
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) == 0:
            self.print_error_message("Not specified message!")
        elif arg[0] in arg_dict.keys():
            self.print_error_message("Not specified message! "+\
                    "Not specified {} argument!".format(arg[0]))
        elif arg_dict["-f"] not in cowsay.list_cows():
            self.print_error_message("Argument -f error!")
        elif len(arg_dict["-e"]) != 2:
            self.print_error_message("Argument -e error!")
        elif len(arg_dict["-T"]) != 2:
            self.print_error_message("Argument -T error!")
        else:
            arg_dict["msg"] = arg[0]
            return arg_dict
        return None

    def do_cowsay(self, arg):
        """
        Print cowsay with message.

        Usage: cowsay [msg] [-f cowfile] [-e eyes] [-T tongue]

        Parameters:
            msg    : Required. Message that cow say.
            -f     : Optional, default - "default". Cowfile that use to print cow.
            -e     : Oprional, default - "oo". Type cow eyes. Two english laters.
            -T     : Optional, default - "  ".Type cow tongue. Two english laters.
        """
        arg_dict = self.make_cow_arguments_dict(arg)
        if arg_dict:
            print(cowsay.cowsay(message=arg_dict["msg"],
                            cow=arg_dict["-f"],
                            eyes=arg_dict["-e"],
                            tongue=arg_dict["-T"]))

    def do_cowthink(self, arg):
        """
        Print cowthink with message.

        Usage: cowthink [msg] [-f cowfile] [-e eyes] [-T tongue]

        Parameters:
            msg    : Required. Message that cow think.
            -f     : Optional, default - "default". Cowfile that use to print cow.
            -e     : Oprional, default - "oo". Type cow eyes. Two english laters.
            -T     : Optional, default - "  ".Type cow tongue. Two english laters.
        """
        arg_dict = self.make_cow_arguments_dict(arg)
        if arg_dict:
            print(cowsay.cowthink(message=arg_dict["msg"],
                            cow=arg_dict["-f"],
                            eyes=arg_dict["-e"],
                            tongue=arg_dict["-T"]))

    def make_cow_complete_list(self, text, line, begidx, endidx):
        """"""
        arg_dict = {"-f" : cowsay.list_cows(),
                    "-e" : [cowsay.Option.eyes, "XX", "YY", "QQ"],
                    "-T" : ["PP", "UU"]}
        args = (line[:endidx] + ".").split()
        match args[-2]:
            case "-f":
                return [c for c in arg_dict["-f"] if c.startswith(text)]
            case "-e":
                return [c for c in arg_dict["-e"] if c.startswith(text)]
            case "-T":
                return [c for c in arg_dict["-T"] if c.startswith(text)]

    def complete_cowsay(self, text, line, begidx, endidx):
        return self.make_cow_complete_list(text, line, begidx, endidx)

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.make_cow_complete_list(text, line, begidx, endidx)

    def do_make_bubble(self, arg):
        """
        Print message in bubble.

        Usage: make_bubble [msg] [-b brackets] [-w width] [-wrap_text 0|1]

        Parameters:
            msg          : Required. Message.
            -b           : Optional, default - "cowsay".
                           Brackets for print bubble.
            -w           : Oprional, default - 40. Text width.
            -wrap_text   : Optional, default - True. Wrap text flag.
        """
        arg = shlex.split(arg)
        arg_dict = {"-b" : "cowsay",
                    "-w" : "40",
                    "-wrap_text" : "1"}
        i = 0
        while i < len(arg)-1:
            if arg[i] in arg_dict.keys():
                arg_dict[arg[i]] = arg[i+1]
                arg.pop(i)
                arg.pop(i)
                i -= 1
            i += 1
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) == 0:
            self.print_error_message("Not specified message!")
        elif arg[0] in arg_dict.keys():
            self.print_error_message("Not specified message! "+\
                    "Not specified {} argument!".format(arg[0]))
        elif arg_dict["-b"] not in ["cowsay", "cowthink"]:
            self.print_error_message("Argument -b error!")
        elif not arg_dict["-w"].isdigit():
            self.print_error_message("Argument -w error!")
        elif arg_dict["-wrap_text"] not in ["0", "1"]:
            self.print_error_message("Argument -wrap_text error!")
        else:
            arg_dict["text"] = arg[0]
            arg_dict["-wrap_text"] = int(arg_dict["-wrap_text"])
            arg_dict["-w"] = int(arg_dict["-w"])
            print(cowsay.make_bubble(text=arg_dict["text"],
                        brackets=cowsay.THOUGHT_OPTIONS[arg_dict["-b"]],
                        width=arg_dict["-w"],
                        wrap_text=arg_dict["-wrap_text"]))

    def complete_make_bubble(self, text, line, begidx, endidx):
        arg_dict = {"-b" : ["cowsay", "cowthink"],
                    "-w" : None,
                    "-wrap_text" : ["0", "1"]}
        args = (line[:endidx] + ".").split()
        match args[-2]:
            case "-b":
                return [c for c in arg_dict["-b"] if c.startswith(text)]
            case "-wrap_text":
                return [c for c in arg_dict["-wrap_text"] if c.startswith(text)]

    def do_exit(self, arg):
        """Exit program"""
        print()
        return 1

    def do_EOF(self, arg):
        """Exit program"""
        print()
        return 1


if __name__ == '__main__':
    cmd_cowsay().cmdloop()

