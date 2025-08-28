# PLATEAU2VISSIM-via-Unity

国土交通省が主導するプロジェクト[PLATEAU](https://www.mlit.go.jp/plateau/)により整備、オープンデータ化されている3D都市モデルを、PTV Groupが開発・販売しているミクロ交通シミュレーター[PTV Vissim](https://www.ptvgroup.com/ja/%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/%E8%A3%BD%E5%93%81/ptv-vissim/)にインポート可能なWavefront OBJ (.obj) 形式に自動で変換し、変換された3D都市モデルをVissim座標系の正しい座標にインポートします。

本ツールは、公式に配布されている[PLATEAU SDK for Unity](https://project-plateau.github.io/PLATEAU-SDK-for-Unity/index.html)というツールを改変し活用しています。
※PLATEAU SDK for UnityはPLATEAUをUnityで活用するためのオープンソースのツールキットであり、3D都市モデルをFBX、OBJ、GlTFデータへの変換・エクスポートができます。<br />
また国土地理院の基盤地図情報を元に標高付きの道路ネットワークを作成する手順についても言及します。

## ファイル構成
```txt
root
　├ **dem_***_op.gml_map
　├ ***bldg_**_appearance
　├ **_dem_***_LOD1.obj
　├ **_dem_***_LOD1.mtl
　├ ***bldg_**_LOD0.obj
　├ ***bldg_**_LOD0.mtl
　├ ***bldg_**_LOD1.obj
　├ ***bldg_**_LOD1.mtl
　├ ***bldg_**_LOD2.obj
　├ ***bldg_**_LOD2.mtl
　├ Importer.py
　├ **.inpx
　└ **.layx
```  
#### Importer.py：
　Vissimから呼び出すPythonファイル。INPXファイルの基準点を取得し、3D都市モデルの緯度・経度をVissim座標に変換。Unityから生成されたOBJファイルを一括でVissimにインポート。  

#### Unityから出力されるフォルダ/ファイル
　dem, bldg等の名前が付いたフォルダ/ファイルは全てUnityから出力されるファイル。

## 使い方  
### Unity及びPLATEAU SDK for Unityのインストール
公式サイト[PLATEAU SDK for Unity](https://project-plateau.github.io/PLATEAU-SDK-for-Unity/index.html)を参考にインストールを行う。<br />
推奨バージョン：
- PLATEAU SDK for Unity v3.1.1 alpha
- Unity 2022.3.25f1

#### インストールしたSDKのコードを修正
Vissimの座標系に合わせて、XZの符号を反転させるようにコードを編集する。<br />
Packages > PLATEAU SDK for Unity > Runtime > CityExport > ModelConvert > SubMeshConvert > UnityMeshToDllModelConverter.cs を開く。<br />
![image](https://github.com/user-attachments/assets/a7c6a1a1-cd19-44b6-90b5-6e704b88bc50)
node.LocalScaleとconvertedEulerの2行をコメントアウトして、下記を追記して保存する。 <br />
```csharp
//node.LocalScale = vertexConverter.ConvertOnlyCoordinateSystem(trans.localScale).ToPlateauVector() *
//                  vertexConverter.ConvertOnlyCoordinateSystem(Vector3.one).ToPlateauVector();
node.LocalScale = vertexConverter.ConvertOnlyCoordinateSystem(trans.localScale).ToPlateauVector() *
                  vertexConverter.ConvertOnlyCoordinateSystem(new Vector3(-1,1,-1)).ToPlateauVector();
```
```csharp
//convertedEuler *= -1;
convertedEuler *= 1;
```

あるいはSDKのバージョンが同じであれば、本Git Hubから公開されているcsファイルに差し替えてもよい。

### 3D都市モデルのインポート
公式サイトを参考に作業を行う。その際にモデル結合は地域単位にするとデータがまとまるため軽量になる。<br />
![image](https://github.com/user-attachments/assets/ec3ab9f7-8605-4684-8eef-56497c97f407) <br />
道路、災害リスク、都市計画決定情報、土地利用は利用しないので、チェックを外す。<br />
![image](https://github.com/user-attachments/assets/28c8e11c-72c3-43b7-a520-55c3e44b3e24) 

インポートに成功すると、建築物がbldgオブジェクトとして、土地起伏がdemオブジェクトとしてインポートされる。<br />
![image](https://github.com/user-attachments/assets/764bfd59-66f5-4cdd-87eb-93d3a558ce0d)

### 3D都市モデルのエクスポート
公式サイトを参考に作業を行う。その際に下記オプションを設定する。
- 出力形式：OBJ
- 座標変換：ローカル
- 座標軸：ＷＵＮ（右手座標系,Y軸が上,Ｚ軸が北）
![image](https://github.com/user-attachments/assets/a9051af3-6b86-439e-8271-085c0e860969)

### Vissimへのインポート
Vissimのファイル（inpx/layx）及びImporter.pyを先ほどエクスポートした3D都市モデルのファイルがあるディレクトリに配置する。<br />
Unity上でインポートした3D都市モデル（本例ではHiroshima）を選択すると、インスペクターウィンドウにモデルの緯度・経度が表示されるので、Importer.pyをテキストエディタ等で開き、緯度・経度情報を書き換えて保存する。<br />
![image](https://github.com/user-attachments/assets/a77674bb-e6aa-44cb-92d4-6a1510d59d79)

Vissimを開き、メニューバーのActions > Run Script File　でImporter.pyを開く。インポートが完了すると、「インポートが完了しました」と表示される。<br />
※この時リンクを3D都市モデルの中心に作成して、道路ネットワークと3Dモデルの基準点をなるべく一致させておく。<br />
![image](https://github.com/user-attachments/assets/f527c091-ed1f-4416-adab-23e0d908afc5)　![image](https://github.com/user-attachments/assets/ffb9d2b1-7416-444b-ab55-bf7e3f23d8b8)

なお、建築物、土地起伏に標高が設定されているため、道路ネットワークに標高が設定されていないと道路が埋没してしまう。


## 標高・座標合わせについて
### 基盤地図情報 数値標高モデルを利用する場合（非推奨）
国土地理院の[基盤地図情報](https://fgd.gsi.go.jp/download/menu.php)にアクセスして、数値標高モデル「ファイル選択へ」をクリック。<br />
メッシュ番号や地図上でダウンロードしたい場所を選択リストに追加する。「ダウンロードファイル確認へ」をクリックして、数値標高モデルをダウンロードし、適当なフォルダに解凍する。<br />
![image](https://github.com/user-attachments/assets/7d1e808e-9abb-47ed-aadb-168fe1768f29)

#### GeoTiff形式への変換
株式会社エコリス様が公開している、[基盤地図情報 標高DEMデータ変換ツール](https://www.ecoris.co.jp/contents/demtool.html)を活用する。<br />
変換結合.vbsを起動し、下記設定で実行する。<br />
- 投影法：0
- 陰影起伏図：不要
- 海域の標高：0m（どちらでもよい）

作成されたmerge.tifファイルをVissimのファイルがある場所に移動させる。

### PLATEAU 地形データ（DEM）を利用する場合（推奨）
こちらの方が同じデータソースを利用するため、標高の誤差が少なくなるので現在はこちらを推奨。<br />
[PLATEAU QGIS Plugin](https://github.com/Project-PLATEAU/plateau-qgis-plugin/blob/main/docs/manual.md)を参考に、PLATEAU 地形モデルをメッシュとして読込み、メッシュをラスタライズする。<br />
ラスタライズの際に出力ラスタとしてファイル名を指定するとGeoTiff形式で保存される。<br />
作成されたtifファイルをVissimのファイルがある場所に移動させる。

### Vissimへの標高データのインポート
PTV Vissimを開き、リンクの編集モードで標高を設定したいリンクをすべて選択する。この状態で右クリック（またはCtrl + 右クリック）、Import height from GeoTiff datasource..を選択。
先程作成したmerge.tifを選択すると、リンクのZOffsetが自動で変更される。（ただし、あくまで地表高さのため橋や立体交差などは反映されないので注意）<br />
<img width="600" alt="import-height" src="https://github.com/user-attachments/assets/032751ce-b188-4c8f-a7f5-0bbfa8eab376" />

標高インポート後も3D都市モデルに道路が埋没している場合は、Static 3D ModelsのCoordZOffsetあるいは対応するLevelのzCoordを-1程度にすると、見栄えがよくなる。<br />
![image](https://github.com/user-attachments/assets/59a55c64-35f3-43ed-8352-be3f3c1147ed)　

### Unityと座標系を合わせる方法
Vissimの追加モジュールDriving Simulator Interface（DSI)を活用すれば、Unityとリアルタイム連携することができる。<br />
このときUnityとVissimで原点を一致させないと、下記画像のようにUnityが動かす車両の位置がVissim上でズレてしまう（逆も同様）。<br />
<img width="900" alt="Offset1" src="https://github.com/user-attachments/assets/493c5e68-a565-4528-83d4-92c67206a30e" />

Edit > Move Network - Adjust network coordinates and backgound mapで3Dモデルの座標を原点（0,0）となるように動かす。<br />
<img width="600" alt="Offset2" src="https://github.com/user-attachments/assets/f40a85c8-24ab-44f5-8a65-e1b105fb819d" />

これでVissimとUnityの原点が一致し、お互いの車両の位置が合致する。

## 動作環境  
- Unity 2022.3.25f1 / PLATEAU SDK for Unity v3.1.1 alpha / PLATEAU QGIS Plugin 0.1.0
- Python 3.11 + pywin32  
- PTV Vissim 2024 SP12 / 2025 SP08 <br />
  ※現在OBJファイルのインポートをPTV Vissimが公式にはサポートしていないため、今後の開発によっては仕様が変わり本ツールが利用できなくなる可能性があります。予めご了承ください。  

## ライセンス  
- 本ツールは、MITライセンスに従います。
- [Unity](https://unity.com/ja)は、Unity Technologies社の製品です。利用料金はUnity社にお問合せください。
- [PLATEAU SDK for Unity](https://project-plateau.github.io/PLATEAU-SDK-for-Unity/index.html)の著作権は国土交通省に帰属します。
- [PLATEAU QGIS Plugin](https://github.com/Project-PLATEAU/plateau-qgis-plugin/tree/main)の著作権は国土交通省に帰属します。
- [基盤地図情報 標高DEMデータ変換ツール](https://www.ecoris.co.jp/contents/demtool.html)の著作権は株式会社エコリスに帰属します。
- [PTV Vissim](https://www.ptvgroup.com/ja/%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/%E8%A3%BD%E5%93%81/ptv-vissim/)は、PTV Groupの販売する有償のソフトウェアです。[こちら](https://www.ptvgroup.com/ja/%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/%E8%A3%BD%E5%93%81/ptv-vissim/%E3%82%B3%E3%83%B3%E3%82%BF%E3%82%AF%E3%83%88/)からお問合せください。

