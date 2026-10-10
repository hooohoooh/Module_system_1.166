# -*- coding: cp1254 -*-
from __future__ import absolute_import
from header_common import *
from header_presentations import *
from header_mission_templates import *
from IDs.ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from header_terrain_types import *
from module_items import *
from header_skills import *
from module_info_pages import *
from module_factions import *
from IDs.ID_postfx_params import *
from IDs.ID_factions import *
from header_parties import *

####################################################################################################################
#  New game (character creation) options screen.
#  Contains the prsnt_vc_options presentation shown when starting a new game
#  (settlement names, campaign type, difficulty type, mod options).
#  Only the three sandbox campaign modes are offered:
#  Royal Sandbox (g_campaign_king), Lordly Sandbox (g_campaign_lord), Sandbox (g_campaign_sandbox).
####################################################################################################################

presentations_game_start = [
("vc_options", 0, mesh_load_window, [
  (ti_on_presentation_load,[
    (try_begin),
      (is_edit_mode_enabled),
      (display_message, "@Edit mode is enabled, it is recommended to disable it for better performance.", message_alert),
    (try_end),
    (presentation_set_duration, 999999),
    (set_fixed_point_multiplier, 1000),
    #(assign, "$autosave_on", 0), #autosave off

    #0. BACKROUND
    (create_mesh_overlay, reg0, "mesh_pic_extra_intro2"),
    (position_set_x, pos1, -1),
    (position_set_y, pos1, -1),
    (overlay_set_position, reg0, pos1),
    (position_set_x, pos1, 1002),
    (position_set_y, pos1, 1002),
    (overlay_set_size, reg0, pos1),

    #1. BASICS
    (position_set_y, pos1, 25),
    (create_game_button_overlay, "$g_presentation_obj_1", "str_continue"),
    (position_set_x, pos1, 825),
    (overlay_set_position, "$g_presentation_obj_1", pos1),
    # (try_begin),
      # (eq, reg60, 0),	#no start game
    (create_game_button_overlay, "$g_presentation_obj_2", "@Diplomacy Options"),
    # (else_try),
      # (create_game_button_overlay, "$g_presentation_obj_2", "str_back"),
    # (try_end),
    (position_set_x, pos1, 625),
    (overlay_set_position, "$g_presentation_obj_2", pos1),

    (create_game_button_overlay, "$g_presentation_obj_5", "@Battle-Morale Options"),
    (position_set_x, pos1, 425),
    (overlay_set_position, "$g_presentation_obj_5", pos1),

    #1. BASICS
    (try_begin),
      (eq, reg60, 1),	#no start game
      (create_game_button_overlay, "$g_presentation_obj_19", "str_back"),
      (position_set_x, pos1, 225),
      (overlay_set_position, "$g_presentation_obj_19", pos1),
    (try_end),

    (try_begin),
      (eq, reg60, 1),	#start game
      #3.1 Welcome message at game start
      (create_text_overlay, reg1, "@Welcome to Aut Caesar aut nihil. ^Before you start the game, choose various options.^Note that realistic savings are always disabled!", tf_center_justify|tf_with_outline),
      (overlay_set_color, reg1, color_information),
      (position_set_x, pos1, 250),
      (position_set_y, pos1, 670),
      (overlay_set_position, reg1, pos1),
      (position_set_x, pos1, 1200),
      (position_set_y, pos1, 1200),
      (overlay_set_size, reg1, pos1),
    (try_end),

    #2. province names
    (create_text_overlay, reg1, "@Settlement names", tf_center_justify|tf_with_outline),
    (overlay_set_color, reg1, color_purple),
    (position_set_x, pos1, 250),
    (position_set_y, pos1, 645),
    (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1200),
    (position_set_y, pos1, 1200),
    (overlay_set_size, reg1, pos1),

    (create_combo_button_overlay, "$g_presentation_obj_admin_panel_6"),
    (position_set_x, pos1, 250),
    (position_set_y, pos1, 605),
    (overlay_set_position, "$g_presentation_obj_admin_panel_6", pos1),
    (try_begin),
      (eq, reg60, 0),	#no start game
      (overlay_set_alpha, "$g_presentation_obj_admin_panel_6", 0xA0),
      (try_begin),
        (eq, "$g_province_names", 1),
        (overlay_add_item, "$g_presentation_obj_admin_panel_6", "@Accurate Province Names"),
      (else_try),
        (eq, "$g_province_names", 2),
        (overlay_add_item, "$g_presentation_obj_admin_panel_6", "@Simple Province Names"),
      (else_try),
        (overlay_add_item, "$g_presentation_obj_admin_panel_6", "@Normal Names"),
      (try_end),
    (else_try),
      (overlay_add_item, "$g_presentation_obj_admin_panel_6", "@Simple Province Names"),
      (overlay_add_item, "$g_presentation_obj_admin_panel_6", "@Accurate Province Names"),
      (overlay_add_item, "$g_presentation_obj_admin_panel_6", "@Normal Names"),
      (try_begin),
        (eq, "$g_province_names", 2),
        (overlay_set_val, "$g_presentation_obj_admin_panel_6", 0),
      (else_try),
        (eq, "$g_province_names", 1),
        (overlay_set_val, "$g_presentation_obj_admin_panel_6", 1),
      (else_try),
        (overlay_set_val, "$g_presentation_obj_admin_panel_6", 2),
      (try_end),
    (try_end),

    #2.1 campaign type
    (try_begin),
        (troop_slot_ge, "trp_global_variables", g_is_dev, 1),
        (create_text_overlay, reg1, "@Campaign type", tf_center_justify|tf_with_outline),
        (overlay_set_color, reg1, color_purple),
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 555),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 1200),
        (position_set_y, pos1, 1200),
        (overlay_set_size, reg1, pos1),

        (create_combo_button_overlay, "$g_presentation_obj_admin_panel_9"),
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 515),
        (overlay_set_position, "$g_presentation_obj_admin_panel_9", pos1),
        (try_begin),
          (eq, reg60, 0),	#no start game
          (overlay_set_alpha, "$g_presentation_obj_admin_panel_9", 0xA0),
          (try_begin),
            (eq, "$g_campaign_type", g_campaign_king),
            (overlay_add_item, "$g_presentation_obj_admin_panel_9", "@ROYAL SANDBOX"),
          (else_try),
            (eq, "$g_campaign_type", g_campaign_lord),
            (overlay_add_item, "$g_presentation_obj_admin_panel_9", "@LORDLY SANDBOX"),
          (else_try),
            (overlay_add_item, "$g_presentation_obj_admin_panel_9", "@SANDBOX"),
          (try_end),
        (else_try),
          #only the three sandbox modes are available for a new game
          (overlay_add_item, "$g_presentation_obj_admin_panel_9", "@ROYAL SANDBOX"),
          (overlay_add_item, "$g_presentation_obj_admin_panel_9", "@LORDLY SANDBOX"),
          (overlay_add_item, "$g_presentation_obj_admin_panel_9", "@SANDBOX"),
          (try_begin),
            (eq, "$g_campaign_type", g_campaign_king),
            (overlay_set_val, "$g_presentation_obj_admin_panel_9", 0),
          (else_try),
            (eq, "$g_campaign_type", g_campaign_lord),
            (overlay_set_val, "$g_presentation_obj_admin_panel_9", 1),
          (else_try),
            (eq, "$g_campaign_type", g_campaign_sandbox),
            (overlay_set_val, "$g_presentation_obj_admin_panel_9", 2),
          (try_end),
        (try_end),
    (try_end),

    #3. DIFFICULTY
    (create_text_overlay, reg1, "@Difficulty Type", tf_center_justify|tf_with_outline),
    (overlay_set_color, reg1, color_purple),
    (position_set_x, pos1, 250),
    (position_set_y, pos1, 465),
    (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1200),
    (position_set_y, pos1, 1200),
    (overlay_set_size, reg1, pos1),

    (create_combo_button_overlay, "$g_presentation_obj_6"),
    (position_set_x, pos1, 250),
    (position_set_y, pos1, 425),
    (overlay_set_position, "$g_presentation_obj_6", pos1),
    (overlay_add_item, "$g_presentation_obj_6", "@ACAN GIGA CHAD"),
    (overlay_add_item, "$g_presentation_obj_6", "@ACAN CHAD"),
    (overlay_add_item, "$g_presentation_obj_6", "@BORING (NORMAL)"),
    (overlay_add_item, "$g_presentation_obj_6", "@DISCORD SCHIZO"),
    (overlay_add_item, "$g_presentation_obj_6", "@LOSER (CUSTOM)"),
    (try_begin),
      (eq, "$difficulty_type", camp_d5),
      (overlay_set_val, "$g_presentation_obj_6", 0),
    (else_try),
      (eq, "$difficulty_type", camp_d4),
      (overlay_set_val, "$g_presentation_obj_6", 1),
    (else_try),
      (eq, "$difficulty_type", camp_d3),
      (overlay_set_val, "$g_presentation_obj_6", 2),
    (else_try),
      (eq, "$difficulty_type", camp_d2),
      (overlay_set_val, "$g_presentation_obj_6", 3),
    (else_try),
      (eq, "$difficulty_type", camp_d1),
      (overlay_set_val, "$g_presentation_obj_6", 4),
    (try_end),

    #4. OPTIONS
    (create_text_overlay, reg1, "@Options", tf_center_justify|tf_with_outline),
    (overlay_set_color, reg1, color_purple),
    (position_set_x, pos1, 750),
    (position_set_y, pos1, 650),
    (overlay_set_position, reg1, pos1),
    (position_set_x, pos2, 1200),
    (position_set_y, pos2, 1200),
    (overlay_set_size, reg1, pos2),

    #5. CONTAINER
    (str_clear, s0),
    (create_text_overlay, "$g_presentation_obj_admin_panel_container", s0, tf_scrollable),
    (position_set_x, pos1, 575),
    (position_set_y, pos1, 90),
    (overlay_set_position, "$g_presentation_obj_admin_panel_container", pos1),
    (position_set_x, pos1, 350),
    (position_set_y, pos1, 535),
    (overlay_set_area_size, "$g_presentation_obj_admin_panel_container", pos1),
    (set_container_overlay, "$g_presentation_obj_admin_panel_container"),

    #lines
    (position_set_x, pos1, 0),
    (position_set_y, pos1, 21*30 + 11*40 + 30),	# 30 for each checkbox or gap + 40 for each other elements + 30 buffer at the end

    #HINT
    (try_begin),
      (eq, reg60, 1),	#start game
      (position_get_y, ":y", pos1),
      (val_add, ":y", 35),
      (position_set_y, pos1, ":y"),
      (create_text_overlay, reg1, "@These options can be changed later in the camp menu.^The Diplomacy preferences can be found in the camp menu too.", tf_double_space|tf_scrollable|tf_center_justify),	#
      (copy_position, pos2, pos1),
      #(position_set_x, pos2, 175),
      (overlay_set_position, reg1, pos2),
      (position_set_x, pos2, 350),
      (position_set_y, pos2, 60),
      (overlay_set_area_size, reg1, pos2),
      (position_set_x, pos2, 900),
      (position_set_y, pos2, 900),
      (overlay_set_size, reg1, pos2),
      (position_get_y, ":y", pos1),
      (val_sub, ":y", 35),
      (position_set_y, pos1, ":y"),
    (try_end),

    #NATIVE DIFFICULTY SETTINGS
    (create_text_overlay, reg1, "str_damage_to_player", 0),
    (call_script, "script_prsnt_vc_menu_helper_2"),
    (overlay_add_item, reg2, "@Reduced to 1/4 (Easiest)"),
    (overlay_add_item, reg2, "@Reduced to 1/2 (Easy)"),
    (overlay_add_item, reg2, "str_normal"),
    (options_get_damage_to_player, reg8), #0 = 1/4, 1 = 1/2, 2 = 1/1
    (overlay_set_val, reg2, reg8),
    (assign, "$g_presentation_obj_25", reg2),

    (create_text_overlay, reg1, "str_damage_to_friends", 0),
    (call_script, "script_prsnt_vc_menu_helper_2"),
    (overlay_add_item, reg2, "@Reduced to 1/2 (Easiest)"),
    (overlay_add_item, reg2, "@Reduced to 3/4 (Easy)"),
    (overlay_add_item, reg2, "str_normal"),
    (options_get_damage_to_friends, reg8), #0 = 1/2, 1 = 3/4, 2 = 1/1
    (overlay_set_val, reg2, reg8),
    (assign, "$g_presentation_obj_26", reg2),

    #gap
    (call_script, "script_prsnt_vc_menu_helper_gap"),

    #DAMAGE SETTINGS
    (create_text_overlay, reg1, "str_combat_ai", 0),
    (call_script, "script_prsnt_vc_menu_helper_2"),
    (overlay_add_item, reg2, "str_hardcore"),
    (overlay_add_item, reg2, "str_normal"),
    (overlay_add_item, reg2, "str_beginner"),
    (options_get_combat_ai, reg8), #0 = good, 1 = average, 2 = poor
    (overlay_set_val, reg2, reg8),
    (assign, "$g_presentation_obj_27", reg2),

    (create_text_overlay, reg1, "str_movement_and_combat_speed", 0),
    (call_script, "script_prsnt_vc_menu_helper_2"),
    (overlay_add_item, reg2, "@Slowest"),
    (overlay_add_item, reg2, "@Slower"),
    (overlay_add_item, reg2, "str_normal"),
    (overlay_add_item, reg2, "@Faster"),
    (overlay_add_item, reg2, "@Fastest"),
    (options_get_combat_speed, reg8), #0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
    (overlay_set_val, reg2, reg8),
    (assign, "$g_presentation_obj_29", reg2),

    (create_text_overlay, reg1, "str_campaign_ai", 0),
    (call_script, "script_prsnt_vc_menu_helper_2"),
    (overlay_add_item, reg2, "str_hardcore"),
    (overlay_add_item, reg2, "str_normal"),
    (overlay_add_item, reg2, "str_beginner"),
    (options_get_campaign_ai, reg8), #0 = good, 1 = average, 2 = poor
    (overlay_set_val, reg2, reg8),
    (assign, "$g_presentation_obj_28", reg2),

    # (create_text_overlay, reg1, "str_quantity_bandit_parties", 0),
    # (call_script, "script_prsnt_vc_menu_helper_2"),
    # (overlay_add_item, reg2, "@Less"),
    # (overlay_add_item, reg2, "str_normal"),
    # (overlay_add_item, reg2, "@More"),
    # (overlay_set_val, reg2, "$bandit_quantity_option"),
    # (assign, "$g_presentation_obj_33", reg2),

    #gap
    (call_script, "script_prsnt_vc_menu_helper_gap"),

    #REALITY SETTINGS
    (create_text_overlay, reg1, "@Warcry", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_charge_on"),
    (assign, "$g_presentation_obj_14", reg2),

    (create_text_overlay, reg1, "@Player auxiliary feature", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$use_player_auxiliary"),
    (assign, "$g_presentation_obj_15", reg2),

    (create_text_overlay, reg1, "@Autoloot", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_autoloot_active"),
    (assign, "$g_presentation_obj_20", reg2),

    (create_text_overlay, reg1, "@Realistic troop wounding", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_realistic_wounding"),
    (assign, "$g_presentation_obj_31", reg2),

    (create_text_overlay, reg1, "str_wounds", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$vc_wounds_on"),
    (assign, "$g_presentation_obj_33", reg2),

    (create_text_overlay, reg1, "str_resting_morale", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$moralep_on"),
    (assign, "$g_presentation_obj_16", reg2),

    (create_text_overlay, reg1, "@Bodyguards", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_body_guard_on"),
    (assign, "$g_presentation_obj_admin_panel_8", reg2),

    # (create_text_overlay, reg1, "@Curb power wargoal", 0),
    # (call_script, "script_prsnt_vc_menu_helper"),
    # (overlay_set_val, reg2, "$g_allow_curb_power"),
    # (assign, "$g_presentation_obj_admin_panel_5", reg2),

    # (create_text_overlay, reg1, "@Tributary mechanic", 0),
    # (call_script, "script_prsnt_vc_menu_helper"),
    # (overlay_set_val, reg2, "$g_tributary_ai"),
    # (assign, "$g_presentation_obj_admin_panel_3", reg2),

    (create_text_overlay, reg1, "@Shieldbash", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_schield_bash"),
    (assign, "$g_presentation_obj_admin_panel_2", reg2),

    #gap
    (call_script, "script_prsnt_vc_menu_helper_gap"),

    (create_text_overlay, reg1, "@Governor/lord appointment notification", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_governor_appointment_message"),
    (assign, "$g_presentation_obj_admin_panel_7", reg2),

    (create_text_overlay, reg1, "@Truce notification menus", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$show_truce_expired"),
    (assign, "$g_presentation_obj_32", reg2),

    (create_text_overlay, reg1, "@Raid notification menus", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$show_raid_messages"),
    (assign, "$form_options_overlay_2", reg2),

    (create_text_overlay, reg1, "@Lovers discovered notifications", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_love_messages_on"),
    (assign, "$g_presentation_obj_11", reg2),

    (create_text_overlay, reg1, "@Senate meetings notifications", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_show_senate_meeting"),
    (assign, "$g_presentation_obj_9", reg2),

    (create_text_overlay, reg1, "@Enemies spotted notifications", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_report_enemies"),
    (assign, "$g_presentation_obj_admin_panel_4", reg2),

    (create_text_overlay, reg1, "@Lord gifts notifications", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_display_gift"),
    (assign, "$g_presentation_obj_24", reg2),

    #gap
    (call_script, "script_prsnt_vc_menu_helper_gap"),

    #PERFORMANCE SETTINGS
    (create_text_overlay, reg1, "str_battle_size", 0),
    (call_script, "script_prsnt_vc_menu_helper_3"),
    (options_get_battle_size, reg8), #0-1000
    (overlay_set_val, reg2, reg8),
    (assign, "$g_presentation_obj_30", reg2),

    # (create_text_overlay, reg1, "str_disable_scenic_menu", 0),	#VC-1954
    # (call_script, "script_prsnt_vc_menu_helper"),
    # (overlay_set_val, reg2, "$g_vc_menu_turned_off"),
    # (assign, "$g_presentation_obj_19", reg2),

    #gap
    (call_script, "script_prsnt_vc_menu_helper_gap"),

    #SPECIAL SETTINGS
    (create_text_overlay, reg1, "str_insane_difficult", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$insanedamage_on"),
    (assign, "$g_presentation_obj_17", reg2),

    (create_text_overlay, reg1, "str_gore", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$g_gore_on"),
    (assign, "$g_presentation_obj_18", reg2),

    # (create_text_overlay, reg1, "str_music_in_battles", 0),
    # (call_script, "script_prsnt_vc_menu_helper"),
    # (overlay_set_val, reg2, "$ambient_music_in_battle"),
    # (assign, "$g_presentation_obj_24", reg2),

    #gap
    (call_script, "script_prsnt_vc_menu_helper_gap"),

    #FORMATION SETTINGS
    (create_text_overlay, reg1, "str_player_division", 0),
    (call_script, "script_prsnt_vc_menu_helper_2"),
    (try_for_range, ":class", -1, 9),
      (try_begin),
        (eq, ":class", -1),
        (overlay_add_item, reg2, "str_none"),
      (else_try),
        (str_store_class_name, s7, ":class"),
        (overlay_add_item, reg2, s7),
      (try_end),
    (try_end),
    (overlay_set_val, reg2, "$form_ai_player_in_division"),
    (assign, "$form_options_overlay_1", reg2),

    (create_text_overlay, reg1, "str_disable_complex_formations", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$form_ai_off"),
    (assign, "$g_presentation_obj_21", reg2),

    (create_text_overlay, reg1, "str_have_formations_face_enemy", 0),
    (call_script, "script_prsnt_vc_menu_helper"),
    (overlay_set_val, reg2, "$form_ai_autorotate"),
    (assign, "$g_presentation_obj_22", reg2),

    # (create_text_overlay, reg1, "str_players_enemies_only_attack", 0),
    # (call_script, "script_prsnt_vc_menu_helper"),
    # (overlay_set_val, reg2, "$FormAI_AI_no_defense"),
    # (assign, "$g_presentation_obj_23", reg2),

    (set_container_overlay, -1),

    #6. DESCRIPTION
    #headline
    (create_text_overlay, reg1, "str_empty_string", tf_center_justify),
    (position_set_x, pos1, 250),
    (position_set_y, pos1, 370),
    (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1200),
    (position_set_y, pos1, 1200),
    (overlay_set_size, reg1, pos1),
    (assign, "$g_presentation_obj_3", reg1),

    (create_text_overlay, reg1, "str_empty_string", tf_double_space|tf_scrollable|tf_center_justify),
    (position_set_x, pos1, 75),
    (position_set_y, pos1, 100),
    (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 350),
    (position_set_y, pos1, 260),
    (overlay_set_area_size, reg1, pos1),
    (position_set_x, pos1, 900),
    (position_set_y, pos1, 900),
    (overlay_set_size, reg1, pos1),
    (assign, "$g_presentation_obj_7", reg1),

    #7. WARNING
    # (str_store_string, s1, "str_beginner"),
    # (str_store_string, s2, "str_hardcore"),
    (str_store_string, s3, "str_continue"),
    (create_text_overlay, reg1, "@Warning: This option can't be disabled any more after you click '{s3}.'", tf_double_space|tf_scrollable|tf_center_justify|tf_with_outline),
    (position_set_x, pos1, 75),
    (position_set_y, pos1, 90),
    (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 350),
    (position_set_y, pos1, 70),
    (overlay_set_area_size, reg1, pos1),
    (position_set_x, pos1, 900),
    (position_set_y, pos1, 900),
    (overlay_set_size, reg1, pos1),
    (overlay_set_color, reg1, 0xFF5555),
    (assign, "$g_presentation_obj_4", reg1),
    (overlay_set_display, "$g_presentation_obj_4", 0),
  ]),
  (ti_on_presentation_mouse_enter_leave,[
    (store_trigger_param_1, ":object"),
    (store_trigger_param_2, ":one_exit_zero_enter"),

    (str_clear, s2),
    (str_clear, s3),
    (str_clear, s4),
    (overlay_set_color, "$g_presentation_obj_3", 0x000000),

    (try_begin),
      (eq, ":one_exit_zero_enter", 1),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_5"),
      # (str_store_string,s2,"@Choose a campaign type!"),
      # (str_store_string,s4,"@Storyline Campaign: Start as a protagonist in a story. Due to certain perma-death results, ironman save mode is not available.^^Sandbox Campaign: Start a long, totally free play game.^^Lordly Sandbox Campaign: Start as a lord.^^Royal Sandbox Campaign: Start as a king."),
    (else_try),
      (eq, ":object", "$g_presentation_obj_6"),
      (str_store_string,s2,"@Choose a difficulty type!"),

    (else_try),
      (store_add, ":object_plus_one", ":object", 1),

      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_11"),
      (eq, ":object", "$g_presentation_obj_11"),
      #(str_store_string,s2,"@RECRUITMENT > Level of difficulty.",0xFFf1e73f),
      (str_store_string,s2,"@Notification about discovered love affairs"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, you will receive messages about discovered love affairs, even if you are not involved."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_14"),
      (eq, ":object", "$g_presentation_obj_14"),
      (str_store_string,s2,"@Warcry"),
      (str_store_string,s3,"str_immersion_feature"),
      (str_store_string,s8,"@Effects player and allies during battles"),
      (str_store_string,s4,"@When the player makes a warcry (T-key), the player agents performe a cheer animation.^^{s8}"),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_15"),
      (eq, ":object", "$g_presentation_obj_15"),
      (str_store_string,s2,"@Auxiliar player feature"),
      (str_store_string,s3,"str_immersion_feature"),
      (str_store_string,s8,"@Effects player after death"),
      (str_store_string,s4,"@Instead of the death camera, the player takes over the control of a troop from his own party, who is still alive.^^{s8}"),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_16"),
      (eq, ":object", "$g_presentation_obj_16"),
      (str_store_string,s2,"str_resting_morale"),
      (str_store_string,s3,"str_realism_feature"),
      (str_store_string,s4,"@Your army needs regular rest in a settlement or your camp site from time to time. Lack of rest will lower your troop morale, while resting will improve it. Resting at camps isn't as good as resting in settlements, while resting in settlements your party will recieve an additional morale boost."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_17"),
      (eq, ":object", "$g_presentation_obj_17"),
      (str_store_string,s2,"str_insane_difficult"),
      (str_store_string,s3,"str_special_setting"),
      (str_store_string,s4,"@Your enemies will cause double damage while you cause only half."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_18"),
      (eq, ":object", "$g_presentation_obj_18"),
      (str_store_string,s2,"str_gore"),
      (str_store_string,s3,"str_special_setting"),
      (str_store_string,s4,"@Add decapitation to battles."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_20"),
      (eq, ":object", "$g_presentation_obj_20"),
      (str_store_string,s2,"@Autoloot"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, you can, if your inventory management or looting skill is higher than 2, manage the equipement of you companions automatically."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_21"),
      (eq, ":object", "$g_presentation_obj_21"),
      (str_store_string,s2,"str_disable_complex_formations"),
      (str_store_string,s3,"str_formation_feature"),
      (str_store_string,s4,"@The divisions of the player's army will not adopt the formations of shield wall, wedge, or square. Moreover, the F4 menu that contains these selections will no longer appear.^^The default ranks formations will always be adopted when the player closes ranks beyond the point needed to make a shoulder-to-shoulder line."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_22"),
      (eq, ":object", "$g_presentation_obj_22"),
      (str_store_string,s2,"str_have_formations_face_enemy"),
      (str_store_string,s3,"str_formation_feature"),
      (str_store_string,s4,"@When multiple divisions are placed, they will set up to face the center of the enemy forces. Without this option, they will set up along the facing that the player has when he/she places them, although individual divisions will still turn to face the enemy.^^For example, with the option OFF and the player facing AWAY from the attacker, infantry will set up on the RIGHT flank rather than the LEFT."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    # (else_try),
      # (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_23"),
      # (eq, ":object", "$g_presentation_obj_23"),
      # (str_store_string,s2,"str_players_enemies_only_attack"),
      # (str_store_string,s3,"str_formation_feature"),
      # (str_store_string,s4,"@The army opposing the player never takes a defensive position at the back of the map, but will always charge the armies of the player and his/her allies."),
      # (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_25"),
      (eq, ":object", "$g_presentation_obj_25"),
      (str_store_string,s2,"str_damage_to_player"),
      (str_store_string,s3,"str_difficulty_setting"),
      (str_store_string,s4,"@Set how much damage is done to your character."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_26"),
      (eq, ":object", "$g_presentation_obj_26"),
      (str_store_string,s2,"str_damage_to_friends"),
      (str_store_string,s3,"str_difficulty_setting"),
      (str_store_string,s4,"@Set how much damage is done to your army."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_27"),
      (eq, ":object", "$g_presentation_obj_27"),
      (str_store_string,s2,"str_combat_ai"),
      (str_store_string,s3,"str_difficulty_setting"),
      (str_store_string,s4,"@Set how well troops fight. They fight worst at Beginner level."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_28"),
      (eq, ":object", "$g_presentation_obj_28"),
      (str_store_string,s2,"str_campaign_ai"),
      (str_store_string,s3,"str_difficulty_setting"),
      (str_store_string,s4,"@Effects size of bandit parties:^^-) Poor: 50% Size.^^-) Average: 75% Size.^^-) Good: 100% Size. THIS DOES NOT EFFECT EXISTING PARTIES!"),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_29"),
      (eq, ":object", "$g_presentation_obj_29"),
      (str_store_string,s2,"str_movement_and_combat_speed"),
      (str_store_string,s3,"str_difficulty_setting"),
      (str_store_string,s8,"str_this_setting_affects_all"),
      (str_store_string,s4,"@Set the running speed of troops in battle.^^{s8}"),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_30"),
      (eq, ":object", "$g_presentation_obj_30"),
      (str_store_string,s2,"str_battle_size"),
      (str_store_string,s3,"str_performance_feature"),
      (call_script, "script_current_battle_size"),
      (str_store_string,s2,"@{s2} {reg0}"),
      (str_store_string,s4,"str_battle_size_text"),
      (overlay_set_display, "$g_presentation_obj_4", 0),
      (try_begin),
        (gt, reg0, 300),
        (overlay_set_color, "$g_presentation_obj_3", 0xFF0000),
      (try_end),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_31"),
      (eq, ":object", "$g_presentation_obj_31"),
      (str_store_string,s2,"@Realistic troop wounding"),
      (str_store_string,s3,"@Realism feature"),
      (str_store_string,s4,"@If enabled, troops may not die immediately, but instead get only wounded, depending damage done. If damage done is larger than 40, they will die, even if a blunt weapon was used."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_32"),
      (eq, ":object", "$g_presentation_obj_32"),
      (str_store_string,s2,"@Truce notification menus"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, you will recieve notification menus, about alliances, defensive pacts, non-aggression pacts, trade agreements and truces which have expired."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_33"),
      (eq, ":object", "$g_presentation_obj_33"),
      (str_store_string,s2,"str_wounds"),
      (str_store_string,s3,"str_realism_feature"),
      (str_store_string,s4,"@The player may receive specific, debilitating wounds in battle. Physicians in larger towns will treat these wounds for a price, after which they will heal within a few days. Any negative effects will then be removed. If wound is not treated after some time, it will change to a scar, and the negative effects will then be permanent."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$form_options_overlay_1"),
      (eq, ":object", "$form_options_overlay_1"),
      (str_store_string,s2,"str_player_division"),
      (str_store_string,s3,"str_formation_feature"),
      (str_store_string,s4,"@Sets the player as commander of the chosen division. This division will set up immediately left and behind the player on Hold and Follow commands (Wedge will put player on the point). Consider it for bodyguard divisions."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$form_options_overlay_2"),
      (eq, ":object", "$form_options_overlay_2"),
      (str_store_string,s2,"@Village raid notification menus"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, you recieve notification menus about your villages which has been raided."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_9"),
      (eq, ":object", "$g_presentation_obj_9"),
      (str_store_string,s2,"@Senate meetings notification menus"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, you recieve notification menus about senate meetings."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_8"),
      (eq, ":object", "$g_presentation_obj_admin_panel_8"),
      (str_store_string,s2,"@Bodyguards"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, up to four companions will accompany you when you walk in taverns, through the streets etc. Companions spawn according to their position inside the party. Companions ordered first, will spawn first."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_7"),
      (eq, ":object", "$g_presentation_obj_admin_panel_7"),
      (str_store_string,s2,"@Governor/lord appointment notification"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled you will receive messages about the appointment of governors/lords for empty provinces/fiefs. The menu has options for you to use your influence to change the outcome to your liking."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    # (else_try),
    #   (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_5"),
    #   (eq, ":object", "$g_presentation_obj_admin_panel_5"),
    #   (str_store_string,s2,"@Curb the other realms power"),
    #   (str_store_string,s3,"@Native feature"),
    #   (str_store_string,s4,"@If enabled, the Campaign AI can use the war goal to 'curb the other realms power' against the strongest faction. This will usually lead to more wars against Rome."),
    #   (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_4"),
      (eq, ":object", "$g_presentation_obj_admin_panel_4"),
      (str_store_string,s2,"@Enemies spotted messages"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled, you will recieve notification if enemies are spotted from nearby settlements or from settlements with messenger posts."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    # (else_try),
      # (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_3"),
      # (eq, ":object", "$g_presentation_obj_admin_panel_3"),
      # (str_store_string,s2,"@Tributary mechanic"),
      # (str_store_string,s3,"@Experimental Mechanic"),
      # (str_store_string,s4,"@If enabled, an AI-kingdom A my subjugets another kingdom B, with which A is at war, depending on various conditions. The conditions are: B has suffered high loses, B has less than 4 walled centers left. B is in multiple wars, which they are losing, B has only a few allies. B is smaller than A."),
      # (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_2"),
      (eq, ":object", "$g_presentation_obj_admin_panel_2"),
      (str_store_string,s2,"@Shieldbash"),
      (str_store_string,s3,"str_realism_feature"),
      (str_store_string,s4,"@If enabled, Ai and player can perform a shieldbash during battle."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_24"),
      (eq, ":object", "$g_presentation_obj_24"),
      (str_store_string,s2,"@Lord gift Messages"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@If enabled you will recieve messages which informs you about gifts a Lord gave his liege."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_6"),
      (eq, ":object", "$g_presentation_obj_admin_panel_6"),
      (str_store_string,s2,"@Display province names"),
      (str_store_string,s3,"str_qual_life_feature"),
      (str_store_string,s4,"@Normal Names:^Settlements are named like in previous versions.^Accurate Province Names:^In the name of the settlement, the province name is displayed, e.g. Lutetia -> Lutetia (Lugdunensis)^Simple province names:^A simplified, more general, name of the province will be displayed, e.g. Lutetia -> Lutetia (GL), where GL stands for Gaul (abbreviations can be found under game concepts)"),
      (overlay_set_display, "$g_presentation_obj_4", 0),
      (try_begin),
        (eq, reg60, 1),
        (overlay_set_display, "$g_presentation_obj_4", 1),
      (try_end),
    (else_try),
      (this_or_next|eq, ":object_plus_one", "$g_presentation_obj_admin_panel_9"),
      (eq, ":object", "$g_presentation_obj_admin_panel_9"),
      (str_store_string,s2,"@Campaign type"),
      (str_store_string,s3,"@Choose a campaign type"),
      (str_store_string,s4,"@Sandbox: Classic M&B sandbox campaign.^Lordly Sandbox: Sandbox campaign where you start as lord.^Royal Sandbox: Sandbox campaign where you start as king."),
      (overlay_set_display, "$g_presentation_obj_4", 0),
      (try_begin),
        (eq, reg60, 1),
        (overlay_set_display, "$g_presentation_obj_4", 1),
      (try_end),
    (try_end),
    (str_store_string,s3,"@{s3}^^{s4}"),
    (overlay_set_text, "$g_presentation_obj_3", s2),
    (overlay_set_text, "$g_presentation_obj_7", s3),
  ]),
  (ti_on_presentation_event_state_change,[
    (store_trigger_param_1, ":object"),
    (store_trigger_param_2, ":value"),

    # (assign, reg8, ":value"),
    # (display_message, "@value = {reg8}"),
    (overlay_set_color, "$g_presentation_obj_3", 0x000000),

    (try_begin),
      (eq, ":object", "$g_presentation_obj_1"),
      (presentation_set_duration, 0),

      # (try_begin),
        # (neq, "$recruitment_on", 0),
        # (assign, "$recruitment_on_freezed", 1),
      # (try_end),
      # (try_begin),
        # (neq, "$easy_levelling", 0),
        # (assign, "$easy_levelling_freezed", 1),
      # (try_end),
      # (try_begin),
        # (neq, "$easy_wage", 0),
        # (assign, "$easy_wage_freezed", 1),
      # (try_end),
      (try_begin),
        (eq, "$moralep_on", 0),
        (party_set_slot, "p_main_party", slot_party_unrested_morale_penalty, 0),
      (try_end),

      # (try_for_range, ":center_no", centers_begin, centers_end),
        # (eq, "$recruitment_on", 1),
        # (party_set_slot,":center_no",recruit_permission_need, 0),
      # (try_end),
      (call_script, "script_dplmc_update_info_settings"),
      (try_begin),
        (eq, reg60, 0),	#no start game
        (jump_to_menu, "mnu_camp"),
      (else_try),
        #only sandbox campaigns available for a new game
        (jump_to_menu, "mnu_start_game_sandbox"),
      (try_end),
    (else_try),
      (eq, ":object", "$g_presentation_obj_2"),
      (start_presentation, "prsnt_adv_diplomacy_preferences"),
      (else_try),
      (eq, ":object", "$g_presentation_obj_5"),
      (start_presentation, "prsnt_moral_tweaks"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_19"),
      (jump_to_menu, "mnu_start_game_11"),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_5"),
      # (eq, reg60, 1),	#only start game
      # (start_presentation, "prsnt_vc_options"),
      # (try_begin),
        # (eq, ":value", 0),
        # (assign, "$campaign_type", camp_kingc),
      # (else_try),
        # (eq, ":value", 1),
        # (assign, "$campaign_type", camp_lordc),
      # (else_try),
        # (eq, ":value", 3),
        # (assign, "$campaign_type", camp_storyline),
      # (else_try),
        # (assign, "$campaign_type", camp_sandbox),
      # (try_end),
    (else_try),
      (eq, ":object", "$g_presentation_obj_6"),
      (try_begin),
        (eq, ":value", 0),
        (assign, "$difficulty_type", camp_d5),	#impossible
        (assign, "$g_gore_on", 1), # gore
        (assign, "$g_charge_on", 1), # charge animation
        (assign, "$use_player_auxiliary", 0), # player respawn after death
        (assign, "$g_autoloot_active", 0), # autoloot
        (assign, "$g_realistic_wounding", 1), # troops get wounded during battle instead of dead
        (assign, "$vc_wounds_on", 1), # player may get wounded
        (assign, "$moralep_on", 1), # resting morale effect
        (assign, "$g_body_guard_on", 0), # body guards
        # (assign, "$g_allow_curb_power", 1), # curb power war goal
        (assign, "$g_schield_bash", 1), # AI uses shieldbash
        (assign, "$g_governor_appointment_message", 1), # message governor/lord gets a center notification
        (assign, "$show_truce_expired", 1), # message truce expired
        (assign, "$show_raid_messages", 1), # message raid
        (assign, "$g_love_messages_on", 1), # message love affair
        (assign, "$g_show_senate_meeting", 1), # message senate meeting
        (assign, "$g_report_enemies", 1), # message enemy spotted
        (assign, "$g_display_gift", 1), # message lord recieves gift
        (options_set_damage_to_player, 2),	#0 = 1/4, 1 = 1/2, 2 = 1/1
        (options_set_damage_to_friends, 2),	#0 = 1/2, 1 = 3/4, 2 = 1/1
        (options_set_combat_ai, 0),		#0 = good, 1 = average, 2 = poor
        (options_set_campaign_ai, 0),	#0 = good, 1 = average, 2 = poor
        (options_set_combat_speed, 4),	#0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
      (else_try),
        (eq, ":value", 1),
        (assign, "$difficulty_type", camp_d4),	#realistic
        (assign, "$g_charge_on", 1), # charge animation
        (assign, "$g_gore_on", 1), # gore
        (assign, "$use_player_auxiliary", 1), # player respawn after death
        (assign, "$g_autoloot_active", 1), # autoloot
        (assign, "$g_realistic_wounding", 1), # troops get wounded during battle instead of dead
        (assign, "$vc_wounds_on", 1), # player may get wounded
        (assign, "$moralep_on", 1), # resting morale effect
        (assign, "$g_body_guard_on", 1), # body guards
        # (assign, "$g_allow_curb_power", 0), # curb power war goal
        (assign, "$g_schield_bash", 1), # AI uses shieldbash
        (assign, "$g_governor_appointment_message", 1), # message governor/lord gets a center notification
        (assign, "$show_truce_expired", 0), # message truce expired
        (assign, "$show_raid_messages", 1), # message raid
        (assign, "$g_love_messages_on", 1), # message love affair
        (assign, "$g_show_senate_meeting", 1), # message senate meeting
        (assign, "$g_report_enemies", 0), # message enemy spotted
        (assign, "$g_display_gift", 1), # message lord recieves gift
        (options_set_damage_to_player, 2),	#0 = 1/4, 1 = 1/2, 2 = 1/1
        (options_set_damage_to_friends, 2),	#0 = 1/2, 1 = 3/4, 2 = 1/1
        (options_set_combat_ai, 1),		#0 = good, 1 = average, 2 = poor
        (options_set_campaign_ai, 1),	#0 = good, 1 = average, 2 = poor
        (options_set_combat_speed, 3),	#0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
      (else_try),
        (eq, ":value", 2),
        (assign, "$difficulty_type", camp_d3),	#normal
        (assign, "$g_gore_on", 1), # gore
        (assign, "$g_charge_on", 1), # charge animation
        (assign, "$use_player_auxiliary", 1), # player respawn after death
        (assign, "$g_autoloot_active", 1), # autoloot
        (assign, "$g_realistic_wounding", 1), # troops get wounded during battle instead of dead
        (assign, "$vc_wounds_on", 0), # player may get wounded
        (assign, "$moralep_on", 1), # resting morale effect
        (assign, "$g_body_guard_on", 1), # body guards
        # (assign, "$g_allow_curb_power", 0), # curb power war goal
        (assign, "$g_schield_bash", 0), # AI uses shieldbash
        (assign, "$g_governor_appointment_message", 1), # message governor/lord gets a center notification
        (assign, "$show_truce_expired", 0), # message truce expired
        (assign, "$show_raid_messages", 0), # message raid
        (assign, "$g_love_messages_on", 1), # message love affair
        (assign, "$g_show_senate_meeting", 1), # message senate meeting
        (assign, "$g_report_enemies", 0), # message enemy spotted
        (assign, "$g_display_gift", 0), # message lord recieves gift
        (options_set_damage_to_player, 1),	#0 = 1/4, 1 = 1/2, 2 = 1/1
        (options_set_damage_to_friends, 1),	#0 = 1/2, 1 = 3/4, 2 = 1/1
        (options_set_combat_ai, 1),		#0 = good, 1 = average, 2 = poor
        (options_set_campaign_ai, 1),	#0 = good, 1 = average, 2 = poor
        (options_set_combat_speed, 2),	#0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
      (else_try),
        (eq, ":value", 3),
        (assign, "$difficulty_type", camp_d2),	#beginner
        (assign, "$g_gore_on", 0), # gore
        (assign, "$g_charge_on", 0), # charge animation
        (assign, "$use_player_auxiliary", 1), # player respawn after death
        (assign, "$g_autoloot_active", 1), # autoloot
        (assign, "$g_realistic_wounding", 0), # troops get wounded during battle instead of dead
        (assign, "$vc_wounds_on", 0), # player may get wounded
        (assign, "$moralep_on", 0), # resting morale effect
        (assign, "$g_body_guard_on", 1), # body guards
        # (assign, "$g_allow_curb_power", 0), # curb power war goal
        (assign, "$g_schield_bash", 0), # AI uses shieldbash
        (assign, "$g_governor_appointment_message", 1), # message governor/lord gets a center notification
        (assign, "$show_truce_expired", 0), # message truce expired
        (assign, "$show_raid_messages", 0), # message raid
        (assign, "$g_love_messages_on", 1), # message love affair
        (assign, "$g_show_senate_meeting", 1), # message senate meeting
        (assign, "$g_report_enemies", 0), # message enemy spotted
        (assign, "$g_display_gift", 0), # message lord recieves gift
        (options_set_damage_to_player, 0),	#0 = 1/4, 1 = 1/2, 2 = 1/1
        (options_set_damage_to_friends, 0),	#0 = 1/2, 1 = 3/4, 2 = 1/1
        (options_set_combat_ai, 2),		#0 = good, 1 = average, 2 = poor
        (options_set_campaign_ai, 2),	#0 = good, 1 = average, 2 = poor
        (options_set_combat_speed, 0),	#0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
      (else_try),
        (eq, ":value", 4),
        (assign, "$difficulty_type", camp_d1),
      (try_end),

      # (try_begin),
        # (neq, "$easy_levelling_freezed", 1),
        # (assign, "$easy_levelling", ":difficulty_level"),
      # (try_end),

      # (try_begin),
        # (neq, "$easy_wage_freezed", 1),
        # (eq, ":difficulty_level", 2),
        # (assign, "$easy_wage", 0),
      # (else_try),
        # (neq, "$easy_wage_freezed", 1),
        # (assign, "$easy_wage", ":difficulty_level"),
      # (try_end),

      # (try_begin),
        # (neq, "$recruitment_on_freezed", 1),
        # (eq, ":difficulty_level", 2),
        # (assign, "$recruitment_on", 0),
      # (else_try),
        # (neq, "$recruitment_on_freezed", 1),
        # (assign, "$recruitment_on", ":difficulty_level"),
      # (try_end),

      # (overlay_set_val, "$g_presentation_obj_11", "$recruitment_on"),
      # (overlay_set_val, "$g_presentation_obj_12", "$easy_levelling"),
      # (overlay_set_val, "$g_presentation_obj_13", "$easy_wage"),

      (options_get_damage_to_player, reg8),
      (overlay_set_val, "$g_presentation_obj_25", reg8),
      (options_get_damage_to_friends, reg8),
      (overlay_set_val, "$g_presentation_obj_26", reg8),
      (options_get_combat_ai, reg8),
      (overlay_set_val, "$g_presentation_obj_27", reg8),
      (options_get_combat_speed, reg8),
      (overlay_set_val, "$g_presentation_obj_29", reg8),
      (options_get_campaign_ai, reg8),
      (overlay_set_val, "$g_presentation_obj_28", reg8),

      # (overlay_set_val, "$g_presentation_obj_33", "$bandit_quantity_option"),
      (overlay_set_val, "$g_presentation_obj_14", "$g_charge_on"),
      (overlay_set_val, "$g_presentation_obj_15", "$use_player_auxiliary"),
      (overlay_set_val, "$g_presentation_obj_20", "$g_autoloot_active"),
      (overlay_set_val, "$g_presentation_obj_31", "$g_realistic_wounding"),
      (overlay_set_val, "$g_presentation_obj_32", "$show_truce_expired"),
      (overlay_set_val, "$form_options_overlay_2", "$show_raid_messages"),
      (overlay_set_val, "$g_presentation_obj_16", "$moralep_on"),
      (overlay_set_val, "$g_presentation_obj_33", "$vc_wounds_on"),

      (overlay_set_val, "$g_presentation_obj_17", "$insanedamage_on"),
      (overlay_set_val, "$g_presentation_obj_18", "$g_gore_on"),
      # (overlay_set_val, "$g_presentation_obj_admin_panel_5", "$g_allow_curb_power"),
      (overlay_set_val, "$g_presentation_obj_admin_panel_2", "$g_schield_bash"),
      (overlay_set_val, "$g_presentation_obj_24", "$g_display_gift"),
      (overlay_set_val, "$g_presentation_obj_admin_panel_4", "$g_report_enemies"),
      (overlay_set_val, "$g_presentation_obj_9", "$g_show_senate_meeting"),
      (overlay_set_val, "$g_presentation_obj_admin_panel_7", "$g_governor_appointment_message"),
      (overlay_set_val, "$form_options_overlay_2", "$show_raid_messages"),
      (overlay_set_val, "$g_presentation_obj_11", "$g_love_messages_on"),
      (overlay_set_val, "$g_presentation_obj_admin_panel_8", "$g_body_guard_on"),

    (else_try),
      (assign, "$difficulty_type", camp_d1),	#all other changes will change the difficulty type
      (overlay_set_val, "$g_presentation_obj_6", 4),
      (overlay_set_val, ":object", ":value"),

      (eq, ":object", "$g_presentation_obj_11"),
      (assign, "$g_love_messages_on", ":value"),
    (else_try),
      # (eq, ":object", "$g_presentation_obj_12"),
      # (neq, "$easy_levelling_freezed", 1),
      # (assign, "$easy_levelling", ":value"),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_13"),
      # (neq, "$easy_wage_freezed", 1),
      # (assign, "$easy_wage", ":value"),
    #(else_try),
      (eq, ":object", "$g_presentation_obj_14"),
      (assign, "$g_charge_on", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_15"),
      (assign, "$use_player_auxiliary", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_16"),
      (assign, "$moralep_on", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_17"),
      (assign, "$insanedamage_on", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_18"),
      (assign, "$g_gore_on", ":value"),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_19"),
      # (assign, "$g_vc_menu_turned_off", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_20"),
      (assign, "$g_autoloot_active", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_21"),
      (assign, "$form_ai_off", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_22"),
      (assign, "$form_ai_autorotate", ":value"),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_23"),
      # (assign, "$FormAI_AI_no_defense", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_24"),
      (assign, "$g_display_gift", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_25"),
      (options_set_damage_to_player, ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_26"),
      (options_set_damage_to_friends, ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_27"),
      (options_set_combat_ai, ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_28"),
      (options_set_campaign_ai, ":value"),
      (call_script, "script_update_party_creation_random_limits"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_29"),
      (options_set_combat_speed, ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_33"),
      (assign, "$vc_wounds_on", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_30"),
      (options_set_battle_size, ":value"),
      (str_store_string,s2,"str_battle_size"),
      #
      (str_store_string,s3,"str_performance_feature"),
      (call_script, "script_current_battle_size"),
      (str_store_string,s2,"@{s2} {reg0}"),
      (str_store_string,s4,"str_battle_size_text"),
      (str_store_string,s3,"@{s3}^^{s4}"),
      (overlay_set_text, "$g_presentation_obj_3", s2),
      (overlay_set_text, "$g_presentation_obj_7", s3),
      (try_begin),
        (gt, reg0, 300),
        (overlay_set_color, "$g_presentation_obj_3", 0xFF0000),
      (try_end),
    (else_try),
      (eq, ":object", "$g_presentation_obj_31"),
      (assign, "$g_realistic_wounding", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_32"),
      (assign, "$show_truce_expired", ":value"),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_33"),
      # (assign, "$bandit_quantity_option", ":value"),
    (else_try),
      (eq, ":object", "$form_options_overlay_1"),
      (assign, "$form_ai_player_in_division", ":value"),
    (else_try),
      (eq, ":object", "$form_options_overlay_2"),
      (assign, "$show_raid_messages", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_9"),
      (assign, "$g_show_senate_meeting", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_admin_panel_8"),
      (assign, "$g_body_guard_on", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_admin_panel_7"),
      (assign, "$g_governor_appointment_message", ":value"),
    # (else_try),
    #   (eq, ":object", "$g_presentation_obj_admin_panel_5"),
    #   (assign, "$g_allow_curb_power", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_admin_panel_4"),
      (assign, "$g_report_enemies", ":value"),
    # (else_try),
      # (eq, ":object", "$g_presentation_obj_admin_panel_3"),
      # (assign, "$g_tributary_ai", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_admin_panel_2"),
      (assign, "$g_schield_bash", ":value"),
    (else_try),
      (eq, ":object", "$g_presentation_obj_admin_panel_6"),
      (try_begin),
        (eq, ":value", 2),
        (assign, "$g_province_names", 0),
      (else_try),
        (eq, ":value", 1),
        (assign, "$g_province_names", 1),
      (else_try),
        (assign, "$g_province_names", 2),
      (try_end),
    (else_try),
        (eq, ":object", "$g_presentation_obj_admin_panel_9"),
        (assign, "$g_campaign_type", ":value"),
      # (try_begin),
        # (eq, ":value", 0),
        # (try_for_range, ":center", centers_begin, centers_end),
          # (party_get_slot, ":province", ":center", slot_center_province),
          # (val_add, ":province", "str_province_begin"),
          # (str_store_string, s61, ":province"),
          # (str_store_party_name, s50, ":center"),
          # (party_set_name, ":center", "@{s50} ({s61})"),
        # (try_end),
      # (else_try),
        # (try_for_range, ":center", centers_begin, centers_end),
          # (party_get_slot, ":province", ":center", slot_center_province),
          # (val_add, ":province", "str_province_begin"),
          # (str_store_string, s61, ":province"),
          # (str_store_party_name, s50, ":center"),
          # (party_set_name, ":center", "@{s50} ({s61})"),
        # (try_end),
      #(try_end),
    (try_end),
  ]),
  (ti_on_presentation_run,[
    (try_begin),
      (key_clicked, key_xbox_b),
      (presentation_set_duration, 0),
      (try_begin),
        (eq, "$moralep_on", 0),
        (party_set_slot, "p_main_party", slot_party_unrested_morale_penalty, 0),
      (try_end),

      (call_script, "script_dplmc_update_info_settings"),
      (try_begin),
        (eq, reg60, 0),	#no start game
        (jump_to_menu, "mnu_camp"),
      (else_try),
        #only sandbox campaigns available for a new game
        (jump_to_menu, "mnu_start_game_sandbox"),
       (try_end),
    (else_try),
      (key_clicked, key_xbox_x),
      (presentation_set_duration, 0),
      (call_script, "script_dplmc_update_info_settings"),
      (try_begin),
        (eq, reg60, 0),	#no start game
        (jump_to_menu, "mnu_camp"),
      (else_try),
        (jump_to_menu, "mnu_start_game_11"),
      (try_end),
    (try_end),
  ]),
]),
]
