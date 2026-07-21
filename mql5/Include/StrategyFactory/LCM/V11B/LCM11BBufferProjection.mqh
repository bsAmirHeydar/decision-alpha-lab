#ifndef __LCM11B_BUFFER_PROJECTION_MQH__
#define __LCM11B_BUFFER_PROJECTION_MQH__
class CLCM11BBufferProjection
  {
public:
   bool Bind(const int index,double &buffer[],const ENUM_INDEXBUFFER_TYPE type=INDICATOR_DATA)
     {
      ArraySetAsSeries(buffer,true);return SetIndexBuffer(index,buffer,type);
     }
   void FillEmpty(double &buffer[],const int begin,const int count,const double empty_value=EMPTY_VALUE)
     {
      int end=MathMin(ArraySize(buffer),begin+count);for(int i=MathMax(0,begin);i<end;i++)buffer[i]=empty_value;
     }
  };
#endif
