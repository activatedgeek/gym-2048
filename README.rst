Gym 2048
=========

.. image:: https://travis-ci.com/activatedgeek/gym-2048.svg?branch=master
    :target: https://travis-ci.com/activatedgeek/gym-2048

.. image:: https://badge.fury.io/py/gym-2048.svg
    :target: https://pypi.org/project/gym-2048/

This package implements the classic grid game 2048
for OpenAI gym environment.

Install
--------

.. code:: shell

    pip install gym-2048

Environment(s)
---------------

The package currently contains two environments

- ``Tiny2048-v0``: A ``2 x 2`` grid game.
- ``2048-v0``: The standard ``4 x 4`` grid game.


Attributes
^^^^^^^^^^^

- **Observation**: All observations are ``n x n`` numpy arrays
  representing the grid. The array is ``0`` for empty locations
  and numbered ``2, 4, 8, ...`` wherever the tiles are placed.

- **Actions**: There are four actions defined by integers.
    - ``LEFT = 0``
    - ``UP = 1``
    - ``RIGHT = 2``
    - ``DOWN = 3``

- **Reward**: Reward is the total score obtained by merging any
  potential tiles for a given action. Score obtained by merging
  two tiles is simply the sum of values of those two tiles.

Rendering
^^^^^^^^^^

Currently only basic print rendering (``mode='human'``) is supported.
Graphic rendering support is coming soon.

Usage
------

Here is a sample rollout of the game which follows the same API as
OpenAI ``gym.Env``.

.. code:: python

    import gym_2048
    import gym


    if __name__ == '__main__':
      env = gym.make('2048-v0')
      env.seed(42)

      env.reset()
      env.render()

      done = False
      moves = 0
      while not done:
        action = env.np_random.choice(range(4), 1).item()
        next_state, reward, done, info = env.step(action)
        moves += 1

        print('Next Action: "{}"\n\nReward: {}'.format(
          gym_2048.Base2048Env.ACTION_STRING[action], reward))
        env.render()

      print('\nTotal Moves: {}'.format(moves))


**NOTE**: Top level ``import gym_2048`` is needed to ensure registration with
``Gym``.
