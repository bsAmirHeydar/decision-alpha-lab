from tools.strategy_factory.lcm.lcm_10b.translation import translate_legacy_request
def test_alias_translation_is_strict(sample_package):
 i=translate_legacy_request(sample_package,{"decision_id":"D5","direction":"SELL","ticker":"XAUUSD","entry":{"kind":"MARKET"},"lots":"0.01"});assert i["side"]=="SELL" and i["symbol"]=="XAUUSD"
def test_unknown_field_blocks(sample_package):
 i=translate_legacy_request(sample_package,{"decision_id":"D6","side":"BUY","symbol":"EURUSD","entry":{"kind":"MARKET"},"enable_live":True});assert i["validation_status"]=="BLOCKED" and "UNTRANSLATABLE_LEGACY_FIELDS" in i["rejection_reasons"]
