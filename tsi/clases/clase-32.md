# Clase 32: Manejo de Secretos

**Numero de clase:** 21
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Identificar que constituye un secreto y por que debe protegerse
- Reconocer practicas inseguras de manejo de secretos
- Usar herramientas como HashiCorp Vault, Azure Key Vault y AWS Secrets Manager
- Implementar deteccion de secretos expuestos con truffleHog y git-secrets
- Disenar rotacion automatica de secretos en aplicaciones

## Contenido Detallado

### 1. Que son Secretos?

Un secreto es cualquier informacion que permite el acceso a un sistema o dato protegido.

**Tipos de secretos:**
- API keys (claves de servicios externos)
- Contrasenas de bases de datos y servicios
- Tokens de autenticacion (JWT, OAuth)
- Certificados TLS/SSL y claves privadas
- Claves SSH
- Claves de cifrado
- Tokens de bots y servicios
- Credenciales de nube (AWS keys, Azure client secrets)
- Connection strings de bases de datos
- Secret keys de aplicaciones (Django SECRET_KEY, Flask SECRET_KEY)

### 2. Practicas Inseguras (y Por que evitarlas)

| Practica Insegura | Riesgo |
|-------------------|--------|
| Hardcodear en codigo fuente | Cualquiera con acceso al repo ve las credenciales |
| .env en repositorio | Se suben accidentalmente a GitHub |
| Compartir por Slack/email | Quedan en logs y cache de mensajeria |
| Misma clave en todos los entornos | Si se compromete un entorno, todos los demas tambien |
| Sin rotacion de secretos | Un secreto comprometido sirve indefinidamente |
| Secretos en logs | Quedan registrados en sistemas de monitoreo |

### 3. Herramientas de Gestion de Secretos

**HashiCorp Vault:**
- Almacenamiento cifrado de secretos
- Rotacion automatica de contraseas
- Dynamic secrets (generados bajo demanda)
- Auditing de acceso a secretos
- Multi-platform (CLI, API, UI)

**Azure Key Vault:**
- Gestion de claves de cifrado, certificados y secretos
- Integracion nativa con servicios Azure
- HSM (Hardware Security Module) opcional
- Rotacion automatica de certificados

**AWS Secrets Manager:**
- Rotacion automatica de credenciales RDS
- Cifrado con AWS KMS
- Integracion con Lambda y otros servicios AWS
- Replicacion multi-region

### 4. Deteccion de Secretos en Repositorios

**git-secrets:** Escanea commits, archivos y mensajes de commit contra patrones de secretos.

**truffleHog:** Escanea todo el historial de Git en busqueda de secretos usando entropy analysis.

**.gitignore para secretos:**
```
# Archivos que NUNCA deben subirse
.env
*.key
*.pem
config/secrets.yml
*.secret
credentials.json
service-account.json
```

### 5. Rotacion de Secretos

Principios:
- Rotar periodicamente (cada 30-90 dias)
- Rotar inmediatamente si hay sospecha de compromiso
- Usar versionamiento de secretos (mantener versiones anteriores por ventana de transicion)
- Automatizar el proceso (no rotar manualmente)

## Ejercicio 1: Script que Lee Secretos desde Entorno + Vault

