## 単語帳

##### テーマ

- 「自分の言葉で単語帳を作成し、辞書のように検索できるようなツール」

- 「語句をテーマ別に整理しながら覚える手助け」
- 「いつでもどこでもできる勉強をスタートする障壁を0に(将来的に)」



##### 現在の機能

- 「csvを読み込んで単語帳のリストをGUI表示」
  - 単語帳(csv)を選択してスタート(未実装)
  - デバッグ用として「デモ用単語帳のみ」(7/13現在こちらのみ)
  - 機能差分はcsvを選択するか、だけ
  - 「単語帳(Wordbook)」
    - 単語(Word)の集まり
  - 単語(Word)
    - ID、単語、読み、ジャンル、タグ、意味、復習フラグ(気が向いたら追加)
    - タグだけリスト形式(スペースで区切る)
- 「検索」ボタン
  - 単語、読み、ジャンル、タグ、が対象
- 「詳細表示」
  - リストの単語ダブルクリック
  - 別ウインドウ単語の詳細表示
  - 更新と削除もできる
- 「新規単語登録」(見た目整える！)
  - csv最後尾に追加
  - IDは欠番(削除による)があれば若い順に埋めて、欠番なければ最後尾に自動割り当て
  - 登録(または削除)をした後は「更新」ボタンの必要あり(気が向いたら改善したい)



###### 今後やりたい

- 単語テスト機能
  - 単語にまつわる4択くらいの問題を作成
  - 選択
  - 実装：DB正規化的な観点から出題のcsvごと別に作る？
    - メリット：一行一問になるので一単語に複数の問題が作りやすい、単語側を削除したとしても問題が残せる(状況によってはデメリット？)
    - デメリット：二つのcsvの整合性をとるのが若干面倒(主キーである「ID」を一致させるがベストだけど、「単語」を外部キーとするの方がバグが少なそう)



- データのクラウドバックアップ
  - S3に保存する実装はうまくいった(コメントアウト済)のでいつでも可能(デバッグ中にわざわざ保存する必要はないかな)



##### 将来やりたい(勉強が必要)

- 単語テスト機能の穴埋め部分の自動生成
  - 機械学習で「意味」の文章から特徴的な部分を抽出して…みたいな
  - これができたらむしろメイン機能



- WebアプリまたはiPhoneアプリとして展開
  - 携帯で触れていつでも勉強できてこそ意味がある