#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_TYPES_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_TYPES_MQH

enum ENUM_SAED_V4_DSL_PROGRAM_STATUS
  {
   SAED_V4_DSL_PROGRAM_ACCEPTED=0,
   SAED_V4_DSL_PROGRAM_REJECTED=1,
   SAED_V4_DSL_PROGRAM_QUARANTINED=2
  };

enum ENUM_SAED_V4_DSL_PRIMITIVE_KIND
  {
   SAED_V4_DSL_ACTION=0,
   SAED_V4_DSL_PAYOFF=1,
   SAED_V4_DSL_DIRECTION=2,
   SAED_V4_DSL_ENTRY=3,
   SAED_V4_DSL_TRIGGER=4,
   SAED_V4_DSL_STOP=5,
   SAED_V4_DSL_TARGET=6,
   SAED_V4_DSL_EXIT=7,
   SAED_V4_DSL_TRAIL=8,
   SAED_V4_DSL_MANAGEMENT=9,
   SAED_V4_DSL_TIME=10,
   SAED_V4_DSL_COST=11,
   SAED_V4_DSL_CAPABILITY=12
  };

struct SAEDV4DslAuthority
  {
   bool read_hypergraph;
   bool define_finite_dsl;
   bool validate_program;
   bool bind_external_descriptor;
   bool solve_action_lattice;
   bool select_treatment;
   bool allocate_risk;
   bool activate_runtime;
   bool send_order;
  };

struct SAEDV4DslProgramHeader
  {
   string program_id;
   string program_hash;
   string program_name;
   string exact_version;
   string evidence_role;
   string known_as_of;
   ENUM_SAED_V4_DSL_PROGRAM_STATUS status;
   int component_count;
   int constraint_count;
  };

struct SAEDV4DslBindingHeader
  {
   string binding_id;
   string binding_hash;
   string descriptor_id;
   string graph_node_id;
   string graph_node_hash;
   string program_id;
   string program_hash;
   bool bound;
  };

#endif
