import numpy as np
import gym
import gym.spaces as spaces
from gym.utils import seeding


class Base2048Env(gym.Env):
  metadata = {
    'render.modes': ['human'],
  }

  LEFT = 0
  UP = 1
  RIGHT = 2
  DOWN = 3

  def __init__(self, width = 4, height = 4):
    self.width = width
    self.height = height

    self.observation_space = spaces.Box(low=2,
                                        high=2**32,
                                        shape=(self.width, self.height),
                                        dtype=np.int64)
    self.action_space = spaces.Discrete(4)

    # Internal Variables
    self.board = None
    self.np_random = None

    self.seed()
    self.reset()

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def step(self, action: int):
    """Rotate board aligned with left action"""

    # Align board action with left action
    rotated_obs = np.rot90(self.board, k=action)
    reward, updated_obs = self._slide_left_and_merge(rotated_obs)
    self.board = np.rot90(updated_obs, k=4 - action)

    # Place one random tile on empty location
    self._place_random_tiles(self.board, count=1)

    done = self.is_done()

    return self.board, reward, done, {}

  def is_done(self):
    copy_board = self.board.copy()

    if not copy_board.all():
      return False

    for action in [0, 1, 2, 3]:
      rotated_obs = np.rot90(copy_board, k=action)
      _, updated_obs = self._slide_left_and_merge(rotated_obs)
      if not updated_obs.all():
        return False

    return True


  def reset(self):
    """Place 2 tiles on empty board."""

    self.board = np.zeros((self.width, self.height), dtype=np.int64)
    self._place_random_tiles(self.board, count=2)

  def render(self, mode='human'):
    if mode == 'human':
      for row in self.board.tolist():
        print(' \t'.join(map(lambda tile: str(tile), row)))

  def _sample_tiles(self, count = 1):
    """Sample tile 2 or 4."""

    choices = [2, 4]
    probs = [0.9, 0.1]

    tiles = self.np_random.choice(choices,
                                  size=count,
                                  p=probs)
    return tiles.tolist()

  def _sample_tile_locations(self, board, count = 1):
    """Sample grid locations with no tile."""

    zero_locs = np.argwhere(board == 0)
    zero_indices = self.np_random.choice(
        len(zero_locs), size=count)

    zero_pos = zero_locs[zero_indices]
    zero_pos = list(zip(*zero_pos))
    return zero_pos

  def _place_random_tiles(self, board, count = 1):
    if not board.all():
      tiles = self._sample_tiles(count)
      tile_locs = self._sample_tile_locations(board, count)
      board[tile_locs] = tiles

  def _slide_left_and_merge(self, board):
    """Slide tiles on a grid to the left and merge."""

    result = []

    score = 0
    for row in board:
      row = np.extract(row > 0, row)
      score_, result_row = self._try_merge(row)
      score += score_
      row = np.pad(np.array(result_row), (0, self.width - len(result_row)),
                   'constant', constant_values=(0,))
      result.append(row)

    return score, np.array(result, dtype=np.int64)

  @staticmethod
  def _try_merge(row):
    score = 0
    result_row = []

    i = 1
    while i < len(row):
      if row[i] == row[i - 1]:
        score += row[i] + row[i - 1]
        result_row.append(row[i] + row[i - 1])
        i += 2
      else:
        result_row.append(row[i - 1])
        i += 1

    if i == len(row):
      result_row.append(row[i - 1])

    return score, result_row
