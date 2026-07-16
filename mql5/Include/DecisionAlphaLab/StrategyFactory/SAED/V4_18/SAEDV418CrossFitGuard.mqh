#pragma once
bool SAEDV418ChronologyValid(const long train_end,const long evaluation_start){ return train_end<evaluation_start; }
bool SAEDV418SiblingSplitAllowed(){ return false; }
