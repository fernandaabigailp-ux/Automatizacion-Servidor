import time
import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime

JIRA_URL = os.environ.get("JIRA_URL", "https://tu-dominio.atlassian.net")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "tu-correo@gmail.com")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN", "TU_TOKEN")
PROJECT_KEY = "SCRUM"

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
        print(f"❌ ERROR DE JIRA [{response.status_code}]: No se pudo crear el ticket. ⚠️")
        print(response.text)

print("🚀 ========================================== 🚀")
print("🛡️      MONITOREO ITIL INICIADO V1.0        🛡️")
print("🚀 ========================================== 🚀")
print("👀 Vigilando el servidor local cada 5 segundos... ⏱️\n")

while True:
    try:
        response = requests.get("http://localhost:8000", timeout=3)
        if response.status_code == 200:
            print(f"💚 [ESTADO OK] Servidor funcionando correctamente ✨ - ⏰ {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"⚠️ [ADVERTENCIA] Código de respuesta inusual: {response.status_code} 🔍")
            crear_incidente()
    except requests.exceptions.RequestException:
        print(f"🚨 [CRÍTICO] ¡SERVIDOR CAÍDO O SIN RESPUESTA! 💥 - ⏰ {datetime.now().strftime('%H:%M:%S')}")
        crear_incidente()

    time.sleep(5)
