# infosec-create-user
ユーザー作成するためのリポジトリ

## TODO
各SaaSの各ユーザーに余計な権限やアカウントが付与されないような仕組みを作成する
### まず対応したいこと
あくまで、ローカルでのコードのメモであるので、terraformは書かない
また、鍵の情報は別で管理しているので、これだけではデバックは成功しない
- アカウント台帳への自動書き込み
- ユーザー削除の自動化
    - 下記ER図のテーブルをDynamo DBに作成し、ユーザー削除の際にはこちらを参照するようにする
    - トリガーはRedmineのチケットステータスが`担当者アサイン`になったとき？
    - ユーザー作成とはAPI GatewayのエンドポイントやLambdaのエンドポイントを分離する
    - 現行ではGoogle Workspaceのユーザー削除するにはダブルチェック必須となっているが、そこはどうする？
- 各SaaSの既存ユーザーIDをDynamo DBテーブルに追加
    - 既存のユーザープロビジョニングシートのプログラムをうまく活用できないか？
- 新規作成したユーザーのIDをDynamo DBテーブルに追加するプログラムの作成
- Microsoftライセンスの自動アタッチ（API自体がbetaなので一旦後回し？）

### いつかは対応すべきこと
- ロギング
    - 監査

### 上記が完了したら対応したいこと
まだ構想がまとまっていない
- ロール変更の自動化
    - Emailをプライマリとしてロールが変更できるようにする？

# インフラ
## 構成図
![](./drawio/infrastructure.drawio.svg)
![](./drawio/dynamodb_er.drawio.svg)

## 詳細
### 各リソースの役割について
| リソース名 | 役割
| --- | ---
| ECR | Lambda用のコンテナイメージの保管
| Lambda | ユーザー作成などのプログラムを実行
| API GW | Sumo LogicからのHTTP POSTを受け取り、Lambdaを実行
| CloudWatch | Lambda / API GWのログの保管
| Secrets Manager | Credentialsの保管
| Dynamo DB | ユーザーIDなどの情報を保管

### ER図について
プライマリをEmailとし、各サービスのIDを引けるようにします。基本的には各SaaSのユーザー削除時やロール変更時に必要なプロパティをDynamoに保管します。現在のER図ではIDと記載があるが、Emailをもとにしてユーザー削除や変更が可能であれば該当SaaSのIDをDynamoに保管する必要はないです。

### API Endpointについて
| HTTPメソッド | エンドポイント名 | 役割
| --- | --- | ---
| `POST` | `users` | ユーザー新規作成
| `DELETE` | `users` | ユーザー削除
| `PUT` | `users` | ユーザー更新



# デプロイ手順
1. Sumo LogicのReal Time Alertを配置するフォルダIDを取得
    ```
    curl -u "{{access_id}}:{{access_key}}" -X GET "https://api.jp.sumologic.com/api/v2/content/path?path=/Library/Admin%20Recommended/Information%20Security/Redmine"
    ```
2. `git push`
    - `terraform apply`や`docker build`などが行われます。リソース作成はすべてGitHub Actionsで行われます。

# ユーザー作成手順
## 対応SaaS
- Google Workspace
    - メールグループ追加は未実装
- OneLogin
- Netskope
- Wrike
    - グループ追加は未実装
- Kibe.la
- Microsoft
    - ライセンス追加は未実装
        - Intune
        - Office365
        - Teams


## TODO


### これからユーザー作成を自動化したいSaaS
- Slack
    - 現時点ではプラン的に無理
    - Enterprise Gridが必要


# 参考文献
- Microsoft
    - [Tokenの取得方法](https://www.softbanktech.co.jp/special/blog/cloud_blog/2020/0079/)
    - [APIリファレンス](https://docs.microsoft.com/ja-jp/graph/api/user-post-users?view=graph-rest-1.0&tabs=http)
