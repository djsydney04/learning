"""Run: python -m labs.04_embeddings

Experiment: change MESSAGE to "tact". Observe ID rows versus position rows.
Use only characters from CORPUS so every character has an ID.
"""

import torch
from torch import nn

CORPUS = "cat!cat!"
MESSAGE = "cat!"
C = 3


def main():
    torch.set_printoptions(precision=2, sci_mode=False)
    characters = sorted(set(CORPUS))
    char_to_id = {character: index for index, character in enumerate(characters)}
    ids = torch.tensor([[char_to_id[character] for character in MESSAGE]], dtype=torch.long)
    _, T = ids.shape
    V = len(characters)
    token_table = nn.Embedding(V, C)
    position_table = nn.Embedding(T, C)
    # These hand-chosen values make lookup visible. Real training starts with
    # random learned tables and updates them with gradients.
    with torch.no_grad():
        token_table.weight.copy_(torch.arange(V * C).reshape(V, C) / 10)
        position_table.weight.copy_(torch.arange(T).unsqueeze(1).expand(T, C) / 100)
    token_vectors = token_table(ids)
    positions = torch.arange(T, dtype=torch.long)
    position_vectors = position_table(positions)
    x = token_vectors + position_vectors  # [1, T, C] + [T, C]
    print("vocabulary:", char_to_id)
    print("IDs [B, T]:", ids.tolist())
    print("token vectors [B, T, C]:\n", token_vectors.detach())
    print("position vectors [T, C]:\n", position_vectors.detach())
    print("combined vectors:\n", x.detach())
    assert x.shape == (1, T, C)

    repeated = token_table(torch.tensor([char_to_id["c"], char_to_id["c"]]))
    assert torch.equal(repeated[0], repeated[1])
    assert not torch.equal(repeated[0] + position_vectors[0], repeated[1] + position_vectors[1])

    # Four input tokens need FIVE corpus tokens to construct four targets.
    stream = torch.tensor([char_to_id[character] for character in CORPUS])
    inputs = stream[:4].unsqueeze(0)
    targets = stream[1:5].unsqueeze(0)
    def decode(row):
        return "".join(characters[token_id] for token_id in row.tolist())

    print("training input:", decode(inputs[0]))
    print("next-token target:", decode(targets[0]))
    assert torch.equal(inputs[:, 1:], targets[:, :-1])
    assert decode(targets[0]) == "at!c"
    print("All embedding checks passed.")


if __name__ == "__main__":
    main()
