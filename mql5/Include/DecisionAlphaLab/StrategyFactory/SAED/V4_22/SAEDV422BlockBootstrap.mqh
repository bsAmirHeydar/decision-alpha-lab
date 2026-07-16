#ifndef SAEDV422_BLOCK_BOOTSTRAP_MQH
#define SAEDV422_BLOCK_BOOTSTRAP_MQH
int SAEDV422BlockSourceIndex(const int seed,const int block,const int count){if(count<=0)return -1;return (seed+block*7919)%count;}
#endif
