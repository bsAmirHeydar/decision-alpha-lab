#ifndef __ALPHALAB_SAEDV4ACTIONLATTICEFALLBACK_MQH__
#define __ALPHALAB_SAEDV4ACTIONLATTICEFALLBACK_MQH__

// SAED V4-07 diagnostic-only mirror. No trading, file, socket or network authority.
bool SAEDV407IsMandatoryFallback(const int action_class){ return action_class==SAED_V4_07_ABSTAIN || action_class==SAED_V4_07_SKIP; }

#endif // __ALPHALAB_SAEDV4ACTIONLATTICEFALLBACK_MQH__
