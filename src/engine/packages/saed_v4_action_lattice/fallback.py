MANDATORY_FALLBACK_CLASSES=('abstain','skip')
def has_mandatory_fallback(nodes:list[dict])->bool:
    classes={n['action_class'] for n in nodes};return all(x in classes for x in MANDATORY_FALLBACK_CLASSES)
