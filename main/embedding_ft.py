# Code to fine-tune embedding model using the generated data and Triplet Loss - and save model in trained embeddings folder.
# Kept separate from the main code.

import torch
from torch import nn
import json
from sentence_transformers import SentenceTransformer, losses, InputExample, models
from transformers import AutoTokenizer, AutoModel
from torch.utils.data import Dataset, DataLoader
from typing import List, Dict, Any, Tuple
import os

class TripletDataset(Dataset):
    """
    Custom dataset for loading triplet data.
 
    """
    def __init__(self, triplets_file: str, tokenizer: AutoTokenizer, max_length: int = 512):
        with open(triplets_file, 'r', encoding = 'utf-8') as f:
            self.triplets = json.load(f)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.triplets)

    def __getitem__(self, idx: int) -> dict:
        triplet = self.triplets[idx]
        return {
            key: self.tokenizer(triplet[key], 
            padding='max_length', 
            truncation=True, 
            max_length=self.max_length, 
            return_tensors='pt') for key in ['anchor', 'positive', 'negative']
        }
            
class TripletLoss(nn.Module):
    def __init__(self, margin: float = 1.0):
        super().__init__()
        self.margin = margin
    
    def forward(self, anchor: torch.Tensor, positive: torch.Tensor, negative: torch.Tensor) -> torch.Tensor:
        # Calculate distances between anchor-positive and anchor-negative pairs
        dist_positive = (anchor - positive).pow(2).sum(1)
        dist_negative = (anchor - negative).pow(2).sum(1)
        
        # Apply margin: ensure negative pairs are further apart than positive pairs by at least margin
        losses = torch.relu(dist_positive - dist_negative + self.margin)
        return losses.mean()

class EmbeddingTrainer:
    def __init__(
        self, 
        model_name: str = ("sentence-transformers/all-MiniLM-L6-v2"),
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.criterion = TripletLoss()
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=2e-5)
    
    def train_epoch(self, dataloader: DataLoader) -> float:
        self.model.train()
        total_loss = 0
        
        for batch in dataloader:
            # Move all inputs to device
            anchor_input = {k: v.squeeze(1).to(self.device) for k, v in batch['anchor'].items()}
            positive_input = {k: v.squeeze(1).to(self.device) for k, v in batch['positive'].items()}
            negative_input = {k: v.squeeze(1).to(self.device) for k, v in batch['negative'].items()}
            
            # Get embeddings
            anchor_emb = self.model(**anchor_input).last_hidden_state[:, 0, :]
            positive_emb = self.model(**positive_input).last_hidden_state[:, 0, :]
            negative_emb = self.model(**negative_input).last_hidden_state[:, 0, :]
            
            # Compute loss
            loss = self.criterion(anchor_emb, positive_emb, negative_emb)
            
            # Backpropagate
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(dataloader)
    
    def save_model(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

def main():
    # Configuration
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    BATCH_SIZE = 8
    NUM_EPOCHS = 3
    OUTPUT_DIR = "trained_embeddings"
    
    # Initialize trainer
    trainer = EmbeddingTrainer(MODEL_NAME)
    
    # Load dataset
    dataset = TripletDataset(
        "training_data/training_tuples.json",
        trainer.tokenizer
    )
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # Training loop
    print("Starting training...")
    for epoch in range(NUM_EPOCHS):
        avg_loss = trainer.train_epoch(dataloader)
        print(f"Epoch {epoch+1}/{NUM_EPOCHS}, Average Loss: {avg_loss:.4f}")
    
    # Save the model
    trainer.save_model(OUTPUT_DIR)
    print(f"Model saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()