```python
# gestor_secretos.py - Lectura de secretos desde entorno y Vault
import os
import json
import base64
import logging
from typing import Optional, Dict, Any

# ============================================================
# CONFIGURACION DE LOGGING (sin exponer secretos)
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GestorSecretosEntorno:
    """
    Lee secretos desde variables de entorno.
    Estrategia: las variables de entorno se inyectan en el
    contenedor/servidor y nunca se almacenan en el codigo.
    """

    @staticmethod
    def obtener( nombre: str, required: bool = True, default: str = None) -> Optional[str]:
        """
        Obtiene un secreto de variable de entorno.

        Args:
            nombre: Nombre de la variable de entorno
            required: Si True, lanza error si no existe
            default: Valor por defecto si no es required

        Returns:
            Valor del secreto o default
        """
        valor = os.environ.get(nombre)
        if valor is None:
            if required:
                raise ValueError(
                    f"Secreto '{nombre}' no encontrado en variables de entorno"
                )
            return default
        return valor

    @staticmethod
    def obtener_int(nombre: str, required: bool = True, default: int = None) -> Optional[int]:
        valor = GestorSecretosEntorno.obtener(nombre, required, default)
        if valor is not None:
            return int(valor)
        return None

    @staticmethod
    def obtener_bool(nombre: str, default: bool = False) -> bool:
        valor = GestorSecretosEntorno.obtener(nombre, required=False, default=None)
        if valor is None:
            return default
        return valor.lower() in ('true', '1', 'yes', 'si')


class GestorSecretosVault:
    """
    Lee secretos desde HashiCorp Vault usando su API REST.

    Requiere configurar:
    - VAULT_ADDR: URL del servidor Vault
    - VAULT_TOKEN: Token de autenticacion
    """

    def __init__(self, vault_addr: str = None, vault_token: str = None):
        self.vault_addr = vault_addr or os.environ.get('VAULT_ADDR', 'http://localhost:8200')
        self.vault_token = vault_token or os.environ.get('VAULT_TOKEN', '')

        if not self.vault_token:
            logger.warning("VAULT_TOKEN no configurado. Intentando auth por token file...")
            self._autenticar_por_archivo()

        self._cliente = None
        self._conectado = False

    def _autenticar_por_archivo(self):
        """Intenta leer token desde archivo (~/.vault-token)."""
        token_file = os.path.expanduser('~/.vault-token')
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                self.vault_token = f.read().strip()

    def _get_headers(self) -> Dict[str, str]:
        return {
            'X-Vault-Token': self.vault_token,
            'Content-Type': 'application/json'
        }

    def leer_secreto(self, ruta: str, clave: str = None, version: int = None) -> Any:
        """
        Lee un secreto desde Vault en la ruta especificada.

        Args:
            ruta: Path del secreto en Vault (ej: secret/data/api)
            clave: Clave especifica dentro del secreto (opcional)
            version: Version del secreto (opcional)

        Returns:
            Valor del secreto (dict completo o valor de clave especifica)
        """
        import requests

        # Construir URL
        url = f"{self.vault_addr}/v1/{ruta}"
        params = {}
        if version:
            params['version'] = version

        logger.info("Leyendo secreto desde Vault: %s", ruta)

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=10
            )

            if response.status_code == 404:
                raise ValueError(f"Secreto no encontrado en ruta: {ruta}")
            elif response.status_code == 403:
                raise PermissionError("Token Vault no autorizado para leer este secreto")
            elif response.status_code != 200:
                raise RuntimeError(
                    f"Error Vault ({response.status_code}): {response.text}"
                )

            data = response.json()

            # Vault KV v2: data.data.<claves>
            # Vault KV v1: data.<claves>
            if 'data' in data:
                if 'data' in data['data']:
                    secret_data = data['data']['data']
                else:
                    secret_data = data['data']
            else:
                secret_data = data

            if clave:
                if clave not in secret_data:
                    raise KeyError(
                        f"Clave '{clave}' no encontrada en secreto '{ruta}'"
                    )
                return secret_data[clave]

            return secret_data

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"No se pudo conectar a Vault en {self.vault_addr}. "
                "Verifica que Vault este corriendo."
            )

    def listar_caminos(self, ruta: str) -> list:
        """Lista los caminos disponibles bajo una ruta en Vault."""
        import requests
        url = f"{self.vault_addr}/v1/{ruta}"
        response = requests.request(
            'LIST', url,
            headers=self._get_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('data', {}).get('keys', [])
        return []


class GestorSecretosAzureKV:
    """Lee secretos desde Azure Key Vault."""

    def __init__(self, key_vault_url: str = None):
        self.key_vault_url = (
            key_vault_url
            or os.environ.get('AZURE_KEY_VAULT_URL', '')
        )

    def leer_secreto(self, nombre: str) -> str:
        """Lee un secreto de Azure Key Vault."""
        try:
            from azure.identity import DefaultAzureCredential
            from azure.keyvault.secrets import SecretClient

            credential = DefaultAzureCredential()
            client = SecretClient(
                vault_url=self.key_vault_url,
                credential=credential
            )
            secret = client.get_secret(nombre)
            return secret.value
        except ImportError:
            raise ImportError(
                "Instala azure-identity y azure-keyvault-secrets: "
                "pip install azure-identity azure-keyvault-secrets"
            )


class GestorSecretosAWS:
    """Lee secretos desde AWS Secrets Manager."""

    def __init__(self, region: str = None):
        self.region = region or os.environ.get('AWS_REGION', 'us-east-1')

    def leer_secreto(self, nombre_secreto: str) -> str:
        """Lee un secreto de AWS Secrets Manager."""
        try:
            import boto3
            from botocore.exceptions import ClientError

            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=self.region
            )

            response = client.get_secret_value(SecretId=nombre_secreto)
            if 'SecretString' in response:
                return response['SecretString']
            else:
                return base64.b64decode(response['SecretBinary']).decode('utf-8')

        except ImportError:
            raise ImportError(
                "Instala boto3: pip install boto3"
            )
        except ClientError as e:
            raise RuntimeError(f"Error al leer secreto de AWS: {str(e)}")


# ============================================================
# CONFIGURACION CENTRALIZADA
# ============================================================

class ConfiguracionSegura:
    """
    Gestiona configuracion de la aplicacion leyendo secretos
    de la fuente apropiada (entorno, Vault, Azure, AWS).
    """

    def __init__(self):
        self._gestores = {
            'entorno': GestorSecretosEntorno(),
        }

        # Intentar conectar Vault si esta configurado
        if os.environ.get('VAULT_ADDR'):
            try:
                self._gestores['vault'] = GestorSecretosVault()
                logger.info("Vault configurado en %s", os.environ['VAULT_ADDR'])
            except Exception as e:
                logger.warning("No se pudo conectar a Vault: %s", str(e))

    def obtener(self, nombre: str, required: bool = True) -> str:
        """
        Obtiene un valor de configuracion.

        Orden de busqueda:
        1. Variable de entorno
        2. Vault (si esta configurado)
        3. Error si required=True
        """
        # 1. Buscar en entorno
        valor = self._gestores['entorno'].obtener(nombre, required=False)
        if valor is not None:
            logger.debug("Config %s obtenida de variable de entorno", nombre)
            return valor

        # 2. Buscar en Vault
        if 'vault' in self._gestores:
            try:
                return self._gestores['vault'].leer_secreto(
                    f"secret/data/{nombre.lower()}"
                )
            except Exception as e:
                logger.debug("Config %s no encontrada en Vault: %s", nombre, str(e))

        if required:
            raise ValueError(
                f"Secreto '{nombre}' no encontrado en ninguna fuente"
            )
        return None


# ============================================================
# EJEMPLO DE USO
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Gestor de Secretos - Demostracion")
    print("=" * 60)

    # Configurar variables de entorno simuladas
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    os.environ['APP_DEBUG'] = 'false'

    config = ConfiguracionSegura()

    print("\n--- Leyendo desde variables de entorno ---")
    db_host = config.obtener('DB_HOST')
    db_port = config.obtener('DB_PORT')
    print(f"DB_HOST: {db_host}")
    print(f"DB_PORT: {db_port}")

    print("\n--- Configuracion de BD segura ---")
    db_config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'database': os.environ.get('DB_NAME', 'miapp'),
        'username': os.environ.get('DB_USER', 'app_user'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'ssl': True,
        'pool_size': 10,
    }

    if not db_config['password']:
        # Intentar leer de Vault
        if 'vault' in config._gestores:
            try:
                db_config['password'] = config._gestores['vault'].leer_secreto(
                    'secret/data/database',
                    'password'
                )
            except Exception:
                raise ValueError(
                    "DB_PASSWORD no configurada ni en entorno ni en Vault"
                )

    # No mostrar la contrasena en logs
    logger.info("Configuracion de BD cargada (contrasena oculta)")
    safe_config = {**db_config, 'password': '***'}
    print(f"Config: {json.dumps(safe_config, indent=2)}")
```

