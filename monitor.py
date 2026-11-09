import time
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURA TUS DATOS DIRECTAMENTE AQUÍ ⚙️
# ==========================================
JIRA_URL = "https://barbosarep25.atlassian.net"
JIRA_EMAIL = "barbosarep25@gmail.com"
JIRA_TOKEN = "TU_TOKEN_DE_JIRA"       # Coloca aquí tu token real de Jira
PROJECT_KEY = "KAN"                  # Clave correcta de tu proyecto

def crear_incidente():
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": "🚨 Servidor sin respuesta - Alerta ITIL ⚠️",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{
                        "type": "text", 
                        "text": f"🔥 Servidor sin respuesta. Fecha y hora: {fecha_actual}. Detectado automáticamente por Python. 🤖"
                    }]
                }]
            },
            "issuetype": {"name": "Tarea"}
        }
    }
    
    print("🔄 Conectando con Jira para reportar el incidente...")
    response = requests.post(url, json=payload, auth=auth, headers=headers)
    
    if response.status_code == 201:
        resultado = response.json()
        print(f"✅ ¡INCIDENTE CREADO EXITOSAMENTE EN JIRA! 🎫 Ticket: {resultado.get('key')} 🎉")
    else:
        print(f"❌ ERROR DE JIRA [{response.status_code}]: Revisa que tu URL y token sean correctos. ⚠️")
        print(response.text)

print("🚀 ========================================== 🚀")
print("🛡️      MONITOREO ITIL INICIADO V2.0        🛡️")
print("🚀 ========================================== 🚀")
print("👀 Vigilando el servidor local cada 5 segundos... ⏱️\n")

ticket_creado = False

while True:
    try:
        response = requests.get("http://localhost:8000", timeout=3)
        if response.status_code == 200:
            print(f"💚[ESTADO OK] Servidor funcionando correctamente ✨ - ⏰{datetime.now().strftime('%H:%M:%S')}")
            ticket_creado = False  # Reinicia el estado para cuando vuelva a fallar
    except requests.exceptions.RequestException:
        print(f"🚨 [CRÍTICO] ¡SERVIDOR CAÍDO O SIN RESPUESTA! 💥 - ⏰ {datetime.now().strftime('%H:%M:%S')}")
        if not ticket_creado:
            crear_incidente()
            ticket_creado = True  # Bloquea el envío de más tickets
            
    time.sleep(5)
