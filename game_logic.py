import random

class RoundState:
    def __init__(self,secret):
        self.secret=secret
        self.attempts=0

class GuessGameSession:
    def __init__(self):
        self.current_round=None
        self.best_attempts=None

    def start_round(self):
        secret=random.randint(0,500)
        self.current_round=RoundState(secret)

    def handle_command(self,line):
        line=line.strip()
        if not line:
            return "ERROR Invalid input"
        parts=line.split()
        cmd=parts[0].upper()
        if cmd=="START":
            self.start_round()
            return None
        if cmd=="GUESS":
            return self.handle_guess(parts)
        return "ERROR Invalid input"

    def handle_guess(self,parts):
        if self.current_round is None:
            return "ERROR Invalid input"
        if len(parts)!=2:
            return "ERROR Invalid input"
        try:
            value=int(parts[1])
        except:
            return "ERROR Invalid input"
        if value<0 or value>500:
            return "ERROR Invalid input"
        self.current_round.attempts+=1
        if value<self.current_round.secret:
            return "TOO_LOW"
        if value>self.current_round.secret:
            return "TOO_HIGH"
        attempts=self.current_round.attempts
        if self.best_attempts is None or attempts<self.best_attempts:
            self.best_attempts=attempts
        best=self.best_attempts
        self.current_round=None
        return f"CORRECT {attempts} {best}"

if __name__=="__main__":
    session=GuessGameSession()
    while True:
        try:
            line=input()
        except EOFError:
            break
        if line.upper()=="QUIT":
            break
        response=session.handle_command(line)
        if response is not None:
            print(response)