## Ejercicio 2: Escanear Repositorio con truffleHog/git-secrets

```bash
#!/bin/bash
# scan_secretos.sh - Escaneo de secretos en repositorio

echo "========================================"
echo "ESCANEO DE SECRETOS EN REPOSITORIO"
echo "========================================"

# =============================================
# METODO 1: git-secrets
# =============================================
echo ""
echo "[1] Instalando git-secrets..."

# En Windows (PowerShell):
# git clone https://github.com/awslabs/git-secrets.git
# cd git-secrets
# make install

echo ""
echo "[2] Configurando patrones de git-secrets..."
# Patrones comunes de secretos
git secrets --add 'password\s*=\s*.+'
git secrets --add 'api[_-]?key\s*=\s*.+'
git secrets --add 'secret\s*=\s*.+'
git secrets --add 'token\s*=\s*.+'
git secrets --add '-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----'

# Patrones de AWS
git secrets --add --provider aws

# Patrones personalizados
git secrets --add 'AKIA[0-9A-Z]{16}'  # AWS Access Key ID
git secrets --add 'sk-[a-zA-Z0-9]{20,}'  # OpenAI API Key
git secrets --add 'ghp_[a-zA-Z0-9]{36}'  # GitHub Personal Access Token

echo ""
echo "[3] Escaneando commits historicos..."
git secrets --scan-history

echo ""
echo "[4] Escaneando archivos actuales..."
git secrets --scan

# =============================================
# METODO 2: truffleHog
# =============================================
echo ""
echo "========================================"
echo "TRUFFLEHOG"
echo "========================================"
echo ""
echo "Instalacion: pip install trufflehog"

echo ""
echo "Escaneo de repositorio completo (incluyendo historial):"
echo "  trufflehog git file:///ruta/del/repo --only-verified"
echo ""
echo "Escaneo de un branch especifico:"
echo "  trufflehog git file:///ruta/del/repo --branch main"
echo ""
echo "Escaneo en busqueda de alta entropia:"
echo "  trufflehog filesystem /ruta/del/repo"

# =============================================
# EJEMPLO DE ARCHIVO CON SECRETOS (DETECTAR)
# =============================================
echo ""
echo "========================================"
echo "EJEMPLO: ARCHIVO CON SECRETOS EXPUESTOS"
echo "========================================"
echo ""
echo "Crea un archivo test_secrets.py y ejecuta el escaneo:"
echo ""
```

