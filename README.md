# analyze

複数の解析コードを追加できる、再現性を重視したPython解析基盤です。
Python 3.12以上を対象とし、標準環境は `.python-version` のPython 3.12です。
現時点では解析アルゴリズムや実データは含みません。

## セットアップ

[uv](https://docs.astral.sh/uv/getting-started/installation/) をインストールした後、実行します。

```bash
git clone https://github.com/ttoommyya/analyze.git
cd analyze
uv python install
uv sync --locked
uv run --locked python -m analyze --version
```

`uv sync` は `.venv/` を作成し、パッケージをeditable形式でインストールします。
`uv.lock` を追跡し、ローカルとCIで同じ依存関係を使用します。

## 構成

```text
pyproject.toml             パッケージ・開発ツール設定
uv.lock                    固定した依存関係
.python-version            標準Pythonバージョン
src/analyze/               共通のパッケージ名前空間
tests/                     人工データによるテスト
configs/                   解析ごとのTOML設定
data/README.md             データ配置・管理方針
.github/workflows/ci.yml   lint・format・pytest
```

## チェック

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest
```

pushとPull requestで同じチェックをGitHub Actionsが実行します。
コードを整形する場合は `uv run --locked ruff format .` を使用してください。

## 解析モジュールの追加

1. `src/analyze/<module>/` に `__init__.py` と解析コードを配置する。
2. 実行用の `__main__.py` を追加し、例えば `python -m analyze.<module>` で実行する。
3. `configs/<module>.toml` に条件を保存し、モジュール側で明示的に読み込み・検証する。
   例として `configs/example.toml` を参照する。相対パスはリポジトリ直下基準とする。
4. 計算処理とファイル入出力を分離し、`tests/test_<module>.py` で人工データを検証する。
5. 結果は `outputs/<module>/<run-id>/` に書き出し、実行方法をREADMEに追記する。

新しい依存関係は `uv add <package>`、開発用は `uv add --dev <package>` で追加します。
`pyproject.toml` と `uv.lock` を同じコミットに含め、チェックを再実行してください。
共通処理は再利用が必要になった時点で `src/analyze/` 内の共通モジュールへ移します。

## 再現性ルール

- 生データを変更せず、前処理と解析をコードに残す。
- 乱数を使う解析ではseedを設定ファイルから受け取り、使用する各ライブラリに設定する。
  並列処理やGPU等で非決定的な処理がある場合は、その条件を記録する。
- 実行ごとにGitコミットSHA、未コミット変更の有無、実行コマンド、設定のコピー、
  Python・依存関係のバージョン、OS、入力ファイルのSHA-256を出力先に記録する。
- 図・表の元データと生成コードを対応づけ、手作業の修正も記録する。
- 設定とコードはGit、データと結果は別の管理先で保存する。

## 誤コミットの防止

`data/` はREADMEのみ追跡します。`outputs/`、`results/`、`figures/`、`reports/`、
仮想環境、キャッシュ、主要な実験データ形式、秘密情報・ローカル設定は除外します。
生成物は必ず上記の出力ディレクトリに保存してください。

コミット前に `git status --short` と `git diff --cached --stat` で追加対象を確認します。
除外理由は `git check-ignore -v <path>` で確認できます。
`.gitignore` は既に追跡されたファイルや `git add -f` を防ぎません。
新しいデータ形式を使う場合は除外設定を追加してください。
