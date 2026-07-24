# -*- coding: UTF-8 -*-

from header_common import *
from header_scene_props import *
from header_operations import *
from header_triggers import *
from header_sounds import *
from header_mission_templates import *
from module_constants import *

####################################################################################################################




ym_1 = 12#最大加特林数量
ym_2 = 900
ym_3 = ym_2 + ym_1

ym_4 = 1# 自动在玩家所在队伍一侧生成加特林。
ym_5 = 420       # 每挺之间横向间隔 4.2 米。
ym_6 = -450  # 相对我方步兵命令点后退 4.5 米，避免刷到队伍正中。

ym_7 = 480
ym_8 = 481

ym_9 = 820
ym_10 = 821
ym_11 = 822
ym_12 = 823
ym_13 = 824
ym_14 = 825

ym_15 = 650          # 士兵距离加特林 6.5 米内才会尝试占用。
ym_16 = 8500           # 最大射程 85 米。
ym_17 = -110       # 士兵站在 prop 原点后方 1.1 米。
ym_18 = 0
ym_19 = 130              # 炮口相对 prop 原点向前 1.3 米。
ym_20 = 95               # 炮口高度 0.95 米。
ym_21 = 140    # 每挺约 7 发/秒。
ym_22 = 8
ym_23 = 19            
ym_24 = 400

#场景 prop触发器


ym_25 = [
  (ti_on_scene_prop_init, [
    (store_trigger_param_1, ":ym_29"),
    (scene_prop_set_slot, ":ym_29", ym_9, -1),
    (scene_prop_set_slot, ":ym_29", ym_10, -1),
    (scene_prop_set_slot, ":ym_29", ym_11, -1),
    (scene_prop_set_slot, ":ym_29", ym_12, -1),
    (scene_prop_set_slot, ":ym_29", ym_13, 0),
    (scene_prop_set_slot, ":ym_29", ym_14, ym_24),
  ]),

  (ti_on_scene_prop_hit, [
    (store_trigger_param_1, ":ym_29"),
    (store_trigger_param_2, ":ym_30"),
    (call_script, "script_coreyna_gatling_prop_hit", ":ym_29", ":ym_30"),
  ]),
]

#场景物
ym_26 = [
  ("coreyna_gatling", 0, "gatling", "0", ym_25),
]


