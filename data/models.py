# Do a bunch of things with modeling all the data that might come through this module
# Need to figure this shit out lol

import typing
from typing import Union
from abc import ABC
import unicodedata
from dataclasses import dataclass
from collections import defaultdict
from functools import cached_property, lru_cache


def deaccent(text):
    norm = unicodedata.normalize("NFD", text)
    result = "".join(ch for ch in norm if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", result)

class UnregisteredDataManager:
    pass

@dataclass
class Ability:
    pass

@dataclass
class Stats:
    hgt: int
    stre: int
    spd: int
    jmp: int
    endu: int
    ins: int
    dnk: int
    ft: int
    fg: int
    tp: int
    oiq: int
    diq: int
    drb: int
    pss: int
    reb: int


@dataclass
class Item:
    id: str
    name: str
    description: str
    cost: int
    effect: str

    instance: typing.Any = UnregisteredDataManager()

    def __str__(self):
        return self.name

@dataclass
class AgeMethod:
    age: int

    instance: typing.Any = UnregisteredDataManager()

    @cached_property
    def text(self):
        return f"Age {self.age}"


@dataclass
class EvolutionTrigger(ABC):
    pass

@dataclass
class AgeTrigger(EvolutionTrigger):
    age: int
    item_id: str
    ability_type: str
    rel_stat: int

    instance: typing.Any = UnregisteredDataManager()

    @cached_property
    def item(self):
        if self.item_id is None: 
            return None
        return self.instance.items[self.item_id]

    @cached_property
    def ability_type(self):
        if self.ability_type is None: 
            return None
        return self.instance.items[self.ability_type]

    @cached_property
    def text(self):
        if self.age is None:
            text = f"when aging up"
        else:
            text = f"starting from age {self.age}"

        if self.item is not None:
            text += f" while holding a {self.item}"

        if self.ability_type is not None:
            text += f" while having a {self.ability_type}-type ability"

        if self.rel_stat == 1:
            text += f" when its Attack is higher than its Defense"
        elif self.rel_stat == -1:
            text += f" when its Defense is higher than its Attack"
        elif self.rel_stat == 0:
            text += f" when its Attack is equal to its Defense"

        return text

@dataclass
class ItemTrigger(EvolutionTrigger):
    item_id: int

    instance: typing.Any = UnregisteredDataManager()

    @cached_property
    def item(self):
        return self.instance.items[self.item_id]

    @cached_property
    def text(self):
        return f"using a {self.item}"

@dataclass
class OtherTrigger(EvolutionTrigger):
    instance: typing.Any = UnregisteredDataManager()

    @cached_property
    def text(self):
        return "somehow"

@dataclass
class Evolution:
    target_id: int
    trigger: EvolutionTrigger
    type: bool

    instance: typing.Any = UnregisteredDataManager()

    @classmethod
    def evolve_from(cls, target: int, trigger: EvolutionTrigger, instance=None):
        if instance is None:
            instance: typing.Any = UnregisteredDataManager()
        return cls(target, trigger, False, instance=instance)

    @classmethod
    def evolve_to(cls, target: int, trigger: EvolutionTrigger, instance=None):
        if instance is None:
            instance: typing.Any = UnregisteredDataManager()
        return cls(target, trigger, True, instance=instance)

    @cached_property
    def dir(self) -> str:
        return "to" if self.type == True else "from" if self.type == False else "??"

    @cached_property
    def target(self):
        return self.instance.pokemon[self.target_id]

    @cached_property
    def text(self):
        if getattr(self.target, f"evolution_{self.dir}") is not None:
            pevo = getattr(self.target, f"evolution_{self.dir}")
            return f"evolves {self.dir} {self.target} {self.trigger.text}, which {pevo.text}"

        return f"evolves {self.dir} {self.target} {self.trigger.text}"

@dataclass
class EvolutionList:
    items: list

    def __init__(self, evolutions: Union[list, Evolution]):
        if type(evolutions) == Evolution:
            evolutions = [evolutions]
        self.items = evolutions

    @cached_property
    def text(self):
        txt = " and ".join(e.text for e in self.items)
        txt = txt.replace(" and ", ", ", txt.count(" and ") - 1)
        return txt

@dataclass
class Pokemon:
    id: int
    slug: str
    base_stats: Stats
    height: int
    weight: int
    dex_number: int
    types: typing.List[str]
    description: str = None
    mega_id: int = None
    mega_x_id: int = None
    mega_y_id: int = None
    evo_from: EvolutionList = None
    evo_to: EvolutionList = None
    mythical: bool = False
    legendary: bool = False
    ultra_beast: bool = False
    event: bool = False
    is_form: bool = False
    form_item: int = None
    region: str = None

    instance: typing.Any = UnregisteredDataManager()

    def __str__(self):
        return self.name

    @cached_property
    def mega(self):
        if self.mega_id is None:
            return None

        return self.instance.pokemon[self.mega_id]

    @cached_property
    def mega_x(self):
        if self.mega_x_id is None:
            return None

        return self.instance.pokemon[self.mega_x_id]

    @cached_property
    def mega_y(self):
        if self.mega_y_id is None:
            return None

        return self.instance.pokemon[self.mega_y_id]

    @cached_property
    def image_url(self):
        return f"https://assets.poketwo.net/images/{self.id}.png?v=26"

    @cached_property
    def shiny_image_url(self):
        return f"https://assets.poketwo.net/shiny/{self.id}.png?v=26"

    @cached_property
    def evolution_text(self):
        if self.is_form and self.form_item is not None:
            species = self.instance.pokemon[self.dex_number]
            item = self.instance.items[self.form_item]
            return f"{self.name} transforms from {species} when given a {item.name}."

        if self.evolution_from is not None and self.evolution_to is not None:
            return (
                f"{self.name} {self.evolution_from.text} and {self.evolution_to.text}."
            )
        elif self.evolution_from is not None:
            return f"{self.name} {self.evolution_from.text}."
        elif self.evolution_to is not None:
            return f"{self.name} {self.evolution_to.text}."
        else:
            return None

@dataclass
class DataManagerBase:
    pokemon: typing.Dict[int, Pokemon] = None
    items: typing.Dict[int, Item] = None
    abilities: typing.Dict[int, Ability] = None

    def all_pokemon(self):
        return self.pokemon.values()

    @cached_property
    def list_alolan(self):
        return [
            10091,
            10092,
            10093,
            10100,
            10101,
            10102,
            10103,
            10104,
            10105,
            10106,
            10107,
            10108,
            10109,
            10110,
            10111,
            10112,
            10113,
            10114,
            10115,
        ]

    @cached_property
    def list_mythical(self):
        return [v.id for v in self.pokemon.values() if v.mythical]

    @cached_property
    def list_legendary(self):
        return [v.id for v in self.pokemon.values() if v.legendary]

    @cached_property
    def list_ub(self):
        return [v.id for v in self.pokemon.values() if v.ultra_beast]

    @cached_property
    def list_mega(self):
        return (
            [v.mega_id for v in self.pokemon.values() if v.mega_id is not None]
            + [v.mega_x_id for v in self.pokemon.values() if v.mega_x_id is not None]
            + [v.mega_y_id for v in self.pokemon.values() if v.mega_y_id is not None]
        )

    @cached_property
    def mons_id_by_type_index(self):
        ret = defaultdict(list)
        for pokemon in self.pokemon.values():
            for type in pokemon.types:
                ret[type.lower()].append(pokemon.id)
        return dict(ret)

    def list_type(self, type: str):
        return self.mons_id_by_type_index.get(type.lower(), [])

    @cached_property
    def mons_id_by_region_index(self):
        ret = defaultdict(list)
        for pokemon in self.pokemon.values():
            ret[pokemon.region.lower()].append(pokemon.id)
        return dict(ret)

    def list_region(self, region: str):
        return self.mons_id_by_region_index.get(region.lower(), [])

    def all_items(self):
        return self.items.values()

    @cached_property
    def mons_by_dex_number_index(self):
        ret = defaultdict(list)
        for pokemon in self.pokemon.values():
            ret[pokemon.dex_number].append(pokemon)
        return dict(ret)

    def all_mons_by_number(self, number: int) -> Pokemon:
        return self.mons_by_dex_number_index.get(number, [])

    def all_mons_by_name(self, name: str) -> Pokemon:
        return self.mons_by_name_index.get(
            deaccent(name.lower().replace("′", "'")), []
        )

    def find_all_matches(self, name: str) -> Pokemon:
        return [
            y.id
            for x in self.all_mons_by_name(name)
            for y in self.all_mons_by_number(x.id)
        ]

    def mons_by_number(self, number: int) -> Pokemon:
        try:
            return self.pokemon[number]
        except KeyError:
            return None

    @cached_property
    def mons_by_name_index(self):
        ret = defaultdict(list)
        for pokemon in self.pokemon.values():
            for name in pokemon.correct_guesses:
                ret[name].append(pokemon)
        return dict(ret)

    def mons_by_name(self, name: str) -> Pokemon:
        try:
            st = deaccent(name.lower().replace("′", "'"))
            return self.species_by_name_index[st][0]
        except (KeyError, IndexError):
            return None

    def item_by_number(self, number: int) -> Item:
        try:
            return self.items[number]
        except KeyError:
            return None

    @cached_property
    def item_by_name_index(self):
        return {item.name.lower(): item for item in self.items.values()}

    def item_by_name(self, name: str) -> Item:
        return self.item_by_name_index.get(deaccent(name.lower().replace("′", "'")))

    @cached_property
    def ability_by_name_index(self):
        return {ability.name.lower(): ability for ability in self.abilities.values()}

    def ability_by_name(self, name: str) -> Ability:
        return self.ability_by_name_index.get(deaccent(name.lower().replace("′", "'")))
