#!/bin/bash

# 2019/10/10
# Author : 

調整中！！動かないと思います(そもそもシェルスクリプトでやる内容じゃないかも)．
ただ，流れは以下のイメージですので参考までにどうぞ！

# host1という仮想マシンのクローンhost2を作成する. 
# usermodは，現在ログインしているユーザの名前を変更することができない．したがって，必ずrootでログインする必要がある．
# 多分うまく行く(未検証)

set -e

if [ $# != 1 ]; then
	echo "Enter the new user name. \n"
	exit 1
fi

echo -e "Are you root?"
read answer

case $answer in
[Yy] )
sed "s/host1/$1/g" /etc/passwd # ユーザ情報の変更. 
sed "s/host1/$1/g" /etc/group # グループ情報の変更. 
mv host1/ $1/ # ホームディレクトリの名前の変更. 
echo $1 | sudo tee passwd # パスワードの変更．
usermod -l host1 $1 # ユーザ名の変更．
echo ;;

* )
echo -e "Cancelled. \n"
exit 1;;
esac

<<COMMENT

<<クローン作成マニュアル>>

1. rootでログイン
2. ユーザ情報の変更(/etc/passwdのユーザ名を新規ユーザ名に置換)
3. 所属グループの変更(/etc/groupも置換)
4. ホームディレクトリ名の変更(普通に名前変えるだけ)
5. パスワードの変更(sudo passwd host2)
6. /etc/hosts も更新
7. ホスト名(マシンの名前) も変えるなら/etc/hostname も変更する

COMMENT
