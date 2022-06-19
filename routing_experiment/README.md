<!-- Date : 2021/08/16 -->
<!-- Author : Naoto Suzuki (Core Concept Technology .inc) -->

実験担当者へ<br>

ネットワーク実験の環境構築方法と，当日何をすればいいのかについてここに残しておきます．
このページの末尾に[エラー対応のQ&A](#Error) を書いておくので，歴代の実験担当者は，自身が経験したエラーはどんな些細なものでもこの項目に書き足してください．

- [全体の流れ](#Flow)
- [仮想マシンの構築](#Build)
- [仮想マシンのクローン](#Clone)
- [当日に解説すべきこと＆作業内容](#Todo)
- [エラー対応](#Error)
- [注意事項](#Attention)

<a id="Flow"></a>
# 全体の流れ
まずは仮想マシン構築の全体の流れを解説します．
以下のような作業手順です:

1. Ubuntu Server のiso イメージを公式からダウンロードし，VirtualBox にUbuntu Server の仮想マシンを作成
2. 最初に雛形となる仮想マシンを1台設定する(NIC の追加，ユーザ名の設定，及びIPアドレスの設定)
3. 上記の仮想マシンのクローンを2~30 台用意する(つまりこっちの作業がメイン，めんどいからスクリプト作成中)

<a id="Build"></a>
# 仮想マシンの構築
ここでは最初の雛形となる仮想マシン1台の作り方を解説します．

まずは公式サイトからUbuntu Server のISOイメージファイルをダウンロードしてきます．
公式は<a href="https://jp.ubuntu.com/download">こちら</a><br>

※ 2021年8月現在，従来までのNIC 設定手法(ifup/down と/etc/network/interfaces) が廃止となり，新方式としてnetplan と/etc/netplan/hoge.yaml に変更になったようです．
ちなみに新方式ではOS の再起動が不要になりました(netplan apply でok)．素晴らしい．


ダウンロードが完了したら，virtualbox を起動します．
virtualbox がない場合には適宜インストールしてください(めっちゃ簡単なので省略します)<br><br>

<a id="Hardware"></a>
## ハードウェアの設定

最初に新規仮想マシンを作成します．<br>
仮想マシンのスペックは以下の通り:
- 名前は"host1-1"，タイプは"Linux"，バージョンは"Ubuntu (64-bit)"
- メモリサイズは"1024MB"
- 仮想ハードディスクを作成する("VDI" を選択)
- 物理ハードディスクにあるストレージは"可変サイズ"を選択
- ファイルの場所はデフォルトのままにして，仮想ハードディスクのサイズは"10.00GB"(ケチったらインストールできなかった)

まぁつまり作業的にはただokをポチポチ押すだけです．
<!-- 画像 -->
<img src="https://github.com/sit-icnl/seminar/blob/img/virtualbox1.jpg" alt="仮想マシンの構築図1">


次に，作成した仮想マシンのハードウェアの設定を行います．
まず，ディスクイメージとして先程ダウンロードしたISO ファイルを指定します．
```
設定 → ストレージ → コントローラIDE → "空" を選択
     → 工学ドライブの一番右のディスクマークをクリック → "ディスクファイルを選択" をクリック
     → Ubuntu Server のiso ファイルを選択 → ok
```
<!-- 画像 -->
<img src="https://github.com/sit-icnl/seminar/blob/img/virtualbox2.jpg" alt="仮想マシンの構築図2">


最後に，NIC デバイス(LAN ポートのこと)を追加します．
この操作によって，仮想マシンに付属するLAN ポートのタイプと個数を自由にカスタマイズすることができます．
今回は，ゼミ生のssh 接続用のLAN ポート以外に2つのLAN ポートが必要なので，「ホストオンリーアダプタ」というタイプのNIC を2つ追加します．
```
設定 → ネットワーク → アダプター2
     → "ネットワークアダプタを有効化" をチェック
     → 割り当て → "ホストオンリーアダプタ" を選択

同様にして，アダプタ3 にもホストオンリーアダプタを追加する

ネットワーク1 のアダプタをNAT から"ブリッジアダプタ" に変更する
```
<!-- 画像 -->
<img src="https://github.com/sit-icnl/seminar/blob/img/virtualbox3.jpg" alt="仮想マシンの構築図3">


これで一応仮想マシンが起動するようになります．
では早速仮想マシンを起動してみましょう．

```
起動すると，サーバなので以下の設定があります．

1.  言語は? → "English"
2.  アップデートするか? → "Continue without updating" (アップデートされると困る)
3.  キーボード配列は? → Layout: "Japanese", Variant: "Japanese" (宮田研のキーボードは日本語配列なので)
4.  NIC のデフォルト設定は以下の様な感じでokか? → "Done" (後で手動で変えるのでこれでok)
5.  プロキシ使うならプロキシサーバのアドレスを入力して → "Done" (使わないからスルー)
6.  ubuntu の代替ミラーサーバを使うなら詳細を入力して → "Done" (デフォルトでok)
7.  ファイルシステムの構成はどうする? → "Use An Entire Disk" (普通に全部使いましょう)
8.  インストール先の仮想ディスクを選択して → "VBOX_HARDDISK_hogehogehoge local disk 10.00GB" 的な名前のやつを選択(つまりさっき作ったやつ)
9.  ファイルシステムの内訳を見せてくれるので"Done" → "Confirm destructive action" という「ディスク内に既存のデータがある場合には消えるぞ」的な警告が出るが，元々空なので"Continue"
10. ユーザ情報を入力する．
    Your name: "host1",
    Your server's name: "host1", 
    Pick a username: "host1",
    Choose a password: "host1"
    Confirm your password: "host1"
11. OpenSSH をインストールするか? →Enter を押して"[X]" の状態にする ＆ Import SSH identity は"No" でok
12. 何か入れたいツールはあるか?(docker やaws cli 等の便利ツールが示される) → "Done" (後で入れられるのでスルーしてok)


この状態でしばらく放置すると，"[ View full log ]" の下に"[ Cancel update and reboot ]" という項目が現れるので，それをクリック

  ↓

目立たないけど"Please remove Install media and then press Enter" 的なメッセージが出るので，Enter を押すと再起動が始まってインストールが完了！


※ 後はログイン画面が出るまで放置すればいいのだが，たまに自動的には出てこないときがある．そういうときはEnter を押すと普通にログイン画面が出る．
```


起動が完了すると，ユーザ名とパスワードが求められるので，先程設定したユーザ情報を入力しましょう(ユーザ名，パスワード共に"host1")．
なお，デフォルトではroot ユーザのパスワードが設定されていないため，root でログインしたい場合には一旦host1 でログインし，root のパスワードを設定する必要があります．


<a id="Software"></a>
## ソフトウェアの設定

ここからは，コマンドラインでの操作となります．
このマシンは他のマシンの雛形なので，作業内容としては主にネットワーク設定だけです．
仮想マシン内ではこのページのコピペが難しいと思うので，頑張って手入力するか，このファイルをダウンロードしてください．<br>
※ 手入力の場合，以下のサンプルコマンドの冒頭の"$" は入力しないでください("$" は可読性を上げるために書いたプロンプトです)．
※ コマンドの入力の際は，tab キーによる補完を使いましょう(typo を防ぐ意味もあるので)

大前提として，<b>ホストOS，仮想マシン，外部からssh を行うマシンは全て同じネットワークに所属していなければなりません．</b>
virtualbox を動かすPC は研究室のルータに有線で繋ぐか，固定IP の設定を行って下さい(ルータに繋ぐのをおすすめします)．

windows マシンを固定IP にする場合，ファイアウォールの設定からICMP の受信も許可する必要があります(じゃないとping が通らない)．
詳しくは調べればすぐ出てくるので書きませんが，windows へのping が通らない場合にはこの設定を疑ってみて下さい．

```
 ### ここからユーザ情報の設定 ###

 # root ユーザのパスワードを設定する(これやらないとroot 権限が全く使えない)
 # root ユーザのパスワードは"root" にする
 $ sudo passwd root


 ### ここからはネットワーク設定 ###

 # NIC の名前を調べる(名前はマシンによるが，enp0s〇〇 とかens〇〇 とかいう名前が多い)
 # デフォルトではDHCP が有効になっているので，後で固定にする
 # まさかのifconfig が入っていない場合には，"sudo apt-get install net-tools" でインストールする(このときはDHCP に頼ろう)
 $ ifconfig -a

 # 固定IP アドレスを設定する(このマシンにssh するための設定なので，本物の宮田研のネットワークを指定すること)
 $ sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/99_config.yaml # 名前はなんでもいいが，元のファイルよりも50音順が後になるようにすること(netpaln の仕組みの問題)
 $ sudo vim /etc/netplan/99_config.yaml # 詳細は下のスクリプトを参照すること
 $ sudo netplan apply

 # IP アドレスの確認(本物のPC にUbuntu を入れて固定IP化する場合は，LAN ケーブルの両端をアクティブなLAN ポートに挿さないと有効化されないので注意)
 $ ifconfig


 # ラズパイやMac などの別のPC をこのPC と同一ネットワーク上の適当なハブなどに有線接続し，ssh 接続ができるか確認する
 # 以下のコマンドをラズパイやMac などのターミナル上から実行(windows はだめです)
 $ sudo ssh host1@192.168.10.〇〇
 # 自分のPC のパスワードを入れた後，host1 のパスワードを聞かれたらok

 # フォワーディングの設定はゼミ内で受講生にやらせたいので，未設定でok

 # ok ならシャットダウン
 $ shutdown -h now
```

```yaml
# このファイルの構造はちゃんと説明すること！
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with following:
# network: {config: disable}

network:
  ethernets:
    enp0s3:
      dhcp4: false
      addresses: [192.168.10.〇〇/24]
      gateway4: 192.168.10.1
      nameservers:
        addresses: [192.168.10.1, 8.8.8.8]

    enp0s8:
      dhcp4: false

    enp0s9:
      dhcp4: false

  version: 2
```

ここまでできたら，仮想マシンのスナップショットをとっておきましょう．
スナップショットを取ると，後で設定を変更してもスナップショットの状態までロールバックすることができます．

後でマシンの状態が分からなくなると後々使い物にならなくなるので，必ずコメント欄に以下の情報を記述して下さい:
- 作成日時(20XX/MM/DD)
- 作成者(学籍番号 名前)
- ssh 用のIP アドレス
- マシンの状態(すぐに実験できる状態なのか，実験後の状態なのか等)
- その他(後々ハマり所になりそうな所やバグっぽい所等があれば書く)


<a id="Clone"></a>
# 仮想マシンのクローン
上記の設定で雛形となる仮想マシンが1台完成したため，この仮想マシンを複製します(上記作業を20 回とか繰り返すのは辛いため)．
注意するところは以下の通り:
1. MAC アドレスとUUID は再割り当てする
1. 仮想マシンの名前をきちんと変更しておく

<img src="https://github.com/sit-icnl/seminar/blob/img/virtualbox4.jpg" alt="クローン画面">

上記操作でハードウェアの複製は完成ですが，中身がhost1 のままなので，今度はコマンド操作でユーザ情報を変更します．
以降はsudo を付けて実行するのではなく，最初からroot ユーザとしてログインして作業して下さい．

```
 ### ユーザ情報の設定 (例: host1 をhost2 に変更する) ###

 # root でログイン(名前: root, パスワード: root)

 #. ユーザ情報の変更(/etc/passwdのユーザ名を新規ユーザ名に置換)
 $ perl -pi -e 's;host1;host2;g' /etc/passwd

 #. 所属グループの変更(/etc/groupも置換)
 $ perl -pi -e 's;host1;host2;g' /etc/group

 #. /etc/hosts の変更(名前解決)
 $ perl -pi -e 's;host1;host2;g' /etc/hosts

 #. ホスト名(マシンの名前) も変えるなら/etc/hostname も変更する(やったほうがいい)
 $ perl -pi -e 's;host1;host2;g' /etc/hostname

 #. ホームディレクトリ名の変更(普通に名前変えるだけ)
 $ mv /home/host1 /home/host2

 #. パスワードの変更(既に/etc/passwd を編集済みなので，host2 のパスワードを変更する事になる)
 $ passwd host2

 #. 再起動して今度はhost2 でログインする
 $ shutdown -r now

```

```
 ### ここからはネットワーク設定 ###

 # NIC の名前を調べる
 $ ifconfig -a

 # SSH 用の固定IP アドレスを変更する(そのままだとhost1 と衝突する)
 $ sudo vim /etc/netplan/99_config.yaml # 詳細は省略するが，他のデバイスとかぶらないようにすること
 $ sudo netplan apply

 # 確認
 $ ifconfig


 ### 疎通確認 ###

 #. 試しにenp0s8 とかに固定IP を設定し，host1 のenp0s8 等にping を飛ばしてみる
 $ ping 10.0.0.XX

```

<a id="Todo"></a>
# 当日に解説すべきこと＆作業内容
このネットワーク実験ですが，基本コンセプトが「本物のサーバとコマンドに触れて，ネットワーク構築を自分で体験してみよう」というところにあるので，基本的には受講生は講師の言うとおりに手を動かすことになります．
そのため，講師のレクチャがいい加減だと，「なんかよくわかんないけど言われたとおりにやったらよく分かんないまま気づいたら終わっちゃってた」という事態になりがちです．
なので，レクチャする際には常に以下のことに細心の注意を払ってください:
- 自分たちがやってる作業がなんなのかを常に把握させる(そのコマンドを実行するとどういう現象が起こるのか)
- なぜその作業が必須なのかを解説する(ネットワークを構築するには何をどこまで考えなきゃいけないのか，その考え方の指針をちゃんと伝える)
- /etc/netplan/hoge.yaml の記述の意味を解説する(このファイルの構造はただの暗号で終わらせてはならない，簡単でいいからyaml の文法と紐づけて意味を解説する)
- 作業を行う上で受講生が疑問に思いそうな「そもそもの疑問」を解説する(「そもそもコマンドっていうのは何者なの?」 とか「なんでssh してるの?」 とか「仮想マシンって何?」 とか)

この実験は，ネットワークやLinux の世界に興味を持ってもらうための最初の入り口になる可能性がある重要な実験です．
中にはこの実験をきっかけにネットワークエンジニアを志す人もいるものなので，間違っても「よく分からなくてトラウマになった」とか「ただの作業ゲーでつまらなかった」といったことにならないように注意してください．

<a id="Error"></a>
# エラー対応
- ping が通らない
	- 仮想マシンのIP アドレスを確認する(受講生の設定が"162.168.10.100" とかになってて運営側が気づかなかったケースがあった)
	- 自分のIP アドレスを確認する
	- windows のファイアウォールの設定を疑う(ファイアウォールの詳細設定の送受信の規則でICMPv4 が遮断されてないか確認，詳しくはググって)
	- ホストOS とゲストOS のアダプタがブリッジ接続になってない
	- LAN ケーブルが断線してないか確認する
- IP アドレスが有効にならない
	- /etc/netplan/hoge.yaml のtypo を確認する
	- LAN ケーブルが有効なLAN ポートに挿さってない(両方とも挿さってないと駄目です)
- ssh できない
	- 入力しているパスワードが正しいか確認する．一回目に求められるのはsudo によるパスワードで，二回目のパスワードがssh 先のパスワードである．
	- コマンドの書式が間違ってないか確認する．"sudo ssh ホスト名@IPアドレス"
	- IP アドレスが衝突してないか確認する．仮想マシン及びラズパイのアドレスがダブってないことは確認済みだったのに，仮想マシンの動作確認で繋いでいた院生のPC のIP アドレスと衝突していたケースがあった．
	- そもそもping が通るか確認する
- ルーティングできない
	- 末端の端末にデフォルトゲートウェイが設定されてない
	- ルーティングの書式が間違っている
	- ルータのフォワーディングがoff になっている(ファイル編集しないと再起動したらoff になります，あとsysctl -p やらないと有効化されません)
	- 宛先ネットワークの指定欄で"0/24" が抜けている，あるいは具体的なホスト部が入力されている(つまり書式ミス)

<a id="Attention"></a>
# 注意事項
- 2021年8月現在，Ubuntu 20.04LTS では"/etc/network/interfaces" が廃止されていた(!! Σ＠口＠)．Ubuntu Server 18.04 ではまだ使えると思うが，今後この実験をする際には固定IP の設定方法が変わってくる可能性がある(systemd の管理下になっていた)．あまり古い手法を教えても意味がないので，その際には適宜資料などを一新すること．
