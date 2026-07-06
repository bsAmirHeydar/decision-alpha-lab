
---
type: concept_graph
---

# Concept Dependency Graph

این جدول رابطه canonical بین مفهوم‌های اصلی است. این رابطه‌ها بر اساس منطق پروژه و محتوای داکیومنت‌ها ساخته شده‌اند و باید در آینده با ADRهای دقیق‌تر سخت‌گیرانه‌تر شوند.

| Source | Relation | Target |
|---|---|---|
| [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Hook|Hook]] |
| [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Rally|Rally]] |
| [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] |
| [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]] |
| [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]] |
| [[docs/obsidian_deep/02_concepts/Hook|Hook]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]] |
| [[docs/obsidian_deep/02_concepts/Hook|Hook]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Rally|Rally]] |
| [[docs/obsidian_deep/02_concepts/Hook|Hook]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] |
| [[docs/obsidian_deep/02_concepts/Hook|Hook]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]] |
| [[docs/obsidian_deep/02_concepts/Hook|Hook]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] |
| [[docs/obsidian_deep/02_concepts/Hook|Hook]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] |
| [[docs/obsidian_deep/02_concepts/Rally|Rally]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] |
| [[docs/obsidian_deep/02_concepts/Rally|Rally]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/Rally|Rally]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]] |
| [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] |
| [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Hook|Hook]] |
| [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Rally|Rally]] |
| [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] |
| [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]] |
| [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]] |
| [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]] |
| [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]] |
| [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]] |
| [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]] |
| [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] |
| [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]] |
| [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]] |
| [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] |
| [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]] |
| [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]] |
| [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] |
| [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Licensing|Licensing]] |
| [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] |
| [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]] |
| [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] |
| [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] |
| [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Licensing|Licensing]] |
| [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] |
| [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] |
| [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]] |
| [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] |
| [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] |
| [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]] |
| [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]] |
| [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]] |
| [[docs/obsidian_deep/02_concepts/Licensing|Licensing]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]] |
| [[docs/obsidian_deep/02_concepts/Licensing|Licensing]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
| [[docs/obsidian_deep/02_concepts/UI____React|UI / React]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]] |
| [[docs/obsidian_deep/02_concepts/UI____React|UI / React]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]] |
| [[docs/obsidian_deep/02_concepts/UI____React|UI / React]] | depends_on / connects_to | [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]] |