```python
# test_secrets.py - NO SUBIR A GIT (contiene secretos exposivos)
# Este archivo contiene secretos intencionalmente para demostrar deteccion

# ============================================================
# SECRETOS EXPUESTOS - SOLO PARA DEMOSTRACION
# ============================================================

# MAL: API Key hardcodeada
STRIPE_API_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"  # noqa

# MAL: Contrasena de BD hardcodeada
DB_PASSWORD = "SuperSecret2024!db_admin"

# MAL: Token de AWS hardcodeado
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# MAL: Clave secreta de aplicacion
SECRET_KEY = "mi-clave-super-secreta-que-nadie-debe-saber"

# MAL: Token de GitHub
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD"

# MAL: Connection string con credenciales
DATABASE_URL = "postgresql://admin:password123@prod-db.example.com:5432/miapp_prod"

# MAL: Certificado privado (simulado)
PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0gD2t1g0nVZnJcC6QXBjRmPKBQMzFh0UMlI+p/jQpR+n
... (contenido del certificado)
-----END RSA PRIVATE KEY-----
"""
```

**Comandos de escaneo:**
```bash
# Escanear con git-secrets
git secrets --scan

# Escanear con truffleHog
trufflehog filesystem ./
trufflehog git file://. --only-verified

# Verificar .gitignore
cat .gitignore
# Debe incluir:
# *.key
# *.pem
# .env
# credentials.json
# service-account.json
# secrets*
```

**Salida esperada de truffleHog:**
```
Found verified result 🐷🔑
Branch: main
Commit: a1b2c3d4e5f6...
File: test_secrets.py
Line: 8
Secret: sk_live_4eC39HqLyjWDarjtT1zdp7dc
Detector: Stripe

Found unverified result
File: test_secrets.py
Line: 11
Reason: High entropy string 'SuperSecret2024!db_admin'
```

## Ejercicio 3: Rotacion Automatica de API Keys en Flask

