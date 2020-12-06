import random
import itertools
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from keras import backend as K
from keras.models import load_model


class SignatureVerification:
    def __init__(self, currentWorkingDir, originalSign, sign):
        self.img_h = 155
        self.img_w = 220
        self.currentWorkingDir = currentWorkingDir
        self.originalSign = originalSign
        self.sign = sign

    def euclidean_distance(self, vects):
        """Compute Euclidean Distance between two vectors"""
        x, y = vects
        return K.sqrt(K.sum(K.square(x - y), axis=1, keepdims=True))

    def eucl_dist_output_shape(self, shapes):
        shape1, shape2 = shapes
        return (shape1[0], 1)

    def contrastive_loss(self, y_true, y_pred):
        """Contrastive loss from Hadsell-et-al.'06
        http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
        """
        margin = 1
        return K.mean(
            y_true * K.square(y_pred)
            + (1 - y_true) * K.square(K.maximum(margin - y_pred, 0))
        )

    def generate_batch(self, orig_groups, forg_groups, batch_size=32):
        """Function to generate a batch of data with batch_size number of data points
        Half of the data points will be Genuine-Genuine pairs and half will be Genuine-Forged pairs"""
        while True:
            orig_pairs = []
            forg_pairs = []
            gen_gen_labels = []
            gen_for_labels = []
            all_pairs = []
            all_labels = []

            # Here we create pairs of Genuine-Genuine image names and Genuine-Forged image names
            # For every person we have 24 genuine signatures, hence we have
            # 24 choose 2 = 276 Genuine-Genuine image pairs for one person.
            # To make Genuine-Forged pairs, we pair every Genuine signature of a person
            # with 12 randomly sampled Forged signatures of the same person.
            # Thus we make 24 * 12 = 300 Genuine-Forged image pairs for one person.
            # In all we have 120 person's data in the training data.
            # Total no. of Genuine-Genuine pairs = 120 * 276 = 33120
            # Total number of Genuine-Forged pairs = 120 * 300 = 36000
            # Total no. of data points = 33120 + 36000 = 69120

            for orig, forg in zip(orig_groups, forg_groups):
                orig_pairs.extend(list(itertools.combinations(orig, 2)))
                for i in range(len(forg)):
                    forg_pairs.extend(
                        list(itertools.product(orig[i : i + 1], random.sample(forg, 1)))
                    )

            # Label for Genuine-Genuine pairs is 1
            # Label for Genuine-Forged pairs is 0
            gen_gen_labels = [1] * len(orig_pairs)
            gen_for_labels = [0] * len(forg_pairs)

            # Concatenate all the pairs together along with their labels and shuffle them
            all_pairs = orig_pairs + forg_pairs
            all_labels = gen_gen_labels + gen_for_labels
            del orig_pairs, forg_pairs, gen_gen_labels, gen_for_labels
            all_pairs, all_labels = shuffle(all_pairs, all_labels)

            # Note the lists above contain only the image names and
            # actual images are loaded and yielded below in batches
            # Below we prepare a batch of data points and yield the batch
            # In each batch we load "batch_size" number of image pairs
            # These images are then removed from the original set so that
            # they are not added again in the next batch.

            k = 0
            pairs = [
                np.zeros((batch_size, self.img_h, self.img_w, 1)) for i in range(2)
            ]
            targets = np.zeros((batch_size,))
            for ix, pair in enumerate(all_pairs):
                img1 = cv2.imread(pair[0], 0)
                img2 = cv2.imread(pair[1], 0)
                img1 = cv2.resize(img1, (self.img_w, self.img_h))
                img2 = cv2.resize(img2, (self.img_w, self.img_h))
                img1 = np.array(img1, dtype=np.float64)
                img2 = np.array(img2, dtype=np.float64)
                for i in range(img1.shape[0]):
                    for j in range(img1.shape[1]):
                        pixel = img1.item(i, j)
                        if pixel > 130:
                            img1[i][j] = 255
                        else:
                            img1[i][j] = 0

                for i in range(img2.shape[0]):
                    for j in range(img2.shape[1]):
                        pixel = img2.item(i, j)
                        if pixel > 150:
                            img2[i][j] = 255
                        else:
                            img2[i][j] = 0
                img1 /= 255
                img2 /= 255
                img1 = img1[..., np.newaxis]
                img2 = img2[..., np.newaxis]
                pairs[0][k, :, :, :] = img1
                pairs[1][k, :, :, :] = img2
                targets[k] = all_labels[ix]
                k += 1
                if k == batch_size:
                    yield pairs, targets
                k = 0
                pairs = [
                    np.zeros((batch_size, self.img_h, self.img_w, 1)) for i in range(2)
                ]
                targets = np.zeros((batch_size,))
                # print(img1.shape)

    def verifySignature(self):
        model = load_model(
            self.currentWorkingDir + "/trained.h5",
            custom_objects={"contrastive_loss": self.contrastive_loss},
        )
        threshold = 0.1
        test_gen1 = self.generate_batch(
            [[self.originalSign]],
            [[self.sign]],
            1,
        )
        test_point, test_label = next(test_gen1)
        img1 = test_point[0]
        img2 = test_point[1]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
        ax1.imshow(np.squeeze(img1), cmap="gray")
        ax2.imshow(np.squeeze(img2), cmap="gray")
        result = model.predict([img1, img2])
        ax1.set_title("Signature in Database")
        ax2.set_title("Given Cheque Signature")
        ax1.axis("off")
        ax2.axis("off")
        plt.show()

        diff = result[0][0]
        # print("Difference Score = ", diff)
        if diff > threshold:
            # print("Forged Signature")
            return 1
        else:
            # print("Genuine Signature")
            return 0
