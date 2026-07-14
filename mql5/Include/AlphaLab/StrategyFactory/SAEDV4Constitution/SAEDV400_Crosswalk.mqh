#ifndef __ALPHALAB_SAEDV400_CROSSWALK_MQH__
#define __ALPHALAB_SAEDV400_CROSSWALK_MQH__

class CSAEDV400Crosswalk
  {
public:
   static bool MutationAllowed(const string ucee_phase)
     {
      // SAED consumes UCEE I01-I18 artifacts read-only. Any phase returns false.
      return(false);
     }
   static string AuthorityOwner(const string ucee_phase)
     {
      return("UCEE");
     }
  };

#endif
