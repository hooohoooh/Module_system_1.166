# -*- coding: cp1254 -*-
from header_presentations import *
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ym_gatling import *
from ym_gatling_shop import *
from zhenyinghebing import *
from lco_scripts import lco_scripts
from upgrade_scripts import upgrade_scripts
##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+

##diplomacy begin
##jrider reports
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *

ibf_item_type_mask = 0x000000ff

def set_item_difficulty():
  item_difficulty = []
  for i_item in xrange(len(items)):
    item_difficulty.append((item_set_slot, i_item, dplmc_slot_item_difficulty, get_difficulty(items[i_item][6])))
  return item_difficulty[:]

def set_item_base_score():
  item_base_score = []
  for i_item in xrange(len(items)):
    if items[i_item][3] & ibf_item_type_mask == itp_type_two_handed_wpn and items[i_item][3] & itp_two_handed == 0:
      item_base_score.append((item_set_slot, i_item, dplmc_slot_two_handed_one_handed, 1))
    type = items[i_item][3] & ibf_item_type_mask
    if type >= itp_type_head_armor and type <= itp_type_hand_armor:
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_head_armor, get_head_armor(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_body_armor, get_body_armor(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_leg_armor, get_leg_armor(items[i_item][6])))
    elif type >= itp_type_one_handed_wpn and type <= itp_type_thrown and type != itp_type_shield:
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_thrust_damage, get_thrust_damage(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_swing_damage, get_swing_damage(items[i_item][6])))
    elif type == itp_type_horse:
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_horse_speed, get_missile_speed(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_horse_armor, get_body_armor(items[i_item][6])))
    elif type == itp_type_shield:
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_shield_size, get_weapon_length(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, dplmc_slot_item_shield_armor, get_body_armor(items[i_item][6])))
  return item_base_score[:]
  #### Autoloot improved by rubik end

##diplomacy end

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################


##split modules begin
from module_scripts_core import scripts_core
from module_scripts_multiplayer import scripts_multiplayer
from module_scripts_battle import scripts_battle
from module_scripts_trade_economy import scripts_trade_economy
from module_scripts_faction_politics import scripts_faction_politics
from module_scripts_party_management import scripts_party_management
from module_scripts_companions_npc import scripts_companions_npc
from module_scripts_quests import scripts_quests
from module_scripts_recruitment import scripts_recruitment
from module_scripts_town_scene import scripts_town_scene
from module_scripts_ui_presentation import scripts_ui_presentation
from module_scripts_tournament import scripts_tournament
from module_scripts_dplmc import scripts_dplmc
from module_scripts_gekokujo import scripts_gekokujo
from module_scripts_dk_invasion import scripts_dk_invasion
##split modules end

scripts = scripts_core + scripts_multiplayer + scripts_battle + scripts_trade_economy + scripts_faction_politics + scripts_party_management + scripts_companions_npc + scripts_quests + scripts_recruitment + scripts_town_scene + scripts_ui_presentation + scripts_tournament + scripts_dplmc + scripts_gekokujo + scripts_dk_invasion + ym_27 + gatling_shop_scripts + zhenyinghebing_scripts + lco_scripts + upgrade_scripts

# modmerger_start version=201 type=2
try:
    component_name = "scripts"
    var_set = { "scripts" : scripts }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
