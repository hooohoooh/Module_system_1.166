# -*- coding: utf-8 -*-
# module_scripts_gekokujo.py -- auto split from module_scripts.py (feature: gekokujo 特有脚本)
# entries: 2 (order preserved within this file)
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


scripts_gekokujo = [

  #(call_script, "script_gekokujo_open_gate", ":gate_id", 1),
  ("gekokujo_open_gate",
    [
      (store_script_param_1, ":gate_id"),
      (store_script_param_2, ":open_time"),
      
      (set_fixed_point_multiplier, 100),
        
      (prop_instance_get_position, pos1, ":gate_id"), #absolute position of gate to pos1
      (prop_instance_get_scale, pos2, ":gate_id"), #get scale of gate to pos2
      (position_get_scale_x, ":width", pos2), #get scale of x axis to find width
      (init_position, pos3),
      (position_set_x, pos3, ":width"), #move pos3 on x axis by width
      (try_begin),
        (gt, ":width", 0), #width was a positive number, it must be the left gate
        (position_set_y, pos3, ":width"), #move pos3 on y axis by the default width
        (position_rotate_z, pos1, 90), #rotate pos1 on z axis by 90 degrees
      (else_try),
        #width was a negative number, it must be the right gate
        (val_mul, ":width", -1), #find the negative of width
        (position_set_y, pos3, ":width"), #move pos3 on y axis by the adjusted width
        (position_rotate_z, pos1, -90), #rotate pos1 on z axis by -90 degrees
      (try_end),
      (position_transform_position_to_parent, pos4, pos1, pos3), #get absolute position of pos3 relative from pos1 to pos4
      (prop_instance_animate_to_position, ":gate_id", pos4, ":open_time"),
    ]),
  #(call_script, "script_gekokujo_close_gate", ":gate_id", 1),
  ("gekokujo_close_gate",
    [
      (store_script_param_1, ":gate_id"),
      (store_script_param_2, ":open_time"),
      
      (set_fixed_point_multiplier, 100),
        
      (prop_instance_get_position, pos1, ":gate_id"), #absolute position of gate to pos1
      (prop_instance_get_scale, pos2, ":gate_id"), #get scale of gate to pos2
      (position_get_scale_x, ":width", pos2), #get scale of x axis to find width
      (init_position, pos3),
      (position_set_x, pos3, ":width"), #move pos3 on x axis by width
      (try_begin),
        (gt, ":width", 0), #width was a positive number, it must be the left gate
        (val_mul, ":width", -1), #find the negative of width
        (position_set_y, pos3, ":width"), #move pos3 on y axis by the adjusted width
        (position_rotate_z, pos1, -90), #rotate pos1 on z axis by -90 degrees
      (else_try),
        #width was a negative number, it must be the right gate
        (position_set_y, pos3, ":width"), #move pos3 on y axis by the default width
        (position_rotate_z, pos1, 90), #rotate pos1 on z axis by 90 degrees
      (try_end),
      (position_transform_position_to_parent, pos4, pos1, pos3), #get absolute position of pos3 relative from pos1 to pos4
      (prop_instance_animate_to_position, ":gate_id", pos4, ":open_time"),
    ]),
]
