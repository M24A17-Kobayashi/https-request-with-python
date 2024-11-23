#　回線速度分析ツール

[みんなのネット回線速度](https://minsoku.net/)から各都道府県の光回線のPing，ダウンロード速度，アップロード速度を取得，分析する．

* request.py
  * 各都道府県の光回線速度の投稿ページのhtmlをopt/data/html/に保存する．
* extract_data.py
  * htmlからPing，ダウンロード速度，アップロード速度と各都道府県のダウンロード速度が速い上位3社のプロバイダ名を抽出する．　/opt/data/csv/todouhukenk.csvに保存．
* analyze.py
  * /opt/data/csv/todouhukenk.csvから各データの最大値，最小値，平均値，分散，標準偏差，箱ひげ図を出力する．/opt/data/imageと/opt/data/csv/に保存