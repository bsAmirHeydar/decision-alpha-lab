#pragma once
bool ACL13KnownTimeSafe(const datetime event_time,const datetime available_at,const datetime cut_at){ return event_time<=available_at && available_at<=cut_at; }
