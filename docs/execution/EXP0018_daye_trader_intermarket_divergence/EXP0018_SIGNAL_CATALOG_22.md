# کاتالوگ ۲۲ سیگنال Daye

## قرارداد شناسه

برای جلوگیری از مشکل راست‌به‌چپ، سه سطح نام تعریف می‌شود:

- **Source Alias:** همان چیزی که در DOCX دیده می‌شود.
- **Canonical ID:** نام بدون ابهام برای کد آینده.
- **Display Label:** متنی که روی چارت نمایش داده می‌شود.

## شش سیگنال بزرگ

| Source | Canonical ID | Current | Reference | Label |
|---|---|---|---|---|
| WW | DAYE_W_CURR_VS_W_PREV | هفته فعلی | هفته قبلی | WW |
| DD | DAYE_D_CURR_VS_D_PREV | روز فعلی | روز قبلی | DD |
| PA | DAYE_A_CURR_VS_P_PREV | A فعلی | P قبلی | PA |
| AL | DAYE_L_CURR_VS_A_PREV | L فعلی | A قبلی | AL |
| LN | DAYE_N_CURR_VS_L_PREV | N فعلی | L قبلی | LN |
| NP | DAYE_P_CURR_VS_N_PREV? | نیازمند تأیید | نیازمند تأیید | NP |

## شانزده سیگنال زیرسایکل

| Source Alias | Canonical ID | Current | Reference | Label روی خط |
|---|---|---|---|---|
| p4a1 | DAYE_A1_VS_P4 | a1 | p4 قبلی | ندارد |
| a1a2 | DAYE_A2_VS_A1 | a2 | a1 | ندارد |
| a2a3 | DAYE_A3_VS_A2 | a3 | a2 | ندارد |
| a3a4 | DAYE_A4_VS_A3 | a4 | a3 | ندارد |
| a4l1 | DAYE_L1_VS_A4 | l1 | a4 | ندارد |
| l1l2 | DAYE_L2_VS_L1 | l2 | l1 | ندارد |
| l2l3 | DAYE_L3_VS_L2 | l3 | l2 | ندارد |
| l3l4 | DAYE_L4_VS_L3 | l4 | l3 | ندارد |
| l4n1 | DAYE_N1_VS_L4 | n1 | l4 | ندارد |
| n1n2 | DAYE_N2_VS_N1 | n2 | n1 | ندارد |
| n2n3 | DAYE_N3_VS_N2 | n3 | n2 | ندارد |
| n3n4 | DAYE_N4_VS_N3 | n4 | n3 | ندارد |
| n4p1 | DAYE_P1_VS_N4 | p1 | n4 | ندارد |
| p1p2 | DAYE_P2_VS_P1 | p2 | p1 | ندارد |
| p2p3 | DAYE_P3_VS_P2 | p3 | p2 | ندارد |
| p3p4 | DAYE_P4_VS_P3 | p4 | p3 | ندارد |

## تعداد

- 6 سیگنال بزرگ
- 16 سیگنال زیرسایکل
- مجموع: 22

عبارت «21 سیگنال» در انتهای منبع با فهرست 22تایی ناسازگار است و به‌عنوان خطای احتمالی متن ثبت شده است.
