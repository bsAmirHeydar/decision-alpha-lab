# M0001 Revisited Zone Colors

When a node survives and receives at least one confirmed revisit, its live zone
rectangle changes color:

- HIGH / peak revisited zone -> purple
- LOW / valley revisited zone -> blue

Rules:

- Fresh live zones keep the normal node-side colors.
- Consumed zones still fall back to the consumed/inactive gray history style.
- Only the rectangle color changes; the revisit logic and state model are unchanged.

Version: `1.47`
