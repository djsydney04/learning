# The practice text

`tiny_stories.txt` contains forty short original passages written for this exercise. It is a tiny teaching corpus, not the external TinyStories research dataset. No dataset download or account is required. You may edit or replace this text for your experiments.

The trainer reserves the final 10% of characters for validation **before** sampling windows. Train and validation windows cannot cross that boundary. The same characters, words, subjects, and story patterns recur across both sections, so this is an easy and narrow practice distribution. Good loss here does not demonstrate broad language understanding.

The character vocabulary is the sorted set of characters in the entire file. This exposes the allowed alphabet, including any validation-only characters, but does not train on validation sequences. This convention avoids unknown characters in this first exercise. A later experiment can use a fixed predefined alphabet or a train-only tokenizer with an explicit unknown-token policy.

The file uses lowercase characters. A prompt containing an unseen uppercase letter will be rejected with a vocabulary error. Start with `the ` or `mia `.

When replacing the corpus, each 90%/10% split needs at least `context_length + 1` characters. For a default context of 32, the smaller split needs at least 33 characters. Give it substantially more than this minimum to make validation useful.
