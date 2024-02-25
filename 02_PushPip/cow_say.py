
import argparse
import cowsay

def MyCowsay():
    parser = argparse.ArgumentParser(description=\
            "This program draws a cow speaking a given text")
    parser.add_argument("msg", nargs="?",\
            help="The text that the cow should say")
    parser.add_argument("-n", action="store_true",\
            help="The given message will not be word-wrapped")
    parser.add_argument("-W", type=int, default=40,\
            help="Option roughly where the message should be wrapped")
    parser.add_argument("-b", action="store_true",\
            help="Option initiates Borg mode")
    parser.add_argument("-d", action="store_true",\
            help="Option causes the cow to appear dead")
    parser.add_argument("-g", action="store_true",\
            help="Option invokes greedy mode")
    parser.add_argument("-p", action="store_true",\
            help="Option causes a state of paranoia to come over the cow")
    parser.add_argument("-s", action="store_true",\
            help="Option makes the cow appear thoroughly stoned")
    parser.add_argument("-t", action="store_true",\
            help="Option yields a tired cow")
    parser.add_argument("-w", action="store_true",\
            help="Option initiates wired mode")
    parser.add_argument("-y", action="store_true",\
            help="Option brings on the cow's youthful appearance")
    parser.add_argument("-e", default=cowsay.Option.eyes,
            help="Option the appearance of the cow's eyes")
    parser.add_argument("-T", default=cowsay.Option.tongue,\
            help="Option the appearance of the cow`s tongue")
    parser.add_argument("-f", default="default",\
            help="Option specifies a particular cow picture file to use")
    parser.add_argument("-l", action="store_true",\
            help="Print list all cow files on the current COWPATH")
    args = parser.parse_args()

    if args.l:
        print(cowsay.list_cows())
    elif args.msg == None:
        print("You didn't write the message!")
    else:
        preset = ""
        for i in "bdgpstwy":
            if getattr(args, i):
                preset += i

        print(cowsay.cowsay(
                message=args.msg,
                cow=args.f,
                preset=preset,
                eyes=args.e,
                tongue=args.T,
                width=args.W,
                wrap_text=args.n
                ))

if __name__ == "__main__":
    MyCowsay()

