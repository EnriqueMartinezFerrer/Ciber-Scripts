import subprocess
import requests
import time

# URL objetivo para comprobar si estás bloqueado
TARGET_URL = "https://tssciberseguridad.com"

# Tiempo entre comprobaciones (en segundos)
CHECK_INTERVAL = 60

def get_ip():
    try:
        ip = requests.get("https://ifconfig.me", timeout=5).text.strip()
        print(f"[+] IP actual: {ip}")
        return ip
    except:
        print("[!] Error al obtener IP.")
        return "Desconocida"

def check_block():
    try:
        response = requests.get(TARGET_URL, timeout=10)
        print(f"[+] Estado HTTP: {response.status_code}")

        # Bloqueos por código HTTP comunes
        if response.status_code in [403, 404, 429, 503]:
            return True

        # Detección de CAPTCHA en contenido HTML
        contenido = response.text.lower()
        palabras_clave = ["recaptcha", "captcha", "verifica que no eres un robot", "cloudflare", "challenge"]
        if any(palabra in contenido for palabra in palabras_clave):
            print("[!] CAPTCHA detectado en el contenido HTML.")
            return True

        return False  # No hay bloqueo
    except:
        print("[!] Posible bloqueo o error de conexión.")
        return True

def change_ip():
    print("[*] Cambiando IP...")
    subprocess.run(["nordvpn", "disconnect"])
    time.sleep(3)
    subprocess.run(["nordvpn", "connect"])
    time.sleep(5)
    get_ip()

# Bucle de vigilancia continua
print("[*] Script iniciado. Vigilando bloqueos...")
get_ip()

while True:
    if check_block():
        print("[!] Bloqueo detectado. Cambiando IP...")
        change_ip()
    else:
        print("[+] Sin bloqueo detectado.")
    time.sleep(CHECK_INTERVAL)
