# Pytest エラーの修正 -回答-

こちらはエラー修正箇所の回答になります。<br>
以下のコードを既存の箇所と置き換えるとすべてのテストがパス（成功）するようになります。

すべて修正できたら、以下のコマンドを実行します。
```sh
docker-compose exec web pytest
```

修正箇所がすべて解消できていれば、現在以下の内容がターミナルに出力されていると思います。
>7 passed

## 回答
### Question１
- 修正内容：期待値としている箇所 `expected` では2件となっていたため、期待値が1件となるように `expected = 1` と修正する。
```python
def test_create(cursor):
    insert_query = "insert into product_product values('99','テストプラン','これはテストプランです', '99999', '2021-08-18','2021-08-19','createuser','updateuser');"
    cursor.execute(insert_query)

    # 件数確認
    counts_query = "select count(1) from product_product;"
    cursor.execute(counts_query)
    result = cursor.fetchone()[0]
    # 1件のデータを入れたため1件の結果を想定
    expected = 1 # 修正箇所

    print("result:{}".format(result))
    print("expected:{}".format(expected))
    assert result == expected
```

### Question2
- 修正内容：構文が誤っていたため、「期待値と取得値が等しいこと」となるように、`assert result == expected` と修正する。
```python
def test_update(cursor):
    # 1件のデータを挿入
    insert_query = "insert into product_product values('99','テストプラン','これはテストプランです', '99999', '2021-08-18','2021-08-19','createuser','updateuser');"
    cursor.execute(insert_query)
    # code=99のnameをtest99に変更する
    update_query = "update product_product set name = 'test99' where code = 99;"
    cursor.execute(update_query)

    # データ取得
    select_query = "select name from product_product where code = 99;"
    cursor.execute(select_query)
    result = cursor.fetchone()[0]

    expected = 'test99' # code=99のnameがtest99になっていることを確認

    print("result:{}".format(result))
    print("expected:{}".format(expected))
    assert result == expected # 修正箇所
```

### Question3
- 修正内容： urls.pyから、 `/product/search/` のリクエストに対応する テンプレートは `product_search` のため、 `{'temp_name': 'product:product_search', 'url': '/product/search/'},` となるように修正する。
```python
@pytest.mark.django_db
@pytest.mark.parametrize('param', [
    {'temp_name': 'product:product_search', 'url': '/product/search/'},　#　修正箇所
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
    assert temp_url == param['url']

    response = client.get(temp_url)

    print("result:{}".format(response.status_code))
    print("expected:{}".format(200))
    # 正しいステータスコードかをテスト
    assert response.status_code == 200
```
