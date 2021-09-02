# アプリケーションコード修正（商品情報検索画面）
当手順では以下の赤枠部分の内、商品情報検索画面の画面レイアウトをwidget_tweaksプラグインを使用してスタイルを適用し綺麗にします。

![](./img/22.png)

## 当画面に関連するソースファイル

- app\product\filter\product_search_filter.py
- app\product\views\product_search_view.py
- app\product\urls.py
- templates\product\product_search.html **←修正対象**
- templates\product\component\product_field.html **←修正対象**


## Template（HTML）の修正
各フォーム項目表示用コンポーネントを作成し、作成したコンポーネントを検索画面に表示されるよう修正します。

>templates\product\component\product_field.html

```html
{% load widget_tweaks %}

<label for={{ field.id_for_label }} class="form-label">
    {% if label %}{{ label }}{% else %}{{ field.label }}{% endif %}
</label>

{% if field.errors %}
    {% render_field field class="form-control is-invalid" %}
{% else %}
    {% render_field field class="form-control" %}
{% endif %}

{% for err_msg in field.errors %}
    <div id="{{ field.id_for_label }}" class="invalid-feedback">{{ err_msg }}</div>
{% endfor %}
```


>templates\product\product_search.html - 15Line~

変更前

```html
    <div class="card-body">
        <div class="row">
            {{ filter.form.as_p }}
        </div>
    </div>
```

変更後

```html
    <div class="card-body">
        <div class="row">
            <div class="col-6">
                <div class="form-group">
                    {% include "product/component/product_field.html" with field=filter.form.code %}
                </div>
            </div>
            <div class="col-6">
                <div class="form-group">
                    {% include "product/component/product_field.html" with field=filter.form.name %}
                </div>
            </div>
        </div>
    </div>
```

- ポイント
  
  フォームなど、繰り返し出現する記載については上記のように別パーツ化をして

  includeタグで呼び出すことによりソースの記述量を減らすことが可能です。

  with xxxx=~~ と記載することで、インクルードするHTMLへパラメータを渡すことも出来ます。



## 画面確認
以下URLをブラウザにて入力し画面を表示します。

http://localhost:8000

商品情報検索ボタンを押下してみてください。

※ 最終差し替え予定 ※
![](./img/4.png)

検索画面が表示されレイアウトがイメージの通り変更されていれば成功です。

![](./img/5.png)


## データの登録
検索画面を表示することが出来ましたが、肝心のデータが0件の為、試しに1件データを登録します。

画面右上のDjango管理サイトというリンクを押下してください。

![](./img/14.png)

以下のような画面が表示される為、2ページ目の手順にて作成したスーパーユーザーの情報を入力しログインします。

![](./img/15.png)

管理サイトという画面が表示される為、Products、Imagesのリンクを押下しそれぞれデータを作成します。任意の値で問題ありません。なお、手頃な画像をお持ちで無い方はappフォルダと同階層にdataというフォルダを用意しておりますので、そちらに格納された画像を使用してください。

![](./img/16.png)

![](./img/17.png)

データ登録後、作成した検索画面にて検索を行うと、登録した商品情報が表示されることを確認できます。

![](./img/18.png)
