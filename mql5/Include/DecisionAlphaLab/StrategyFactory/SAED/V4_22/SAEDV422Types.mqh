#ifndef SAEDV422_TYPES_MQH
#define SAEDV422_TYPES_MQH
struct SAEDV422PathPoint { datetime timestamp; double open; double high; double low; double close; double bid; double ask; double volume; double liquidity; string regime; };
struct SAEDV422Authority { bool decision; bool execution; bool promotion; bool production; bool risk_allocation; bool runtime; };
#endif
