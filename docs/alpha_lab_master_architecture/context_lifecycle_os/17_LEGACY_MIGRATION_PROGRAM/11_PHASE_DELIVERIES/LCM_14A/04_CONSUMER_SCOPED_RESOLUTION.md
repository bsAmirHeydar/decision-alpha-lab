# Consumer-Scoped Resolution

Some legacy locators represent several extracted canonical surfaces. Resolution therefore uses `(legacy_locator, consumer_id)` as the exact key. An unscoped request for an ambiguous locator fails closed instead of selecting an arbitrary successor.
