# Session Geometry Contract

For one symbol and one session snapshot:

- left boundary = scheduled session start;
- right boundary = scheduled session end;
- top = highest High of that symbol inside the session;
- bottom = lowest Low of that symbol inside the session.

Open sessions use the scheduled end boundary while their High/Low update as new closed base bars arrive. This preserves a stable time footprint and a live range. Complete sessions become immutable evidence except for repair of manual chart edits.
