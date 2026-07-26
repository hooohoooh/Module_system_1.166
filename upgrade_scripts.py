# -*- coding: UTF-8 -*-
####################################################################################################################
# UPGRADE SCRIPTS - One-Click Upgrade & Upgrade Template System
####################################################################################################################

from header_common import *
from header_operations import *
from module_constants import *
from header_presentations import *
from header_troops import *

upgrade_scripts = [

    # script_count_upgradable_troops
    # Counts how many troops in the player's party are upgradable (have at least one upgrade path)
    # and calculates the total upgrade cost.
    # Output: reg0 = number of upgradable troops, reg1 = total cost
    ("count_upgradable_troops",
        [
            (assign, ":count", 0),
            (assign, ":total_cost", 0),
            (party_get_num_companion_stacks, ":num_troops", "p_main_party"),
            (try_for_range, ":slot", 0, ":num_troops"),
                (party_stack_get_troop_id, ":troop_id", "p_main_party", ":slot"),
                (troop_is_hero, ":troop_id"),
                (neg),
                (troop_get_upgrade_troop, ":upgrade_1", ":troop_id", 0),
                (gt, ":upgrade_1", 0),
                (val_add, ":count", 1),
                (call_script, "script_game_get_upgrade_cost", ":troop_id"),
                (val_add, ":total_cost", reg0),
            (try_end),
            (assign, reg0, ":count"),
            (assign, reg1, ":total_cost"),
        ]
    ),

    # script_calculate_upgrade_cost
    # Calculates the total upgrade cost for all upgradable troops in the player's party.
    # Output: reg0 = total cost
    ("calculate_upgrade_cost",
        [
            (assign, ":total_cost", 0),
            (party_get_num_companion_stacks, ":num_troops", "p_main_party"),
            (try_for_range, ":slot", 0, ":num_troops"),
                (party_stack_get_troop_id, ":troop_id", "p_main_party", ":slot"),
                (troop_is_hero, ":troop_id"),
                (neg),
                (troop_get_upgrade_troop, ":upgrade_1", ":troop_id", 0),
                (gt, ":upgrade_1", 0),
                (call_script, "script_game_get_upgrade_cost", ":troop_id"),
                (val_add, ":total_cost", reg0),
            (try_end),
            (assign, reg0, ":total_cost"),
        ]
    ),

    # script_upgrade_all_troops
    # Upgrades all upgradable troops in the player's party.
    # Uses the upgrade template if available, otherwise defaults to first branch (path 0).
    # If insufficient funds, upgrades in order until money runs out.
    # Output: reg0 = number upgraded, reg1 = 1 if all upgraded (0 if ran out of money)
    ("upgrade_all_troops",
        [
            (assign, ":upgraded", 0),
            (assign, ":all_upgraded", 1),
            (store_troop_gold, ":player_gold", "trp_player"),
            (party_get_num_companion_stacks, ":num_troops", "p_main_party"),
            (try_for_range, ":slot", 0, ":num_troops"),
                (party_stack_get_troop_id, ":troop_id", "p_main_party", ":slot"),
                # Skip heroes
                (troop_is_hero, ":troop_id"),
                (neg),
                # Determine upgrade path from template
                (assign, ":upgrade_path", 0),
                (try_begin),
                    (call_script, "script_get_upgrade_preference", ":troop_id"),
                    (assign, ":preference", reg0),
                    (store_random_in_range, ":random", 0, 100),
                    (ge, ":random", ":preference"),
                    (assign, ":upgrade_path", 1),
                (try_end),
                (troop_get_upgrade_troop, ":upgrade_troop", ":troop_id", ":upgrade_path"),
                (gt, ":upgrade_troop", 0),
                (call_script, "script_game_get_upgrade_cost", ":troop_id"),
                (assign, ":cost", reg0),
                (try_begin),
                    (ge, ":player_gold", ":cost"),
                    # Upgrade this troop
                    (troop_set_slot, "trp_temp_array_a", 0, ":troop_id"),
                    (troop_set_slot, "trp_temp_array_a", 1, ":upgrade_path"),
                    (party_upgrade_with_xp, "p_main_party", 1, ":upgrade_path"),
                    (val_sub, ":player_gold", ":cost"),
                    (troop_remove_gold, "trp_player", ":cost"),
                    (val_add, ":upgraded", 1),
                (else_try),
                    (assign, ":all_upgraded", 0),
                    (assign, ":slot", ":num_troops"), # Exit loop
                (try_end),
            (try_end),
            (assign, reg0, ":upgraded"),
            (assign, reg1, ":all_upgraded"),
        ]
    ),

    # script_init_upgrade_template
    # Initializes the upgrade template storage.
    ("init_upgrade_template",
        [
            (troop_set_slot, lco_upgrade_template, 0, -1), # Marker: uninitialized
        ]
    ),

    # script_save_upgrade_template
    # Saves the current upgrade preferences to the template troop.
    # This is called when the user clicks "Save" in the template editor.
    # Input: param1 = troop_id, param2 = preference value (0-100)
    ("save_upgrade_template",
        [
            (store_script_param, ":troop_id", 1),
            (store_script_param, ":value", 2),
            (troop_set_slot, lco_upgrade_template, ":troop_id", ":value"),
        ]
    ),

    # script_reset_upgrade_template
    # Resets all upgrade preferences to default (100 = first branch).
    # Sets a marker so get_upgrade_preference returns default.
    ("reset_upgrade_template",
        [
            (troop_set_slot, lco_upgrade_template, 0, -1), # Marker: uninitialized
        ]
    ),

    # script_get_upgrade_preference
    # Gets the upgrade preference for a specific troop.
    # Input: param1 = troop_id
    # Output: reg0 = preference value (0-100), 100 = first branch, 0 = second branch
    # Default: 100 (always first branch) when no preference has been set
    ("get_upgrade_preference",
        [
            (store_script_param, ":troop_id", 1),
            (troop_get_slot, ":pref", lco_upgrade_template, ":troop_id"),
            (try_begin),
                (lt, ":pref", 0),
                (assign, ":pref", 100), # Default to first branch
            (try_end),
            (try_begin),
                (gt, ":pref", 100),
                (assign, ":pref", 100),
            (try_end),
            (assign, reg0, ":pref"),
        ]
    ),

    # script_set_upgrade_preference
    # Sets the upgrade preference for a specific troop.
    # Input: param1 = troop_id, param2 = preference value (0-100)
    ("set_upgrade_preference",
        [
            (store_script_param, ":troop_id", 1),
            (store_script_param, ":value", 2),
            (val_clamp, ":value", 0, 100),
            (troop_set_slot, lco_upgrade_template, ":troop_id", ":value"),
        ]
    ),

    # script_upgrade_template_tree
    # Recursively draws the troop tree with upgrade preference sliders for troops with 2 upgrade paths.
    # Input: param1 = troop_id, param2 = cur_x, param3 = cur_y, param4 = offset_x
    # Output: reg0 = y position of current node
    ("upgrade_template_tree",
        [
            (store_script_param, ":troop_no", 1),
            (store_script_param, ":cur_x", 2),
            (store_script_param, ":cur_y", 3),
            (store_script_param, ":offset_x", 4),
            
            (store_add, ":next_x", ":cur_x", ":offset_x"),
            # upgrade_troop
            (troop_get_upgrade_troop, ":upgrade_troop_1", ":troop_no", 0),
            (troop_get_upgrade_troop, ":upgrade_troop_2", ":troop_no", 1),
            (try_begin),
                (gt, ":upgrade_troop_2", 0),
                (call_script, "script_upgrade_template_tree", ":upgrade_troop_2", ":next_x", reg2, ":offset_x"),
                (assign, ":upgrade_troop_2_y", reg0),
                (val_add, reg2, 200), # current global y
                (call_script, "script_upgrade_template_tree", ":upgrade_troop_1", ":next_x", reg2, ":offset_x"),
                (assign, ":upgrade_troop_1_y", reg0),
            (else_try),
                (gt, ":upgrade_troop_1", 0),
                (call_script, "script_upgrade_template_tree", ":upgrade_troop_1", ":next_x", reg2, ":offset_x"),
                (assign, ":upgrade_troop_1_y", reg0),
            (try_end),
            
            # troop_tree_line
            (try_begin),
                (gt, ":upgrade_troop_2", 0),
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
                (gt, ":upgrade_troop_1", 0),
                (assign, reg0, ":upgrade_troop_1_y"),
                (call_script, "script_prsnt_line", ":offset_x", 4, ":cur_x", ":upgrade_troop_1_y", 0),
            (else_try),
                (assign, reg0, ":cur_y"),
            (try_end),
            
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
            
            # troop avatar (non-clickable mesh)
            (store_sub, ":avatar_x", ":cur_x", 75),
            (store_sub, ":avatar_y", reg0, 75),
            (store_mul, ":cur_troop", ":troop_no", 2), # with weapons
            (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
            (position_set_x, pos1, 450),
            (position_set_y, pos1, 600),
            (overlay_set_size, reg1, pos1),
            (position_set_x, pos1, ":avatar_x"),
            (position_set_y, pos1, ":avatar_y"),
            (overlay_set_position, reg1, pos1),
            
            # Slider for troops with 2 upgrade paths
            (try_begin),
                (troop_get_upgrade_troop, ":upg_1", ":troop_no", 0),
                (troop_get_upgrade_troop, ":upg_2", ":troop_no", 1),
                (gt, ":upg_1", 0),
                (gt, ":upg_2", 0),
                # Create slider (0-100 range)
                (create_slider_overlay, ":slider_id", 0, 100),
                # Get current preference from template
                (call_script, "script_get_upgrade_preference", ":troop_no"),
                (assign, ":pref", reg0),
                (overlay_set_val, ":slider_id", ":pref"),
                # Position slider below the avatar
                (store_sub, ":slider_x", ":cur_x", 60),
                (store_add, ":slider_y", reg0, 5),
                (position_set_x, pos1, ":slider_x"),
                (position_set_y, pos1, ":slider_y"),
                (overlay_set_position, ":slider_id", pos1),
                (position_set_x, pos1, 120),
                (position_set_y, pos1, 15),
                (overlay_set_size, ":slider_id", pos1),
                # Store slider ID → troop ID mapping in temp_array_b
                (troop_set_slot, "trp_temp_array_b", "$g_upgrade_template_slider_count", ":slider_id"),
                (store_add, ":troop_slot", "$g_upgrade_template_slider_count", 200),
                (troop_set_slot, "trp_temp_array_b", ":troop_slot", ":troop_no"),
                (val_add, "$g_upgrade_template_slider_count", 1),
            (try_end),
            
            (assign, reg0, ":cur_y"),
        ]
    ),

]