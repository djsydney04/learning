# Sources and next readings

You can complete the project from the local lessons. These primary sources document the underlying operations or provide a next step. API behavior was checked while preparing the guide; the tested local environment is recorded in [the run notes](../examples/RESULTS.md).

| Read after | Primary source | What to look for |
|---|---|---|
| Lesson 1 | [Python tutorial](https://docs.python.org/3/tutorial/) | Functions, control flow, lists, dictionaries, classes. |
| Lesson 2 | [PyTorch tensors](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) | Shape, dtype, device, indexing, and matrix multiplication. |
| Lesson 3 | [PyTorch automatic differentiation](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) | Computation graphs and gradient tracking. |
| Lesson 3 | [PyTorch optimization](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) | Zeroing gradients, backward, and the optimizer step. |
| Lesson 4 | [Embedding API](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html) | Integer IDs index a learned table. |
| Lesson 5 | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | Scaled dot-product attention, multiple heads, FFNs, positional information. |
| Lesson 6 | [Scaled dot-product attention API](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html) | Compare the explicit implementation with a fused operation; inspect mask and dropout semantics. |
| Lesson 7 | [Linear API](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html) | Weight storage convention and preservation of leading dimensions. |
| Lesson 7 | [GELU API](https://docs.pytorch.org/docs/stable/generated/torch.nn.GELU.html) | Exact and approximate activation forms. |
| Lesson 8 | [LayerNorm API](https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html) | Feature statistics, epsilon, learned scale and bias. |
| Lesson 9 | [CrossEntropyLoss API](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) | Raw logits, integer targets, class dimension. |
| Lesson 10 | [Saving and loading models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) | State dictionaries, model reconstruction, evaluation mode. |

The explanations, exercises, code, practice stories, and PNG diagrams in this project are newly written. The references support the concepts and API choices; this guide does not reproduce a paper or course verbatim.

## What this implementation deliberately chooses

This is a small decoder-only model with character tokens, learned positions, pre-normalization, GELU, explicit dense causal attention, and ordinary multihead projections. The 2017 paper describes an encoder–decoder model, sinusoidal positions, ReLU feed-forward activation, and different normalization placement. Use the paper to connect the common building blocks, not to assume this is a line-for-line reproduction.

Learn extensions by identifying which existing component would change:

- **Subword tokenization:** replace the character tokenizer and vocabulary; the transformer still consumes integer IDs.
- **Encoder attention:** allow positions to attend to the full input when the task permits it.
- **Cross-attention:** compute queries from the decoder and keys/values from encoder output.
- **Different position schemes:** replace or change how positional information enters embeddings or attention.
- **Gated feed-forward networks:** change the nonlinear feature transformation while preserving the block's interface.
- **Fused attention and caching:** change how the same or related attention computation is executed to improve efficiency.

Return to [the course](../README.md).
