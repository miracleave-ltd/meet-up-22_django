# Pytest エラーの修正 -問題-

前のページの内容を踏まえて、簡単な問題を用意しました。<br>
まずは、実際に発生するエラーを修正してみましょう。
以下のコマンドを実行して下さい。

```sh
docker-compose exec web pytest
```

実行すると、現在以下の内容がターミナルに出力されていると思います。

>3 failed, 4 passe

こちらのエラーは、7件のテストのうち３件が失敗し、4件が成功しているという意味になります。<br>
発生しているエラー内容については以下でも補足しています。補足内容も参考にしつつ、7件のテストを成功させてみましょう。

## 問題
### Question１
- 対象ファイル：`app/product/test/crud_test.py`<br>
- 対象関数：`test_create`<br>
- テスト内容：1件のデータを登録し、登録したデータが1件であることを確認しています。<br>
- エラー内容：期待しているデータ件数が取得したデータ件数と一致していない。（期待値の設定箇所`expected`）

```sh
cursor = <sqlite3.Cursor object at 0x7f2f585ec340>

    def test_create(cursor):
        insert_query = "insert into product_product values('99','テストプラン','これはテストプランです', '99999', '2021-08-18','2021-08-19','createuser','updateuser');"
        cursor.execute(insert_query)

        # 件数確認
        counts_query = "select count(1) from product_product where code = 99;"
        cursor.execute(counts_query)
        result = cursor.fetchone()[0]
        # 1件のデータを入れたため1件の結果を想定
        expected = 2

        print("result:{}".format(result))
        print("expected:{}".format(expected))
>       assert result == expected
E       assert 1 == 2

app/product/test/crud_test.py:18: AssertionError
```

### Question2
- 対象ファイル：`app/product/test/crud_test.py`<br>
- 対象関数：`test_update`<br>
- テスト内容：登録したデータの「name」を「`テストプラン`から`test99`」へ更新しています。期待している値`test99`と比較し、取得できた値が等しいことを確認します。<br>
- エラー内容：テスト内容は「期待値と取得値が等しいこと」を確認したいが、エラーが発生している箇所の構文は「期待値と取得値が等しくないこと」という条件になっている。

```sh
cursor = <sqlite3.Cursor object at 0x7fc8a6e5ed50>

    def test_update(cursor):
        insert_query = "insert into product_product values('99','テストプラン','これはテストプランです', '99999', '2021-08-18','2021-08-19','createuser','updateuser');"

        cursor.execute(insert_query)
        update_query = "update product_product set name = 'test99' where code = 99;"
        cursor.execute(update_query)
    
        select_query = "select name from product_product where code = 99;"
        cursor.execute(select_query)
        result = cursor.fetchone()[0]

        expected =  'test99'
    
        print("result:{}".format(result))
        print("expected:{}".format(expected))
>       assert result != expected
E       AssertionError: assert 'test99' != 'test99'

app/product/test/crud_test.py:58: AssertionError
```

### Question3
- 対象ファイル：`app/product/test/views_test.py`<br>
- 対象関数：`test_render_views`<br>
- テスト内容：リクエストを受けた`url`に対して、表示させる`template_name`が正しいことを確認し、正常なステータスコード(`status_code=200`)を返すことを確認しています。<br>
- エラー内容：リクエストを受けた`url`に対して、正しいテンプレートが選択されていない。(`app/product/urls.py`をみてみましょう。以下にも記載しています。)<br>
**Tips!!!**<br>
- `@pytest.mark.django_db`：このデコデータを使用する事で、Djangoのテスト用DBを作成し、使用することができます。<br>
- `@pytest.mark.parametrize`：パラメータに設定している引数を、テスト関数に順番に渡してくれます。<br>


```sh
client = <django.test.client.Client object at 0x7f2f586bff10>, param = {'temp_name': 'product:product_create', 'url': '/product/search/'}, get_model = <Product: Product object (1)>

    @pytest.mark.django_db
    @pytest.mark.parametrize('param', [
        {'temp_name': 'product:product_create', 'url': '/product/search/'},
        {'temp_name': 'product:product_detail', 'url': '/product/detail/1'},
        {'temp_name': 'product:product_create', 'url': '/product/create/'},
        {'temp_name': 'product:product_update', 'url': '/product/update/1/'}
    ])
    def test_render_views(client, param, get_model):
    
        if param['temp_name'] == 'product:product_detail' or \
                param['temp_name'] == 'product:product_update':
            temp_url = urls.reverse(param['temp_name'], args=(1,))
        else:
            temp_url = urls.reverse(param['temp_name'])
    
        print("result:{}".format(temp_url))
        print("expected:{}".format(param['url']))
        # 正しいテンプレートを使用しているかテスト
>       assert temp_url == param['url']
E       AssertionError: assert '/product/create/' == '/product/search/'
E         - /product/search/
E         ?          ^  ^^^
E         + /product/create/
E         ?          ^^  ^^

app/product/test/views_test.py:40: AssertionError
```

> app/product/urls.py

```python
app_name = 'product'

urlpatterns = [
    path('', TemplateView.as_view(template_name='product/product_top.html'), name='top'),
    path('search/', ProductSearchListView.as_view(), name='product_search'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('create/', CreateProductView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
]
```
