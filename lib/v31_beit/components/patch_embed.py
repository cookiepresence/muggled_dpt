#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---------------------------------------------------------------------------------------------------------------------
#%% Imports

import torch.nn as nn


# ---------------------------------------------------------------------------------------------------------------------
#%% Classes


class PatchEmbed(nn.Module):
    
    '''
    Simplified implementation of the patch embedding step for:
        "Vision Transformers for Dense Prediction"
        By: René Ranftl, Alexey Bochkovskiy, Vladlen Koltun
        @ https://arxiv.org/abs/2103.13413
    
    Based on code from timm library:
        @ https://github.com/huggingface/pytorch-image-models/blob/main/timm/layers/patch_embed.py
    
    Purpose is to take input images and convert them to 'lists' of (1D) tokens,
    one token for each (16x16 default) image patch.
    '''
    
    # .................................................................................................................
    
    
    def __init__(self, features_per_token, patch_size_px=16, num_input_channels=3, bias=True):
        
        # Inherit from parent
        super().__init__()
        
        # Store config for inspection, if needed
        self.patch_size_px = patch_size_px
        self.features_per_token = features_per_token
        
        self.proj = nn.Conv2d(num_input_channels, features_per_token,
                              kernel_size=patch_size_px, stride=patch_size_px, bias=bias)

    # .................................................................................................................
    
    def forward(self, image_tensor_bchw):
        
        '''
        Projects & reshapes image tensor: BxCxHxW -> BxNxF
            -> Where B is batch size
            -> C is image channels (i.e. 3 for RGB image)
            -> H, W are the height & width of the image
            -> N is the number of tokens (equal to number of image patches)
            -> F is the number of features per token
        '''
        
        # Convert image width/height to patch grid width/height, and image channels to feature count
        output = self.proj(image_tensor_bchw)
        
        # Convert tensor shape: BxFxHxW -> BxNxF (N tokens, F features per token, H & W are patch grid size)
        patch_grid_hw = output.shape[2:]
        output = output.flatten(2).transpose(1, 2)
        
        return output, patch_grid_hw
    
    # .................................................................................................................


# ---------------------------------------------------------------------------------------------------------------------
#%% Functions

