from playground import catalogue, pipeline


def test_pipeline_finds_every_requested_product():
    products = catalogue.build_catalogue(300)
    stats = pipeline.run_pipeline(products, list(range(100)))
    assert stats["found_count"] == 100
    assert stats["categories_ranked"] == 5
    assert stats["report_length"] > 0
    assert stats["average_price"] > 0


def test_price_band_boundaries():
    assert pipeline.price_band({"price": 99.0}) == "cheap"
    assert pipeline.price_band({"price": 100.0}) == "mid"
    assert pipeline.price_band({"price": 5000.0}) == "premium"
