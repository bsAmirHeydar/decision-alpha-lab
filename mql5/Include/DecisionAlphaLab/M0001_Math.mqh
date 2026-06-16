//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Math Utils                            |
//+------------------------------------------------------------------+

double DAL_LogMove(double high, double low)
{
   const double move = MathAbs(high - low);
   if(move <= 0.0)
      return 0.0;
   return MathLog(move);
}

bool DAL_InZone(double high, double low, double lower, double upper)
{
   return !(high < lower || low > upper);
}

void DAL_BuildTerritory(double node_price, double extreme, double zone_ratio, double &lower, double &upper)
{
   const double distance = MathAbs(extreme - node_price);
   const double half_width = distance * (1.0 - zone_ratio);
   lower = node_price - half_width;
   upper = node_price + half_width;
}

bool DAL_HuntBreached(int node_type, double node_price, double high, double low)
{
   if(node_type == DAL_NODE_LOW)
      return low < node_price;
   if(node_type == DAL_NODE_HIGH)
      return high > node_price;
   return false;
}

double DAL_HuntPrice(int node_type, double node_price, double high, double low)
{
   if(node_type == DAL_NODE_LOW)
      return MathMin(low, node_price);
   if(node_type == DAL_NODE_HIGH)
      return MathMax(high, node_price);
   return node_price;
}

void DAL_PushLog(double &arr[], const double value, int max_len = 0)
{
   int size = ArraySize(arr);
   if(max_len > 0 && size >= max_len)
   {
      for(int i = 1; i < size; i++)
         arr[i - 1] = arr[i];
      arr[size - 1] = value;
      return;
   }

   ArrayResize(arr, size + 1);
   arr[size] = value;
}

void DAL_ClearLogs(double &arr[])
{
   ArrayResize(arr, 0);
}

void DAL_CopyLogs(double &src[], double &dst[])
{
   const int n = ArraySize(src);
   ArrayResize(dst, n);
   for(int i = 0; i < n; i++)
      dst[i] = src[i];
}

double DAL_MeanLastN(double &arr[], int n)
{
   const int size = ArraySize(arr);
   if(n <= 0 || size < n)
      return EMPTY_VALUE;

   double sum = 0.0;
   for(int i = size - n; i < size; i++)
      sum += arr[i];

   return sum / (double)n;
}

double DAL_MeanAll(double &arr[])
{
   const int size = ArraySize(arr);
   if(size <= 0)
      return EMPTY_VALUE;

   double sum = 0.0;
   for(int i = 0; i < size; i++)
      sum += arr[i];

   return sum / (double)size;
}

double DAL_MedianAll(double &arr[])
{
   const int size = ArraySize(arr);
   if(size <= 0)
      return EMPTY_VALUE;

   double copy[];
   ArrayResize(copy, size);
   for(int i = 0; i < size; i++)
      copy[i] = arr[i];

   ArraySort(copy);

   if((size % 2) == 1)
      return copy[size / 2];

   return (copy[size / 2 - 1] + copy[size / 2]) * 0.5;
}

string DAL_NodeTypeText(int node_type)
{
   if(node_type == DAL_NODE_LOW)
      return "LOW";
   if(node_type == DAL_NODE_HIGH)
      return "HIGH";
   return "UNKNOWN";
}
