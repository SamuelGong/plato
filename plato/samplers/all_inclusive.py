"""
Samples all the data from a dataset. Applicable in cases where the dataset comes from
local sources only. Used by the Federated EMNIST dataset and the MistNet server.
"""

from plato.samplers import base
from plato.config import Config


class Sampler(base.Sampler):
    """Create a data sampler that samples all the data in the dataset.
       Used by the MistNet server.
    """
    def __init__(self, dataset, client_id=0):
        super().__init__()
        self.client_id = client_id

        self.all_inclusive = range(dataset.num_train_examples())

    def get(self):
        # return random.shuffle(self.all_inclusive)
        if hasattr(Config().trainer, 'use_mindspore'):
            return list(self.all_inclusive)
        elif hasattr(Config().trainer, 'use_tensorflow'):
            return list(self.all_inclusive)
        else:
            from torch.utils.data import SubsetRandomSampler
            return SubsetRandomSampler(self.all_inclusive)

    def trainset_size(self):
        """Returns the length of the dataset after sampling. """
        return len(self.all_inclusive)
