from playground import catalogue, search


def test_finds_an_existing_product():
    products = catalogue.build_catalogue(100)
    found = search.find_product_by_id(products, 42)
    assert found is not None
    assert found["id"] == 42


def test_returns_none_for_a_missing_product():
    products = catalogue.build_catalogue(100)
    assert search.find_product_by_id(products, 9999) is None


def test_filters_by_category():
    products = catalogue.build_catalogue(100)
    laptops = search.find_products_by_category(products, "laptops")
    assert len(laptops) == 20
    assert all(p["category"] == "laptops" for p in laptops)


def test_counts_cheaper_products():
    products = [{"price": 10.0}, {"price": 50.0}, {"price": 500.0}]
    assert search.count_cheaper_than(products, 100.0) == 2
