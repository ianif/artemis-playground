from playground.cache import SimpleCache


def test_stores_and_returns_a_value():
    cache = SimpleCache(capacity=2)
    cache.put("a", 1)
    assert cache.get("a") == 1


def test_missing_key_returns_none():
    assert SimpleCache().get("nope") is None


def test_evicts_the_least_recently_used_entry():
    cache = SimpleCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")          # "a" is now the most recently used
    cache.put("c", 3)       # so "b" should be dropped
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_size_never_exceeds_capacity():
    cache = SimpleCache(capacity=3)
    for i in range(10):
        cache.put(i, i)
    assert cache.size() == 3
