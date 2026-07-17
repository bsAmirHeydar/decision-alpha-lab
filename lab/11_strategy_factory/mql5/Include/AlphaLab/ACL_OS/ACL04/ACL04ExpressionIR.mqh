#ifndef AL_ACL04_EXPRESSION_IR_MQH
#define AL_ACL04_EXPRESSION_IR_MQH

enum ENUM_AL_ACL04_EXPRESSION_OP
  {
   AL_ACL04_EXPR_ATOM=0,
   AL_ACL04_EXPR_ALL=1,
   AL_ACL04_EXPR_ANY=2,
   AL_ACL04_EXPR_NOT=3
  };

struct AL_ACL04_ExpressionNode
  {
   ENUM_AL_ACL04_EXPRESSION_OP op;
   string atom_id;
   string serialized_arguments;
   int    first_child_index;
   int    child_count;
   int    depth;
  };

bool AL_ACL04_ExpressionNodeWithinBudget(const AL_ACL04_ExpressionNode &node,const int max_depth)
  {
   return(node.depth>=0 && node.depth<=max_depth && node.child_count>=0);
  }

#endif
