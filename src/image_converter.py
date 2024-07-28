#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: A.Akdogan
"""

import os
import cv2
from pathlib import Path


class ImageConverter:

    def __init__(self, row, col):

        self.row = row
        self.col = col

    @staticmethod
    def get_final_path(sub_count, join_list):
    
        path = os.path.dirname(os.path.realpath(__file__))
        for i in range(sub_count):path = os.path.dirname(os.path.normpath(path))
        for i in range(len(join_list)):path = os.path.join(path, join_list[i])
        
        return path

    def converter(self, files, base_folder, dest_folder, tp):
        
        Path(os.path.join(dest_folder, tp)).mkdir(parents=True, exist_ok=True)
        for i in range(len(files)):
            
            if files[i].split('.')[1] == 'jpg' or files[i].split('.')[1] == 'JPG' or files[i].split('.')[1] == 'jpeg' or files[i].split('.')[1] == 'JPEG' or files[i].split('.')[1] == 'png' or files[i].split('.')[1] == 'PNG':
                
                img_path = os.path.join(base_folder, tp, files[i])
                print(img_path)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                #print(img)
  
                # Resize
                border_v = 0
                border_h = 0
                IMG_COL = self.col
                IMG_ROW = self.row
                if (IMG_COL/IMG_ROW) >= (img.shape[0]/img.shape[1]):
                    border_v = int((((IMG_COL/IMG_ROW)*img.shape[1])-img.shape[0])/2)
                else:
                    border_h = int((((IMG_ROW/IMG_COL)*img.shape[0])-img.shape[1])/2)
                img = cv2.copyMakeBorder(img, border_v, border_v, border_h, border_h, cv2.BORDER_CONSTANT, 0)
                img = cv2.resize(img, (IMG_ROW, IMG_COL))
                save_filename = os.path.join(dest_folder, tp, files[i])
                cv2.imwrite(save_filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                print(i)
                
                pass
            else:
                pass

    def main(self):

        raw_base_path = ImageConverter.get_final_path(1, ['dataset', 'raw'])
        processed_base_path = ImageConverter.get_final_path(1, ['dataset', 'processed'])

        train_folder = os.path.join(raw_base_path, 'train')
        test_folder = os.path.join(raw_base_path, 'test')
        val_folder = os.path.join(raw_base_path, 'val')
        train_masks_folder = os.path.join(raw_base_path, 'train_masks')
        test_masks_folder = os.path.join(raw_base_path, 'test_masks')
        val_masks_folder = os.path.join(raw_base_path, 'val_masks')

        train_files = os.listdir(train_folder)
        test_files = os.listdir(test_folder)
        val_files = os.listdir(val_folder)
        train_masks_files = os.listdir(train_masks_folder)
        test_masks_files = os.listdir(test_masks_folder)
        val_masks_files = os.listdir(val_masks_folder)

        self.converter(train_files, raw_base_path, processed_base_path, 'train')
        self.converter(test_files, raw_base_path, processed_base_path, 'test')
        self.converter(val_files, raw_base_path, processed_base_path, 'val')
        self.converter(train_masks_files, raw_base_path, processed_base_path, 'train_masks')
        self.converter(test_masks_files, raw_base_path, processed_base_path, 'test_masks')
        self.converter(val_masks_files, raw_base_path, processed_base_path, 'val_masks')

        return
    
if __name__ == '__main__':

    ImageConverter(800,800).main()
