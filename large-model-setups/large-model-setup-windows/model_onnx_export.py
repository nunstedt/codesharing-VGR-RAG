#Code transforming the embedding model to ONNX format to align with docker implementation.

from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn as nn
import onnx
import os
#model_path = "trained_embeddings/"
model_name = "intfloat/multilingual-e5-large-instruct"
export_dir = "export_models"
onnx_output_path = os.path.join(export_dir, "model.onnx")


model_name = "intfloat/multilingual-e5-large-instruct"
onnx_output_path = os.path.join("export_models", "model.onnx")

# # Load your model and tokenizer
#model = AutoModel.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

model.save_pretrained(export_dir)
tokenizer.save_pretrained(export_dir)
# Prepare dummy input
dummy_text = "This is a dummy input for ONNX export"
inputs = tokenizer(dummy_text, return_tensors="pt")

# Export to ONNX
torch.onnx.export(
    model,                                           # model to export
    (inputs["input_ids"], inputs["attention_mask"],),                          # model inputs as a tuple
    onnx_output_path,                                # where to save the ONNX file
    input_names=["input_ids", "attention_mask"],
    output_names=["last_hidden_state"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "last_hidden_state": {0: "batch_size", 1: "sequence_length"}
    },
    opset_version=14,
)

#torch_model = ImageClassifierModel()
# Create example inputs for exporting the model. The inputs should be a tuple of tensors.
# example_inputs = (torch.randn(3,384)).long()
# onnx_program = torch.onnx.export(model, example_inputs)
#onnx_program.save(onnx_output_path)
print(f"ONNX model saved at {onnx_output_path}")
