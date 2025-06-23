#!/bin/bash

echo "🔧 Creando capa simplificada de Graphviz para AWS Lambda..."

# Crear directorio para la capa
mkdir -p layers/graphviz-layer/python/lib/python3.9/site-packages
mkdir -p layers/graphviz-layer/opt/graphviz

cd layers/graphviz-layer

echo "📦 Instalando dependencias Python..."
# Instalar las dependencias de Python en la estructura correcta
pip install diagrams==0.23.3 graphviz==0.20.1 -t python/lib/python3.9/site-packages/

echo "⬇️ Configurando Graphviz..."
# Crear un directorio opt para los binarios de Graphviz
mkdir -p opt/graphviz/bin
mkdir -p opt/graphviz/lib

# Crear scripts wrapper que usen el PATH del sistema
cat > opt/graphviz/bin/dot << 'EOF'
#!/bin/bash
export PATH="/usr/bin:$PATH"
export LD_LIBRARY_PATH="/usr/lib64:$LD_LIBRARY_PATH"
exec /usr/bin/dot "$@"
EOF

cat > opt/graphviz/bin/neato << 'EOF'
#!/bin/bash
export PATH="/usr/bin:$PATH"
export LD_LIBRARY_PATH="/usr/lib64:$LD_LIBRARY_PATH"
exec /usr/bin/neato "$@"
EOF

# Hacer los scripts ejecutables
chmod +x opt/graphviz/bin/*

echo "🗜️ Comprimiendo capa..."
# Crear el archivo ZIP de la capa
zip -r graphviz-layer.zip python/ opt/

echo "✅ Capa creada exitosamente: layers/graphviz-layer/graphviz-layer.zip"
echo "📁 Tamaño de la capa: $(du -h graphviz-layer.zip | cut -f1)"

cd ../..

echo ""
echo "📋 Próximos pasos:"
echo "1. Instalar Serverless Framework: npm install -g serverless"
echo "2. Configurar AWS CLI: aws configure"
echo "3. Desplegar la API: serverless deploy"
