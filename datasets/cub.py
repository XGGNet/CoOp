import os
import pickle

from dassl.data.datasets import DATASET_REGISTRY, Datum, DatasetBase
from dassl.utils import mkdir_if_missing

from .oxford_pets import OxfordPets
from .dtd import DescribableTextures as DTD

from pdb import set_trace as st

import random
from collections import defaultdict


@DATASET_REGISTRY.register()
class CUB(DatasetBase):

    dataset_dir = "CUB_200_2011"

    def __init__(self, cfg):
        root = os.path.abspath(os.path.expanduser(cfg.DATASET.ROOT))
        self.dataset_dir = os.path.join(root, self.dataset_dir)
        self.image_dir = os.path.join(self.dataset_dir, "images")
        self.split_path = os.path.join(self.dataset_dir, "split_li_cub.json")
        self.split_fewshot_dir = os.path.join(self.dataset_dir, "split_fewshot")
        mkdir_if_missing(self.split_fewshot_dir)


        if os.path.exists(self.split_path):
            train, val, test = OxfordPets.read_split(self.split_path, self.dataset_dir)
        else:
            # trainval = self.read_data(split_file="trainval.txt")

            # train-test split
            self.split_ids= {'train':[],'test':[]}
            with open( os.path.join(self.dataset_dir, 'train_test_split.txt'), 'r') as in_file:
                for line in in_file:
                    idx, use_train = line.strip('\n').split(' ', 2)
                    if int(use_train) == 1:
                        self.split_ids['train'].append(int(idx))
                    else:
                        self.split_ids['test'].append(int(idx))

            # obtain filenames of images
            self.image_id2paths = {}
            with open(os.path.join(self.dataset_dir, 'images.txt'), 'r') as in_file:
                for line in  in_file:
                    idx, fn = line.strip('\n').split(' ', 2)
                    self.image_id2paths[int(idx)] = os.path.join(self.image_dir,fn)
            
            self.label_names = {}
            with open(os.path.join(self.dataset_dir, 'classes.txt'), 'r') as in_file:
                for line in in_file:
                    cls_id, fn = line.strip('\n').split(' ', 2)
                    self.label_names[int(cls_id)] = fn
            
            self.image_id2labels = {}
            with open(os.path.join(self.dataset_dir, 'image_class_labels.txt'), 'r') as in_file:
                for line in  in_file:
                    idx, fn = line.strip('\n').split(' ', 2)
                    self.image_id2labels[int(idx)] = int(fn)
            

            train, val, test = self.process_data()
            OxfordPets.save_split(train, val, test, self.split_path, self.dataset_dir)


        num_shots = cfg.DATASET.NUM_SHOTS
        if num_shots >= 1:
            seed = cfg.SEED
            preprocessed = os.path.join(self.split_fewshot_dir, f"shot_{num_shots}-seed_{seed}.pkl")
            
            if os.path.exists(preprocessed):
                print(f"Loading preprocessed few-shot data from {preprocessed}")
                with open(preprocessed, "rb") as file:
                    data = pickle.load(file)
                    train, val = data["train"], data["val"]
            else:
                train = self.generate_fewshot_dataset(train, num_shots=num_shots)
                val = self.generate_fewshot_dataset(val, num_shots=min(num_shots, 4))
                data = {"train": train, "val": val}
                print(f"Saving preprocessed few-shot data to {preprocessed}")
                with open(preprocessed, "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

        subsample = cfg.DATASET.SUBSAMPLE_CLASSES
        train, val, test = OxfordPets.subsample_classes(train, val, test, subsample=subsample)

        super().__init__(train_x=train, val=val, test=test)
    

    def process_data(self):
        items = []

        train_val_ids = self.split_ids['train']
        test_ids = self.split_ids['test']

        p_val = 0.2
        p_trn = 1 - p_val
        print(f"Splitting trainval into {p_trn:.0%} train and {p_val:.0%} val")

        n_val = round(len(train_val_ids) * p_val)
        random.shuffle(train_val_ids)
        assert n_val > 0

        val_ids = train_val_ids[:n_val]
        train_ids = train_val_ids[n_val:]


        train = []
        for id in train_ids:
            impath =  self.image_id2paths[id]
            label = self.image_id2labels[id] 
            classname = self.label_names[ label]

   
            modified_label = label-1
            item = Datum(impath=impath, label=int(modified_label), classname=classname)

            train.append(item)

        val = []
        for id in val_ids:
            impath =  self.image_id2paths[id]
            label = self.image_id2labels[id] 
            classname = self.label_names[ label]
            
            modified_label = label-1
            item = Datum(impath=impath, label=int(modified_label), classname=classname)

            val.append(item)

        test = []
        for id in test_ids:
            impath =  self.image_id2paths[id]
            label = self.image_id2labels[id] 
            classname = self.label_names[ label]
            
            modified_label = label-1
            item = Datum(impath=impath, label=int(modified_label), classname=classname)

            test.append(item)

        return train, val, test



