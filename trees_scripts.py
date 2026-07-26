# Troop Tree Module by sphere
# Scripts for troop tree system with clickable detail view

from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

scripts = [
  ("show_troop_detail",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":root_troop_no"),
      (assign, reg0, ":troop_no"),
      # Store root troop ID for return to troop tree
      (troop_set_slot, "trp_temp_array_c", 99, ":root_troop_no"),
      # Store faction ID for return to faction troop tree
      (store_troop_faction, ":faction_no", ":troop_no"),
      (troop_set_slot, "trp_temp_array_c", 98, ":faction_no"),
      (start_presentation, "prsnt_troop_detail_view"),
    ]),

  ("cf_return_to_troop_tree",
    [
      # Get stored faction ID and restart faction troop tree presentation
      (troop_get_slot, ":faction_no", "trp_temp_array_c", 98),
      (gt, ":faction_no", 0),
      # Convert faction to index for faction_upgrade_trees
      (store_sub, ":faction_index", ":faction_no", npc_kingdoms_begin),
      (try_begin),
        (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, "$temp", ":faction_index"),
      (else_try),
        (eq, ":faction_no", "fac_kingdoms_end"), # Mercenary
        (assign, "$temp", 5),
      (else_try),
        (eq, ":faction_no", "fac_robber_knights"), # Outlaws
        (assign, "$temp", 6),
      (else_try),
        (eq, ":faction_no", "fac_khergits"), # Others
        (assign, "$temp", 7),
      (try_end),
      (start_presentation, "prsnt_faction_upgrade_trees"),
    ]),

  ("troop_tree_recursive_backtracking_with_click",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":cur_x", 2),
      (store_script_param, ":cur_y", 3),
      (store_script_param, ":offset_x", 4),
      (store_script_param, ":overlay_start", 5),
      
      (store_add, ":next_x", ":cur_x", ":offset_x"),
      # upgrade_troop
      (troop_get_upgrade_troop, ":upgrade_troop_1", ":troop_no", 0),
      (troop_get_upgrade_troop, ":upgrade_troop_2", ":troop_no", 1),
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (call_script, "script_troop_tree_recursive_backtracking_with_click", ":upgrade_troop_2", ":next_x", reg2, ":offset_x", ":overlay_start"),
        (assign, ":upgrade_troop_2_y", reg0),
        (val_add, reg2, 200), # current global y
        (call_script, "script_troop_tree_recursive_backtracking_with_click", ":upgrade_troop_1", ":next_x", reg2, ":offset_x", ":overlay_start"),
        (assign, ":upgrade_troop_1_y", reg0),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (call_script, "script_troop_tree_recursive_backtracking_with_click", ":upgrade_troop_1", ":next_x", reg2, ":offset_x", ":overlay_start"),
        (assign, ":upgrade_troop_1_y", reg0),
      (try_end),
      
      # troop_tree_line
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (store_add, reg0, ":upgrade_troop_1_y", ":upgrade_troop_2_y"),
        (val_div, reg0, 2),
        (store_div, ":half_offset_x", ":offset_x", 2),
        (store_add, ":middle_x", ":cur_x", ":half_offset_x"),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":cur_x", reg0, 0),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":middle_x", ":upgrade_troop_1_y", 0),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":middle_x", ":upgrade_troop_2_y", 0),
        (store_sub, ":size_y", ":upgrade_troop_1_y", ":upgrade_troop_2_y"),
        (val_add, ":size_y", 4),
        (call_script, "script_prsnt_line", 4, ":size_y", ":middle_x", ":upgrade_troop_2_y", 0),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (assign, reg0, ":upgrade_troop_1_y"),
        (call_script, "script_prsnt_line", ":offset_x", 4, ":cur_x", ":upgrade_troop_1_y", 0),
      (else_try),
        (assign, reg0, ":cur_y"),
      (try_end),
      
      # Store troop ID in temp slot for click handling
      (troop_set_slot, "trp_temp_array_c", ":overlay_start", ":troop_no"),
      (val_add, ":overlay_start", 1),
      
      # troop name
      (str_store_troop_name, s1, ":troop_no"),
      (create_text_overlay, reg1, "@{s1}", tf_center_justify|tf_vertical_align_center|tf_double_space|tf_scrollable),
      (store_sub, ":name_x", ":cur_x", 50),
      (store_sub, ":name_y", reg0, 130),
      (position_set_x, pos1, ":name_x"),
      (position_set_y, pos1, ":name_y"),
      (overlay_set_position, reg1, pos1),
      (position_set_x, pos1, 100),
      (position_set_y, pos1, 60),
      (overlay_set_area_size, reg1, pos1),
      (position_set_x, pos1, 800),
      (position_set_y, pos1, 800),
      (overlay_set_size, reg1, pos1),
      
      # troop avatar (clickable button)
      (store_sub, ":avatar_x", ":cur_x", 75),
      (store_sub, ":avatar_y", reg0, 75),
      (store_mul, ":cur_troop", ":troop_no", 2), #with weapons
      (create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
      (position_set_x, pos1, 450),
      (position_set_y, pos1, 600),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, ":avatar_x"),
      (position_set_y, pos1, ":avatar_y"),
      (overlay_set_position, reg1, pos1),
      
      (assign, reg0, ":overlay_start"),
    ]),
]

def modmerge(var_set):
    try:
        var_name_1 = "scripts"
        orig_scripts = var_set[var_name_1]
        orig_scripts.extend(scripts)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)