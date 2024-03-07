from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

import numpy as np
import gymnasium as gym


class BaseEnv(gym.Env):
    robot = None
    sim = None
    task = None

    def __init__(self) -> None:
        observation, _ = self.reset()

        robot_pos_shape = observation["robot_pos"].shape
        obstacle_dist_shape = observation["obstacle_dist"].shape
        achieved_goal_shape = observation["achieved_goal"].shape
        desired_goal_shape = observation["achieved_goal"].shape

        self.observation_space = gym.spaces.Dict(
            dict(
                robot_pos=gym.spaces.Box(-10.0, 10.0, shape=robot_pos_shape, dtype=np.float32),
                obstacle_dist=gym.spaces.Box(-10.0, 10.0, shape=obstacle_dist_shape, dtype=np.float32),
                desired_goal=gym.spaces.Box(-10.0, 10.0, shape=achieved_goal_shape, dtype=np.float32),
                achieved_goal=gym.spaces.Box(-10.0, 10.0, shape=desired_goal_shape, dtype=np.float32),
            )
        )

        self.action_space = self.robot.action_space
        self.compute_reward = self.task.compute_reward
        self._saved_goal = dict()

    def _get_obs(self) -> Dict[str, np.ndarray]:
        robot_pos = self.robot.get_obs().astype(np.float32)
        obstacle_dist = self.sim.get_distances().astype(np.float32)
        achieved_goal = self.task.get_achieved_goal().astype(np.float32)
        desired_goal = self.task.get_goal().astype(np.float32)
        return {
            "robot_pos": robot_pos,
            "obstacle_dist": obstacle_dist,
            "achieved_goal": achieved_goal,
            "desired_goal": desired_goal,
        }

    def reset(
        self, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
        return NotImplemented

    def step(self, action: np.ndarray) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict[str, Any]]:
        return NotImplemented

    def close(self):
        return NotImplemented

    def render(self) -> Optional[np.ndarray]:
        return NotImplemented