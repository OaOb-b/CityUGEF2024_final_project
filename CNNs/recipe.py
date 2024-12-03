# %%
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import utils, models, layers, optimizers, losses, callbacks
import matplotlib.pyplot as plt
import seaborn as sns

# %%
print('Versions')
print('numpy:', np.__version__)
print('pandas:', pd.__version__)
print('kreas:', tf.keras.__version__)

sns.set_theme()

# %%