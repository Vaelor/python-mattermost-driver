#!/usr/bin/env bash

STORE_DIR="mattermostdriver"

rm -f src/$STORE_DIR/endpoints/*.py
touch src/$STORE_DIR/endpoints/__init__.py

cat << EOF > src/$STORE_DIR/endpoints/base.py
class Base:
    def __init__(self, client):
        self.client = client
EOF

python bin/generate_endpoints_ast.py
