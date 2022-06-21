from time import perf_counter

class Console:
    def __init__(self):
        self.tic = perf_counter()
        self.outputTypes = {
            'INFO': 0,
            'DEBUG': 1,
            'ERROR': 2
        }
        self.outputs = [False, False, False]
        self.infoMethod = None
        self.ping = perf_counter()
    # ----------------------------------------------------------------
        
    def toc(self):
        return round((perf_counter() - self.tic) * 60 * 1000)
    
    def pong(self):
        pong = round((perf_counter() - self.ping) * 60 * 1000)
        self.ping = perf_counter()
        return pong
    
    def colored(self, r, g, b, text):
        return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)
    
    def setOwner(self, owner):
        self.filename = owner.split('Window')[0].split('\\')[-1]
    # ----------------------------------------------------------------
    
    def debug(self, *messages, nl = ''):
        msg = f'[{self.toc()}] {", ".join(messages)}'
        self.send(f'[{self.colored(150,255,150, "DEBUG")}]: {msg}', nl)
        self.sendLink(self.outputs[self.outputTypes['DEBUG']], messages)

    def info(self, *messages, nl = ''):
        msg = f'[{self.toc()}] {", ".join(messages)}'
        self.send(f'[{self.colored(150,150,255, "INFO")}]: {msg}', nl)
        self.sendLink(self.outputs[self.outputTypes['INFO']], messages)

    def error(self, *messages, nl = ''):
        msg = f'[{self.toc()}] {", ".join(messages)}'
        self.send(f'[{self.colored(255,150,150, "ERROR")}]: {msg}', nl)
        self.sendLink(self.outputs[self.outputTypes['ERROR']], messages)

    # ----------------------------------------------------------------


    def link(self, outputTypes, method):
        self.outputs[self.outputTypes[outputTypes]] = method
        
    def sendLink(self, output, messages):
        if output:
            output.setText(", ".join(messages))

    def prefix(self):
        return f'[{self.filename}]' if (hasattr(self, 'filename')) else ''

    def send(self, message: str, nl = ''):
        if(nl == True):
            nl = '\n'
        print(f'{self.prefix()} {message}')
