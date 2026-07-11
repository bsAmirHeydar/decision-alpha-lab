#ifndef __SF02_ASSERT_MQH__
#define __SF02_ASSERT_MQH__

class CSF02Assert
{
private:
   int m_passed;
   int m_failed;
public:
   CSF02Assert(void) { m_passed = 0; m_failed = 0; }
   void True(const bool condition, const string name)
   {
      if(condition) { m_passed++; Print("PASS: ", name); }
      else { m_failed++; Print("FAIL: ", name); }
   }
   int Passed(void) const { return m_passed; }
   int Failed(void) const { return m_failed; }
};

#endif
