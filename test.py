import ray
from ray.rllib.agents.ppo import PPOTrainer

if __name__ == '__main__':
    ray.init()
    trainer = PPOTrainer(env='CartPole-v0')
    results = trainer.train()
    print(results)
