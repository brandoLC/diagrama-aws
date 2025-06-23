# API de Diagramas Serverless

API construida con AWS Lambda y Serverless Framework que recibe código Python para generar diagramas usando la librería `diagrams` y devuelve la imagen generada.

## 🚀 Características

- **Entrada**: Código Python con sintaxis de la librería `diagrams`
- **Salida**: Imagen en formato base64 (PNG, SVG, PDF)
- **Serverless**: Ejecuta en AWS Lambda con escalado automático
- **CORS**: Habilitado para uso desde aplicaciones web

## 📋 Prerrequisitos

1. **Node.js** (v14 o superior)
2. **Python** (3.9)
3. **AWS CLI** configurado
4. **Serverless Framework**

```bash
# Instalar Serverless Framework globalmente
npm install -g serverless

# Configurar AWS CLI (si no está configurado)
aws configure
```

## 🛠️ Instalación y Despliegue

### 1. Instalar dependencias

```bash
npm install
```

### 2. Crear la capa de Graphviz

```bash
# Hacer el script ejecutable
chmod +x scripts/create-simple-layer.sh

# Crear la capa
./scripts/create-simple-layer.sh
```

### 3. Desplegar la API

```bash
# Desplegar en desarrollo
npm run deploy-dev

# O usar serverless directamente
serverless deploy --stage dev
```

Después del despliegue, obtendrás la URL de tu API:

```
endpoints:
  POST - https://tu-api-id.execute-api.us-east-1.amazonaws.com/dev/generar-diagrama
```

## 📡 Uso de la API

### Endpoint

```
POST /generar-diagrama
Content-Type: application/json
```

### Payload

```json
{
  "codigo": "from diagrams import Diagram\\nfrom diagrams.aws.compute import Lambda\\n\\nwith Diagram('Mi Diagrama', show=False):\\n    Lambda('Mi Función')",
  "formato": "png"
}
```

### Respuesta Exitosa

```json
{
  "success": true,
  "imagen": "iVBORw0KGgoAAAANSUhEUgAA...", // imagen en base64
  "formato": "png",
  "contentType": "image/png",
  "tamaño": 15420,
  "mensaje": "Diagrama generado exitosamente como mi_diagrama.png"
}
```

### Respuesta de Error

```json
{
  "error": "Error de sintaxis en el código: invalid syntax"
}
```

## 🧪 Pruebas

### Prueba Local

```bash
# Probar la función localmente
npm run test-local
```

### Prueba con cURL

```bash
curl -X POST https://tu-api-url/dev/generar-diagrama \\
  -H "Content-Type: application/json" \\
  -d '{
    "codigo": "from diagrams import Diagram\\nfrom diagrams.aws.compute import Lambda\\n\\nwith Diagram(\"Test\", show=False):\\n    Lambda(\"Test\")"
  }'
```

### Prueba con Python

```python
import requests
import base64

url = "https://tu-api-url/dev/generar-diagrama"
payload = {
    "codigo": """
from diagrams import Diagram
from diagrams.aws.compute import Lambda

with Diagram("Mi Diagrama", show=False):
    Lambda("Mi Función")
    """
}

response = requests.post(url, json=payload)
data = response.json()

if data['success']:
    # Decodificar y guardar imagen
    imagen_bytes = base64.b64decode(data['imagen'])
    with open('diagrama.png', 'wb') as f:
        f.write(imagen_bytes)
```

## 📚 Librerías Soportadas

La API soporta las siguientes librerías de diagramas:

### AWS

- `diagrams.aws.compute`: ECS, Lambda, EC2, Batch, EKS
- `diagrams.aws.database`: RDS, ElastiCache, DynamoDB, Redshift
- `diagrams.aws.network`: ELB, APIGateway, CloudFront, Route53
- `diagrams.aws.storage`: S3
- `diagrams.aws.analytics`: EMR, Glue, Kinesis
- `diagrams.aws.integration`: SQS, SNS
- `diagrams.aws.security`: IAM, Cognito

### Azure

- `diagrams.azure.compute`: VM, FunctionApps, ContainerInstances
- `diagrams.azure.database`: SQLDatabases, CosmosDb
- `diagrams.azure.network`: LoadBalancers, ApplicationGateway

### Google Cloud

- `diagrams.gcp.compute`: ComputeEngine, Functions, GKE
- `diagrams.gcp.database`: SQL, Firestore
- `diagrams.gcp.network`: LoadBalancing

### On-Premise

- `diagrams.onprem.database`: MySQL, PostgreSQL, MongoDB
- `diagrams.onprem.inmemory`: Redis
- `diagrams.onprem.network`: Nginx

## 💡 Ejemplos de Código

### Ejemplo Básico

```python
from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS

with Diagram("Aplicación Simple", show=False):
    app = Lambda("API")
    db = RDS("Base de Datos")

    app >> db
```

### Ejemplo con Clusters

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB

with Diagram("Microservicios", show=False):
    lb = ELB("Load Balancer")

    with Cluster("Aplicación"):
        apps = [ECS("App 1"), ECS("App 2")]

    with Cluster("Base de Datos"):
        db = RDS("MySQL")
        cache = ElastiCache("Redis")

    lb >> apps >> db
    apps >> cache
```

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
npm run logs

# Eliminar el stack
npm run remove

# Redesplegar solo una función
serverless deploy function --function generarDiagrama

# Invocar función localmente con evento personalizado
serverless invoke local -f generarDiagrama -p test/event.json
```

## 📁 Estructura del Proyecto

```
api-diagramas/
├── handler.py              # Función Lambda principal
├── serverless.yml          # Configuración de Serverless
├── requirements.txt        # Dependencias Python
├── package.json           # Scripts y dependencias Node.js
├── scripts/
│   ├── create-layer.sh     # Script para crear capa de Graphviz
│   └── create-simple-layer.sh
├── test/
│   ├── event.json         # Evento de prueba
│   └── test_api.py        # Script de prueba
└── layers/                # Capas generadas (creadas automáticamente)
```

## 🛡️ Limitaciones

- **Timeout**: 30 segundos máximo por ejecución
- **Memoria**: 512MB configurados
- **Tamaño de payload**: Máximo 6MB para API Gateway
- **Formatos**: PNG, SVG, PDF soportados
- **Librerías**: Solo las pre-instaladas en la capa

## 🔐 Seguridad

- CORS habilitado para todas las peticiones
- No se ejecuta código arbitrario del sistema
- Entorno sandboxed de Lambda
- Directorio temporal limpiado automáticamente

## 🚨 Troubleshooting

### Error: "Graphviz not found"

- Verificar que la capa se creó correctamente
- Revisar permisos de ejecución en scripts

### Error: "Module not found"

- Verificar que todas las dependencias están en requirements.txt
- Recrear la capa con `./scripts/create-simple-layer.sh`

### Error de timeout

- Simplificar el diagrama
- Verificar que use `show=False` en Diagram()

## 📄 Licencia

MIT License - Puedes usar este código libremente para proyectos comerciales y no comerciales.
