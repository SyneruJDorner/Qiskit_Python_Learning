import sys, argparse

class Config():
    #Handle the parameters for the application
    def __determine_active_args():
        parser = argparse.ArgumentParser(prog = 'Quantum Computing', description = 'A quantum program using qiskit and python.', add_help=False)
        parser.add_argument('-help', '--help', action='store_true', default=False)
        parser.add_argument('-install', '--install', action='store_true', default=False)
        parser.add_argument('-uninstall', '--uninstall', action='store_true', default=False)
        parser.add_argument('-version', '--version', action='store_true', default=False)
        parser.add_argument('-run', '--run', action='store_true', default=False)
        listed_arguments = parser.parse_args()

        args = []
        for argument in vars(listed_arguments):
            if getattr(listed_arguments, argument):
                args.append(argument)

        if (len(args) >= 2):
            print("Too many arguments, please use only one argument at a time")
            sys.exit(0)
        
        if (len(args) == 0):
            print("No argument provided, please use -help to see the list of available arguments")
            sys.exit(0)
        return str(args[0]).lower()

    exec_mudule = __determine_active_args()

config = Config()