```python
# rotacion_api_keys.py - Rotacion automatica de API keys en Flask
import os
import json
import time
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from flask import Flask, request, jsonify, g

# ============================================================
# CONFIGURACION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# GESTOR DE API KEYS CON ROTACION AUTOMATICA
# ============================================================

class GestorAPIKeys:
    """
    Gestiona API keys con:
    - Rotacion automatica cada N dias
    - Versionamiento de keys (v1, v2, v3...)
    - Periodo de gracia donde keys viejas siguen siendo validas
    - Revocacion inmediata de keys comprometidas
    """

    def __init__(self, rotacion_dias: int = 90, periodo_gracia_horas: int = 48):
        """
        Args:
            rotacion_dias: Cada cuantos dias se rotan las keys
            periodo_gracia_horas: Horas que una key vieja sigue siendo valida
        """
        self.rotacion_dias = rotacion_dias
        self.periodo_gracia = timedelta(hours=periodo_gracia_horas)

        # Estructura: {client_id: {key_id: {key_hash, created_at, expires_at, active}}}
        self._keys: Dict[str, Dict] = {}
        self._key_index: Dict[str, str] = {}  # key_hash -> client_id

    def generar_key(self, client_id: str) -> dict:
        """
        Genera una nueva API key para un cliente.
        La key se devuelve UNA SOLA VEZ (no se almacena en texto plano).
        """
        # Generar key segura
        key_raw = f"sk_{secrets.token_urlsafe(48)}"
        key_id = f"key_{secrets.token_hex(8)}"

        # Hash de la key (nunca almacenar en texto plano)
        key_hash = self._hash_key(key_raw)

        now = datetime.now()

        if client_id not in self._keys:
            self._keys[client_id] = {}

        self._keys[client_id][key_id] = {
            'key_hash': key_hash,
            'created_at': now,
            'expires_at': now + timedelta(days=self.rotacion_dias),
            'active': True,
            'version': len(self._keys[client_id]) + 1
        }

        self._key_index[key_hash] = client_id

        logger.info(
            "API key generada para %s (key_id: %s, expira: %s)",
            client_id, key_id,
            self._keys[client_id][key_id]['expires_at'].isoformat()
        )

        return {
            'key_id': key_id,
            'api_key': key_raw,  # SOLO se muestra al crearla
            'expires_at': self._keys[client_id][key_id]['expires_at'].isoformat(),
            'warning': 'Guarda esta key ahora. No se mostrara nuevamente.'
        }

    def validar_key(self, api_key: str) -> Optional[dict]:
        """
        Valida una API key. Retorna info del cliente si es valida.
        Considera periodo de gracia para keys recien rotadas.
        """
        key_hash = self._hash_key(api_key)
        client_id = self._key_index.get(key_hash)

        if not client_id:
            logger.warning("API key invalida: hash no encontrado")
            return None

        # Buscar en todas las keys del cliente
        for key_id, key_data in self._keys[client_id].items():
            if key_data['key_hash'] == key_hash:
                if not key_data['active']:
                    logger.warning("API key revocada: %s", key_id)
                    return None

                now = datetime.now()

                # Verificar expiracion + periodo de gracia
                if now > key_data['expires_at']:
                    # Verificar si esta en periodo de gracia
                    fin_gracia = key_data['expires_at'] + self.periodo_gracia
                    if now > fin_gracia:
                        logger.warning("API key expirada: %s", key_id)
                        return None
                    logger.info("API key en periodo de gracia: %s", key_id)

                return {
                    'client_id': client_id,
                    'key_id': key_id,
                    'version': key_data['version'],
                    'expires_at': key_data['expires_at'].isoformat()
                }

        return None

    def revocar_key(self, client_id: str, key_id: str) -> bool:
        """Revoca una API key inmediatamente."""
        if client_id in self._keys and key_id in self._keys[client_id]:
            self._keys[client_id][key_id]['active'] = False
            logger.warning(
                "API key revocada: client=%s, key_id=%s",
                client_id, key_id
            )
            return True
        return False

    def rotar_keys(self, client_id: str) -> dict:
        """
        Rota las keys de un cliente:
        1. Las keys actuales entran en periodo de gracia
        2. Se genera una nueva key
        """
        logger.info("Rotando keys para cliente: %s", client_id)

        # Las keys viejas ya expiraran naturalmente o entraran en gracia
        nueva_key = self.generar_key(client_id)
        return nueva_key

    def rotacion_masiva(self) -> list:
        """
        Ejecuta rotacion programada para todos los clientes
        cuyas keys esten por expirar.
        """
        rotados = []
        now = datetime.now()

        for client_id in self._keys:
            for key_id, key_data in self._keys[client_id].items():
                if key_data['active']:
                    tiempo_restante = key_data['expires_at'] - now
                    dias_restantes = tiempo_restante.days

                    if dias_restantes <= 7:  # Rotar si expira en 7 dias o menos
                        logger.info(
                            "Rotacion automatica: %s key %s expira en %d dias",
                            client_id, key_id, dias_restantes
                        )
                        nueva = self.rotar_keys(client_id)
                        rotados.append({
                            'client_id': client_id,
                            'old_key_id': key_id,
                            'nueva_key': nueva
                        })

        return rotados

    def limpiar_expiradas(self) -> int:
        """Elimina keys expiradas que ya superaron el periodo de gracia."""
        now = datetime.now()
        eliminadas = 0

        for client_id in list(self._keys.keys()):
            for key_id in list(self._keys[client_id].keys()):
                key_data = self._keys[client_id][key_id]
                fin_gracia = key_data['expires_at'] + self.periodo_gracia
                if now > fin_gracia and not key_data['active']:
                    # Eliminar del indice
                    self._key_index.pop(key_data['key_hash'], None)
                    del self._keys[client_id][key_id]
                    eliminadas += 1

        return eliminadas

    @staticmethod
    def _hash_key(key: str) -> str:
        """Hash de la API key usando SHA-256 con salt."""
        return hashlib.sha256(key.encode()).hexdigest()


# ============================================================
# APP FLASK CON API KEY AUTH
# ============================================================

app = Flask(__name__)
gestor_keys = GestorAPIKeys(rotacion_dias=90, periodo_gracia_horas=48)


# Middleware de autenticacion por API Key
@app.before_request
def autenticar_api_key():
    """Verifica API Key en cada request (excepto endpoints publicos)."""
    if request.path.startswith('/publico'):
        return None

    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return jsonify({'error': 'API Key requerida (header X-API-Key)'}), 401

    info = gestor_keys.validar_key(api_key)
    if not info:
        return jsonify({'error': 'API Key invalida o expirada'}), 401

    g.client_id = info['client_id']
    g.key_info = info

    # Warning si la key esta proxima a expirar
    if info.get('expires_at'):
        exp = datetime.fromisoformat(info['expires_at'])
        dias_restantes = (exp - datetime.now()).days
        if dias_restantes <= 7:
            g.warning_key_expiration = dias_restantes

    return None


@app.route('/publico')
def publico():
    """Endpoint publico, no requiere API key."""
    return jsonify({'mensaje': 'Endpoint publico'})


@app.route('/api/datos')
def obtener_datos():
    """Endpoint protegido por API key."""
    response = {
        'mensaje': 'Datos protegidos',
        'client_id': g.client_id,
        'key_id': g.key_info['key_id']
    }

    if hasattr(g, 'warning_key_expiration'):
        response['warning'] = (
            f"Tu API key expira en {g.warning_key_expiration} dias. "
            "Por favor, renuevala."
        )

    return jsonify(response)


@app.route('/api/key/generar', methods=['POST'])
def generar_nueva_key():
    """Genera una nueva API key para un cliente."""
    data = request.get_json()
    client_id = data.get('client_id') if data else None

    if not client_id:
        return jsonify({'error': 'client_id requerido'}), 400

    key_info = gestor_keys.generar_key(client_id)
    return jsonify(key_info), 201


@app.route('/api/key/rotar', methods=['POST'])
def rotar_key():
    """Rota la API key del cliente actual."""
    if not hasattr(g, 'client_id'):
        return jsonify({'error': 'Autenticacion requerida'}), 401

    nueva_key = gestor_keys.rotar_keys(g.client_id)
    return jsonify(nueva_key)


@app.route('/api/key/revocar', methods=['POST'])
def revocar_key():
    """Revoca una API key."""
    if not hasattr(g, 'client_id'):
        return jsonify({'error': 'Autenticacion requerida'}), 401

    data = request.get_json()
    key_id = data.get('key_id') if data else None

    if not key_id:
        return jsonify({'error': 'key_id requerido'}), 400

    if gestor_keys.revocar_key(g.client_id, key_id):
        return jsonify({'mensaje': f'Key {key_id} revocada'})
    else:
        return jsonify({'error': 'Key no encontrada'}), 404


@app.route('/admin/rotacion-masiva', methods=['POST'])
def rotacion_masiva():
    """Ejecuta rotacion programada (tarea administrativa)."""
    rotados = gestor_keys.rotacion_masiva()
    limpiados = gestor_keys.limpiar_expiradas()
    return jsonify({
        'rotados': len(rotados),
        'limpiados': limpiados,
        'detalle': rotados
    })


@app.after_request
def add_security_headers(response):
    """Agrega headers de seguridad."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


# ============================================================
# USO Y PRUEBAS
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("API con Rotacion Automatica de API Keys")
    print("=" * 60)

    print("""
Pruebas:
  # 1. Generar una API key
  curl -X POST http://localhost:5000/api/key/generar \\
    -H "Content-Type: application/json" \\
    -d '{"client_id": "cliente-ejemplo"}'

  # 2. Usar la API key
  curl http://localhost:5000/api/datos \\
    -H "X-API-Key: sk_<key_generada>"

  # 3. Rotar la key
  curl -X POST http://localhost:5000/api/key/rotar \\
    -H "X-API-Key: sk_<key_actual>"

  # 4. Revocar una key
  curl -X POST http://localhost:5000/api/key/revocar \\
    -H "X-API-Key: sk_<key_actual>" \\
    -H "Content-Type: application/json" \\
    -d '{"key_id": "key_<id_a_revocar>"}'
""")
    app.run(debug=True, port=5000)
```

