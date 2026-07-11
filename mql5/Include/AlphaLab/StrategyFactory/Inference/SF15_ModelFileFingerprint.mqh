#ifndef __SF15_MODEL_FILE_FINGERPRINT_MQH__
#define __SF15_MODEL_FILE_FINGERPRINT_MQH__
#include "SF15_Hashing.mqh"
bool SF15_ReadModelFingerprint(const string relative_path,const bool common_folder,long &size_bytes,string &fnv_hex,string &error)
  {
   int flags=FILE_READ|FILE_BIN; if(common_folder)flags|=FILE_COMMON;
   int handle=FileOpen(relative_path,flags);if(handle==INVALID_HANDLE){error="model file open failed: "+IntegerToString(GetLastError());return false;}
   long size=FileSize(handle);if(size<1||size>2147483647){FileClose(handle);error="model file size outside bound";return false;}
   uchar data[];ArrayResize(data,(int)size);int read=FileReadArray(handle,data,0,(int)size);FileClose(handle);
   if(read!=(int)size){error="model file read was incomplete";return false;}size_bytes=size;fnv_hex=SF15_Fnv1aBytes(data);error="";return true;
  }
#endif
