# Google Earth 地区代表点の根拠

国土地理院の住所検索（2026-09-24取得）。APIの応答は経度・緯度の順。台本・Google Earth指示は緯度・経度の順に記載。

| 地区 | 住所検索の応答 | Google Earth入力 | 代表点の地形標高 |
|:--|:--|:--|--:|
| せたな町北檜山区新成 | `139.794357, 42.332954` | `42.332954, 139.794357` | 280m |
| せたな町大成区太田 | `139.802475, 42.280846` | `42.280846, 139.802475` | 223.4m |
| 今金町金原 | `139.970032, 42.372704` | `42.372704, 139.970032` | 94.6m |

住所検索: https://msearch.gsi.go.jp/address-search/AddressSearch?q=北海道せたな町北檜山区新成 ／ https://msearch.gsi.go.jp/address-search/AddressSearch?q=北海道せたな町大成区太田 ／ https://msearch.gsi.go.jp/address-search/AddressSearch?q=北海道今金町金原

標高API: `https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php?lon=<経度>&lat=<緯度>&outtype=JSON`。3点とも `hsrc` は「1m（レーザ）」で応答。

上記は地区の代表点で、2013年・2014年の事故地点、2014年の捕獲地点、捜索区域中心の確定座標ではない。資料の「約8km」「約16km」を代表点間の計測値として扱わない。カメラの中心・高度・俯角は演出用の値で、現場の地形標高を意味しない。

Google Earthのオンライン動画利用条件: https://about.google/brand-resource-center/products-and-services/geo-guidelines/ 。教育・ドキュメンタリー用途のオンライン動画は、収益化されていても掲載条件の範囲で利用できる。表示中は Google Earth と画像提供元のクレジットを残す。
