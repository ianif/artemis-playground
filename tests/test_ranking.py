from playground import catalogue, ranking


def test_top_rated_is_ordered_high_to_low():
    products = catalogue.build_catalogue(50)
    best = ranking.top_rated(products, 5)
    assert len(best) == 5
    ratings = [p["rating"] for p in best]
    assert ratings == sorted(ratings, reverse=True)


def test_cheapest_is_ordered_low_to_high():
    products = catalogue.build_catalogue(50)
    cheap = ranking.cheapest(products, 5)
    prices = [p["price"] for p in cheap]
    assert prices == sorted(prices)


def test_average_price_of_empty_catalogue_is_zero():
    assert ranking.average_price([]) == 0.0


def test_average_price():
    assert ranking.average_price([{"price": 10.0}, {"price": 20.0}]) == 15.0
