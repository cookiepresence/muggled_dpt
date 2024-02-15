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
    
    Based on code from Depth-Anything/facebookresearch:
        @ https://github.com/LiheYoung/Depth-Anything/blob/e7ef4b4b7a0afd8a05ce9564f04c1e5b68268516/torchhub/facebookresearch_dinov2_main/dinov2/layers/patch_embed.py#L26
    
    Purpose is to take input images and convert them to 'lists' of (1D) tokens,
    one token for each (14x14 default) image patch.
    '''
    
    # .................................................................................................................
    
    def __init__(self, features_per_token, patch_size_px=14, num_input_channels=3, bias=True):
        
        # Inherit from parent
        super().__init__()
        
        # Both grouping + linear transformation is handled with a single strided convolution step!
        self.proj = nn.Conv2d(
            num_input_channels,
            features_per_token,
            kernel_size=patch_size_px,
            stride=patch_size_px,
            bias=bias,
        )

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
        # -> result has shape: BxFxhxw, where F is features per token, h & w are the patch grid height & width
        output = self.proj(image_tensor_bchw)
        
        # Convert from image-like shape to 'rows of tokens' shape
        # -> result has shape: BxNxF
        patch_grid_hw = output.shape[2:]
        output = output.flatten(2).transpose(1, 2)
        
        return output, patch_grid_hw
    
    # .................................................................................................................
