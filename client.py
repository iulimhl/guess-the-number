import socket
import sys

def read_line(f):
    line=f.readline()
    if not line:
        return None
    return line.rstrip("\n")

def main():
    host="127.0.0.1"
    port=5000
    if len(sys.argv)>=2:
        host=sys.argv[1]
    if len(sys.argv)>=3:
        port=int(sys.argv[2])

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    f_in=s.makefile("r",encoding="utf-8",newline="\n")
    f_out=s.makefile("w",encoding="utf-8",newline="\n")

    try:
        f_out.write("START\n")
        f_out.flush()

        while True:
            while True:
                guess=input("Your guess (0-500): ").strip()
                try:
                    n=int(guess)
                except:
                    print("Invalid input. Enter an integer between 0 and 500.")
                    continue
                if n<0 or n>500:
                    print("Invalid input. Enter an integer between 0 and 500.")
                    continue

                f_out.write(f"GUESS {n}\n")
                f_out.flush()

                resp=read_line(f_in)
                if resp is None:
                    print("Disconnected.")
                    return

                if resp=="TOO_LOW":
                    print("The number is higher.")
                    continue
                if resp=="TOO_HIGH":
                    print("The number is lower.")
                    continue

                if resp.startswith("CORRECT"):
                    parts=resp.split()
                    if len(parts)==3:
                        attempts=parts[1]
                        best=parts[2]
                        print(f"Correct! You found it in {attempts} attempts. Best: {best} attempts.")
                    else:
                        print("Correct!")
                    break

                if resp.startswith("ERROR"):
                    print("Server error:",resp)
                    continue

                print("Server:",resp)

            while True:
                again=input("Play again? (y/n): ").strip().lower()
                if again=="y":
                    f_out.write("START\n")
                    f_out.flush()
                    break
                if again=="n":
                    try:
                        s.shutdown(socket.SHUT_WR)
                    except:
                        pass
                    final_msg=read_line(f_in)
                    if final_msg is not None:
                        print(final_msg)
                    return
                print("Please type y or n.")
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
            s.close()
        except:
            pass

if __name__=="__main__":
    main()
