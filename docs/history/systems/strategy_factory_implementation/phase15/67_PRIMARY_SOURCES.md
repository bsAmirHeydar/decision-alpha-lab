# Primary Sources

Phase 15 is aligned to the official MQL5 ONNX API and the normative ONNX protobuf schema.

## MQL5

- MetaQuotes, **OnnxCreate**: model paths are resolved relative to `MQL5/Files`, with `ONNX_COMMON_FOLDER` available for `Common/Files`.
- MetaQuotes, **OnnxRun**: model inputs and outputs are passed as typed MQL5 matrices and vectors; `ONNX_NO_CONVERSION` disables implicit conversion.
- MetaQuotes, **OnnxSetInputShape** and **OnnxSetOutputShape**: static runtime shapes are bound by input and output ordinal before execution.

Official references:

- https://www.mql5.com/en/docs/onnx/onnxcreate
- https://www.mql5.com/en/docs/onnx/onnxrun
- https://www.mql5.com/en/docs/onnx/onnxsetinputshape
- https://www.mql5.com/en/docs/onnx/onnxsetoutputshape

## ONNX

- ONNX `ModelProto`, `GraphProto`, `NodeProto`, `TensorProto`, `ValueInfoProto`, `TypeProto`, `TensorShapeProto` and `OperatorSetIdProto` field numbers follow the official `onnx.proto3` schema.
- The reference graph uses only standard-domain `MatMul` and `Add` nodes with opset 13, float32 initializers and fixed tensor shapes.

Official reference:

- https://github.com/onnx/onnx/blob/main/onnx/onnx.proto3

Source review date: 2026-07-11.
