#
#
# import os
# import torch
# import cv2
# import numpy as np
# from .UnetLight import unet_model  # Ensure this module is available
# import math
# import torch.nn.functional as F
# def load_model(weights_path):
#     """Load the U-Net model with the given weights."""
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = unet_model(out_channels=3).to(device)
#     Test_checkpoint_iou = torch.load('best.pt', map_location=torch.device(device))
#     model.load_state_dict(Test_checkpoint_iou['model_state_dict'])
#     model.eval()
#     return model, device
#
# def preprocess_image(image_path):
#     """Read and preprocess the input image."""
#     image = cv2.imread(image_path, cv2.IMREAD_COLOR)
#     if image is None:
#         raise FileNotFoundError(f"Image not found: {image_path}")
#     return image
#
# def inference(model, image_path, tile_size=512, tile_pad=0):
#     img = cv2.imread(image_path)
#     height, width,channel = img.shape
#     output_height = height
#     output_width = width
#     # start with black image
#
#     tiles_x = math.ceil(width / tile_size)
#     tiles_y = math.ceil(height / tile_size)
#     output = np.zeros((output_height,output_width))
#     # loop over all tiles
#     for y in range(tiles_y):
#         for x in range(tiles_x):
#     #         # extract tile from input image
#             ofs_x = x * tile_size
#             ofs_y = y * tile_size
#             # input tile area on total image
#             input_start_x = ofs_x
#             input_end_x = min(ofs_x + tile_size, width)
#             input_start_y = ofs_y
#             input_end_y = min(ofs_y + tile_size, height)
#
#             # input tile area on total image with padding
#             input_start_x_pad = max(input_start_x - tile_pad, 0)
#             input_end_x_pad = min(input_end_x + tile_pad, width)
#             input_start_y_pad = max(input_start_y - tile_pad, 0)
#             input_end_y_pad = min(input_end_y + tile_pad, height)
#
#             # input tile dimensions
#             input_tile_width = input_end_x - input_start_x
#             input_tile_height = input_end_y - input_start_y
#             tile_idx = y * tiles_x + x + 1
#             input_tile = img[  input_start_y_pad:input_end_y_pad, input_start_x_pad:input_end_x_pad,:]
#
#
#             input_tile = 2 * ((input_tile - input_tile.min()) / (input_tile.max() - input_tile.min())) - 1
#             input_tile =np.float32(input_tile)
#
#             input_tile = torch.from_numpy(input_tile)
#             input_tile = torch.permute(input_tile,(2,0,1))
#
#             input_tile = torch.unsqueeze(input_tile,dim=0)
#             # print("input_tile",input_tile.shape)
#             if input_tile.shape[-1] == tile_size and input_tile.shape[-2]==tile_size:
#                 with torch.no_grad():
#                     output_tile = model(input_tile)
#                     preds = torch.argmax(F.softmax(output_tile), dim=1)[0]
#             else:
#                 preds = torch.zeros((tile_size,tile_size))
#             # output tile area on total image
#             output_start_x = input_start_x
#             output_end_x = input_end_x
#             output_start_y = input_start_y
#             output_end_y = input_end_y
#
#             # output tile area without padding
#             output_start_x_tile = (input_start_x - input_start_x_pad)
#             output_end_x_tile = output_start_x_tile + input_tile_width
#             output_start_y_tile = (input_start_y - input_start_y_pad)
#             output_end_y_tile = output_start_y_tile + input_tile_height
#
#             # put tile into output image
#             output[output_start_y:output_end_y,
#             output_start_x:output_end_x] = preds[output_start_y_tile:output_end_y_tile, output_start_x_tile:output_end_x_tile]
#     return output
#
# def save_output(output,output_path):
#     """Save the model's output as an image."""
#     output_image = (output * 255).astype(np.uint8)  # Scale to [0, 255]
#     cv2.imwrite(output_path, output_image)
#     output[output == 1] = 255
#     output[output == 2] = 128
#     output = np.uint8(output)
#     output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
#     cv2.imwrite(output_path,output)
#
# def main(weights_path, image_path, output_path):
#     """Main function to load model, process image, and save output."""
#     model, device = load_model(weights_path)
#     output = inference(model, image_path)
#     save_output(output,output_path)
#
# if __name__ == "__main__":
#     import argparse
#
#     parser = argparse.ArgumentParser(description="Run inference and save visualization.")
#     parser.add_argument("--weights", required=True, help="Path to model weights.")
#     parser.add_argument("--image", required=True, help="Path to input image.")
#     parser.add_argument("--output", required=True, help="Path to save output image.")
#
#     args = parser.parse_args()
#     main(args.weights, args.image, args.output)
