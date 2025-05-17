import torch
import torch.nn as nn

class HealthEncoder(nn.Module):
    def __init__(self, input_dim, embed_dim):
        super().__init__()
        self.gru = nn.GRU(input_dim, embed_dim, batch_first=True)

    def forward(self, x):  # [B, T, F]
        _, h_n = self.gru(x)
        return h_n.squeeze(0)  # [B, embed_dim]

class Satellite3DEncoder(nn.Module):
    def __init__(self, input_channels, embed_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv3d(input_channels, 16, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool3d((1, 2, 2)),
            nn.Conv3d(16, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool3d((1, 1, 1))
        )
        self.fc = nn.Linear(32, embed_dim)

    def forward(self, x):  # [B, C, T, H, W]
        x = self.encoder(x)  # → [B, 32, 1, 1, 1]
        x = x.view(x.size(0), -1)  # → [B, 32]
        return self.fc(x)  # → [B, embed_dim]

class HybridFusionModel(nn.Module):
    def __init__(self, health_input_dim, sat_input_channels, embed_dim, num_classes):
        super().__init__()
        self.health_encoder = HealthEncoder(health_input_dim, embed_dim)
        self.sat_encoder = Satellite3DEncoder(sat_input_channels, embed_dim)
        self.classifier = nn.Sequential(
            nn.Linear(embed_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )

    def forward(self, health_ts, sat_seq):  
        # health_ts: [B, T_h, F]  
        # sat_seq:   [B, C, T_s, H, W]
        h_embed = self.health_encoder(health_ts)
        s_embed = self.sat_encoder(sat_seq)
        fused = torch.cat([h_embed, s_embed], dim=1)
        return self.classifier(fused)
