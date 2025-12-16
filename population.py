import config
from bird import *
import math
import species
import operator


class Population:
    def __init__(self, size):
        self.birds = []
        self.generation = 1
        self.species = []
        self.size = size
        for i in range(0, self.size):
            self.birds.append(Bird())

    def update_live_birds(self, draw_vision = False, manual = False):
        for b in self.birds:
            if b.alive:
                b.look(draw_vision)
                if not manual:
                    b.think()
                b.draw(config.window)
                b.update(config.ground)

    def natural_selection(self):
        self.speciate()
        self.calculate_fitness()
        self.kill_extinct_species()
        self.kill_stale_species()
        self.sort_species_by_fitness()
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.birds = []

        for b in self.birds:
            add_to_species = False
            for s in self.species:
                if s.similarity(b.brain):
                    s.add_to_species(b)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(b))

    def calculate_fitness(self):
        for b in self.birds:
            b.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        species_bin = []
        for s in self.species:
            if len(s.birds) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        bird_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for b in s.birds:
                        bird_bin.append(b)
                else:
                    s.staleness = 0
        for b in bird_bin:
            self.birds.remove(b)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_birds_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []
        for s in self.species:
            children.append(s.champion.clone())
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.birds = []
        for child in children:
            self.birds.append(child)
        self.generation += 1

    def extinct(self):
        extinct = True
        for b in self.birds:
            if b.alive:
                extinct = False
        return extinct











