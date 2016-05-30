from lib.base import *
from lib.player_generators.base_player_generator import BasePlayerGenerator
from lib.tiered_leagues.base_tiered_league import BaseTieredLeague

pb = BasePlayerGenerator(10000)
tl = BaseTieredLeague(pb)

for i in range(0, 100):
  tl.do_an_iteration()
tl.print_summary()
