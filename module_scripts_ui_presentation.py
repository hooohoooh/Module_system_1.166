# -*- coding: utf-8 -*-
# module_scripts_ui_presentation.py -- auto split from module_scripts.py (feature: 演示/面板/旗帜辅助)
# entries: 26 (order preserved within this file)
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
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *


scripts_ui_presentation = [

  #script_agent_troop_get_banner_mesh
  # INPUT: agent_no, troop_no
  # OUTPUT: banner_mesh
  ("agent_troop_get_banner_mesh",
    [
       (store_script_param, ":agent_no", 1),
       (store_script_param, ":troop_no", 2),
       (assign, ":banner_troop", -1),
       (assign, ":banner_mesh", "mesh_banners_default_b"),
       (try_begin),
         (lt, ":agent_no", 0),
         (try_begin),
           (ge, ":troop_no", 0),
           (this_or_next|troop_slot_ge, ":troop_no", slot_troop_banner_scene_prop, 1),
           (eq, ":troop_no", "trp_player"),
           (assign, ":banner_troop", ":troop_no"),
         (else_try),
		   #gekokujo 3.0 microfactions! include fort companions start
           #(is_between, ":troop_no", companions_begin, companions_end),
           (is_between, ":troop_no", companions_begin, fort_companions_end),
		   #gekokujo 3.0 microfactions! include fort companions end
           (assign, ":banner_troop", "trp_player"),
         (else_try),
           (assign, ":banner_mesh", "mesh_banners_default_a"),
         (try_end),
       (else_try),
         (eq, "$g_is_quick_battle", 1),
         (agent_get_team, ":agent_team", ":agent_no"),
         (try_begin),
           (eq, ":agent_team", 0),
           (assign, ":banner_mesh", "$g_quick_battle_team_0_banner"),
         (else_try),
           (assign, ":banner_mesh", "$g_quick_battle_team_1_banner"),
         (try_end),
       (else_try),
         (game_in_multiplayer_mode),
         (agent_get_group, ":agent_group", ":agent_no"),
         (try_begin),
           (neg|player_is_active, ":agent_group"),
           (agent_get_player_id, ":agent_group", ":agent_no"),
         (try_end),
         (try_begin),
           #if player banners are not allowed, use the default banner mesh
           (eq, "$g_multiplayer_allow_player_banners", 1),
           (player_is_active, ":agent_group"),
           (player_get_banner_id, ":player_banner", ":agent_group"),
           (ge, ":player_banner", 0),
           (store_add, ":banner_mesh", ":player_banner", arms_meshes_begin),
           (assign, ":already_used", 0),
           (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end), #wrong client data check
             (faction_slot_eq, ":cur_faction", slot_faction_banner, ":banner_mesh"),
             (assign, ":already_used", 1),
           (try_end),
           (eq, ":already_used", 0), #otherwise use the default banner mesh
         (else_try),
           (agent_get_team, ":agent_team", ":agent_no"),
           (team_get_faction, ":team_faction_no", ":agent_team"),

           (try_begin),
             (agent_is_human, ":agent_no"),
             (faction_get_slot, ":banner_mesh", ":team_faction_no", slot_faction_banner),
           (else_try),
             (agent_get_rider, ":rider_agent_no", ":agent_no"),
             #(agent_get_position, pos1, ":agent_no"),
             #(position_get_x, ":pos_x", pos1),
             #(position_get_y, ":pos_y", pos1),
             #(assign, reg0, ":pos_x"),
             #(assign, reg1, ":pos_y"),
             #(assign, reg2, ":agent_no"),
             #(display_message, "@{!}agent_no:{reg2}, pos_x:{reg0} , posy:{reg1}"),
             (try_begin),
               (ge, ":rider_agent_no", 0),
               (agent_is_active, ":rider_agent_no"),
               (agent_get_team, ":rider_agent_team", ":rider_agent_no"),
               (team_get_faction, ":rider_team_faction_no", ":rider_agent_team"),
               (faction_get_slot, ":banner_mesh", ":rider_team_faction_no", slot_faction_banner),
             (else_try),
               (assign, ":banner_mesh", "mesh_banners_default_c"),
             (try_end),                   
           (try_end),             
         (try_end),
       (else_try),
         (agent_get_troop_id, ":troop_id", ":agent_no"),
         (this_or_next|troop_slot_ge,  ":troop_id", slot_troop_banner_scene_prop, 1),
         (eq, ":troop_no", "trp_player"),
         (assign, ":banner_troop", ":troop_id"),
       (else_try),
         (agent_get_party_id, ":agent_party", ":agent_no"),
         (try_begin),
           (lt, ":agent_party", 0),
		   #gekokujo 3.0 microfactions! include fort companions start
           #(is_between, ":troop_id", companions_begin, companions_end),
           (is_between, ":troop_id", companions_begin, fort_companions_end),
		   #gekokujo 3.0 microfactions! include fort companions end
           (main_party_has_troop, ":troop_id"),
           (assign, ":agent_party", "p_main_party"),
         (try_end),
         (ge, ":agent_party", 0),
         (party_get_template_id, ":party_template", ":agent_party"),
         (try_begin),
           (eq, ":party_template", "pt_deserters"),
           (assign, ":banner_mesh", "mesh_banners_default_c"),
         (else_try),
           (is_between, ":agent_party", centers_begin, centers_end),
		   #gekokujo 3.0 microfactions! include fort companions start
           #(is_between, ":troop_id", companions_begin, companions_end),
           (is_between, ":troop_id", companions_begin, fort_companions_end),
		   #gekokujo 3.0 microfactions! include fort companions end
           (neq, "$talk_context", tc_tavern_talk),
           #this should be a captured companion in prison
           (assign, ":banner_troop", "trp_player"),
         (else_try),
           (is_between, ":agent_party", centers_begin, centers_end),
           (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
           (ge, ":town_lord", 0),
           (assign, ":banner_troop", ":town_lord"),
         (else_try),
           (this_or_next|party_slot_eq, ":agent_party", slot_party_type, spt_kingdom_hero_party),
           (eq, ":agent_party", "p_main_party"),
           (party_get_num_companion_stacks, ":num_stacks", ":agent_party"),
           (gt, ":num_stacks", 0),
           (party_stack_get_troop_id, ":leader_troop_id", ":agent_party", 0),
           (this_or_next|troop_slot_ge,  ":leader_troop_id", slot_troop_banner_scene_prop, 1),
           (eq, ":leader_troop_id", "trp_player"),
           (assign, ":banner_troop", ":leader_troop_id"),
         (try_end),
       (else_try), #Check if we are in a tavern
         (eq, "$talk_context", tc_tavern_talk),
         (neq, ":troop_no", "trp_player"),
         (assign, ":banner_mesh", "mesh_banners_default_d"),
       (else_try), #can't find party, this can be a town guard
         (neq, ":troop_no", "trp_player"),
         (is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
         (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
         (ge, ":town_lord", 0),
         (assign, ":banner_troop", ":town_lord"),
       (try_end),
       (try_begin),
         (ge, ":banner_troop", 0),
         (try_begin),
           (neg|troop_slot_ge, ":banner_troop", slot_troop_banner_scene_prop, 1),
           (assign, ":banner_mesh", "mesh_banners_default_b"),
         (else_try), 
           (troop_get_slot, ":banner_spr", ":banner_troop", slot_troop_banner_scene_prop),
           (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
           (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
           (val_sub, ":banner_spr", banner_scene_props_begin),
           (store_add, ":banner_mesh", ":banner_spr", arms_meshes_begin),
         (try_end),
       (try_end),
       (assign, reg0, ":banner_mesh"),
     ]),
  #script_shield_item_set_banner
  # INPUT: agent_no
  # OUTPUT: none
  ("shield_item_set_banner",
    [
       (store_script_param, ":tableau_no",1),
       (store_script_param, ":agent_no", 2),
       (store_script_param, ":troop_no", 3),
       (call_script, "script_agent_troop_get_banner_mesh", ":agent_no", ":troop_no"),
       (cur_item_set_tableau_material, ":tableau_no", reg0),
     ]),
  #script_troop_agent_set_banner
  # INPUT: agent_no
  # OUTPUT: none
  ("troop_agent_set_banner",
    [
       (store_script_param, ":tableau_no",1),
       (store_script_param, ":agent_no", 2),
       (store_script_param, ":troop_no", 3),
       (call_script, "script_agent_troop_get_banner_mesh", ":agent_no", ":troop_no"),
       (cur_agent_set_banner_tableau_material, ":tableau_no", reg0),
     ]),
  #script_add_troop_to_cur_tableau
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),
       (assign, ":banner_mesh", -1),
       (troop_get_slot, ":banner_spr", ":troop_no", slot_troop_banner_scene_prop),
       (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
       (try_begin),
         (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
         (val_sub, ":banner_spr", banner_scene_props_begin),
         (store_add, ":banner_mesh", ":banner_spr", banner_meshes_begin),
       (try_end),

       (cur_tableau_clear_override_items),
       
#       (cur_tableau_set_override_flags, af_override_fullhelm),
       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":eye_height", 162),
       (store_mul, ":camera_distance", ":troop_no", 87323),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 139),
       (store_mul, ":camera_yaw", ":troop_no", 124337),
       (val_mod, ":camera_yaw", 50),
       (val_add, ":camera_yaw", -25),
       (store_mul, ":camera_pitch", ":troop_no", 98123),
       (val_mod, ":camera_pitch", 20),
       (val_add, ":camera_pitch", -14),
       (assign, ":animation", "anim_stand_man"),
       
##       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
##       (try_begin),
##         (gt, ":horse_item", 0),
##         (assign, ":eye_height", 210),
##         (cur_tableau_add_horse, ":horse_item", pos2, anim_horse_stand, 0),
##         (assign, ":animation", anim_ride_0),
##         (position_set_z, pos5, 125),
##         (try_begin),
##           (is_between, ":camera_yaw", -10, 10), #make sure horse head doesn't obstruct face.
##           (val_min, ":camera_pitch", -5),
##         (try_end),
##       (try_end),
       (position_set_z, pos5, ":eye_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (ge, ":banner_mesh", 0),

         (init_position, pos1),
         (position_set_z, pos1, -1500),
         (position_set_x, pos1, 265),
         (position_set_y, pos1, 400),
         (position_transform_position_to_parent, pos3, pos5, pos1),
         (cur_tableau_add_mesh, ":banner_mesh", pos3, 400, 0),
       (try_end),
       (cur_tableau_add_troop, ":troop_no", pos2, ":animation" , 0),

       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
  #script_add_troop_to_cur_tableau_for_character
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_character",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (cur_tableau_set_override_flags, af_override_fullhelm),
##       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 4, 8, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 150),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 360),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
  #script_add_troop_to_cur_tableau_for_inventory
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_inventory",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":side", ":troop_no", 4), #side flag is inside troop_no value
       (val_div, ":troop_no", 4), #removing the flag bit
       (val_mul, ":side", 90), #to degrees

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       
       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
  #script_add_troop_to_cur_tableau_for_profile
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_profile",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (profile_get_banner_id, ":profile_banner"),
       (try_begin),
         (ge, ":profile_banner", 0),
         (init_position, pos2),
         (val_add, ":profile_banner", banner_meshes_begin),
         (position_set_x, pos2, -175),
         (position_set_y, pos2, -300),
         (position_set_z, pos2, 180),
         (position_rotate_x, pos2, 90),
         (position_rotate_y, pos2, -15),
         (cur_tableau_add_mesh, ":profile_banner", pos2, 0, 0),
       (try_end),

       (init_position, pos2),
       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
  #script_add_troop_to_cur_tableau_for_retirement
  # INPUT: type
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_retirement", [
    (store_script_param, ":type", 1),
    (cur_tableau_set_override_flags, af_override_everything),

    (try_begin),
      (eq, ":type", 0),
      (cur_tableau_add_override_item, "itm_gekokujo_sugegasa_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_1_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (assign, ":animation", "anim_pose_1"),
    (else_try),
      (eq, ":type", 1),
      (cur_tableau_add_override_item, "itm_gekokujo_sugegasa_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_1_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_tanto_1"),
      (assign, ":animation", "anim_pose_1"),
    (else_try),
      (eq, ":type", 2),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_1_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (assign, ":animation", "anim_pose_2"),
    (else_try),
      (eq, ":type", 3),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_1_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (assign, ":animation", "anim_pose_2"),
    (else_try),
      (eq, ":type", 4),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_1_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (assign, ":animation", "anim_pose_3"),
    (else_try),
      (eq, ":type", 5),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_1_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sugegasa_1"),
      (assign, ":animation", "anim_pose_3"),
    (else_try),
      (eq, ":type", 6),
      (cur_tableau_add_override_item, "itm_gekokujo_kimono_2_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_katana_1"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 7),
      (cur_tableau_add_override_item, "itm_gekokujo_hakama_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_katana_1"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 8),
      (cur_tableau_add_override_item, "itm_gekokujo_haori_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_sandal_1"),
      (cur_tableau_add_override_item, "itm_gekokujo_katana_1"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
##      (eq, ":type", 9),
      (cur_tableau_add_override_item, "itm_gekokujo_jinbaori_7"),
      (cur_tableau_add_override_item, "itm_gekokujo_tsubo_suneate_3"),
      (cur_tableau_add_override_item, "itm_gekokujo_katana_1"),
      (assign, ":animation", "anim_pose_5"),
##    (else_try), #not used
##      (cur_tableau_add_override_item, "itm_heraldic_mail_with_tabard"),
##      (cur_tableau_add_override_item, "itm_iron_greaves"),
##      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
##      (assign, ":animation", "anim_pose_5"),
    (try_end),

##    (set_fixed_point_multiplier, 100),
##    (cur_tableau_set_background_color, 0x00000000),
##    (cur_tableau_set_ambient_light, 10,11,15),

##     (init_position, pos8),
##     (position_set_x, pos8, -210),
##     (position_set_y, pos8, 200),
##     (position_set_z, pos8, 300),
##     (cur_tableau_add_point_light, pos8, 550,500,450),


    (set_fixed_point_multiplier, 100),
    (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),
    (assign, ":cam_height", 155),
    (assign, ":camera_distance", 575),
    (assign, ":camera_yaw", -5),
    (assign, ":camera_pitch", 10),

    (init_position, pos5),
    (position_set_z, pos5, ":cam_height"),
    # camera looks towards -z axis
    (position_rotate_x, pos5, -90),
    (position_rotate_z, pos5, 180),
    # now apply yaw and pitch
    (position_rotate_y, pos5, ":camera_yaw"),
    (position_rotate_x, pos5, ":camera_pitch"),
    (position_move_z, pos5, ":camera_distance", 0),
    (position_move_x, pos5, 60, 0),

    (init_position, pos2),
    (cur_tableau_add_troop, "trp_player", pos2, ":animation", 0),
    (cur_tableau_set_camera_position, pos5),

    (copy_position, pos8, pos5),
    (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
    (position_rotate_z, pos8, 30),
    (position_rotate_x, pos8, -60),
    (cur_tableau_add_sun_light, pos8, 175,150,125),
    ]),
  #script_add_troop_to_cur_tableau_for_party
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_party",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":hide_weapons", ":troop_no", 2), #hide_weapons flag is inside troop_no value
       (val_div, ":troop_no", 2), #removing the flag bit

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (try_begin),
         (eq, ":hide_weapons", 1),
         (cur_tableau_set_override_flags, af_override_fullhelm|af_override_head|af_override_weapons),
       (try_end),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 450),
       (assign, ":camera_yaw", 15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
       (try_begin),
         (gt, ":horse_item", 0),
         (eq, ":hide_weapons", 0),
         (cur_tableau_add_horse, ":horse_item", pos2, "anim_horse_stand", 0),
         (assign, ":animation", "anim_ride_0"),
         (assign, ":camera_yaw", 23),
         (assign, ":cam_height", 150),
         (assign, ":camera_distance", 550),
       (try_end),
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
  #script_get_prosperity_text_to_s50
  # INPUT: center_no
  # OUTPUT: none
  ("get_prosperity_text_to_s50",
    [(store_script_param, ":center_no", 1),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (val_div, ":prosperity", 20),
     (try_begin),
       (eq, ":prosperity", 0), #0..19
       (str_store_string, s50, "@Very Poor"),
     (else_try),
       (eq, ":prosperity", 1), #20..39
       (str_store_string, s50, "@Poor"),
     (else_try),
       (eq, ":prosperity", 2), #40..59
       (str_store_string, s50, "@Average"),
     (else_try),
       (eq, ":prosperity", 3), #60..79
       (str_store_string, s50, "@Rich"),
     (else_try),
       (str_store_string, s50, "@Very Rich"), #80..99
     (try_end),
     ]),
  #script_get_name_from_dna_to_s50
  # INPUT: arg1 = dna
  # OUTPUT: s50 = name
  ("get_name_from_dna_to_s50",
    [(store_script_param, ":dna", 1),
     (store_sub, ":num_names", names_end, names_begin),
     (store_sub, ":num_surnames", surnames_end, surnames_begin),
     (assign, ":selected_name", ":dna"),
     (val_mod, ":selected_name", ":num_names"),
     (assign, ":selected_surname", ":dna"),
     (val_div, ":selected_surname", ":num_names"),
     (val_mod, ":selected_surname", ":num_surnames"),
     (val_add, ":selected_name", names_begin),
     (val_add, ":selected_surname", surnames_begin),
     (str_store_string, s50, ":selected_name"),
     (str_store_string, s50, ":selected_surname"),
     ]),
  # script_place_player_banner_near_inventory
  # Input: none
  # Output: none
  ("place_player_banner_near_inventory",
    [
    	#normal_banner_begin
    	(troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
    	#custom_banner_begin
#    	(troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),

     (try_begin),
    	#normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (scene_prop_get_instance, ":flag_object", ":troop_banner_object", 0),
    	#custom_banner_begin
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (scene_prop_get_instance, ":flag_object", ":flag_spr", 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (get_player_agent_no, ":player_agent"),
         (agent_get_look_position, pos1, ":player_agent"),
         (position_move_y, pos1, -500),
         (position_rotate_z, pos1, 180),
         (position_set_z_to_ground_level, pos1),
         (position_move_z, pos1, 300),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (position_move_z, pos1, -320),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (else_try),
       (init_position, pos1),
       (position_move_z, pos1, -1000000),
       (scene_prop_get_instance, ":flag_object", banner_scene_props_begin, 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (try_end),
     ]),
  # script_place_player_banner_near_inventory_bms
  # Input: none
  # Output: none
  ("place_player_banner_near_inventory_bms",
    [
    	    	#normal_banner_begin
    	(troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
    	    	#custom_banner_begin
#      (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
     (try_begin),
    	    	#normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
    	    	#custom_banner_begin
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
     (try_end),
     ]),
  # script_draw_banner_to_region
  # Input: arg1 = troop_no, arg2 = center_pos_x, arg3 = center_pos_y, arg4 = width, arg5 = height, arg6 = stretch_width, arg7 = stretch_height, arg8 = default_scale, arg9 = max_charge_scale, arg10 = drawn_item_type
  # drawn_item_type is 0 for banners, 1 for shields, 2 for heater shield, 3 for armor
  # arguments will be used as fixed point values
  # Output: none
  ("draw_banner_to_region",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_pos_x", 2),
      (store_script_param, ":center_pos_y", 3),
      (store_script_param, ":width", 4),
      (store_script_param, ":height", 5),
      (store_script_param, ":stretch_width", 6),
      (store_script_param, ":stretch_height", 7),
      (store_script_param, ":default_scale", 8),
      (store_script_param, ":max_charge_scale", 9),
      (store_script_param, ":drawn_item_type", 10),

      (troop_get_slot, ":bg_type", ":troop_no", slot_troop_custom_banner_bg_type),
      (val_add, ":bg_type", custom_banner_backgrounds_begin),
      (troop_get_slot, ":bg_color_1", ":troop_no", slot_troop_custom_banner_bg_color_1),
      (troop_get_slot, ":bg_color_2", ":troop_no", slot_troop_custom_banner_bg_color_2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (troop_get_slot, ":positioning", ":troop_no", slot_troop_custom_banner_positioning),
      (call_script, "script_get_troop_custom_banner_num_positionings", ":troop_no"),
      (assign, ":num_positionings", reg0),
      (val_mod, ":positioning", ":num_positionings"),

      (init_position, pos2),
      (position_set_x, pos2, ":width"),
      (position_set_y, pos2, ":height"),
      (assign, ":default_value", 1),
      (convert_to_fixed_point, ":default_value"),
      (position_set_z, pos2, ":default_value"),

      (init_position, pos1),
      (position_set_x, pos1, ":center_pos_x"),
      (position_set_y, pos1, ":center_pos_y"),
      (position_move_z, pos1, -20),

      (init_position, pos3),
      (position_set_x, pos3, ":default_scale"),
      (position_set_y, pos3, ":default_scale"),
      (position_set_z, pos3, ":default_value"),

      (try_begin),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_bg"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg01"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg02"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg03"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg08"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg09"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg10"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg11"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg12"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg13"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg16"),
        (eq, ":bg_type", "mesh_custom_banner_fg17"),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos2, 0, ":bg_color_1"),
      (else_try),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos3, 0, ":bg_color_1"),
      (try_end),
      (position_move_z, pos1, -20),
      (position_move_x, pos2, ":width"),
      (position_move_y, pos2, ":height"),
      (cur_tableau_add_mesh_with_scale_and_vertex_color, "mesh_custom_banner_bg", pos1, pos2, 0, ":bg_color_2"),
      
      (assign, ":charge_stretch", ":stretch_width"),
      (val_min, ":charge_stretch", ":stretch_height"),
      (val_min, ":charge_stretch", ":max_charge_scale"),
      (call_script, "script_get_custom_banner_charge_type_position_scale_color", "trp_player", ":positioning"),

      (try_begin),
        (this_or_next|eq, ":drawn_item_type", 2), #heater shield
        (eq, ":drawn_item_type", 3), #armor
        (assign, ":change_center_pos", 0),
        (try_begin),
          (eq, ":num_charges", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 2),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 3),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (try_end),
        (try_begin),
          (eq, ":change_center_pos", 1),
          (val_add, ":center_pos_y", 30),
        (try_end),
      (try_end),
      
      (try_begin),
        (ge, ":num_charges", 1),
        (val_mul, reg1, ":charge_stretch"),
        (val_div, reg1, 10000),
        (position_get_x, ":x", pos0),
        (position_get_y, ":y", pos0),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos0, ":x"),
        (position_set_y, pos0, ":y"),
        (assign, ":scale_value", reg1),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg0, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg0, 256), #remove orientation flags
        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg0, pos0, pos4, 0, reg2),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 2),
        (val_mul, reg4, ":charge_stretch"),
        (val_div, reg4, 10000),
        (position_get_x, ":x", pos1),
        (position_get_y, ":y", pos1),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos1, ":x"),
        (position_set_y, pos1, ":y"),

        (assign, ":scale_value", reg4),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg3, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg3, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg3, pos1, pos4, 0, reg5),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 3),
        (val_mul, reg7, ":charge_stretch"),
        (val_div, reg7, 10000),
        (position_get_x, ":x", pos2),
        (position_get_y, ":y", pos2),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos2, ":x"),
        (position_set_y, pos2, ":y"),

        (assign, ":scale_value", reg7),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg6, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg6, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg6, pos2, pos4, 0, reg8),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 4),
        (val_mul, reg10, ":charge_stretch"),
        (val_div, reg10, 10000),
        (position_get_x, ":x", pos3),
        (position_get_y, ":y", pos3),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos3, ":x"),
        (position_set_y, pos3, ":y"),

        (assign, ":scale_value", reg10),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg9, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg9, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg9, pos3, pos4, 0, reg11),
      (try_end),
     ]),
  # script_get_troop_custom_banner_num_positionings
  # Input: arg1 = troop_no
  # Output: reg0 = num_positionings
  ("get_troop_custom_banner_num_positionings",
    [
      (store_script_param, ":troop_no", 1),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (try_begin),
        (eq, ":num_charges", 1),
        (assign, ":num_positionings", 2),
      (else_try),
        (eq, ":num_charges", 2),
        (assign, ":num_positionings", 4),
      (else_try),
        (eq, ":num_charges", 3),
        (assign, ":num_positionings", 6),
      (else_try),
        (assign, ":num_positionings", 2),
      (try_end),
      (assign, reg0, ":num_positionings"),
     ]),
  # script_get_custom_banner_charge_type_position_scale_color
  # Input: arg1 = troop_no, arg2 = positioning_index
  # Output: reg0 = type_1
  #         reg1 = scale_1
  #         reg2 = color_1
  #         reg3 = type_2
  #         reg4 = scale_2
  #         reg5 = color_2
  #         reg6 = type_3
  #         reg7 = scale_3
  #         reg8 = color_3
  #         reg9 = type_4
  #         reg10 = scale_4
  #         reg11 = color_4
  ("get_custom_banner_charge_type_position_scale_color",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":positioning", 2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (init_position, pos0),
      (init_position, pos1),
      (init_position, pos2),
      (init_position, pos3),

      (troop_get_slot, reg0, ":troop_no", slot_troop_custom_banner_charge_type_1),
      (val_add, reg0, custom_banner_charges_begin),
      (troop_get_slot, reg2, ":troop_no", slot_troop_custom_banner_charge_color_1),
      (troop_get_slot, reg3, ":troop_no", slot_troop_custom_banner_charge_type_2),
      (val_add, reg3, custom_banner_charges_begin),
      (troop_get_slot, reg5, ":troop_no", slot_troop_custom_banner_charge_color_2),
      (troop_get_slot, reg6, ":troop_no", slot_troop_custom_banner_charge_type_3),
      (val_add, reg6, custom_banner_charges_begin),
      (troop_get_slot, reg8, ":troop_no", slot_troop_custom_banner_charge_color_3),
      (troop_get_slot, reg9, ":troop_no", slot_troop_custom_banner_charge_type_4),
      (val_add, reg9, custom_banner_charges_begin),
      (troop_get_slot, reg11, ":troop_no", slot_troop_custom_banner_charge_color_4),

      (try_begin),
        (eq, ":num_charges", 1),
        (try_begin),
          (eq, ":positioning", 0),
          (assign, reg1, 100),
        (else_try),
          (assign, reg1, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 2),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -25),
          (position_set_x, pos1, 25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 3),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 33),
          (position_set_y, pos2, -33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -33),
          (position_set_x, pos2, 33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, 30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 3),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, 30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 4),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, -25),
          (position_set_y, pos2, -25),
          (position_set_x, pos3, 25),
          (position_set_y, pos3, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
          (assign, reg10, 50),
        (else_try),
          (position_set_y, pos0, 30),
          (position_set_x, pos1, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos3, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
          (assign, reg10, 35),
        (try_end),
      (try_end),
     ]),
  # script_get_random_custom_banner
  # Input: arg1 = troop_no
  # Output: none
  ("get_random_custom_banner",
    [
      (store_script_param, ":troop_no", 1),
      (store_random_in_range, ":num_charges", 1, 5),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_num_charges, ":num_charges"),
      (store_random_in_range, ":random_color_index", 0, 42),
      (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
      (assign, ":color_1", reg0),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_1, ":color_1"),
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":color_2", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":color_1", ":color_2"),
          (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_2, ":color_2"),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (assign, ":end_cond", 4),
      (assign, ":cur_charge", 0),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":charge_color", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_1"),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_2"),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_color_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":charge_color"),
          (store_random_in_range, ":random_charge", custom_banner_charges_begin, custom_banner_charges_end),
          (val_sub, ":random_charge", custom_banner_charges_begin),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_type_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":random_charge"),
          (val_add, ":cur_charge", 1),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (store_random_in_range, ":random_bg", custom_banner_backgrounds_begin, custom_banner_backgrounds_end),
      (val_sub, ":random_bg", custom_banner_backgrounds_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_type, ":random_bg"),
      (store_random_in_range, ":random_flag", custom_banner_flag_types_begin, custom_banner_flag_types_end),
      (val_sub, ":random_flag", custom_banner_flag_types_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_flag_type, ":random_flag"),
      (store_random_in_range, ":random_positioning", 0, 4),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_positioning, ":random_positioning"),
     ]),
  # script_get_custom_banner_color_from_index
  # Input: arg1 = color_index
  # Output: reg0 = color
  ("get_custom_banner_color_from_index",
    [
      (store_script_param, ":color_index", 1),

      (assign, ":cur_color", 0xFF000000),
      (assign, ":red", 0x00),
      (assign, ":green", 0x00),
      (assign, ":blue", 0x00),
      (store_mod, ":mod_i_color", ":color_index", 7),
      (try_begin),
        (eq, ":mod_i_color", 0),
        (assign, ":blue", 0xFF),
      (else_try),
        (eq, ":mod_i_color", 1),
        (assign, ":red", 0xEE),
      (else_try),
        (eq, ":mod_i_color", 2),
        (assign, ":red", 0xFB),
        (assign, ":green", 0xAC),
      (else_try),
        (eq, ":mod_i_color", 3),
        (assign, ":red", 0x5F),
        (assign, ":blue", 0xFF),
      (else_try),
        (eq, ":mod_i_color", 4),
        (assign, ":red", 0x05),
        (assign, ":green", 0x44),
      (else_try),
        (eq, ":mod_i_color", 5),
        (assign, ":red", 0xEE),
        (assign, ":green", 0xEE),
        (assign, ":blue", 0xEE),
      (else_try),
        (assign, ":red", 0x22),
        (assign, ":green", 0x22),
        (assign, ":blue", 0x22),
      (try_end),
      (store_div, ":cur_tone", ":color_index", 7),
      (store_sub, ":cur_tone", 8, ":cur_tone"),
      (val_mul, ":red", ":cur_tone"),
      (val_div, ":red", 8),
      (val_mul, ":green", ":cur_tone"),
      (val_div, ":green", 8),
      (val_mul, ":blue", ":cur_tone"),
      (val_div, ":blue", 8),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":cur_color", ":blue"),
      (val_add, ":cur_color", ":green"),
      (val_add, ":cur_color", ":red"),
      (assign, reg0, ":cur_color"),
     ]),
  # script_cf_check_color_visibility
  # Input: arg1 = color_1, arg2 = color_2
  # Output: none
  ("cf_check_color_visibility",
    [
      (store_script_param, ":color_1", 1),
      (store_script_param, ":color_2", 2),
      (store_mod, ":blue_1", ":color_1", 256),
      (store_div, ":green_1", ":color_1", 256),
      (val_mod, ":green_1", 256),
      (store_div, ":red_1", ":color_1", 256 * 256),
      (val_mod, ":red_1", 256),
      (store_mod, ":blue_2", ":color_2", 256),
      (store_div, ":green_2", ":color_2", 256),
      (val_mod, ":green_2", 256),
      (store_div, ":red_2", ":color_2", 256 * 256),
      (val_mod, ":red_2", 256),
      (store_sub, ":red_dif", ":red_1", ":red_2"),
      (val_abs, ":red_dif"),
      (store_sub, ":green_dif", ":green_1", ":green_2"),
      (val_abs, ":green_dif"),
      (store_sub, ":blue_dif", ":blue_1", ":blue_2"),
      (val_abs, ":blue_dif"),
      (assign, ":max_dif", 0),
      (val_max, ":max_dif", ":red_dif"),
      (val_max, ":max_dif", ":green_dif"),
      (val_max, ":max_dif", ":blue_dif"),
      (ge, ":max_dif", 64),
     ]),
