<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Instrucciones para Copilot - API de Diagramas Serverless

Este es un proyecto serverless que usa AWS Lambda para generar diagramas a partir de código Python.

## Contexto del Proyecto

- **Framework**: Serverless Framework con AWS Lambda
- **Lenguaje**: Python 3.9
- **Librerías principales**: diagrams, graphviz
- **Objetivo**: API REST que recibe código Python y devuelve imágenes de diagramas

## Patrones de Código

### Estructura de Función Lambda

```python
def generar_diagrama(event, context):
    # Parsear body JSON
    # Ejecutar código de diagrama en sandbox
    # Devolver imagen en base64
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(resultado)
    }
```

### Manejo de Errores

- Capturar SyntaxError para errores de código
- Capturar ImportError para librerías no disponibles
- Devolver errores HTTP apropiados (400, 500)

### Configuración Serverless

- Usar capas para dependencias binarias
- Configurar CORS correctamente
- Timeout de 30 segundos para diagramas complejos

## Convenciones

1. **Archivos temporales**: Usar `tempfile.TemporaryDirectory()`
2. **Base64**: Codificar imágenes para transport HTTP
3. **Validación**: Verificar que el código contenga `with Diagram(...)`
4. **Seguridad**: No ejecutar código del sistema, solo librerías permitidas

## Comandos Importantes

- `serverless deploy`: Desplegar API
- `./scripts/create-simple-layer.sh`: Crear capa de Graphviz
- `serverless invoke local`: Pruebas locales
