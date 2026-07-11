#ifndef __SF01_CONTRACT_VERSION_MQH__
#define __SF01_CONTRACT_VERSION_MQH__

#define SF01_CONTRACT_KERNEL_MAJOR 1
#define SF01_CONTRACT_KERNEL_MINOR 0
#define SF01_CONTRACT_KERNEL_PATCH 0
#define SF01_CONTRACT_KERNEL_NAME  "strategy_factory_contracts"

string SF01_ContractKernelVersion()
{
   return IntegerToString(SF01_CONTRACT_KERNEL_MAJOR) + "." +
          IntegerToString(SF01_CONTRACT_KERNEL_MINOR) + "." +
          IntegerToString(SF01_CONTRACT_KERNEL_PATCH);
}

#endif
