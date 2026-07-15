#pragma once
bool SAEDV413KnownTimeAllowed(const datetime event_time,const datetime known_time,const datetime cutoff){ return event_time<=known_time && known_time<=cutoff; }
