#!/usr/bin/env bash

# Date : 2019/11/13
# Author : Naoto Suzuki (MA19046)

# このスクリプトは，/etc/network/interfaces ファイルの設定を行うものである．
# 以下のネットワーク設定を正しく設定したら，シェル上で以下のコマンドを実行する．
# 
# ./build_network.sh
# 
# 本当に実行して良いか聞かれるので，okなら'Y'か'y'を入力する．
# フォワーディングの設定まではやっていないので，そこは自分でやること．
# 実行したら再起動すること．
# 
# 絶対に2回連続して実行しないでください．一応バックアップも取ってありますが，
# 普通に考えてこれを何度も実行すると設定がおかしなことになります．
# 詳しくは man 5 interfaces を見てみると良いと思います．

set -eu

# file="./test.conf" # テスト用
file="/etc/network/interfaces"

cat << EOF
### Ubuntu Only ###
this script build the NIC configuration file : "/etc/network/interfaces". 
If the following network settings are complete, 
please run this script and reboot this machine. 
EOF
echo -e "\x1b[1;31mDon't run this script twice. \x1b[0m"
echo -e "Do you want to run? [Y/n] : "

read answer
case $answer in
[^Yy] )
	echo -e "Aborted. "
	exit 1;;
esac


cp $file ${file}_backup
echo -e "\x1b[33m"
# 以下の設定はサンプルです(画面表示はoff にしてあります)
cat <<EOF | sudo tee -a $file 1>/dev/null

auto eth0
iface eth0 inet static
address=192.168.10.2
network=192.168.10.0/24
netmask=255.255.255.0

auto eth1
iface eth1 inet static
address=192.168.10.3
network=192.168.10.0/24
netmask=255.255.255.0

auto eth2
iface eth2 inet static
address=192.168.10.4
network=192.168.10.0/24
netmask=255.255.255.0
EOF

echo -e "\x1b[0m"

cat << EOF

complete. Please enable forwarding settings if you haven't done it. 
Then, reboot this machine. 

[forwarding]
 $ sudo vi /etc/sysctl.conf
 $ sudo sysctl -p
 $ shutdown -r now

EOF

# スクリプトを実行して再起動したら以下のコマンドでルーティングテーブルを作成すること．
# あるいは上記の設定ファイルにデフォルトゲートウェイの設定を書いてもよい．
# 
# $ sudo route 行き先IP/24 gw ゲートウェイのIP
# 
