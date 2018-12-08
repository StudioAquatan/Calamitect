# bosite
災害知見共有サイト

## 実行
### 環境
- python 3.6.x
- pipenv 2018.7.1

### 実行方法
```bash
cd bosite
# 依存パッケージのインストール
pipenv install
# env_filesディレクトリ内に.envファイルを作成，編集
vi env_files
# マイグレーションを行い実行
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```
`http://127.0.0.1:8000/poll`に接続する

## LICENSE
MIT License (c) 2018 StudioAquatan