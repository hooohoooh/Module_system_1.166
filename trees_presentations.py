# -*- coding: utf-8 -*-
# Troop Tree Module by sphere
# Enhanced troop tree presentation with clickable troop detail view
# Uses native Mount & Blade inventory style

from header_common import *
from header_presentations import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from header_troops import *
from header_skills import *
from header_items import *
from module_constants import *

presentations = [

  ("troop_detail_view", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (assign, ":troop_no", reg0),

        # Title: troop name (top center)
        (str_store_troop_name, s1, ":troop_no"),
        (create_text_overlay, reg1, "@{s1}", tf_center_justify|tf_with_outline),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 710),
        (overlay_set_position, reg1, pos1),

        # Close button (top right)
        (create_game_button_overlay, "$g_presentation_obj_troop_detail_close", "@关闭"),
        (position_set_x, pos1, 880),
        (position_set_y, pos1, 710),
        (overlay_set_position, "$g_presentation_obj_troop_detail_close", pos1),

        # Back to troop tree button (top right, below Close)
        (create_game_button_overlay, "$g_presentation_obj_troop_detail_back", "@返回兵种树"),
        (position_set_x, pos1, 830),
        (position_set_y, pos1, 660),
        (overlay_set_position, "$g_presentation_obj_troop_detail_back", pos1),

        # ===== Left panel: Equipment slots (Armor section) =====
        # Background
        (create_mesh_overlay, reg0, "mesh_mp_inventory_left"),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg0, pos1),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 14),
        (overlay_set_position, reg0, pos1),

        # Helmet slot (inventory slot 4)
        (troop_get_inventory_slot, ":item", ":troop_no", 4),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 525),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 53),
          (position_set_y, pos1, 576),
          (overlay_set_position, ":icon", pos1),
          (assign, "$g_troop_detail_overlay_0", ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_helmet", "mesh_mp_inventory_slot_helmet"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 525),
          (overlay_set_position, ":btn", pos1),
          (assign, "$g_troop_detail_overlay_0", ":btn"),
        (try_end),
        (assign, "$g_troop_detail_item_0", ":item"),

        # Armor slot (inventory slot 5)
        (troop_get_inventory_slot, ":item", ":troop_no", 5),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 425),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 53),
          (position_set_y, pos1, 476),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 1, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_armor", "mesh_mp_inventory_slot_armor"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 425),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 1, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 10, ":item"),

        # Boots slot (inventory slot 6)
        (troop_get_inventory_slot, ":item", ":troop_no", 6),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 325),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 53),
          (position_set_y, pos1, 376),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 2, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_boot", "mesh_mp_inventory_slot_boot"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 325),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 2, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 11, ":item"),

        # Gloves slot (inventory slot 7)
        (troop_get_inventory_slot, ":item", ":troop_no", 7),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 225),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 53),
          (position_set_y, pos1, 276),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 3, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_glove", "mesh_mp_inventory_slot_glove"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 225),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 3, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 12, ":item"),

        # Horse slot (inventory slot 8)
        (troop_get_inventory_slot, ":item", ":troop_no", 8),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 125),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 53),
          (position_set_y, pos1, 176),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 4, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_horse", "mesh_mp_inventory_slot_horse"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 2),
          (position_set_y, pos1, 125),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 4, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 13, ":item"),

        # ===== Right panel: Weapon slots =====
        # Background
        (create_mesh_overlay, reg0, "mesh_mp_inventory_right"),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg0, pos1),
        (position_set_x, pos1, 894),
        (position_set_y, pos1, 65),
        (overlay_set_position, reg0, pos1),

        # Weapon1 slot (inventory slot 0)
        (troop_get_inventory_slot, ":item", ":troop_no", 0),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 475),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 950),
          (position_set_y, pos1, 526),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 5, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_equip", "mesh_mp_inventory_slot_equip"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 475),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 5, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 14, ":item"),

        # Weapon2 slot (inventory slot 1)
        (troop_get_inventory_slot, ":item", ":troop_no", 1),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 375),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 950),
          (position_set_y, pos1, 426),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 6, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_equip", "mesh_mp_inventory_slot_equip"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 375),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 6, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 15, ":item"),

        # Weapon3 slot (inventory slot 2)
        (troop_get_inventory_slot, ":item", ":troop_no", 2),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 275),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 950),
          (position_set_y, pos1, 326),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 7, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_equip", "mesh_mp_inventory_slot_equip"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 275),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 7, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 16, ":item"),

        # Weapon4 slot (inventory slot 3)
        (troop_get_inventory_slot, ":item", ":troop_no", 3),
        (try_begin),
          (ge, ":item", 0),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 175),
          (overlay_set_position, ":btn", pos1),
          (create_mesh_overlay_with_item_id, ":icon", ":item"),
          (position_set_x, pos1, 950),
          (position_set_y, pos1, 226),
          (overlay_set_position, ":icon", pos1),
          (troop_set_slot, "trp_temp_array_c", 8, ":icon"),
        (else_try),
          (create_image_button_overlay, ":btn", "mesh_mp_inventory_slot_equip", "mesh_mp_inventory_slot_equip"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, ":btn", pos1),
          (position_set_x, pos1, 899),
          (position_set_y, pos1, 175),
          (overlay_set_position, ":btn", pos1),
          (troop_set_slot, "trp_temp_array_c", 8, ":btn"),
        (try_end),
        (troop_set_slot, "trp_temp_array_c", 17, ":item"),

        # ===== Backpack (inventory slots 9+) =====
        (str_store_string, s0, "@背包:"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 390),
        (position_set_y, pos1, 690),
        (overlay_set_position, reg1, pos1),

        # Backpack grid: 4 columns, 100x100 spacing
        (assign, ":backpack_start_x", 370),
        (assign, ":backpack_start_y", 630),
        (assign, ":backpack_col_width", 100),
        (assign, ":backpack_row_height", 100),
        (assign, ":backpack_col", 0),
        (assign, ":backpack_row", 0),
        (assign, ":backpack_index", 0),

        # Get inventory capacity and loop through backpack slots
        (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
        (try_begin),
          (gt, ":inv_cap", 50),
          (assign, ":inv_cap", 50),
        (try_end),
        (try_for_range, ":inv_slot", 9, ":inv_cap"),
          (troop_get_inventory_slot, ":item", ":troop_no", ":inv_slot"),
          (try_begin),
            (ge, ":item", 0),
            # Calculate position
            (store_mul, ":cur_x", ":backpack_col", ":backpack_col_width"),
            (store_add, ":cur_x", ":backpack_start_x", ":cur_x"),
            (store_mul, ":cur_y", ":backpack_row", ":backpack_row_height"),
            (store_sub, ":cur_y", ":backpack_start_y", ":cur_y"),
            
            # Create button background
            (create_image_button_overlay, ":btn", "mesh_mp_inventory_choose", "mesh_mp_inventory_choose"),
            (position_set_x, pos1, 800),
            (position_set_y, pos1, 800),
            (overlay_set_size, ":btn", pos1),
            (position_set_x, pos1, ":cur_x"),
            (position_set_y, pos1, ":cur_y"),
            (overlay_set_position, ":btn", pos1),
            
            # Create item icon
            (create_mesh_overlay_with_item_id, ":icon", ":item"),
            (store_add, ":item_x", ":cur_x", 50),
            (store_add, ":item_y", ":cur_y", 50),
            (position_set_x, pos1, ":item_x"),
            (position_set_y, pos1, ":item_y"),
            (overlay_set_position, ":icon", pos1),
            
            # Store overlay ID and item ID for mouseover tracking (offset by 200 to avoid conflict with equipment slots and troop tree)
            (store_add, ":overlay_slot", ":backpack_index", 200),
            (troop_set_slot, "trp_temp_array_c", ":overlay_slot", ":icon"),
            (store_add, ":item_slot", ":backpack_index", 250),
            (troop_set_slot, "trp_temp_array_c", ":item_slot", ":item"),
            
            # Move to next column
            (val_add, ":backpack_col", 1),
            (val_add, ":backpack_index", 1),
            (try_begin),
              (eq, ":backpack_col", 4),
              (assign, ":backpack_col", 0),
              (val_add, ":backpack_row", 1),
            (try_end),
          (try_end),
        (try_end),

        # ===== 3D Character Model (center of screen) =====
        (store_mul, ":cur_troop", ":troop_no", 2), #with weapons
        (create_mesh_overlay_with_tableau_material, reg0, -1, "tableau_game_party_window", ":cur_troop"),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg0, pos1),
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 220),
        (overlay_set_position, reg0, pos1),

        # ===== Attributes/Skills text area (center of screen) =====
        # Smaller font, compact layout, centered
        (assign, ":cur_y", 100),
        (assign, ":line_height", 20),

        # Level
        (store_character_level, reg0, ":troop_no"),
        (str_store_string, s0, "@等级: {reg0}"),
        (create_text_overlay, reg1, s0, tf_center_justify|tf_with_outline),
        (position_set_x, pos1, 280),
        (position_set_y, pos1, 220),
        (overlay_set_position, reg1, pos1),  


        # Strength & Agility
        (store_attribute_level, reg0, ":troop_no", ca_strength),
        (str_store_string, s0, "@力量: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 320),
        (position_set_y, pos1, 200),
        (overlay_set_position, reg1, pos1),
        (store_attribute_level, reg0, ":troop_no", ca_agility),
        (str_store_string, s0, "@敏捷: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 320),
        (position_set_y, pos1, 180),
        (overlay_set_position, reg1, pos1),


        # Intelligence & Charisma
        (store_attribute_level, reg0, ":troop_no", ca_intelligence),
        (str_store_string, s0, "@智力: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 320),
        (position_set_y, pos1, 160),
        (overlay_set_position, reg1, pos1),
        (store_attribute_level, reg0, ":troop_no", ca_charisma),
        (str_store_string, s0, "@魅力: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 320),
        (position_set_y, pos1, 140),
        (overlay_set_position, reg1, pos1),




        # One-Handed & Two-Handed
        (store_proficiency_level, reg0, ":troop_no", wpt_one_handed_weapon),
        (str_store_string, s0, "@单手: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 200),
        (overlay_set_position, reg1, pos1),
        (store_proficiency_level, reg0, ":troop_no", wpt_two_handed_weapon),
        (str_store_string, s0, "@双手: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 180),
        (overlay_set_position, reg1, pos1),


        # Polearm & Archery
        (store_proficiency_level, reg0, ":troop_no", wpt_polearm),
        (str_store_string, s0, "@长柄: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 160),
        (overlay_set_position, reg1, pos1),
        (store_proficiency_level, reg0, ":troop_no", wpt_archery),
        (str_store_string, s0, "@弓箭: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 140),
        (overlay_set_position, reg1, pos1),


        # Crossbow & Throwing
        (store_proficiency_level, reg0, ":troop_no", wpt_crossbow),
        (str_store_string, s0, "@弩: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 120),
        (overlay_set_position, reg1, pos1),
        (store_proficiency_level, reg0, ":troop_no", wpt_throwing),
        (str_store_string, s0, "@投掷: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg1, pos1),
        
        (store_proficiency_level, reg0, ":troop_no", wpt_firearm),
        (str_store_string, s0, "@火器: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 480),
        (position_set_y, pos1, 200),
        (overlay_set_position, reg1, pos1),
        
        
        # Skills header
        (str_store_string, s0, "@技能:"),
        (create_text_overlay, reg1, s0, tf_center_justify|tf_with_outline),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", ":line_height"),

        # Ironflesh & Power Strike
        (store_skill_level, reg0, skl_ironflesh, ":troop_no"),
        (str_store_string, s0, "@铁骨: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (store_skill_level, reg0, skl_power_strike, ":troop_no"),
        (str_store_string, s0, "@强击: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 460),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", ":line_height"),

        # Power Draw & Power Throw
        (store_skill_level, reg0, skl_power_draw, ":troop_no"),
        (str_store_string, s0, "@强弓: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (store_skill_level, reg0, skl_power_throw, ":troop_no"),
        (str_store_string, s0, "@强掷: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 460),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", ":line_height"),

        # Shield & Riding
        (store_skill_level, reg0, skl_shield, ":troop_no"),
        (str_store_string, s0, "@盾牌: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (store_skill_level, reg0, skl_riding, ":troop_no"),
        (str_store_string, s0, "@骑术: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 460),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", ":line_height"),

        # Athletics
        (store_skill_level, reg0, skl_athletics, ":troop_no"),
        (str_store_string, s0, "@跑动: {reg0}"),
        (create_text_overlay, reg1, s0, tf_left_align),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
      ]),

    # Mouse-over for item details
    (ti_on_presentation_mouse_enter_leave,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":enter_leave"),

        (try_begin),
          (eq, ":enter_leave", 0),
          # Mouse entering - show item details for equipment slots (0-8)
          (try_for_range, ":slot_no", 0, 9),
            (troop_slot_eq, "trp_temp_array_c", ":slot_no", ":object"),
            (store_add, ":item_slot", ":slot_no", 9),
            (troop_get_slot, ":item_no", "trp_temp_array_c", ":item_slot"),
            (ge, ":item_no", 0),
            (overlay_get_position, pos0, ":object"),
            (show_item_details, ":item_no", pos0, 100),
          (try_end),
          # Check backpack slots in temp_array_c (200-249 = overlay IDs, 250-299 = item IDs)
          (try_for_range, ":slot_no", 200, 250),
            (troop_slot_eq, "trp_temp_array_c", ":slot_no", ":object"),
            (store_add, ":item_slot", ":slot_no", 50),
            (troop_get_slot, ":item_no", "trp_temp_array_c", ":item_slot"),
            (ge, ":item_no", 0),
            (overlay_get_position, pos0, ":object"),
            (show_item_details, ":item_no", pos0, 100),
          (try_end),
        (else_try),
          # Mouse leaving - close item details
          (close_item_details),
        (try_end),
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_troop_detail_close"),
          (close_item_details),
          (presentation_set_duration, 0),
        (try_end),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_troop_detail_back"),
          (close_item_details),
          (call_script, "script_cf_return_to_troop_tree"),
        (try_end),
      ]),

    (ti_on_presentation_run,
      [
        # Escape key - close the detail view
        (try_begin),
          (key_clicked, key_escape),
          (close_item_details),
          (presentation_set_duration, 0),
        (try_end),
        # Enter key - return to troop tree
        (try_begin),
          (key_clicked, key_enter),
          (close_item_details),
          (call_script, "script_cf_return_to_troop_tree"),
        (try_end),
        # Backspace key - return to troop tree
        (try_begin),
          (key_clicked, key_back_space),
          (close_item_details),
          (call_script, "script_cf_return_to_troop_tree"),
        (try_end),
      ]),
    ]),

]

def modmerge(var_set):
    try:
        var_name_1 = "presentations"
        orig_presentations = var_set[var_name_1]
        orig_presentations.extend(presentations)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)