
---
type: conversation_derived_knowledge
---

# User-Stated Principles — اصولی که از گفتار پروژه استخراج شده

این فایل از دانش آشکارشده در مکالمات همین پروژه ساخته شده است. این‌ها باید به تدریج به hard rule، ADR، template و validation policy تبدیل شوند.

## P001 — پتانسیل مهم‌تر از قطعیت است

در این پروژه سناریوها برای «درست بودن مطلق» ساخته نمی‌شوند؛ هر سناریو به عنوان پتانسیل کم‌هزینه/پرسود ارزیابی می‌شود. هدف، پیدا کردن ساختارهایی است که هزینه شکست محدود و سود بالقوه بازتر دارند.

**Links:** [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## P002 — وین‌ریت قبل از تحدب اصل نیست

طبق منطق پروژه، قبل از اینکه ساختار معامله محدب شود، وین‌ریت معیار اصلی نیست. ابتدا باید نسبت هزینه به گستره سود و امکان انفجار بررسی شود؛ بعد از آن وین‌ریت برای پایداری و deployment اهمیت می‌گیرد.

**Links:** [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]

## P003 — همه ادله باید از آناتومی داخلی بازار بیاید

قانون سخت پروژه این است که تصمیمات و مدل‌ها باید از مفاهیم داخلی خود پروژه مثل Hook، Rally، F-counting، Decision Node، Zone و RTV تغذیه شوند، نه از اندیکاتورهای بیرونی و تفسیرهای نامتصل.

**Links:** [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]

## P004 — هر ایده باید traceable باشد

هر مفهوم باید به hypothesis، experiment، validation، code module و decision log قابل ردیابی باشد. هیچ ایده‌ای نباید فقط در چت یا حافظه ذهنی باقی بماند.

**Links:** [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]], [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## P005 — AI جایگزین rule engine نیست

ایجنت در پروژه باید پژوهش، ممیزی، مستندسازی، ساخت پچ، ژورنال و طراحی تست را اتوماتیک کند. اجرای live، risk و order باید پشت hard rule و موتور deterministic بماند.

**Links:** [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## P006 — فرکتال بودن باید متریک داشته باشد

ادعای فرکتال بودن بازار کافی نیست. باید روشن شود از چه نظر فرکتال است: ساختار، مسیر، توزیع، زمان، برگشت، continuation، smoothness یا انفجار.

**Links:** [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## P007 — شهود فقط داخل چارچوب قدرت دارد

شهود تریدر وقتی ارزشمند می‌شود که داخل چارچوب تعریف‌شده، ژورنال‌پذیر و قابل تست باشد. تجربه انسانی باید به label، episode، context و feature تبدیل شود.

**Links:** [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