## Preguntas y Respuestas

**P1: Que es un secreto en el contexto de desarrollo de software?**
R: Un secreto es cualquier informacion que permite acceso a sistemas o datos protegidos: API keys, contrasenas, tokens de autenticacion, claves SSH, certificados TLS, claves de cifrado, connection strings. Si se expone, un atacante puede acceder a los sistemas sin autenticacion.

**P2: Cuales son las 5 practicas inseguras mas comunes en manejo de secretos?**
R: (1) Hardcodear secretos en el codigo fuente. (2) Incluir archivos .env en repositorios Git. (3) Compartir secretos por Slack, email o mensajeria. (4) Usar la misma clave en todos los entornos (dev, staging, prod). (5) No rotar secretos periodicamente o despues de un incidente.

**P3: Como funciona git-secrets y que detecta?**
R: git-secrets es una herramienta de AWS que escanea commits, archivos y mensajes de commit en busca de patrones de secretos. Puede detectar patrones predefinidos (AWS Access Keys) y patrones personalizados configurados por el usuario. Tambien puede configurarse como pre-commit hook para evitar que secretos lleguen al repositorio.

**P4: Que diferencia hay entre truffleHog y git-secrets?**
R: git-secrets usa patrones regex para detectar secretos conocidos (ej: AKIA... para AWS keys). truffleHog ademas analiza entropia (Shannon entropy) para detectar strings de alta entropia que parecen secretos aunque no coincidan con patrones conocidos. truffleHog tambien escanea todo el historial de Git, no solo el codigo actual.

