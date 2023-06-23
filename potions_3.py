import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from random import choice, poissonvariate, randint

class Ingredient(ABC):
    quality_options = ['normal', 'premium', 'legendary']
    quality_costs = {'normal': 1, 'premium': 3, 'legendary': 5}

    def __init__(self, quantity, quality):
        self.quantity = quantity
        self.quality = quality

    @abstractmethod
    def get_name(self):
        pass

    def get_cost(self):
        return self.quantity * self.quality_costs[self.quality]

class Herb(Ingredient):
    def get_name(self):
        return "Herb"

class Mushroom(Ingredient):
    def get_name(self):
        return "Mushroom"

class Root(Ingredient):
    def get_name(self):
        return "Root"

class MagickalPotion(ABC):
    active_instances = []

    def __init__(self):
        self.active_instances.append(self)
        self._extra_powers = 0

    @abstractmethod
    def brew(self):
        pass

    def get_extra_powers(self):
        return self._extra_powers

    def set_extra_powers(self, value):
        self._extra_powers = value

class HealingPotion(MagickalPotion):
    def brew(self):
        print("Brewing a healing potion...")
        extra_powers = poissonvariate(3, 1)
        self.set_extra_powers(extra_powers)

        ingredients = {
            Herb(3, 'normal'),
            Mushroom(2, 'normal'),
            Root(1, 'normal')
        }
        return ingredients

class InvisibilityPotion(MagickalPotion):
    def brew(self):
        print("Brewing an invisibility potion...")
        extra_powers = poissonvariate(2, 1)
        self.set_extra_powers(extra_powers)

        ingredients = {
            Herb(2, 'premium'),
            Mushroom(1, 'normal'),
            Root(1, 'normal')
        }
        return ingredients

class StrengthPotion(MagickalPotion):
    def brew(self):
        print("Brewing a strength potion...")
        extra_powers = poissonvariate(4, 2)
        self.set_extra_powers(extra_powers)

        ingredients = {
            Herb(2, 'legendary'),
            Mushroom(3, 'premium'),
            Root(2, 'premium')
        }
        return ingredients

    def get_extra_powers(self):
        return super().get_extra_powers() + 10

class Sorcerer:
    def __init__(self):
        self.inventory = {}
        self.potion_count = {HealingPotion: 0, InvisibilityPotion: 0, StrengthPotion: 0}

    def generate_potion(self, potion_graph):
        potion_class = choice(list(potion_graph.nodes))
        potion = potion_class()
        ingredients = potion.brew()

        print("Generated potion ingredients:")
        for ingredient in ingredients:
            print(f"- {ingredient.quantity} {ingredient.quality} {ingredient.get_name()}")

        return potion

    def generate_graph(self, potions):
        potion_graph = nx.DiGraph()
        potion_graph.add_nodes_from(potions)

        for potion in potions:
            ingredients = potion.brew()
            for ingredient in ingredients:
                potion_graph.add_edge(potion, ingredient)

        return potion_graph

    def optimize_potions(self, potion_graph):
        sorted_potions = list(nx.topological_sort(potion_graph))
        herbs_used = {quality: 0 for quality in Ingredient.quality_options}
        optimized_potions = []

        for potion_class in sorted_potions:
            potion = potion_class()

            available_ingredients = potion_graph.predecessors(potion_class)
            for ingredient_class in available_ingredients:
                herbs_used = self.consume_ingredient(ingredient_class, potion_graph, herbs_used)

            optimized_potions.append(potion)

        return optimized_potions

    def consume_ingredient(self, ingredient_class, potion_graph, herbs_used):
        ingredients = potion_graph.successors(ingredient_class)
        for ingredient in ingredients:
            herb_cost = ingredient.get_cost()
            quality = ingredient.quality

            if herbs_used[quality] >= herb_cost:
                self.inventory[ingredient.get_name()].remove(ingredient)
                herbs_used[quality] -= herb_cost

        return herbs_used

class Botanist:
    def __init__(self):
        self.inventory = {}

    def add_ingredient(self, ingredient):
        if ingredient.get_name() not in self.inventory:
            self.inventory[ingredient.get_name()] = []
        self.inventory[ingredient.get_name()].append(ingredient)

    def remove_ingredient(self, ingredient):
        if ingredient.get_name() in self.inventory:
            if ingredient in self.inventory[ingredient.get_name()]:
                self.inventory[ingredient.get_name()].remove(ingredient)

    def generate_ingredient(self):
        ingredient_classes = [Herb, Mushroom, Root]
        ingredient_class = choice(ingredient_classes)
        quantity = randint(1, 5)
        quality = choice(Ingredient.quality_options)

        ingredient = ingredient_class(quantity, quality)
        self.add_ingredient(ingredient)

        print(f"Generated ingredient: {quantity} {quality} {ingredient.get_name()}")

    def show_inventory(self):
        print("Inventory:")
        for ingredient_name, ingredient_list in self.inventory.items():
            print(f"- {ingredient_name}: {len(ingredient_list)}")

# Creating instances of the potion subclasses
potion1 = HealingPotion()
potion2 = InvisibilityPotion()
potion3 = StrengthPotion()

# Creating the sorcerer
sorcerer = Sorcerer()

# Generating a graph of potions
potions = [HealingPotion, InvisibilityPotion, StrengthPotion]
potion_graph = sorcerer.generate_graph(potions)

# Visualizing the potion graph
nx.draw(potion_graph, with_labels=True)
plt.show()

# Generating a potion using the sorcerer
generated_potion = sorcerer.generate_potion(potion_graph)

# Creating a botanist and managing the inventory
botanist = Botanist()

# Generating ingredients using the botanist
for _ in range(10):
    botanist.generate_ingredient()

# Displaying the botanist's inventory
botanist.show_inventory()

# Optimize potion creation using the sorcerer
optimized_potions = sorcerer.optimize_potions(potion_graph)

print("Optimized potion creation:")
for potion in optimized_potions:
    print(f"- {potion.__class__.__name__}")
