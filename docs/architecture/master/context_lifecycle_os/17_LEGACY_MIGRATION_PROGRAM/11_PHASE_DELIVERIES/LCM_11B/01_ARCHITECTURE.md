# Architecture

The architecture is `Canonical Event -> Pure Visualizer -> Projection Registry`. Event semantics and style are independent. Renderers have no domain mutation, dispatch, execution, promotion or capital ports.