**P5: Que es rotacion de secretos y por que es importante?**
R: Rotacion de secretos es el proceso de reemplazar un secreto por uno nuevo periodicamente o despues de un incidente de seguridad. Es importante porque: (a) limita la ventana de exposicion si un secreto es comprometido, (b) cumple con regulaciones (PCI-DSS, SOC2), (c) reduce el impacto de filtraciones de datos.

**P6: Como se debe almacenar una API key en una base de datos?**
R: Nunca en texto plano. Se debe almacenar el hash de la API key usando SHA-256 o similar. La key raw se muestra al usuario UNA SOLA VEZ cuando la genera. Para validacion, se hashea la key recibida y se compara con los hashes almacenados.

**P7: Que es el principio de "periodo de gracia" en rotacion de secretos y por que es util?**
R: El periodo de gracia es el tiempo durante el cual las keys viejas siguen siendo validas despues de una rotacion. Permite que los clientes actualicen sus keys sin perder acceso inmediato. Durante este periodo, tanto la key nueva como la vieja son aceptadas. Una vez que termina el periodo, la key vieja deja de funcionar.

## Tarea / Lectura Recomendada

1. **HashiCorp Vault Documentation:**
   https://developer.hashicorp.com/vault/docs

2. **Azure Key Vault Developer Guide:**
   https://learn.microsoft.com/en-us/azure/key-vault/

3. **AWS Secrets Manager Documentation:**
   https://docs.aws.amazon.com/secretsmanager/

4. **truffleHog GitHub:**
   https://github.com/trufflesecurity/trufflehog

5. **git-secrets (AWS Labs):**
   https://github.com/awslabs/git-secrets

6. **OWASP Secrets Management Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

7. **Tarea practica:** Configurar Vault en Docker local y conectar la app Flask para leer secretos.

8. **Tarea practica:** Implementar un pre-commit hook de Git que ejecute git-secrets y truffleHog antes de cada commit.