#脚本
ym_27 = [
  ("coreyna_gatling_position_face_position",
  [

    (store_script_param, ":ym_31", 1),
    (store_script_param, ":ym_32", 2),
    (assign, ":ym_33", 9999999),
    (assign, ":ym_34", 0),
    (try_for_range, ":ym_35", 0, 361),
      (copy_position, pos60, ":ym_31"),
      (position_rotate_x, pos60, ":ym_35"),
      (copy_position, pos61, pos60),
      (position_move_y, pos61, 1000),
      (get_distance_between_positions, ":ym_36", pos61, ":ym_32"),
      (lt, ":ym_36", ":ym_33"),
      (assign, ":ym_33", ":ym_36"),
      (assign, ":ym_34", ":ym_35"),
    (try_end),
    (position_rotate_x, ":ym_31", ":ym_34"),

    (assign, ":ym_33", 9999999),
    (assign, ":ym_37", 0),
    (try_for_range, ":ym_35", 0, 361),
      (copy_position, pos60, ":ym_31"),
      (position_rotate_z, pos60, ":ym_35"),
      (copy_position, pos61, pos60),
      (position_move_y, pos61, 1000),
      (get_distance_between_positions, ":ym_36", pos61, ":ym_32"),
      (lt, ":ym_36", ":ym_33"),
      (assign, ":ym_33", ":ym_36"),
      (assign, ":ym_37", ":ym_35"),
    (try_end),
    (position_rotate_z, ":ym_31", ":ym_37"),
  ]),

  ("coreyna_gatling_setup_instance",
  [
    (store_script_param, ":ym_29", 1),
    (store_script_param, ":ym_38", 2),
    (scene_prop_set_slot, ":ym_29", ym_9, ":ym_38"),
    (scene_prop_set_slot, ":ym_29", ym_10, -1),
    (scene_prop_set_slot, ":ym_29", ym_11, -1),
    (scene_prop_set_slot, ":ym_29", ym_12, -1),
    (scene_prop_set_slot, ":ym_29", ym_13, 0),
    (scene_prop_set_slot, ":ym_29", ym_14, ym_24),
  ]),

  ("coreyna_gatling_get_player_team_anchor",
  [
    (assign, reg0, -1),
    (init_position, pos10),
    (get_player_agent_no, ":ym_39"),
    (try_begin),
      (ge, ":ym_39", 0),
      (agent_is_active, ":ym_39"),
      (agent_get_team, ":ym_40", ":ym_39"),
      (assign, reg0, ":ym_40"),
      (team_get_order_position, pos10, ":ym_40", grc_infantry),
      (position_set_z, pos10, 10000),
      (position_set_z_to_ground_level, pos10),
    (try_end),
  ]),

  ("coreyna_gatling_find_enemy_position_for_team",
  [

    (store_script_param, ":ym_40", 1),
    (assign, reg0, 0),
    (assign, ":ym_33", 99999999),
    (copy_position, pos12, pos10),
    (try_for_agents, ":ym_41"),
      (agent_is_active, ":ym_41"),
      (agent_is_alive, ":ym_41"),
      (agent_is_human, ":ym_41"),
      (agent_get_team, ":ym_42", ":ym_41"),
      (teams_are_enemies, ":ym_40", ":ym_42"),
      (agent_get_position, pos13, ":ym_41"),
      (get_distance_between_positions, ":ym_43", pos10, pos13),
      (lt, ":ym_43", ":ym_33"),
      (assign, ":ym_33", ":ym_43"),
      (copy_position, pos12, pos13),
      (assign, reg0, 1),
    (try_end),
  ]),

  ("ym_4",
  [
    (call_script, "script_coreyna_gatling_get_player_team_anchor"),
    (assign, ":ym_40", reg0),
    (try_begin),
      (ge, ":ym_40", 0),
      (assign, "$ym_44", 1),
      (scene_prop_get_num_instances, ":ym_45", "spr_coreyna_gatling"),
      (store_sub, ":ym_46", ym_1, ":ym_45"),
      (val_max, ":ym_46", 0),
      (gt, ":ym_46", 0),

      (call_script, "script_coreyna_gatling_find_enemy_position_for_team", ":ym_40"),
      (assign, ":ym_47", reg0),
      (try_begin),
        (eq, ":ym_47", 1),
        (set_fixed_point_multiplier, 100),
        (position_get_z, ":ym_48", pos10),
        (position_set_z, pos12, ":ym_48"),
        (set_fixed_point_multiplier, 1),
      (try_end),

      (store_sub, ":ym_49", ":ym_46", 1),
      (val_mul, ":ym_49", ym_5),
      (val_div, ":ym_49", 2),

      (try_for_range, ":ym_50", 0, ":ym_46"),
        (copy_position, pos11, pos10),
        (try_begin),
          (eq, ":ym_47", 1),
          (call_script, "script_coreyna_gatling_position_face_position", 11, 12),
        (try_end),
        (store_mul, ":ym_51", ":ym_50", ym_5),
        (val_sub, ":ym_51", ":ym_49"),
        (position_move_x, pos11, ":ym_51"),
        (position_move_y, pos11, ym_6),
        (position_set_z, pos11, 10000),
        (position_set_z_to_ground_level, pos11),
        (set_spawn_position, pos11),
        (spawn_scene_prop, "spr_coreyna_gatling"),
      (try_end),
    (try_end),
  ]),

  ("coreyna_gatling_register_scene_props",
  [
    (try_begin),
      (eq, ym_4, 1),
      (neq, "$ym_44", 1),
      (call_script, "script_coreyna_gatling_auto_spawn_for_player_team"),
    (try_end),

    (store_current_scene, ":ym_52"),
    (try_for_range, ":ym_53", ym_2, ym_3),
      (scene_set_slot, ":ym_52", ":ym_53", -1),
    (try_end),

    (scene_prop_get_num_instances, ":ym_54", "spr_coreyna_gatling"),
    (val_min, ":ym_54", ym_1),
    (try_for_range, ":ym_55", 0, ":ym_54"),
      (scene_prop_get_instance, ":ym_29", "spr_coreyna_gatling", ":ym_55"),
      (ge, ":ym_29", 0),
      (store_add, ":ym_53", ym_2, ":ym_55"),
      (scene_set_slot, ":ym_52", ":ym_53", ":ym_29"),
      (call_script, "script_coreyna_gatling_setup_instance", ":ym_29", ":ym_55"),
    (try_end),
    (assign, "$ym_56", 1),
  ]),

  ("coreyna_gatling_clear_gunner",
  [
    (store_script_param, ":ym_29", 1),
    (scene_prop_get_slot, ":ym_57", ":ym_29", ym_10),
    (try_begin),
      (ge, ":ym_57", 0),
      (agent_is_active, ":ym_57"),
      (agent_set_slot, ":ym_57", ym_7, 0),
      (agent_clear_scripted_mode, ":ym_57"),
      (agent_set_speed_limit, ":ym_57", 100),
    (try_end),
    (scene_prop_set_slot, ":ym_29", ym_10, -1),
    (scene_prop_set_slot, ":ym_29", ym_11, -1),
    (scene_prop_set_slot, ":ym_29", ym_12, -1),
  ]),

  ("coreyna_gatling_find_gunner_for_prop",
  [

    (store_script_param, ":ym_29", 1),
    (assign, reg0, -1),
    (assign, ":ym_33", ym_15),
    (prop_instance_get_position, pos1, ":ym_29"),
    (try_for_agents, ":ym_58"),
      (agent_is_active, ":ym_58"),
      (agent_is_alive, ":ym_58"),
      (agent_is_human, ":ym_58"),
      (agent_is_non_player, ":ym_58"),
      (agent_get_horse, ":ym_59", ":ym_58"),
      (lt, ":ym_59", 0),
      (agent_get_slot, ":ym_60", ":ym_58", ym_7),
      (le, ":ym_60", 0),
      (agent_get_position, pos2, ":ym_58"),
      (get_distance_between_positions, ":ym_43", pos1, pos2),
      (lt, ":ym_43", ":ym_33"),
      (assign, ":ym_33", ":ym_43"),
      (assign, reg0, ":ym_58"),
    (try_end),
  ]),

  ("coreyna_gatling_find_target",
  [

    (store_script_param, ":ym_61", 1),
    (store_script_param, ":ym_62", 2),
    (assign, reg0, -1),
    (assign, reg1, 9999999),
    (try_for_agents, ":ym_41"),
      (agent_is_active, ":ym_41"),
      (agent_is_alive, ":ym_41"),
      (agent_is_human, ":ym_41"),
      (agent_get_team, ":ym_42", ":ym_41"),
      (teams_are_enemies, ":ym_61", ":ym_42"),
      (agent_get_position, pos3, ":ym_41"),
      (position_move_z, pos3, 110),
      (get_distance_between_positions, ":ym_43", ":ym_62", pos3),
      (lt, ":ym_43", reg1),
      (lt, ":ym_43", ym_16),
      (position_has_line_of_sight_to_position, ":ym_62", pos3),
      (assign, reg0, ":ym_41"),
      (assign, reg1, ":ym_43"),
    (try_end),
  ]),

  ("coreyna_gatling_apply_hit",
  [

    (store_script_param, ":ym_57", 1),
    (store_script_param, ":ym_41", 2),
    (store_script_param, ":ym_43", 3),
    (assign, ":ym_63", 92),
    (store_div, ":ym_64", ":ym_43", 150),
    (val_sub, ":ym_63", ":ym_64"),
    (val_clamp, ":ym_63", 35, 93),
    (store_random_in_range, ":ym_65", 0, 100),
    (try_begin),
      (lt, ":ym_65", ":ym_63"),
      (store_random_in_range, ":ym_66", ym_22, ym_23),
      (agent_deliver_damage_to_agent, ":ym_57", ":ym_41", ":ym_66"),
    (else_try),
      (agent_get_position, pos4, ":ym_41"),
      (store_random_in_range, ":ym_67", -120, 121),
      (store_random_in_range, ":ym_68", -120, 121),
      (position_move_x, pos4, ":ym_67"),
      (position_move_y, pos4, ":ym_68"),
      (particle_system_burst, "psys_bullet_kick_dirt", pos4, 3),
      (particle_system_burst, "psys_bullet_kick_dust", pos4, 3),
    (try_end),
  ]),

  ("coreyna_gatling_fire_from_prop",
  [

    (store_script_param, ":ym_29", 1),
    (store_script_param, ":ym_57", 2),
    (agent_is_active, ":ym_57"),
    (agent_is_alive, ":ym_57"),
    (agent_get_team, ":ym_61", ":ym_57"),

    (prop_instance_get_position, pos1, ":ym_29"),
    (copy_position, pos2, pos1),
    (position_move_y, pos2, ym_19),
    (position_move_z, pos2, ym_20),

    (call_script, "script_coreyna_gatling_find_target", ":ym_61", 2),
    (assign, ":ym_41", reg0),
    (assign, ":ym_43", reg1),
    (try_begin),
      (ge, ":ym_41", 0),
      (agent_is_active, ":ym_41"),
      (agent_is_alive, ":ym_41"),
      (scene_prop_set_slot, ":ym_29", ym_12, ":ym_41"),
      (agent_set_look_target_agent, ":ym_57", ":ym_41"),

      (agent_get_position, pos3, ":ym_41"),
      (position_move_z, pos3, 110),
      (call_script, "script_coreyna_gatling_position_face_position", 2, 3),
      (store_random_in_range, ":ym_69", -2, 3),
      (store_random_in_range, ":ym_70", -3, 4),
      (position_rotate_x, pos2, ":ym_69"),
      (position_rotate_z, pos2, ":ym_70"),

      (particle_system_burst_no_sync, "psys_gatling_fire", pos2, 18),
      (particle_system_burst_no_sync, "psys_pistol_smoke", pos2, 5),
      (agent_play_sound, ":ym_57", "snd_c_shoot"),
      (call_script, "script_coreyna_gatling_apply_hit", ":ym_57", ":ym_41", ":ym_43"),
    (else_try),
      (scene_prop_set_slot, ":ym_29", ym_12, -1),
    (try_end),
  ]),

  ("coreyna_gatling_update_prop",
  [
    (store_script_param, ":ym_29", 1),
    (prop_instance_is_valid, ":ym_29"),
    (scene_prop_get_slot, ":ym_71", ":ym_29", ym_14),
    (gt, ":ym_71", 0),

    (scene_prop_get_slot, ":ym_57", ":ym_29", ym_10),
    (try_begin),
      (this_or_next|lt, ":ym_57", 0),
      (neg|agent_is_active, ":ym_57"),
      (call_script, "script_coreyna_gatling_clear_gunner", ":ym_29"),
      (call_script, "script_coreyna_gatling_find_gunner_for_prop", ":ym_29"),
      (assign, ":ym_57", reg0),
      (try_begin),
        (ge, ":ym_57", 0),
        (agent_get_team, ":ym_61", ":ym_57"),
        (scene_prop_set_slot, ":ym_29", ym_10, ":ym_57"),
        (scene_prop_set_slot, ":ym_29", ym_11, ":ym_61"),
        (store_add, ":ym_72", ":ym_29", 1),
        (agent_set_slot, ":ym_57", ym_7, ":ym_72"),
        (agent_set_slot, ":ym_57", ym_8, ":ym_72"),
      (try_end),
    (else_try),
      (neg|agent_is_alive, ":ym_57"),
      (call_script, "script_coreyna_gatling_clear_gunner", ":ym_29"),
    (try_end),

    (scene_prop_get_slot, ":ym_57", ":ym_29", ym_10),
    (try_begin),
      (ge, ":ym_57", 0),
      (agent_is_active, ":ym_57"),
      (agent_is_alive, ":ym_57"),
      (agent_get_horse, ":ym_59", ":ym_57"),
      (lt, ":ym_59", 0),
      (prop_instance_get_position, pos1, ":ym_29"),
      (copy_position, pos5, pos1),
      (position_move_y, pos5, ym_17),
      (position_move_z, pos5, ym_18),
      (agent_get_position, pos6, ":ym_57"),
      (get_distance_between_positions, ":ym_73", pos5, pos6),
      (try_begin),
        (gt, ":ym_73", 160),
        (agent_set_scripted_destination_no_attack, ":ym_57", pos5, 1),
        (agent_set_speed_limit, ":ym_57", 8),
      (else_try),
        (agent_set_scripted_destination_no_attack, ":ym_57", pos5, 1),
        (agent_set_speed_limit, ":ym_57", 1),
        (store_mission_timer_c_msec, ":ym_74"),
        (scene_prop_get_slot, ":ym_75", ":ym_29", ym_13),
        (ge, ":ym_74", ":ym_75"),
        (store_add, ":ym_76", ":ym_74", ym_21),
        (scene_prop_set_slot, ":ym_29", ym_13, ":ym_76"),
        (call_script, "script_coreyna_gatling_fire_from_prop", ":ym_29", ":ym_57"),
      (try_end),
    (else_try),
      (call_script, "script_coreyna_gatling_clear_gunner", ":ym_29"),
    (try_end),
  ]),

  ("coreyna_gatling_update_all",
  [
    (try_begin),
      (neq, "$ym_56", 1),
      (store_mission_timer_c_msec, ":ym_74"),
      (ge, ":ym_74", 1000),
      (call_script, "script_coreyna_gatling_register_scene_props"),
    (try_end),
    (store_current_scene, ":ym_52"),
    (try_for_range, ":ym_53", ym_2, ym_3),
      (scene_get_slot, ":ym_29", ":ym_52", ":ym_53"),
      (ge, ":ym_29", 0),
      (call_script, "script_coreyna_gatling_update_prop", ":ym_29"),
    (try_end),
  ]),

  ("coreyna_gatling_prop_hit",
  [
    (store_script_param, ":ym_29", 1),
    (store_script_param, ":ym_30", 2),
    (scene_prop_get_slot, ":ym_71", ":ym_29", ym_14),
    (try_begin),
      (gt, ":ym_71", 0),
      (assign, ":ym_66", ":ym_30"),
      (val_div, ":ym_66", 2),
      (val_clamp, ":ym_66", 5, 45),
      (val_sub, ":ym_71", ":ym_66"),
      (scene_prop_set_slot, ":ym_29", ym_14, ":ym_71"),
      (try_begin),
        (le, ":ym_71", 0),
        (scene_prop_set_slot, ":ym_29", ym_14, 0),
        (call_script, "script_coreyna_gatling_clear_gunner", ":ym_29"),
        (prop_instance_get_position, pos1, ":ym_29"),
        (particle_system_burst, "psys_bullet_kick_dust", pos1, 20),
      (else_try),
        (prop_instance_get_position, pos1, ":ym_29"),
        (particle_system_burst, "psys_bullet_kick_dust", pos1, 5),
      (try_end),
    (try_end),
  ]),
]


#战场触发器

ym_28 = [
  (ti_before_mission_start, 0, 0, [],
  [
    (assign, "$ym_56", 0),
    (assign, "$ym_44", 0),
  ]),

  (1, 0, ti_once, [],
  [
    (call_script, "script_coreyna_gatling_register_scene_props"),
  ]),

  (0.1, 0, 0, [],
  [
    (call_script, "script_coreyna_gatling_update_all"),
  ]),
]
