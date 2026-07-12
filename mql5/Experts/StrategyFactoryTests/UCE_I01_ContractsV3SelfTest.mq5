#property strict
#include <AlphaLab/StrategyFactory/Contracts/UCE03_AllContracts.mqh>

int g_passed=0;
int g_failed=0;

void Check(const bool condition,const string name)
{
   if(condition)
   {
      g_passed++;
      Print("PASS | ",name);
   }
   else
   {
      g_failed++;
      Print("FAIL | ",name);
   }
}

void TestCanonicalCodec()
{
   CUCE03CanonicalObject value;
   value.AddLong("z",1);
   value.AddString("a","ASCII");
   value.AddString("escaped","line\nquote\"");
   Check(value.Serialize()=="{\"a\":\"ASCII\",\"escaped\":\"line\\nquote\\\"\",\"z\":1}",
         "canonical object ordering and escaping");
   Check(UCE03_CanonicalScaledInteger(1234567,5)=="12.34567","fixed-scale number");
   Check(UCE03_CanonicalScaledInteger(0,4)=="0.0000","zero normalization contract");
}

void TestIdentityVector()
{
   CUCE03CanonicalObject dimensions;
   dimensions.AddLong("confirmation_time_ms",1783800000000);
   dimensions.AddString("direction","long");
   dimensions.AddString("primary_symbol","US100");
   dimensions.AddString("reference_symbol","US500");
   dimensions.AddString("source_event_id","EXP0017_EVT_000042");

   UCE03_IdentityKey key;
   key.kind=UCE03_ID_CONTEXT_OCCURRENCE;
   key.semantic_namespace="exp0017.cycle_divergence";
   key.semantic_version="1.0.0";
   key.owner_id="exp0017";
   key.dimensions_json=dimensions.Serialize();

   string error="";
   Check(UCE03_ValidateIdentityKey(key,error),"identity validates");
   Check(UCE03_IdentityCanonicalMaterial(key)==
         "{\"contract_release\":\"3.0.0\",\"dimensions\":{\"confirmation_time_ms\":1783800000000,\"direction\":\"long\",\"primary_symbol\":\"US100\",\"reference_symbol\":\"US500\",\"source_event_id\":\"EXP0017_EVT_000042\"},\"kind\":\"context_occurrence\",\"owner_id\":\"exp0017\",\"semantic_namespace\":\"exp0017.cycle_divergence\",\"semantic_version\":\"1.0.0\"}",
         "identity canonical material parity");
   Check(UCE03_StableIdentity(key)=="uce3_context_occurrence_06893bba7f56fb57",
         "Python/MQL5 golden identity parity");
}

void TestKnownTime()
{
   UCE03_KnownTimeChain chain;
   chain.event_time=UCE03_MakeUtcInstant(1783799940000,"market_event");
   chain.known_time=UCE03_MakeUtcInstant(1783800000000,"bar_close");
   chain.confirmation_time=UCE03_MakeUtcInstant(1783800000000,"bar_close");
   chain.observation_cut=UCE03_MakeUtcInstant(1783800000000,"feature_cut");
   chain.decision_time=UCE03_MakeUtcInstant(1783800000001,"decision");
   chain.has_action_time=true;
   chain.action_time=UCE03_MakeUtcInstant(1783800000002,"execution");
   chain.has_fill_time=true;
   chain.fill_time=UCE03_MakeUtcInstant(1783800000010,"broker");
   chain.has_label_maturity_time=true;
   chain.label_maturity_time=UCE03_MakeUtcInstant(1783886400000,"label_engine");

   string error="";
   Check(UCE03_ValidateKnownTimeChain(chain,error),"known-time chain validates");
   Check(!UCE03_FeatureKnownByCut(chain,1783800000001),"future feature rejected");
   chain.known_time.epoch_ms=1783799939999;
   Check(!UCE03_ValidateKnownTimeChain(chain,error),"reversed known-time rejected");
}

void TestExactSchemaRegistry()
{
   CUCE03SchemaRegistry registry;
   UCE03_SchemaDescriptor descriptor;
   descriptor.schema_id=UCE03_MakeSchemaId("alpha_lab.ucee","identity_key",3,0,0);
   descriptor.semantic_owner="strategy_factory_contracts";
   descriptor.semantic_hash_sha256="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
   descriptor.required_fields_csv="kind,semantic_namespace,semantic_version,owner_id,dimensions";
   descriptor.optional_fields_csv="";

   string error="";
   Check(registry.Register(descriptor,error),"schema registers");
   UCE03_SchemaDescriptor resolved;
   Check(registry.ResolveExact(descriptor.schema_id,resolved),"exact schema resolves");
   Check(!registry.SupportsMajor("alpha_lab.ucee","identity_key",4),"future major rejected");
}

int OnInit()
{
   TestCanonicalCodec();
   TestIdentityVector();
   TestKnownTime();
   TestExactSchemaRegistry();
   Print("UCE-I01 SELF TEST | passed=",g_passed," failed=",g_failed);
   return g_failed==0 ? INIT_SUCCEEDED : INIT_FAILED;
}

void OnTick(){}
