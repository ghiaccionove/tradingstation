from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


session = PromptSession()
mode_completer = WordCompleter(['spotter','manual','auto','shut'])
input_mode = session.prompt('Trading Station - Seleziona modalità: >', completer=mode_completer)
print(input_mode)