# Jrider +
   ###################################################################################
   # REPORT PRESENTATIONS v1.2 scripts
   # Script overlay_container_add_listbox_item
   # use ...
   # return ...
   ("overlay_container_add_listbox_item", [
        (store_script_param, ":line_y", 1),
        (store_script_param, ":npc_id", 2),

        (set_container_overlay, "$g_jrider_character_relation_listbox"),

        # create text overlay for entry
        (create_text_overlay, reg10, s1, tf_left_align),
        (overlay_set_color, reg10, 0xDDDDDD),
        (position_set_x, pos1, 650),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),

        # create button
        (create_image_button_overlay, reg10, "mesh_white_plane", "mesh_white_plane"),
        (position_set_x, pos1, 0), # 590 real, 0 scrollarea
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),
        (position_set_x, pos1, 16000),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (overlay_set_alpha, reg10, 0),
        (overlay_set_color, reg10, 0xDDDDDD),

        # store relation of button id to character number for use in triggers
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", reg10),
        (troop_set_slot, "trp_temp_array_b", ":current_storage_index", "$num_charinfo_candidates"),

        # reset variables if appropriate flags are up
        (try_begin),
            (try_begin),
                (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
                (ge, "$g_jrider_reset_selected_on_faction", 1),

                (assign, "$character_info_id", ":npc_id"),
                (assign, "$g_jrider_last_checked_indicator", reg10),
                (assign, "$g_latest_character_relation_entry", "$num_charinfo_candidates"),
            (try_end),
        (try_end),

        # close the container
        (set_container_overlay, -1),
   ]),
   # script get_relation_candidate_list_for_presentation
   # return a list of candidate according to type of list and restrict options
   # Use ...
   ("fill_relation_canditate_list_for_presentation",
    [
        (store_script_param, ":pres_type", 1),
        (store_script_param, ":base_candidates_y", 2),

        # Type of list from global variable: 0 courtship, 1 known lords
        (try_begin),
        ## For courtship:
            (eq, ":pres_type", 0),

            (try_for_range_backwards, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
                (troop_slot_ge, ":lady", slot_troop_met, 1), # met or better
                (troop_slot_eq, ":lady", slot_troop_spouse, -1), # unmarried

                # use faction filter
                (store_troop_faction, ":lady_faction", ":lady"),
                (val_sub, ":lady_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":lady_faction"),

                (call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
                (gt, reg0, 0),
                (assign, reg3, reg0),

                (str_store_troop_name, s2, ":lady"),

                (store_current_hours, ":hours_since_last_visit"),
                (troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
                (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
                (store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
                (assign, reg4, ":days_since_last_visit"),

                #(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
                (str_store_string, s1, "@{s2}: {reg3}, {reg4} days"),

                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":lady"),

                # candidate found, store troop id for later use
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":lady"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## End courtship relations
        (else_try),
        ## For lord relations
            (eq, ":pres_type", 1),

            # Loop to identify
            (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                (troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
            (try_end),

            (try_for_range, ":unused", active_npcs_begin, active_npcs_end),

                (assign, ":score_to_beat", 101),
                (assign, ":best_relation_remaining_npc", -1),

                (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                        (troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
                        (troop_slot_ge, ":active_npc", slot_troop_met, 1),
                        (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

                        (call_script, "script_troop_get_player_relation", ":active_npc"),
                        (assign, ":relation_with_player", reg0),
                        (le, ":relation_with_player", ":score_to_beat"),

                        (assign, ":score_to_beat", ":relation_with_player"),
                        (assign, ":best_relation_remaining_npc", ":active_npc"),
                (try_end),
                (gt, ":best_relation_remaining_npc", -1),

                (str_store_troop_name, s4, ":best_relation_remaining_npc"),
                (assign, reg4, ":score_to_beat"),

                (str_store_string, s1, "@{s4}: {reg4}"),
                (troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),

                # use faction filter
                (store_troop_faction, ":npc_faction", ":best_relation_remaining_npc"),
                (val_sub, ":npc_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":npc_faction"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":best_relation_remaining_npc"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":best_relation_remaining_npc"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## END Lords relations
        (else_try),
        ## Character and Companions
            (eq, ":pres_type", 2),

            # companions
			#gekokujo 3.0 microfactions! include fort companions start
            #(try_for_range_backwards, ":companion", companions_begin, companions_end),
            (try_for_range_backwards, ":companion", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
                (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),

                (str_store_troop_name, s1, ":companion"),

        (try_begin),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
                    (str_store_string, s1, "@{s1}(gathering support)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
                    (str_store_string, s1, "@{s1} (intelligence)" ),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
                    (neg|troop_slot_eq, ":companion", slot_troop_current_mission, 8),
                    (str_store_string, s1, "@{s1} (ambassy)"),
                (else_try),
                        (eq, ":companion", "$g_player_minister"),
                    (str_store_string, s1, "@{s1} (minister"),
                (else_try),
                    (main_party_has_troop, ":companion"),
                    (str_store_string, s1, "@{s1} (under arms)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
                    (str_store_string, s1, "@{s1} (attempting to rejoin)"),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_cur_center, 1),
                    (str_store_string, s1, "@{s1} (separated after battle)"),
                (try_end),
                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":companion"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":companion"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # END companions

            # Wife/Betrothed
            # END Wife/Betrothed

            (try_begin),
            # Character
                (str_store_troop_name, s1, "trp_player"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", "trp_player"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", "trp_player"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # End Character

        (try_end),
        ## END Character and Companions
    ]),
    # script get_troop_relation_to_player_string
    # return relation to player string in the specified parameters
    #
    ("get_troop_relation_to_player_string",
     [
         (store_script_param, ":target_string", 1),
         (store_script_param, ":troop_no", 2),

         (call_script, "script_troop_get_player_relation", ":troop_no"),
         (assign, ":relation", reg0),
         (str_clear, s61),

         (store_add, ":normalized_relation", ":relation", 100),
         (val_add, ":normalized_relation", 5),
         (store_div, ":str_offset", ":normalized_relation", 10),
         (val_clamp, ":str_offset", 0, 20), 
         (store_add, ":str_rel_id", "str_relation_mnus_100_ns",  ":str_offset"),

         ## Make something if troop has relation but not strong enought to warrant a string
         (try_begin),
           (neq, ":str_rel_id", "str_relation_plus_0_ns"),
           (str_store_string, s61, ":str_rel_id"),
         (else_try),
           (neg|eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ knows of you."),
         (else_try),
           (eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ has no opinion about you."),
         (try_end),

         ## copy result string to target string
         (str_store_string_reg, ":target_string", s61),
     ]),
    # script get_troop_holdings
    # returns number of fief and list name (reg50, s50)
    ("get_troop_holdings",
     [
         (store_script_param, ":troop_no", 1),

         (assign, ":owned_centers", 0),
         (assign, ":num_centers", 0),
         (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
             (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
             (try_begin),
               (eq, ":num_centers", 0),
               (str_store_party_name, s50, ":cur_center"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (eq, ":num_centers", 1),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{s57} and {s50}"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{!}{s57}, {s50}"),
               (val_add, ":owned_centers", 1),
             (try_end),
             (val_add, ":num_centers", 1),
         (try_end),
         (assign, reg50, ":owned_centers"),
     ]),
    # script generate_extended_troop_relation_information_string
    # return information about troop according to type (lord, lady, maiden)
    # Use (hm lots of registers and strings)
    # result stored in s1
    ("generate_extended_troop_relation_information_string",
     [
         (store_script_param, ":troop_no", 1),

         # clear the strings and registers we'll use to prevent external interference
         (str_clear, s1),
         (str_clear, s2),
         (str_clear, s60),
         (str_clear, s42),
         (str_clear, s43),
         (str_clear, s44),
         (str_clear, s45),
         (str_clear, s46),
         (str_clear, s47),
         (str_clear, s48),
         (str_clear, s49),
         (str_clear, s50),
         (assign, reg40,0),
         (assign, reg41,0),
         (assign, reg43,0),
         (assign, reg44,0),
         (assign, reg46,0),
         (assign, reg47,0),
         (assign, reg48,0),
         (assign, reg49,0),
         (assign, reg50,0),
         (assign, reg51,0),

         (try_begin),
             (eq, ":troop_no", "trp_player"),
             (overlay_set_display, "$g_jrider_character_faction_filter", 0),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Honor - $player_honor
             (assign, reg42, "$player_honor"),

             # Right to rule - $player_right_to_rule
             (assign, reg43, "$player_right_to_rule"),

             # Current faction
             (store_add, reg45, "$players_kingdom"),
             (try_begin),
                 (is_between, "$players_kingdom", "fac_player_supporters_faction", npc_kingdoms_end),
                 (str_store_faction_name, s45, "$players_kingdom"),
             (else_try),
                 (assign, reg45, 0),
                 (str_store_string, s45, "@Japan."),
             (try_end),

             # status
             (assign, ":origin_faction", "$players_kingdom"),
             (try_begin),
                 (is_between, ":origin_faction", npc_kingdoms_begin, npc_kingdoms_end),
                 (str_store_string, s44, "@sworn man"),
             (else_try),
                 (eq, ":origin_faction", "fac_player_supporters_faction"),
                 (str_store_string, s44, "@ruler"),
             (else_try),
                 (str_store_string, s44, "@free man"),
             (try_end),

             # Current liege and relation
             (faction_get_slot, ":liege", "$players_kingdom", slot_faction_leader),
             (str_store_troop_name, s46, ":liege"),
             (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
             (else_try),
                 (assign, reg46, ":liege"),
                 (str_clear, s47),
                 (str_clear, s60),

                 # Relation to liege
                 (call_script, "script_get_troop_relation_to_player_string", s47, ":liege"),
             (end_try),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

             #### Final Storage
             (str_store_string, s1, "@{s1} Renown: {reg40}, Controversy: {reg41}^Honor: {reg42}, Right to rule: {reg43}^\
You are a {s44} of {s45}^{reg45?{reg46?Your liege, {s46},{s47}:You are the ruler of {s45}}:}^^Friends: ^Enemies: ^^Fiefs:^  {reg50?{s50}:no fief}"),
         #######################
         # END Player information
         (else_try),
         #######################
         # Lord information
             (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Get Reputation type - slot_lord_reputation_type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (assign, reg42, "str_personality_archetypes"),
             (val_add, reg42, ":reputation"),
             (str_store_string, s42, reg42),

             (assign, reg42, ":reputation"),
             # Intrigue impatience - slot_troop_intrigue_impatience
             (troop_get_slot, ":impatience", ":troop_no", slot_troop_intrigue_impatience),
             (assign, reg43, ":impatience"),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
             (end_try),
             (str_store_faction_name, s45, ":faction"),

             # Current liege - deduced from current faction
             (faction_get_slot, ":liege", ":faction", slot_faction_leader),
             (try_begin),
               #When a member of a faction without a valid leader
               (lt, ":liege", 0),
               (assign, reg46, ":liege"),
               (str_store_string, s46, "str_noone"),
               (assign, reg47, 0),
             (else_try),
               (str_store_troop_name, s46, ":liege"),
               (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
               (else_try),
                 (assign, reg46, ":liege"),
                 # Relation to liege
                 (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
                 (assign, reg47, reg0),
               (end_try),
             (try_end),

             # Promised a fief ?
             (troop_get_slot, reg51, ":troop_no", slot_troop_promised_fief),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

              # slot_troop_prisoner_of_party
              (assign, reg48, 0),
              (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
              (try_end),

              # Days since last meeting
              (store_current_hours, ":hours_since_last_visit"),
              (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
              (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
              (store_div, reg49, ":hours_since_last_visit", 24),

              #### Final Storage (8 lines)
              (str_store_string, s1, "@{s1}{s2} {reg46?Reputed to be {s42}:}^Renown: {reg40}, Controversy: {reg41} {reg46?Impatience: {reg43}:}^\
{s44} samurai of the {s45}^{reg46?Overlord: {s46}, Relation: {reg47}:Ruler of the {s45}}^^{reg48?Currently prisoner of the {s48}:}^\
Days since last meeting: {reg49}^^Fiefs {reg51?(was promised a fief):}:^  {reg50?{s50}:no fief}"),
        ######################
        ## END lord infomation
        (else_try),
        #########################
        # kingdom lady, unmarried
             (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
             (troop_slot_eq, ":troop_no", slot_troop_spouse, -1),

             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Reputation type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (try_begin),
                 (eq, ":reputation", lrep_conventional),
                 (str_store_string, s42, "@conventional"),
             (else_try),
                 (eq, ":reputation", lrep_adventurous),
                 (str_store_string, s42, "@adventurous"),
             (else_try),
                 (eq, ":reputation", lrep_otherworldly),
                 (str_store_string, s42, "@otherwordly"),
             (else_try),
                 (eq, ":reputation", lrep_ambitious),
                 (str_store_string, s42, "@ambitious"),
             (else_try),
                 (eq, ":reputation", lrep_moralist),
                 (str_store_string, s42, "@moralist"),
             (else_try),
                 (assign, reg42, "str_personality_archetypes"),
                 (val_add, reg42, ":reputation"),
                 (str_store_string, s42, reg42),
             (try_end),

             # courtship state - slot_troop_courtship_state
             (troop_get_slot, ":courtship_state", ":troop_no", slot_troop_courtship_state),
             (try_begin),
               (eq, ":courtship_state", 1),
               (str_store_string, s43, "@just met"),
             (else_try),
               (eq, ":courtship_state", 2),
               (str_store_string, s43, "@admirer"),
             (else_try),
               (eq, ":courtship_state", 3),
               (str_store_string, s43, "@promised"),
             (else_try),
               (eq, ":courtship_state", 4),
               (str_store_string, s43, "@breakup"),
             (else_try),
               (str_store_string, s43, "@unknown"),
             (try_end),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
             (end_try),
             (str_store_faction_name, s45, ":faction"),

             # Father/Guardian
             (assign, reg46, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_father, 0),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
                 (assign, reg46, 1),
             (else_try),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
             (try_end),
             (str_store_troop_name, s46, ":guardian"),

             # Relation with player
             (str_clear, s47),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s47, ":guardian"),

             # courtship permission - slot_lord_granted_courtship_permission
             (try_begin),
                 (troop_slot_ge, ":guardian", slot_lord_granted_courtship_permission, 1),
                 (assign, reg45, 1),
             (else_try),
                 (assign, reg45, 0),
             (try_end),

             # betrothed
             (assign, reg48, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_betrothed, 0),
                 (troop_get_slot, reg48, ":troop_no", slot_troop_betrothed),
                 (str_store_troop_name, s48, reg48),
                 (assign, reg48, 1),
             (try_end),

             # Days since last meeting
             (store_current_hours, ":hours_since_last_visit"),
             (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
             (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
             (store_div, reg49, ":hours_since_last_visit", 24),

             # Heard poems
             (assign, reg50, 0),
             (str_clear, s50),

             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_heroic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Heroic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_allegoric_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Allegoric {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_comic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Comic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_mystic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Mystic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_tragic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Tragic {s50}"),
             (try_end),

             #### Final Storage (8 lines)
             (str_store_string, s1, "@{s1}{s2} Controversy: {reg41}^Reputation: {s42}, Courtship state: {s43}^\
Belongs to the {s45}^{reg46?Her father, {s46}:Her guardian, {s46}}{s47}^Allowed to visit: {reg45?yes:no} {reg48?Betrothed to {s48}:}^^\
Days since last meeting: {reg49}^^Poems:^  {reg50?{s50}:no poem heard}"),
        #########################
        # END kingdom lady, unmarried
        (else_try),
        #########################
        # companions
		    #gekokujo 3.0 microfactions! include fort companions start
            #(is_between, ":troop_no", companions_begin, companions_end),
            (is_between, ":troop_no", companions_begin, fort_companions_end),
		    #gekokujo 3.0 microfactions! include fort companions end
            (overlay_set_display, "$g_jrider_character_faction_filter", 0),

            (str_store_troop_name, s1, ":troop_no"),

            (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),

            (assign, reg42, "str_personality_archetypes"),
            (val_add, reg42, ":reputation"),
            (str_store_string, s42, reg42),

            # birthplace
            (troop_get_slot, ":home", ":troop_no", slot_troop_home),
            (str_store_party_name, s43, ":home"),

            # contacts town - slot_troop_town_with_contacts
            (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
            (str_store_party_name, s44, ":contact_town"),

            # current faction of contact town
            (store_faction_of_party, ":town_faction", ":contact_town"),
            (str_store_faction_name, s45, ":town_faction"),

            # slot_troop_prisoner_of_party
            (assign, reg48, 0),
            (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
            (try_end),

            # Days since last meeting
            (store_current_hours, ":hours_since_last_visit"),
            (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
            (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
            (store_div, reg49, ":hours_since_last_visit", 24),

            (try_begin), # Companion gathering support for Right to Rule
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_kingsupport),
                (str_store_string, s50, "@Gathering support"),
            (else_try), # Companion gathering intelligence
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_gather_intel),
                (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
                (store_faction_of_party, ":town_faction", ":contact_town"),
                (str_store_faction_name, s66, ":town_faction"),
                (str_store_string, s50, "@Gathering intelligence in the {s66}"),
            (else_try), # Companion on peace mission
                (troop_slot_ge, ":troop_no", slot_troop_current_mission, npc_mission_peace_request),
                (neg|troop_slot_ge, ":troop_no", slot_troop_current_mission, 8),

                (troop_get_slot, ":troop_no", ":troop_no", slot_troop_mission_object),
                (str_store_faction_name, s66, ":faction"),

                (str_store_string, s50, "@Ambassy to {s66}"),
            (else_try), # Companion is serving as minister player has court
                (eq, ":troop_no", "$g_player_minister"),
                (str_store_string, s50, "@Minister"),
            (else_try),
                (str_store_string, s50, "@none"),
        (try_end),

            # days left
            (troop_get_slot, reg50, ":troop_no", slot_troop_days_on_mission),

            #### Final Storage (8 lines)
            (str_store_string, s1, "@{s1}, {s2}^Reputation: {s42}^\
Born at {s43}^Contact in {s44} of the {s45}.^\
^{reg48?Currently prisoner of the {s48}:}^Days since last talked to: {reg49}^^Current mission:^  {s50}{reg50?, back in {reg50} days.:}"),
        #########################
        # END companions
        (try_end),
    ]),
    # Script generate_known_poems_string
    # generate in s1 list of known poems filling with blank lines for unknown ones
    ("generate_knonwn_poems_string",
     [
        # Known poems string
        (assign, ":num_poems", 0),
        (str_store_string, s1, "str_s1__poems_known"),
        (try_begin),
            (gt, "$allegoric_poem_recitations", 0),
            (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$tragic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$comic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$heroic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$mystic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
            (val_add, ":num_poems", 1),
        (try_end),

        # fill blank lines
        (try_for_range, ":num_poems", 5),
            (str_store_string, s1, "@{s1}^"),
        (try_end),
    ]),
  ("prsnt_line",
    [
      (store_script_param, ":size_x", 1),
      (store_script_param, ":size_y", 2),
      (store_script_param, ":pos_x", 3),
      (store_script_param, ":pos_y", 4),
      (store_script_param, ":color", 5),

      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (val_mul, ":size_x", 50),
      (val_mul, ":size_y", 50),
      (position_set_x, pos0, ":size_x"),
      (position_set_y, pos0, ":size_y"),
      (overlay_set_size, reg1, pos0),
      (position_set_x, pos0, ":pos_x"),
      (position_set_y, pos0, ":pos_y"),
      (overlay_set_position, reg1, pos0),
      (overlay_set_color, reg1, ":color"),
  ]),
]
