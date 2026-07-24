# -*- coding: utf-8 -*-

from header_common import *
from header_operations import *
from header_parties import *
from module_constants import *

#注：该代码为夜幕原创开源代码，如果使用我的代码严禁任何形式的收费，使用必须给与无论形式的认可，如致谢，贡献名单等; 源码内标注的#夜幕begin #夜幕end不可删除或修改

#参数1: 合并后的目标阵营
#参数2: 参与合并的阵营 1
#参数3: 参与合并的阵营 2
#参数4: 参与合并的阵营 3
#参数5: 合并后的国王

#   (call_script, "script_merge_three_factions_into_one", "fac_kingdom_28",  "fac_kingdom_4", "fac_kingdom_15", "fac_kingdom_12", "trp_kingdom_28_lord"), 


#夜幕begin
zhenyinghebing_scripts = [
    ("merge_factions", [
    (store_script_param, ":ym_1", 1),
    (store_script_param, ":ym_2", 2),
    (store_script_param, ":ym_3", 3),
    (store_script_param, ":ym_4", 4),
    (store_script_param, ":ym_5", 5),

    (assign, reg0, 0),

    (try_begin),
        (is_between, ":ym_1", npc_kingdoms_begin, npc_kingdoms_end),
        (is_between, ":ym_2", npc_kingdoms_begin, npc_kingdoms_end),
        (is_between, ":ym_3", npc_kingdoms_begin, npc_kingdoms_end),
        (is_between, ":ym_4", npc_kingdoms_begin, npc_kingdoms_end),
        (is_between, ":ym_5", kings_begin, lords_end),

        (store_faction_of_troop, ":ym_6", ":ym_5"),
        (this_or_next|eq, ":ym_6", ":ym_1"),
        (this_or_next|eq, ":ym_6", ":ym_2"),
        (this_or_next|eq, ":ym_6", ":ym_3"),
        (eq, ":ym_6", ":ym_4"),

        (faction_set_slot, ":ym_1", slot_faction_state, sfs_active),
        (faction_set_slot, ":ym_1", slot_faction_leader, ":ym_5"),

        (try_for_range, ":ym_7", active_npcs_begin, active_npcs_end),
            (troop_slot_eq, ":ym_7", slot_troop_occupation, slto_kingdom_hero),
            (store_faction_of_troop, ":ym_8", ":ym_7"),
            (this_or_next|eq, ":ym_8", ":ym_2"),
            (this_or_next|eq, ":ym_8", ":ym_3"),
            (eq, ":ym_8", ":ym_4"),
            (troop_set_faction, ":ym_7", ":ym_1"),
            (call_script, "script_troop_set_title_according_to_faction",
                ":ym_7", ":ym_1"),
        (try_end),

        (troop_set_faction, ":ym_5", ":ym_1"),
        (call_script, "script_troop_set_title_according_to_faction",
            ":ym_5", ":ym_1"),

        (try_for_parties, ":ym_9"),
            (store_faction_of_party, ":ym_10", ":ym_9"),
            (this_or_next|eq, ":ym_10", ":ym_2"),
            (this_or_next|eq, ":ym_10", ":ym_3"),
            (eq, ":ym_10", ":ym_4"),
            (party_set_faction, ":ym_9", ":ym_1"),
        (try_end),

        (try_begin),
            (neq, ":ym_2", ":ym_1"),
            (faction_set_slot, ":ym_2", slot_faction_state, sfs_defeated),
        (try_end),

        (try_begin),
            (neq, ":ym_3", ":ym_1"),
            (faction_set_slot, ":ym_3", slot_faction_state, sfs_defeated),
        (try_end),

        (try_begin),
            (neq, ":ym_4", ":ym_1"),
            (faction_set_slot, ":ym_4", slot_faction_state, sfs_defeated),
        (try_end),

        (call_script, "script_faction_recalculate_strength", ":ym_1"),
        (call_script, "script_faction_recalculate_strength", ":ym_2"),
        (call_script, "script_faction_recalculate_strength", ":ym_3"),
        (call_script, "script_faction_recalculate_strength", ":ym_4"),
        (call_script, "script_update_all_notes"),
        (call_script, "script_update_village_market_towns"),
        (assign, "$g_recalculate_ais", 1),

        (assign, reg0, 1),
    (try_end),
    ]),
]
#夜幕end