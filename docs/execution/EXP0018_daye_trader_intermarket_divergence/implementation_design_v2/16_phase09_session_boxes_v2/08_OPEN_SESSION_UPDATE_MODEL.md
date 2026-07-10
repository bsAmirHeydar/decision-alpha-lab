# Open Session Update Model

An open box is provisional visual state. Its time boundaries are stable, but its top and bottom may expand when new closed source bars change the session High or Low. The same deterministic object name is updated in place.

P09 does not use the forming tick stream directly. It inherits P03 closed-base-bar causality. When the session closes and P03 marks it COMPLETE, the box transitions from update behavior to closed verification behavior.
