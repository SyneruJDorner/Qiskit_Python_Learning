def help_handler():
    help_contents = "Usage(s):\n"
    help_contents += "===================================================================================\n"
    help_contents += "'python .\main.py --run'\n"
    help_contents += "This will allow you to execute the program.\n"
    help_contents += "\n"
    help_contents += "'python .\main.py --version'\n"
    help_contents += "This will print out the versions of karas, cuda, cuDNN and other important versions.\n"
    help_contents += "===================================================================================\n"
    print(help_contents)
    return
