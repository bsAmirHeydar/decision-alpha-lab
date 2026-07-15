from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[3];S=ROOT/'lab/11_strategy_factory/schemas/saed_v4_07';E=ROOT/'lab/11_strategy_factory/examples/saed_v4_07'
cat=json.loads((E/'schema_catalog.json').read_text());schemas=list(S.glob('*.schema.json'))
if len(schemas)<28:raise SystemExit('insufficient V4-07 schemas')
for p in schemas:
 x=json.loads(p.read_text());Draft202012Validator.check_schema(x)
 if x.get('additionalProperties') is not False:raise SystemExit(f'top-level schema open: {p}')
for row in cat['schemas']:
 if not row.get('example'):continue
 doc=json.loads((ROOT/row['example']).read_text());sch=json.loads((ROOT/row['path']).read_text());errors=list(Draft202012Validator(sch).iter_errors(doc))
 if errors:raise SystemExit(f"{row['name']}: {errors[0].message}")
print(f'validated {len(schemas)} closed schemas and {sum(bool(x.get("example")) for x in cat["schemas"])} examples')
