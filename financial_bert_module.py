import torch
from torch import nn
from transformers import BertModel, BertTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

class FinBERTRegressor(nn.Module):
    def __init__(self, finbert_model_name="ProsusAI/finbert", hidden_size=768, output_size=1):
        super(FinBERTRegressor, self).__init__()
        # Load the FinBERT model
        self.finbert = BertModel.from_pretrained(finbert_model_name)

        # Regression layer
        self.regressor = nn.Linear(hidden_size, output_size)

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        # Get embeddings from FinBERT
        with torch.no_grad():  # No need to calculate gradients for FinBERT
            outputs = self.finbert(input_ids=input_ids, attention_mask=attention_mask)

        # We use the [CLS] token's embedding for regression
        cls_embedding = outputs.last_hidden_state[:, 0, :]

        # Pass through the regression layer
        return self.regressor(cls_embedding)

if not ('model' in globals()):
    model = FinBERTRegressor()
    model.to(device)
    model.regressor.load_state_dict(torch.load('model_regressor_weight_v2.pth', map_location=torch.device('cpu')))
if not ('tokenizer' in globals()):
    tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")

def predict_monthly_stock_price_change_rate(text: str):
    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Move the inputs to the same device as the model
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate output
    output = model(**inputs)

    return output.item()


'''
FinBERT is a variant of BERT pre-trained on financial data, making it particularly good at understanding financial text.

Model Definition:
Load FinBERT, a BERT variant specialized in financial text.
Add a regression layer to predict stock price changes.

Load Pre-trained Components:
Initialize the model and load pre-trained weights.
Load the tokenizer for FinBERT to convert text into model-friendly tokens.

Prediction Process:
Input: Take a financial text (e.g., news headline).
Tokenization: Convert text to tokens using FinBERT's tokenizer.
Model Inference: Use FinBERT to get embeddings, then apply the regression layer.
Output: Return a predicted stock price change rate (e.g., 0.03 for a 3% increase).


'''