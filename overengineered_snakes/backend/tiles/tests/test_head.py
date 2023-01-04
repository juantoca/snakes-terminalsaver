from typing import Tuple

from hypothesis import assume
from hypothesis import given
from hypothesis.strategies import integers
from hypothesis.strategies import tuples

from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tests.strategies.mapa import empty_mapa_st
from overengineered_snakes.backend.tiles.body import Body
from overengineered_snakes.backend.tiles.head import Head
from overengineered_snakes.backend.tiles.tests.strategies.head import head_st


@given(head_st, empty_mapa_st)
def test_head_die(head: Head, mapa: Mapa) -> None:
    mapa.set_coords(head.coords, head)
    head.die(mapa)
    assert type(mapa.get_coords(head.coords)) is Body


@given(head_st, empty_mapa_st, tuples(integers(), integers()))
def test_head_move(head: Head, mapa: Mapa, coords: Tuple[int, int]) -> None:
    original_coords = head.coords
    mapa.set_coords(head.coords, head)
    assume(mapa.get_coords(coords) is not head)
    head.move(coords, mapa)
    assert type(mapa.get_coords(original_coords)) is Body
    assert type(mapa.get_coords(coords)) is Head
    assert head.nextone == original_coords
