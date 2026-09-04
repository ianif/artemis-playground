from playground import report


def test_price_is_formatted_to_two_decimals():
    assert report.format_price(3.5) == "3.50"


def test_report_contains_a_line_per_product():
    products = [
        {"name": "a", "category": "phones", "price": 1.0},
        {"name": "b", "category": "phones", "price": 2.0},
    ]
    text = report.build_report(products)
    assert "PRODUCT REPORT" in text
    assert "Total products: 2" in text
    assert "a | phones | 1.00" in text


def test_summary_counts_successes():
    products = [{"name": "a"}, {"name": "b"}, {"name": "c"}]
    assert report.summarise(products, occured_errors=1) == "processed 3 products, 2 succesful"
