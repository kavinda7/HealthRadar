import torch
import torch.nn as nn

# --- 1. Health Data Model (LSTM) ---
class HealthEncoder(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        
    def forward(self, x):  # x: [batch, seq_len, input_dim]
        _, (h_n, _) = self.lstm(x)
        return h_n[-1]  # [batch, hidden_dim]

# --- 2. Satellite Data Model (CNN) ---
class SatelliteEncoder(nn.Module):
    def __init__(self, input_channels, hidden_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.fc = nn.Linear(32, hidden_dim)

    def forward(self, x):  # x: [batch, C, H, W]
        x = self.encoder(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)  # [batch, hidden_dim]

# --- 3. Fusion + Classification ---
class HybridFusionModel(nn.Module):
    def __init__(self, health_input_dim, sat_input_channels, embed_dim, num_classes):
        super().__init__()
        self.health_encoder = HealthEncoder(health_input_dim, embed_dim)
        self.sat_encoder = SatelliteEncoder(sat_input_channels, embed_dim)
        self.classifier = nn.Sequential(
            nn.Linear(embed_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )

    def forward(self, health_ts, sat_img):
        h_embed = self.health_encoder(health_ts)
        s_embed = self.sat_encoder(sat_img)
        fused = torch.cat([h_embed, s_embed], dim=1)
        return self.classifier(fused)


# Dummy input
model = HybridFusionModel(2, 2, 16, 2)
health_data = torch.randn(2, 12, 2)
satellite_data = torch.randn(2, 2, 16, 16)

with torch.no_grad():
    output = model(health_data, satellite_data)
    print("Logits:", output)
    print("Predicted class:", torch.argmax(output, dim=1))