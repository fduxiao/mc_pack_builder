from enum import Enum
from typing import TypeVar

from ..pack import Dir
from ..natural_model import DictModel, Field
from ..resources import Resource
from .tags import Tag


class Category(Enum):
    food = "food"
    blocks = "blocks"
    misc = "misc"
    building = "building"
    redstone = "redstone"
    equipment = "equipment"


def parse_category(category):
    if isinstance(category, Category):
        return category.value
    return str(category)


class Recipe(DictModel):
    default_type = "minecraft:recipe"
    multi_result = True

    type = Field()
    category = Field(cast=parse_category)
    group = Field()
    show_notification = Field()

    def __init__(self):
        super().__init__()
        self.type = self.default_type

    def set_type(self, new_type):
        self.type = new_type
        return self

    def set_category(self, cat):
        self.category = cat
        return self

    def result(self, item=None, count=1):
        """
        to set the result conveniently. only set if necessary

        :param item:
        :param count:
        :return:
        """
        if item is None:
            return self.dict['result']
        if isinstance(item, Resource):
            item = item.resource_location()
        else:
            item = str(item)
        result = {"item": item}
        if self.multi_result:
            result['count'] = count
        self.dict['result'] = result
        return self


def parse_ingredient(value):
    if isinstance(value, Tag):
        return {"tag": value.resource_location()}
    if isinstance(value, Resource):
        return {"item": value.resource_location()}
    if isinstance(value, list | tuple):
        return [parse_ingredient(v) for v in value]
    return str(value)


class CraftingShaped(Recipe):
    default_type = "minecraft:crafting_shaped"

    pattern: list = Field(default=[])
    key = Field(default={})

    def define(self, pattern, **key):
        self.pattern = pattern
        for k, v in key.items():
            self.key[k] = parse_ingredient(v)
        return self

    def set_key(self, key, *values):
        self.key[key] = parse_ingredient(values)
        return self


class CraftingShapeless(Recipe):
    default_type = "minecraft:crafting_shapeless"
    ingredients: list = Field(default=[])

    def define(self, *ingredients):
        for i in ingredients:
            self.ingredients.append(parse_ingredient(i))
        return self


class StoneCutting(Recipe):
    default_type = "minecraft:stonecutting"
    ingredient = Field()

    def define(self, ingredient):
        self.ingredient = parse_ingredient(ingredient)
        return self

    def result(self, item=None, count=1):
        if item is None:
            return self.dict(item)
        if isinstance(item, Resource):
            item = item.resource_location()
        self['result'] = item
        self['count'] = count


T = TypeVar("T")


class Recipes(Dir):
    def add_recipe(self, name, recipe: T = None) -> T:
        if recipe is None:
            recipe = Recipe()
        self.add_json(f'{name}.json', recipe)
        return recipe

    def crafting_shaped(self, name):
        return self.add_recipe(name, CraftingShaped())

    def crafting_shapeless(self, name):
        return self.add_recipe(name, CraftingShapeless())

    def stone_cutting(self, name):
        return self.add_recipe(name, StoneCutting())
