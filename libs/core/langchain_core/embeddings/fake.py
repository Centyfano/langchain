"""Module contains a few fake embedding models for testing purposes."""

# Please do not add additional fake embedding model implementations here.
import hashlib
from typing import List

from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel


class FakeEmbeddings(Embeddings, BaseModel):
    """Fake embedding model for unit testing purposes.

    This embedding model creates embeddings by sampling from a normal distribution.

    Do not use this outside of testing, as it is not a real embedding model.

    Example:

        .. code-block:: python

            from langchain_core.embeddings import FakeEmbeddings

            fake_embeddings = FakeEmbeddings(size=100)
            fake_embeddings.embed_documents(["hello world", "foo bar"])
    """

    size: int
    """The size of the embedding vector."""

    def _get_embedding(self) -> List[float]:
        import numpy as np  # type: ignore[import-not-found, import-untyped]

        return list(np.random.normal(size=self.size))

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._get_embedding() for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._get_embedding()


class DeterministicFakeEmbedding(Embeddings, BaseModel):
    """Deterministic fake embedding model for unit testing purposes.

    This embedding model creates embeddings by sampling from a normal distribution
    with a seed based on the hash of the text.

    Do not use this outside of testing, as it is not a real embedding model.

    Example:

        .. code-block:: python

            from langchain_core.embeddings import DeterministicFakeEmbedding

            fake_embeddings = DeterministicFakeEmbedding(size=100)
            fake_embeddings.embed_documents(["hello world", "foo bar"])
    """

    size: int
    """The size of the embedding vector."""

    def _get_embedding(self, seed: int) -> List[float]:
        import numpy as np  # type: ignore[import-not-found, import-untyped]

        # set the seed for the random generator
        np.random.seed(seed)
        return list(np.random.normal(size=self.size))

    def _get_seed(self, text: str) -> int:
        """Get a seed for the random generator, using the hash of the text."""
        return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % 10**8

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._get_embedding(seed=self._get_seed(_)) for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._get_embedding(seed=self._get_seed(text))
