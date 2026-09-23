# A glossary you can use while coding

| Term | Meaning in this project |
|---|---|
| Activation | Elementwise nonlinear function such as ReLU or GELU. |
| Attention | Input-dependent weights used to combine value vectors across positions. |
| Autograd | PyTorch's system for computing derivatives through tensor operations. |
| Autoregressive | Producing the next item from earlier items, then repeating. |
| Axis / dimension | One direction in an array, such as batch, position, or feature. |
| Batch, B | Several sequences processed together. |
| Bias | A learned offset added by a layer. |
| Broadcasting | Matching compatible tensor shapes by virtually repeating size-one or missing leading axes. |
| Causal | A position uses itself and earlier positions; future information is unavailable. |
| Checkpoint | Saved parameters and reconstruction metadata. |
| Context length, T maximum | Largest number of input positions the model accepts in one forward pass. |
| Cross-entropy | A loss that penalizes low probability on the correct class. |
| Decoder-only model | A transformer used here to predict the continuation of a prefix. |
| Dtype | The type of each tensor element, such as float32 or int64. |
| Embedding | Learned table mapping discrete IDs to feature vectors. |
| Epoch | One full pass through a dataset; our sampler instead counts random-batch update steps. |
| Feature / channel, C | One numeric coordinate in a position's representation. |
| Feed-forward network | A small nonlinear network applied with shared parameters to each position. |
| Forward pass | Compute outputs from inputs and current parameters. |
| Gradient | Derivative of loss with respect to a parameter; indicates local sensitivity. |
| Head, H | One attention subspace with its own projected queries, keys, and values. |
| Head width, D | Number of features per head, `C/H` here. |
| Hyperparameter | A choice such as width or learning rate, set before training rather than learned by gradient descent. |
| Key, K | A vector compared with queries to compute attention scores. |
| LayerNorm | Normalize a position's features, then apply learned elementwise scale and offset. |
| Learning rate | A scale controlling how large optimizer updates are. |
| Linear layer | A learned affine map: weighted sums plus optional bias. |
| Logit | An unconstrained output score, before conversion into probabilities. |
| Loss | A number measuring error according to the training objective. |
| Mask | A rule disabling certain attention connections. |
| Matrix multiplication | Row/column dot products, with matching contracted dimensions. |
| Module | A PyTorch object that can own parameters and compute a forward function. |
| Optimizer | An algorithm that updates parameters using gradients. |
| Overfitting | Improving on training examples while fitting details that do not generalize well. |
| Parameter | A stored tensor whose values are learned, such as a projection weight. |
| Position embedding | Learned vector added to indicate a position within the context window. |
| Query, Q | A vector whose dot products with keys determine one receiver's weights. |
| Residual connection | Addition of an input to a branch's output: `x + update`. |
| Scalar | A single number; a scalar tensor has zero axes. |
| Seed | Initial state used to make pseudorandom experiments repeatable. |
| Shape | The sizes of a tensor's axes, such as `[B,T,C]`. |
| Softmax | Convert a row of scores into positive normalized weights. Masked entries can be exactly zero. |
| Tensor | A multidimensional array with a dtype and device. |
| Token | A sequence item; one character in this project. |
| Tokenizer | Convert text into IDs and IDs back into text. |
| Training step | One forward/loss/backward/optimizer update on a batch. |
| Validation | Measurement on held-out data without updating parameters. |
| Value, V | Vector mixed into attention outputs. Also V means vocabulary size in some shape tables; context distinguishes them. |
| Vector | An ordered list of numbers; a rank-one tensor. |

If a symbol feels ambiguous, write its shape next to it. In this guide `v` is usually the value tensor and `V` in `[B,T,V]` is vocabulary size.
