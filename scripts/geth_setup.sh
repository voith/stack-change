mkdir -p /root/node
cd /root/node
wget https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.8.12-37685930.tar.gz
tar -xvzf geth-linux-amd64-1.8.12-37685930.tar.gz
mkdir -p geth-dir
tar -xvzf geth-linux-amd64-1.8.12-37685930.tar.gz -C geth-dir --strip-components 1
cp scripts/config/geth.conf /etc/supervisor/conf.d/
