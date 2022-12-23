import src.app as app
import src.handlers as handler
import installation.wizard as wizard
from src.config import config

def main():
    # Hold a reference to all the functions that can be executed within a dictionary.
    func_list = {
        "help":         handler.help_handler,
        "version":      handler.version_handler,
        "install":      wizard.install_wizzard,
        "uninstall":    wizard.uninstall_wizzard,
        "run":          app.execute
    }
    
    # Pull the execution module from the config file, this will be passed by the args when the program starts.
    # Depending on the args passed, the program will execute the corresponding function.
    executed_func = func_list[config.exec_mudule]
    executed_func()

if __name__ == "__main__":
    main()