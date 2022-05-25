from __future__ import print_function
import os
import neat
import visualize
import posgen
import numpy as np
import tqdm

# 2-input XOR inputs and expected outputs.
class io():

    def __init__(self):
        self.xori = None
        self.xoro = None
        self.run = 0
        self.database = []
        self.nchm = 0
        pbar = tqdm.tqdm(total = 1768 * 2)
        

        while len(self.database)<1768:
            y = posgen.psgenesis((0.5/5000)*self.nchm + 0.5) 
            if (len(self.database) - self.nchm) < 1768:
                self.database.append(y)
                pbar.update()
            elif not y.is_checkmate() and self.nchm < 5000:
                self.database.append(y)
                self.nchm += 1
                pbar.update()



    def fget(self):

        questions = np.random.choice(self.database, size=10)

        preproxoro = [x.is_checkmate() for x in questions]
        proxoro = []
        for z in preproxoro:
            if z:
                proxoro.append((1.0,))
            else:
                proxoro.append((0.0,))
        self.xoro = proxoro

        mapq = [posgen.map(u) for u in questions ]
        self.run += 1
        self.xori = mapq
        return mapq


    def fset(self, value):
        self.xori = value 


    xorip = property(fget, fset)

I = io()

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(I.xorip, I.xoro):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0]) ** 2


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(I.xorip, I.xoro):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)