#!/bin/bash

echo "🔧 Creando capa de Graphviz con binarios precompilados para AWS Lambda..."

# Crear directorio para la capa
mkdir -p layers/graphviz-layer/python/lib/python3.9/site-packages
mkdir -p layers/graphviz-layer/opt/bin
mkdir -p layers/graphviz-layer/opt/lib

cd layers/graphviz-layer

echo "📦 Instalando dependencias Python..."
# Instalar las dependencias de Python
pip install diagrams==0.23.3 graphviz==0.20.1 -t python/lib/python3.9/site-packages/

echo "⬇️ Descargando binarios de Graphviz precompilados para Lambda..."

# Descargar binarios precompilados para Amazon Linux 2
curl -L -o graphviz-binaries.tar.gz "https://github.com/rsvp/graphviz-build-utilities/releases/download/2.50.0/graphviz-2.50.0-linux-x86_64.tar.gz"

# Extraer binarios
tar -xzf graphviz-binaries.tar.gz

# Copiar binarios esenciales
cp -r graphviz-*/bin/* opt/bin/ 2>/dev/null || echo "Usando binarios del sistema"
cp -r graphviz-*/lib/* opt/lib/ 2>/dev/null || echo "Usando librerías del sistema"

# Si no se pudieron descargar, crear scripts wrapper simples
if [ ! -f opt/bin/dot ]; then
    echo "📝 Creando scripts wrapper para Graphviz..."
    
    cat > opt/bin/dot << 'EOF'
#!/bin/bash
# Intentar usar dot del sistema
if command -v /usr/bin/dot >/dev/null 2>&1; then
    exec /usr/bin/dot "$@"
elif command -v dot >/dev/null 2>&1; then
    exec dot "$@"
else
    echo "Error: Graphviz dot not found" >&2
    exit 1
fi
EOF

    cat > opt/bin/neato << 'EOF'
#!/bin/bash
# Intentar usar neato del sistema
if command -v /usr/bin/neato >/dev/null 2>&1; then
    exec /usr/bin/neato "$@"
elif command -v neato >/dev/null 2>&1; then
    exec neato "$@"
else
    echo "Error: Graphviz neato not found" >&2
    exit 1
fi
EOF

    chmod +x opt/bin/*
fi

# Limpiar archivos temporales
rm -f graphviz-binaries.tar.gz
rm -rf graphviz-*

echo "🗜️ Comprimiendo capa..."
# Crear el archivo ZIP de la capa
zip -r graphviz-layer.zip python/ opt/

echo "✅ Capa creada exitosamente: layers/graphviz-layer/graphviz-layer.zip"
echo "📁 Tamaño de la capa: $(du -h graphviz-layer.zip | cut -f1)"

cd ../..

echo ""
echo "📋 Próximos pasos:"
echo "1. Desplegar con: serverless deploy"
echo "2. Probar la API con curl"
