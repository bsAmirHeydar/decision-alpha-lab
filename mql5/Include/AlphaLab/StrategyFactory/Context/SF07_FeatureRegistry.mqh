#ifndef __SF07_FEATURE_REGISTRY_MQH__
#define __SF07_FEATURE_REGISTRY_MQH__

#include "ISF07_FeatureNode.mqh"
#include "SF07_ContextState.mqh"

class CSF07FeatureRegistry
{
private:
   ISF07FeatureNode *m_nodes[];
   SF07_FeatureDescriptor m_descriptors[];
   int m_topological_order[];
   bool m_compiled;
   string m_graph_hash;

   int FindDescriptorIndex(const string feature_id) const
   {
      const int count = ArraySize(m_descriptors);
      for(int i = 0; i < count; i++)
         if(m_descriptors[i].feature_id == feature_id) return i;
      return -1;
   }

   int SelectNextReady(const int &indegree[], const bool &selected[]) const
   {
      int best = -1;
      const int count = ArraySize(m_descriptors);
      for(int i = 0; i < count; i++)
      {
         if(selected[i] || indegree[i] != 0) continue;
         if(best < 0 || m_descriptors[i].feature_id < m_descriptors[best].feature_id) best = i;
      }
      return best;
   }

public:
   CSF07FeatureRegistry(void)
   {
      ArrayResize(m_nodes, 0);
      ArrayResize(m_descriptors, 0);
      ArrayResize(m_topological_order, 0);
      m_compiled = false;
      m_graph_hash = "";
   }

   int Count(void) const { return ArraySize(m_nodes); }
   bool IsCompiled(void) const { return m_compiled; }
   string GraphHash(void) const { return m_graph_hash; }

   bool RegisterNode(ISF07FeatureNode *node, string &error)
   {
      if(CheckPointer(node) == POINTER_INVALID)
      { error = "invalid feature node pointer"; return false; }
      SF07_FeatureDescriptor descriptor;
      SF07_ResetFeatureDescriptor(descriptor);
      node.GetDescriptor(descriptor);
      if(!SF07_ValidateFeatureDescriptor(descriptor, error)) return false;
      if(FindDescriptorIndex(descriptor.feature_id) >= 0)
      { error = "duplicate feature owner: " + descriptor.feature_id; return false; }
      const int count = ArraySize(m_nodes);
      ArrayResize(m_nodes, count + 1);
      ArrayResize(m_descriptors, count + 1);
      m_nodes[count] = node;
      m_descriptors[count] = descriptor;
      m_compiled = false;
      m_graph_hash = "";
      error = "";
      return true;
   }

   bool Compile(string &error)
   {
      const int count = ArraySize(m_nodes);
      if(count <= 0)
      { error = "feature registry is empty"; return false; }
      int indegree[];
      bool selected[];
      ArrayResize(indegree, count);
      ArrayResize(selected, count);
      for(int i = 0; i < count; i++)
      {
         indegree[i] = m_descriptors[i].dependency_count;
         selected[i] = false;
         for(int d = 0; d < m_descriptors[i].dependency_count; d++)
         {
            if(FindDescriptorIndex(m_descriptors[i].dependencies[d]) < 0)
            { error = "missing feature dependency: " + m_descriptors[i].dependencies[d]; return false; }
         }
      }
      ArrayResize(m_topological_order, count);
      for(int position = 0; position < count; position++)
      {
         const int next = SelectNextReady(indegree, selected);
         if(next < 0)
         { error = "feature dependency cycle detected"; return false; }
         selected[next] = true;
         m_topological_order[position] = next;
         const string completed = m_descriptors[next].feature_id;
         for(int i = 0; i < count; i++)
         {
            if(selected[i]) continue;
            for(int d = 0; d < m_descriptors[i].dependency_count; d++)
               if(m_descriptors[i].dependencies[d] == completed) indegree[i]--;
         }
      }
      string canonical = "";
      for(int i = 0; i < count; i++)
      {
         const int index = m_topological_order[i];
         canonical += (i == 0 ? "" : "|") + SF07_FeatureDescriptorCanonical(m_descriptors[index]);
      }
      m_graph_hash = SF01_StableId("fdag", canonical);
      m_compiled = true;
      error = "";
      return true;
   }

   ISF07FeatureNode *NodeAtTopological(const int position) const
   {
      if(!m_compiled || position < 0 || position >= ArraySize(m_topological_order)) return NULL;
      return m_nodes[m_topological_order[position]];
   }

   bool DescriptorAtTopological(const int position, SF07_FeatureDescriptor &descriptor) const
   {
      if(!m_compiled || position < 0 || position >= ArraySize(m_topological_order)) return false;
      descriptor = m_descriptors[m_topological_order[position]];
      return true;
   }

   bool GetDescriptor(const string feature_id, SF07_FeatureDescriptor &descriptor) const
   {
      const int index = FindDescriptorIndex(feature_id);
      if(index < 0) return false;
      descriptor = m_descriptors[index];
      return true;
   }

   bool MarkDependentsDirty(const string feature_id,
                            CSF07ContextState &state,
                            const ENUM_SF07_INVALIDATION_REASON reason) const
   {
      bool changed = false;
      const int count = ArraySize(m_descriptors);
      for(int pass = 0; pass < count; pass++)
      {
         for(int i = 0; i < count; i++)
         {
            for(int d = 0; d < m_descriptors[i].dependency_count; d++)
            {
               const string dependency = m_descriptors[i].dependencies[d];
               if(dependency == feature_id || state.IsDirty(dependency))
               {
                  if(state.MarkDirty(m_descriptors[i].feature_id, reason)) changed = true;
               }
            }
         }
      }
      return changed;
   }
};

#endif
