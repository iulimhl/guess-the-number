import socket
from game_logic import GuessGameSession

def read_line(f):
    line=f.readline()
    if not line:
        return None
    return line.rstrip("\n")

def main():
    host="0.0.0.0"
    port=5000
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))
    s.listen(5)
    while True:
        conn,addr=s.accept()
        session=GuessGameSession()
        f_in=conn.makefile("r",encoding="utf-8",newline="\n")
        f_out=conn.makefile("w",encoding="utf-8",newline="\n")
        try:
            while True:
                line=read_line(f_in)
                if line is None:
                    break
                response=session.handle_command(line)
                if response is not None:
                    f_out.write(response+"\n")
                    f_out.flush()
        finally:
            try:
                f_in.close()
            except:
                pass
            try:
                f_out.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

if __name__=="__main__":
    main()
