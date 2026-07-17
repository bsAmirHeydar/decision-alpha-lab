#ifndef AL_ACL04_STATIC_BOUNDARY_MQH
#define AL_ACL04_STATIC_BOUNDARY_MQH

bool AL_ACL04_IsReferenceDefinitionBoundary()
  {
   return(true);
  }

bool AL_ACL04_MaySubmitLiveOrders()
  {
   return(false);
  }

bool AL_ACL04_MayActivateCapital()
  {
   return(false);
  }

bool AL_ACL04_MayRewriteACL03ContextSemantics()
  {
   return(false);
  }

#endif
