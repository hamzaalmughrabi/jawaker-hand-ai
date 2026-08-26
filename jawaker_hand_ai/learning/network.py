"""Vectorized Neural Value Network for Jawaker Hand state and action evaluation."""

from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from typing import Optional


class NeuralValueNetwork:
    """A 2-hidden layer feed-forward value network (32 -> 64 -> 32 -> 1) with ReLU activations."""

    INPUT_DIM = 32
    HIDDEN1_DIM = 64
    HIDDEN2_DIM = 32
    OUTPUT_DIM = 1

    def __init__(self, seed: Optional[int] = 42):
        rng = np.random.default_rng(seed)
        # He / Kaiming initialization
        self.W1 = rng.normal(0, np.sqrt(2.0 / self.INPUT_DIM), (self.INPUT_DIM, self.HIDDEN1_DIM))
        self.b1 = np.zeros(self.HIDDEN1_DIM, dtype=np.float64)

        self.W2 = rng.normal(0, np.sqrt(2.0 / self.HIDDEN1_DIM), (self.HIDDEN1_DIM, self.HIDDEN2_DIM))
        self.b2 = np.zeros(self.HIDDEN2_DIM, dtype=np.float64)

        self.W3 = rng.normal(0, np.sqrt(2.0 / self.HIDDEN2_DIM), (self.HIDDEN2_DIM, self.OUTPUT_DIM))
        self.b3 = np.zeros(self.OUTPUT_DIM, dtype=np.float64)

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Forward pass. X shape: (N, 32) or (32,). Returns (y_pred, h2, h1, z1)."""
        is_1d = (X.ndim == 1)
        if is_1d:
            X = X.reshape(1, -1)

        z1 = np.dot(X, self.W1) + self.b1
        h1 = np.maximum(0, z1)  # ReLU

        z2 = np.dot(h1, self.W2) + self.b2
        h2 = np.maximum(0, z2)  # ReLU

        y_pred = np.dot(h2, self.W3) + self.b3  # Linear output (predicted score)

        if is_1d:
            return float(y_pred[0, 0]), h2[0], h1[0], z1[0]
        return y_pred, h2, h1, z1

    def predict(self, X: np.ndarray) -> float:
        """Fast prediction for single state feature vector."""
        if X.ndim == 1:
            z1 = np.dot(X, self.W1) + self.b1
            h1 = np.maximum(0, z1)
            z2 = np.dot(h1, self.W2) + self.b2
            h2 = np.maximum(0, z2)
            y = np.dot(h2, self.W3) + self.b3
            return float(y[0])
        else:
            return self.forward(X)[0]

    def train_step(self, X: np.ndarray, y_target: np.ndarray, lr: float = 0.001) -> float:
        """Single backpropagation gradient descent step. Returns mean squared loss."""
        if X.ndim == 1:
            X = X.reshape(1, -1)
        if y_target.ndim == 1:
            y_target = y_target.reshape(-1, 1)

        N = X.shape[0]

        # Forward pass
        z1 = np.dot(X, self.W1) + self.b1
        h1 = np.maximum(0, z1)

        z2 = np.dot(h1, self.W2) + self.b2
        h2 = np.maximum(0, z2)

        y_pred = np.dot(h2, self.W3) + self.b3

        # Loss & Gradients
        error = y_pred - y_target
        loss = float(np.mean(error ** 2))

        d_out = (2.0 / N) * error  # (N, 1)

        dW3 = np.dot(h2.T, d_out)
        db3 = np.sum(d_out, axis=0)

        dh2 = np.dot(d_out, self.W3.T)
        dz2 = dh2 * (z2 > 0)
        dW2 = np.dot(h1.T, dz2)
        db2 = np.sum(dz2, axis=0)

        dh1 = np.dot(dz2, self.W2.T)
        dz1 = dh1 * (z1 > 0)
        dW1 = np.dot(X.T, dz1)
        db1 = np.sum(dz1, axis=0)

        # Gradient clipping
        np.clip(dW1, -5.0, 5.0, out=dW1)
        np.clip(dW2, -5.0, 5.0, out=dW2)
        np.clip(dW3, -5.0, 5.0, out=dW3)

        # Update weights
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W3 -= lr * dW3
        self.b3 -= lr * db3

        return loss

    def save(self, filepath: str | Path) -> None:
        data = {
            "W1": self.W1.tolist(), "b1": self.b1.tolist(),
            "W2": self.W2.tolist(), "b2": self.b2.tolist(),
            "W3": self.W3.tolist(), "b3": self.b3.tolist()
        }
        Path(filepath).write_text(json.dumps(data), encoding="utf-8")

    def load(self, filepath: str | Path) -> None:
        data = json.loads(Path(filepath).read_text(encoding="utf-8"))
        self.W1 = np.array(data["W1"], dtype=np.float64)
        self.b1 = np.array(data["b1"], dtype=np.float64)
        self.W2 = np.array(data["W2"], dtype=np.float64)
        self.b2 = np.array(data["b2"], dtype=np.float64)
        self.W3 = np.array(data["W3"], dtype=np.float64)
        self.b3 = np.array(data["b3"], dtype=np.float64)
