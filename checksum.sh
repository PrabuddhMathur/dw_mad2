#!/usr/bin/bash

BACKEND="$HOME/21f1000147/code/backend"
FRONTEND="$HOME/21f1000147/code/frontend"
cd "$HOME"

unzip "$HOME/Downloads/qxQDgkYZNh.zip" > /dev/null

cat << EOF > checksum.py
#!/usr/bin/python3
import checksumdir

hash=checksumdir.dirhash("21f1000147")
print(f'Checksum: {hash}')
EOF

chmod 755 checksum.py

./checksum.py

echo "-----Copying node_modules-----"
cp -r "$HOME/dw_mad2/frontend/node_modules" "$HOME/21f1000147/code/frontend"
echo "-----Completed-----"

echo "-----Copying Virtual Environment-----"
cp -r "$HOME/dw_mad2/.venv" "$HOME/21f1000147/code/backend"
echo "-----Completed-----"
