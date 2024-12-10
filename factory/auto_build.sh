#!/bin/bash

Path=./factory
cd $Path

python3 ad.py
python3 gfwlist.py
python3 build_confs.py
python3 build_singbox_confs.py

VERSION=$(curl -s https://api.github.com/repos/SagerNet/sing-box/releases/latest \
| grep tag_name \
| cut -d ":" -f2 \
| sed 's/\"//g;s/\,//g;s/\ //g;s/v//')

curl -Lo sing-box.tar.gz "https://github.com/SagerNet/sing-box/releases/download/v${VERSION}/sing-box-${VERSION}-linux-amd64.tar.gz"
tar -xzvf sing-box.tar.gz
mv ./sing-box-${VERSION}-linux-amd64/sing-box .
chmod +x sing-box

./sing-box rule-set compile --output ../figure/proxy_list.srs ../figureproxy_list.json
