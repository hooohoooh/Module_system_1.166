# -*- coding: UTF-8 -*-
from aheader_operations import *
from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from module_constants import *
from header_triggers import *
from header_terrain_types import * #gekokujo 3.0 no running away in sea battles
from ym_gatling import *

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#     
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags.
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
#  Please note that mission templates is work in progress and can be changed in the future versions.
# 
####################################################################################################################

pilgrim_disguise = [itm_gekokujo_monk_headwrap,itm_gekokujo_kimono_2_monk,itm_gekokujo_jo, itm_gekokujo_shuriken]
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian

#llf's tigger and common
#common
common_fade=(
    ti_before_mission_start,0,0,[],
    [
        (start_presentation, "prsnt_fade_from_black"),
    ]
)

common_key_press=(
	0, 0, 0, 
	[
		(key_is_down,key_x),
	],
    [
      (get_player_agent_no,":player"),
	  (agent_get_animation,reg1,":player",1),
	  (display_message,"@animation_is:{reg1}"),
	  
    ])
#tigger
common_init_cannoneer=(
	ti_on_agent_spawn, 0, 0, 
	[],
    [
      (store_trigger_param_1, ":cannoneer"),
      # Only set to -1 if not already set (common_spawn_party_cannons may have already linked a cannon)
      (agent_get_slot, ":existing_cannon", ":cannoneer", slot_agent_cannon),
      (try_begin),
        # agent slot 默认值为 0，需用 le 检查（0 和负数都视为未设置）
        (le, ":existing_cannon", 0),
        (agent_set_slot, ":cannoneer", slot_agent_cannon, -1),
      (try_end),
      # Only apply speed limit to cannoneer troop
      (agent_get_troop_id, ":troop", ":cannoneer"),
      (eq, ":troop", "trp_gekokujo_zunwang_veteran_gunner"),
      (agent_set_speed_limit, ":cannoneer", 5),
      # Offset cannoneers only if not already positioned by common_spawn_party_cannons
      (try_begin),
        (lt, ":existing_cannon", 0),
        (troop_get_slot, ":cannoneer_count", "trp_temp_array_c", 96),
        (val_add, ":cannoneer_count", 1),
        (troop_set_slot, "trp_temp_array_c", 96, ":cannoneer_count"),
        (store_mod, ":offset_dir", ":cannoneer_count", 2),
        (agent_get_position, pos31, ":cannoneer"),
        (set_fixed_point_multiplier, 100),
        (try_begin),
          (eq, ":offset_dir", 0),
          (position_move_x, pos31, 400),
        (else_try),
          (eq, ":offset_dir", 1),
          (position_move_x, pos31, -400),
        (try_end),
        (agent_set_position, ":cannoneer", pos31),
      (try_end),
    ])
common_init_cannon=(
	1,0,0,
	[],
	[
		(try_for_agents,":cannoneer"),
			(agent_is_alive,":cannoneer"),
			(agent_get_troop_id, ":troop", ":cannoneer"),
			(agent_get_slot,":cannon",":cannoneer",slot_agent_cannon),
			(lt,":cannon",0),
			(eq,":troop","trp_gekokujo_zunwang_veteran_gunner"),
			# llf: 仅NPC炮兵按旧逻辑生成火炮；玩家炮兵由party槽位系统处理
			(get_player_agent_no, ":player"),
			(agent_get_team, ":player_team", ":player"),
			(agent_get_team, ":cannoneer_team", ":cannoneer"),
			(neq, ":cannoneer_team", ":player_team"),
			(spawn_scene_prop,"spr_cannon"),
			(agent_set_slot,":cannoneer",slot_agent_cannon,reg0),
			(agent_get_position, pos31,":cannoneer"),
			(set_fixed_point_multiplier,100),
			(position_move_y, pos31,200),
			(prop_instance_set_position,reg0,pos31),
			(scene_prop_set_slot,reg0,scene_prop_driver,":cannoneer"),
			(scene_prop_set_slot,reg0,scene_prop_assistant,-1),
		(try_end),
	])
# llf 新增：战场开始时重置火炮生成标志
common_init_party_cannons_reset=(
	ti_before_mission_start, 0, ti_once, [],
	[
		(troop_set_slot, "trp_temp_array_c", 97, 0),
	])
# llf 新增：根据party火炮数量生成火炮资产（一次性）
common_spawn_party_cannons=(
	1, 0, 0,
	[
		(troop_get_slot, ":spawned", "trp_temp_array_c", 97),
		(eq, ":spawned", 0),
		(get_player_agent_no, ":player"),
		(agent_is_active, ":player"),
	],
	[
		(troop_set_slot, "trp_temp_array_c", 97, 1),
		(party_get_slot, ":num_cannons", "p_main_party", slot_party_cannons),
		(gt, ":num_cannons", 0),
		(get_player_agent_no, ":player"),
		(agent_get_team, ":team", ":player"),
		# 从玩家team的agent中找一个普通士兵，用他的位置和朝向作为基准
		(assign, ":base_agent", -1),
		(try_for_agents, ":agent"),
			(agent_is_human, ":agent"),
			(agent_is_non_player, ":agent"),
			(agent_is_alive, ":agent"),
			(agent_get_team, ":agent_team", ":agent"),
			(eq, ":agent_team", ":team"),
			(lt, ":base_agent", 0),
			(assign, ":base_agent", ":agent"),
		(try_end),
		# 用base_agent的位置和朝向作为基准（有普通士兵就用他，没有就用玩家）
		(try_begin),
			(ge, ":base_agent", 0),
			(agent_get_position, pos30, ":base_agent"),
		(else_try),
			(agent_get_position, pos30, ":player"),
		(try_end),
		# pos30已经带有agent的朝向，直接使用
		(set_fixed_point_multiplier, 100),
		(assign, ":n_minus_1", ":num_cannons"),
		(val_sub, ":n_minus_1", 1),
		(store_div, ":start_offset", ":n_minus_1", 2),
		(store_mul, ":start_offset", ":start_offset", 300),
		(try_for_range, ":i", 0, ":num_cannons"),
			# 生成火炮
			(spawn_scene_prop, "spr_cannon"),
			(assign, ":cannon", reg0),
			# 生成炮兵（现场生成，套用已有兵种）
			(spawn_agent, "trp_gekokujo_zunwang_veteran_gunner"),
			(assign, ":cannoneer", reg0),
			(agent_set_team, ":cannoneer", ":team"),
			# 计算位置：以基准位置为中心，朝向一致（复制原点和旋转）
			(position_copy_origin, pos31, pos30),
			(position_copy_rotation, pos31, pos30),
			(store_mul, ":x_off", ":i", 300),
			(val_sub, ":x_off", ":start_offset"),
			(position_move_x, pos31, ":x_off"),
			# 火炮在前方+200（朝向敌军方向）
			(position_move_y, pos31, 200),
			(position_set_z_to_ground_level, pos31),
			(prop_instance_set_position, ":cannon", pos31),
			# 炮兵在火炮后方-300（我军一侧）
			(position_move_y, pos31, -300),
			(agent_set_position, ":cannoneer", pos31),
			# 关联炮兵和火炮（覆盖common_init_cannoneer的-1）
			(agent_set_slot, ":cannoneer", slot_agent_cannon, ":cannon"),
			(scene_prop_set_slot, ":cannon", scene_prop_driver, ":cannoneer"),
			(scene_prop_set_slot, ":cannon", scene_prop_assistant, -1),
			(scene_prop_set_slot, ":cannon", scene_prop_assistant_spawned, 0),
			(scene_prop_set_slot, ":cannon", scene_prop_fire_state, 0),
		(try_end),
	])
# llf 新增：主炮手阵亡后释放火炮（不再生成增援）
common_cannon_release_dead=(
	1, 0, 0, [],
	[
		(scene_prop_get_num_instances, ":total", "spr_cannon"),
		(try_for_range, ":j", 0, ":total"),
			(scene_prop_get_instance, ":cannon", "spr_cannon", ":j"),
			(scene_prop_get_slot, ":driver", ":cannon", scene_prop_driver),
			(try_begin),
				# driver 存在且已阵亡：释放火炮（不再生成增援）
				(gt, ":driver", 0),
				(neg|agent_is_alive, ":driver"),
				(scene_prop_set_slot, ":cannon", scene_prop_driver, -1),
				(scene_prop_set_slot, ":cannon", scene_prop_fire_state, 0),
			(try_end),
		(try_end),
	])
#
common_cannoneer_find_cannon=(
	1, 0, 0, [],
	[
		(try_for_agents, ":cannoneer"),
			(agent_is_alive, ":cannoneer"),
			(agent_get_troop_id, ":troop", ":cannoneer"),
			(eq, ":troop", "trp_gekokujo_zunwang_veteran_gunner"),
			(agent_get_slot, ":cannon", ":cannoneer", slot_agent_cannon),
			(lt, ":cannon", 0),
			# 仅玩家方炮兵走认领逻辑
			(agent_get_party_id, ":party", ":cannoneer"),
			(eq, ":party", "p_main_party"),
			# 寻找最近的无主火炮（scene_prop_driver < 0）
			(agent_get_position, pos30, ":cannoneer"),
			(assign, ":nearest", -1),
			(assign, ":nearest_dist", 100000),
			(scene_prop_get_num_instances, ":total", "spr_cannon"),
			(try_for_range, ":j", 0, ":total"),
				(scene_prop_get_instance, ":sp", "spr_cannon", ":j"),
				(scene_prop_get_slot, ":drv", ":sp", scene_prop_driver),
				(lt, ":drv", 0),
				(prop_instance_get_position, pos31, ":sp"),
				(get_distance_between_positions, ":dist", pos30, pos31),
				(lt, ":dist", ":nearest_dist"),
				(assign, ":nearest", ":sp"),
				(assign, ":nearest_dist", ":dist"),
				(position_copy_origin, pos32, pos31),
			(try_end),
			(try_begin),
				(ge, ":nearest", 0),
				(le, ":nearest_dist", 200),
				# 距离≤200：直接认领
				(agent_set_slot, ":cannoneer", slot_agent_cannon, ":nearest"),
				(scene_prop_set_slot, ":nearest", scene_prop_driver, ":cannoneer"),
			(else_try),
				(ge, ":nearest", 0),
				# 距离>200：walk过去
				(agent_set_scripted_destination, ":cannoneer", pos32),
			(else_try),
				# 找不到无主火炮：清除scripted destination，作为步兵参战
				(agent_clear_scripted_mode, ":cannoneer"),
			(try_end),
		(try_end),
	])

common_init_assistant=(
	1,0,0,
	[],
	[
		(get_player_agent_no,":player"),
		(agent_get_team,":player_team",":player"),
		(try_for_agents,":cannoneer"),
			(agent_is_alive,":cannoneer"),
			(agent_get_troop_id, ":troop", ":cannoneer"),
			(eq,":troop","trp_gekokujo_zunwang_veteran_gunner"),
			(agent_get_slot,":cannon",":cannoneer",slot_agent_cannon),
			(ge,":cannon",0),
			(scene_prop_get_slot,":assistant",":cannon",scene_prop_assistant),
			(lt,":assistant",0),
			# 获取主炮手的团队
			(agent_get_team, ":gunner_team", ":cannoneer"),
			# 玩家方副炮手：仅首次生成，死后不再重生
			# 敌方副炮手：死后可以重生
			(try_begin),
				# 玩家方：检查是否首次生成
				(eq, ":gunner_team", ":player_team"),
				(scene_prop_get_slot,":ever_spawned",":cannon",scene_prop_assistant_spawned),
				(eq,":ever_spawned",0),
				(spawn_agent,"trp_assistant_gunner"),
				(agent_set_team,reg0,":gunner_team"),
				(set_fixed_point_multiplier,100),
				(prop_instance_get_position,pos31,":cannon"),
				(position_move_x,pos31,140),
				(agent_set_position,reg0,pos31),
				(agent_set_scripted_destination_no_attack,reg0,pos31,1),
				(agent_set_speed_limit,reg0,8),
				(scene_prop_set_slot,":cannon",scene_prop_assistant_spawned,1),
				(scene_prop_set_slot,":cannon",scene_prop_assistant,reg0),
				(agent_set_slot,reg0,slot_agent_cannon,":cannon"),
			(else_try),
				# 敌方：可以随时重生
				(spawn_agent,"trp_assistant_gunner"),
				(agent_set_team,reg0,":gunner_team"),
				(set_fixed_point_multiplier,100),
				(prop_instance_get_position,pos31,":cannon"),
				(position_move_x,pos31,140),
				(agent_set_position,reg0,pos31),
				(agent_set_scripted_destination_no_attack,reg0,pos31,1),
				(agent_set_speed_limit,reg0,8),
				(scene_prop_set_slot,":cannon",scene_prop_assistant,reg0),
				(agent_set_slot,reg0,slot_agent_cannon,":cannon"),
			(try_end),
		(try_end),
	])
common_move_assistant=(
	0, 0, 0, 
	[],
    [
	  (try_for_agents,":cannoneer"),
		(agent_get_troop_id, ":troop", ":cannoneer"),
		(eq,":troop","trp_gekokujo_zunwang_veteran_gunner"),
		(agent_get_slot,":cannon",":cannoneer",slot_agent_cannon),
		(ge,":cannon",0),
		(scene_prop_get_slot,":assistant",":cannon",scene_prop_assistant),
		(scene_prop_get_slot,":fire_state",":cannon",scene_prop_fire_state),
		(try_begin),
			(agent_is_alive,":cannoneer"),
			(gt,":assistant",0),
			(agent_is_alive,":assistant"),
			(set_fixed_point_multiplier,100),
			(prop_instance_get_position,pos31,":cannon"),
			(position_move_x,pos31,100),
			# 检查副炮手是否已经到达大炮旁（距离特别近时才进入逻辑）
			(agent_get_position, pos32, ":assistant"),
			(get_distance_between_positions, ":dist", pos31, pos32),
			(le, ":dist", 150),
			(try_begin),
				# 开火中（状态1）：不干预副炮手动画，由common_move_cannon处理
				(eq,":fire_state",1),
			(else_try),
				(agent_ai_get_look_target, ":target", ":cannoneer"),
				(agent_is_active,":target"),
				# 有目标：用 scripted destination 走向位置
				(agent_set_scripted_destination_no_attack,":assistant",pos31,1),
				(agent_set_speed_limit,":assistant",8),
			(else_try),
				# 无目标：只设置位置紧贴大炮，不设置拉绳动画
				(agent_set_position,":assistant",pos31),
			(try_end),
		(else_try),
			(agent_is_alive,":cannoneer"),
			(gt,":assistant",0),
			(neg|agent_is_alive,":assistant"),
			(scene_prop_set_slot,":cannon",scene_prop_assistant,-1),
		(try_end),
	  (try_end),
    ])
#
common_move_cannon=(
	0.01, 0, 0, 
	[],
    [
      (try_for_agents,":cannoneer"),
		(agent_is_alive,":cannoneer"),
		(agent_get_troop_id, ":troop", ":cannoneer"),
		(agent_get_slot,":cannon",":cannoneer",slot_agent_cannon),
		(ge,":cannon",0),
		(eq,":troop","trp_gekokujo_zunwang_veteran_gunner"),
		(agent_get_position, pos31,":cannoneer"),
		(set_fixed_point_multiplier,100),
		(scene_prop_get_slot,":assistant",":cannon",scene_prop_assistant),
		(scene_prop_get_slot,":fire_state",":cannon",scene_prop_fire_state),
		# 检查炮手是否已到达火炮操作位置（火炮后方-300）
		(prop_instance_get_position, pos33, ":cannon"),
		(position_move_y, pos33, -300),
		(get_distance_between_positions, ":op_dist", pos31, pos33),
		(try_begin),
			# 炮手还没到位：只走向操作位置，不进入操作逻辑（避免在远处装填/移动大炮）
			# 阈值与操作距离一致（150）
			(gt, ":op_dist", 150),
			(agent_set_scripted_destination, ":cannoneer", pos33),
		(else_try),
			# 炮手已到位：正常操作
		(try_begin),
			# 状态1：开火中，不需要look target
			(eq,":fire_state",1),
			(scene_prop_get_slot,":fire_target",":cannon",scene_prop_fire_target),
			(try_begin),
				(agent_is_alive,":fire_target"),
				(agent_get_position, pos52,":fire_target"),
			(try_end),
			# 停下主炮手（设置目标为当前位置，清除状态0的scripted destination）
			(agent_get_position, pos35,":cannoneer"),
			(agent_set_scripted_destination,":cannoneer",pos35),
			# 等待0.8秒后发射炮弹（捂耳动画已在common_fire_cannon中设置一次）
			(store_mission_timer_a_msec,":cur_time"),
			(scene_prop_get_slot,":fire_timer",":cannon",scene_prop_fire_timer),
			(try_begin),
				(ge,":cur_time",":fire_timer"),
				# 发射炮弹（目标仍存活时）
				(try_begin),
					(agent_is_alive,":fire_target"),
					(prop_instance_get_position,pos45,":cannon"),
					(position_move_y,pos45,450),
					(position_move_z,pos45,100),
					(get_distance_between_positions,":dis",pos45,pos52),
					(le,":dis",12500),
					(set_fixed_point_multiplier, 1),
					(assign,":ammo_speed",10000),
					(convert_to_fixed_point,":ammo_speed"),
					(call_script,"script_point_missile_position",pos45,pos52,":ammo_speed"),
					(add_missile,":cannoneer", pos45,":ammo_speed", "itm_shell", 0, "itm_shell", 0),
					(set_fixed_point_multiplier, 100),
					(particle_system_burst, "psys_gekokujo_shoot_smoke", pos45,100),
					(play_sound_at_position,"snd_gekokujo_shot",pos45,0),
				(try_end),
				# 回到装填状态
				(scene_prop_set_slot,":cannon",scene_prop_fire_state,0),
				# 设置随机冷却时间（2~5秒），使各火炮下次开火时间错开
				(store_mission_timer_a_msec, ":cur_time"),
				(store_random_in_range, ":cooldown", 2000, 5000),
				(val_add, ":cur_time", ":cooldown"),
				(scene_prop_set_slot,":cannon",scene_prop_fire_cooldown,":cur_time"),
			(try_end),
		(else_try),
			# 状态0：装填中，需要目标
			(agent_ai_get_look_target, ":target", ":cannoneer"),
			(agent_is_active,":target"),
			(agent_is_alive,":target"),
			(agent_get_position, pos52,":target"),
			(get_distance_between_positions,":dis",pos31,pos52),
			(le,":dis",20000),
			(prop_instance_get_position,pos35,":cannon"),
			(position_move_y,pos35,-300),
			(agent_set_scripted_destination,":cannoneer",pos35),
			(agent_get_animation,":current_anim",":cannoneer",0),
			(try_begin),
				(neq,":current_anim","anim_reload_cannon"),
				(agent_set_animation,":cannoneer","anim_reload_cannon"),
			(try_end),
			(try_begin),
				(gt,":assistant",0),
				(agent_is_active,":assistant"),
				(agent_is_alive,":assistant"),
				(agent_get_animation,":assist_anim",":assistant",0),
				(neq,":assist_anim","anim_aim_cannon"),
				(neq,":assist_anim","anim_Yuri_CannonEarsPlugging_Right_fire"),
				(agent_set_animation,":assistant","anim_aim_cannon",1),
			(try_end),
		(else_try),
			# 无目标：移动大炮，主炮手walk跟随大炮后方
			(position_move_y, pos31,200),
			(prop_instance_animate_to_position,":cannon",pos31,1),
			(prop_instance_get_position,pos35,":cannon"),
			(position_move_y,pos35,-300),
			(agent_set_scripted_destination,":cannoneer",pos35),
		(try_end),
		(try_end),
	  (try_end),
    ])
common_fire_cannon=(
	8,0,0,[],
	[
		(try_for_agents,":cannoneer"),
			(set_fixed_point_multiplier, 100),
			(agent_is_active,":cannoneer"),
			(agent_is_human,":cannoneer"),
			(agent_get_troop_id,":troop",":cannoneer"),
			(eq,":troop","trp_gekokujo_zunwang_veteran_gunner"),
			(agent_get_slot,":cannon",":cannoneer",slot_agent_cannon),
			(ge,":cannon",0),
			(scene_prop_get_slot,":fire_state",":cannon",scene_prop_fire_state),
			(try_begin),
				(agent_is_alive,":cannoneer"),
				# 距离检查：炮手必须到达操作位置（火炮后方-300）才触发开火
				# 避免增援炮手还在远方走来时火炮自己开火
				(agent_get_position, pos34, ":cannoneer"),
				(prop_instance_get_position, pos33, ":cannon"),
				(position_move_y, pos33, -300),
				(get_distance_between_positions, ":op_dist", pos34, pos33),
				(le, ":op_dist", 150),
				(agent_ai_get_look_target, ":target", ":cannoneer"),
				(ge,":target",0),
				(agent_is_alive,":target"),
				(agent_get_bone_position, pos52, ":target", 9,1),
				(agent_set_look_target_position,":cannoneer",pos52),
				(prop_instance_get_position,pos35,":cannon"),
				(agent_get_look_position, pos36, ":cannoneer"),
				(position_move_y,pos35,200),
				(position_move_y,pos36,200),
				(position_get_rotation_around_z, ":agent_look_around_z", pos36),
				(position_get_rotation_around_z, ":sprop_instance_around_z", pos35),
				(store_sub,":sub_value",":agent_look_around_z",":sprop_instance_around_z"),
				(assign,":sub_value_a",":sub_value"),
				(val_abs,":sub_value_a"),
				(assign,":rotate_z",0),
				(try_begin),
					(this_or_next|ge,":sub_value_a",3),#3
					(le,":sub_value_a",-357),
					(store_div,":rotate_z",":sub_value_a",1),#3
					(val_max,":rotate_z",1),#3
					(try_begin),
						(gt,":sub_value",0),
						(val_mul,":rotate_z",1),
					(else_try),
						(lt,":sub_value",0),
						(val_mul,":rotate_z",-1),
					(try_end),
				(try_end),
				(try_begin),#
					(neq,":rotate_z",0),
					(prop_instance_get_position,pos45,":cannon"),
					(position_rotate_z,pos45,":rotate_z"),
					(position_set_z_to_ground_level,pos45),
					(get_distance_between_positions,":dis",pos45,pos52),
					(is_between,":dis",12500,17500),
					(prop_instance_animate_to_position,":cannon",pos45,100),
				(else_try),#
					# 角度对准，仅在状态0（装填中）且距离合适时触发开火流程
					(eq,":fire_state",0),
					# 冷却检查：火炮发射后需要冷却一段时间（避免所有火炮同步开火）
					(store_mission_timer_a_msec, ":cur_time"),
					(scene_prop_get_slot, ":cooldown", ":cannon", scene_prop_fire_cooldown),
					(gt, ":cur_time", ":cooldown"),
					# 检查发射距离（与状态2中的计算方式一致）
					(prop_instance_get_position,pos45,":cannon"),
					(position_move_y,pos45,450),
					(position_move_z,pos45,100),
					(get_distance_between_positions,":dis",pos45,pos52),
					(le,":dis",12500),
					# 距离合适，触发开火流程
					(prop_instance_get_position,pos45,":cannon"),
					(position_set_z_to_ground_level,pos45),
					(prop_instance_animate_to_position,":cannon",pos45,1),
					# 设置状态为1，记录时间和目标
					(scene_prop_set_slot,":cannon",scene_prop_fire_state,1),
					(scene_prop_set_slot,":cannon",scene_prop_fire_target,":target"),
					# 主炮手捂耳（只设置一次）
					(agent_set_animation,":cannoneer","anim_Yuri_CannonEarsPlugging_Right_fire"),
					# 副炮手同时捂耳
					(scene_prop_get_slot,":assistant",":cannon",scene_prop_assistant),
					(try_begin),
						(gt,":assistant",0),
						(agent_is_active,":assistant"),
						(agent_is_alive,":assistant"),
						(agent_set_animation,":assistant","anim_Yuri_CannonEarsPlugging_Right_fire"),
					(try_end),
					(store_mission_timer_a_msec,":cur_time"),
					# 设置随机发射延迟（800~3000ms），使各火炮发射时间错开，避免同步开火
					(store_random_in_range, ":delay", 800, 3000),
					(val_add, ":cur_time", ":delay"),
					(scene_prop_set_slot,":cannon",scene_prop_fire_timer,":cur_time"),
				(try_end),
			(else_try),
				(neg|agent_is_alive,":cannoneer"),
				# llf 修改：炮兵死亡，火炮标记为无主（不隐藏），等待其他炮兵接管
				(scene_prop_set_slot,":cannon",scene_prop_driver,-1),
				(scene_prop_set_slot,":cannon",scene_prop_fire_state,0),
			(try_end),
		(try_end),
	])
trigger_cannon=[
	common_init_cannoneer,
	common_init_party_cannons_reset,
	common_init_cannon,
	common_spawn_party_cannons,
	common_cannon_release_dead,
	common_cannoneer_find_cannon,
	common_init_assistant,
	common_move_assistant,
	common_move_cannon,
	common_fire_cannon,
] + ym_28


    

#llf's tigger and common end

#gekokujo 3.0 equipment distributions
#the point of this script is to allow skirmisher weapon variation, reduced "loot spam", and guaranteed items
#first and foremost, this script determines whether an ashigaru skirmisher spawns with bows or guns
#the proportions are based on the unit's faction, the exact weapon is based on the unit's tier
#there are 66 skirmisher units split into 4 tiers and 3 ratios
#tier 1 are basic, tier 2 are "trained", tier 3 are "veteran", and tier 4 are "elite"
#(oda and tokugawa) have 60/40 gunners/archers 
#(uesugi, date, mori, takeda, otomo, hojo, shimazu, and ryuzoji) have 40/60 gunners/archers 
#(everyone else) has 20/80 gunners/archers
#NOTE: always pair yumi_1 with yumi_2 and yumi_5 with yumi_6
common_gekokujo_equip = (ti_on_agent_spawn, 0, 0, [],
	[
		(store_trigger_param_1, ":agent_no"),
		(agent_get_troop_id,":troop_no",":agent_no"),
		(store_character_level, ":troop_level", ":troop_no"),
        (agent_get_party_id, ":agent_party", ":agent_no"),
		(store_troop_faction, ":troop_faction", ":troop_no"), #we use these for gunner ratios
        
		#gekokujo 3.1 encounters start
		#there should be no sashimonos worn in the encounters system
		(try_begin),
			(gt, "$gekokujo_encounter_mode", 0),
			(assign, ":faction", -1),
		(else_try),
			(store_faction_of_party, ":faction", ":agent_party"), #we use these for sashimono
			(store_sub, ":offset", ":faction", "fac_kingdom_1"),
		(try_end),
		#gekokujo 3.1 encounters end
		
		#re-equip ashigaru skirmishers start
		(try_begin),
			(is_between, ":troop_no", ashigaru_troops_begin, ashigaru_troops_end), #ashigaru only
			(troop_is_guarantee_ranged, ":troop_no"), #ranged only
			
			#determine ratios based on troop factions rather than actual factions
			(try_begin),
				(eq, ":troop_faction", "fac_kingdom_3"), #oda
				(assign, ":gunner_ratio", 50), #50% gunners
			(else_try),
				(this_or_next|eq, ":troop_faction", "fac_kingdom_1"), #uesugi
				(this_or_next|eq, ":troop_faction", "fac_kingdom_2"), #date
				(this_or_next|eq, ":troop_faction", "fac_kingdom_4"), #mori
				(this_or_next|eq, ":troop_faction", "fac_kingdom_5"), #takeda
				(this_or_next|eq, ":troop_faction", "fac_kingdom_6"), #tokugawa
				(this_or_next|eq, ":troop_faction", "fac_kingdom_9"), #otomo
				(this_or_next|eq, ":troop_faction", "fac_kingdom_11"), #asakura
				(this_or_next|eq, ":troop_faction", "fac_kingdom_15"), #shimazu
				(this_or_next|eq, ":troop_faction", "fac_kingdom_16"), #ryuzoji
				(eq, ":troop_faction", "fac_kingdom_20"), #ikko
				(assign, ":gunner_ratio", 30), #30% gunners
			(else_try),
				#miyoshi	fac_kingdom_7
				#amako		fac_kingdom_8
				#nanbu		fac_kingdom_10
				#chosokabe	fac_kingdom_12
				#hojo		fac_kingdom_13
				#mogami		fac_kingdom_14
				#satake		fac_kingdom_17
				#satomi		fac_kingdom_18
				#ukita		fac_kingdom_19
				(assign, ":gunner_ratio", 15), #15% gunners
			(try_end),
			
			#prep the agents by unequipping their weapons
			#this might not be necessary
			(agent_unequip_item,":agent_no","itm_gekokujo_yumi_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yumi_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yumi_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yumi_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yumi_5"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yumi_6"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arrows_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arrows_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arrows_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arquebus_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arquebus_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arquebus_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_arquebus_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_bullets_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_bullets_2"),
			
			#determine tier from level
			(try_begin),
				(eq, ":troop_level", 9), #basic skirmisher
				(assign, ":skirmisher_tier", 1), 
			(else_try),
				(eq, ":troop_level", 14), #trained skirmisher
				(assign, ":skirmisher_tier", 2),
			(else_try),
				(eq, ":troop_level", 19), #veteran skirmisher
				(assign, ":skirmisher_tier", 3),
			(else_try),
				(assign, ":skirmisher_tier", 4), #elite skirmisher (level 25)
			(try_end),
			
			#roll the dice
			(store_random_in_range, ":gunner_seed", 0, 100),
			
			(try_begin), #on success, turn them into a gunner
				(le, ":gunner_seed", ":gunner_ratio"), 
				(try_begin),
					(eq, ":skirmisher_tier", 1),
					(agent_equip_item,":agent_no","itm_gekokujo_bullets_1"),
					(agent_equip_item,":agent_no","itm_gekokujo_arquebus_1"),
					(agent_set_wielded_item,":agent_no","itm_gekokujo_arquebus_1"), #this is also probably not even necessary
				(else_try),
					(eq, ":skirmisher_tier", 2),
					(agent_equip_item,":agent_no","itm_gekokujo_bullets_1"),
					(agent_equip_item,":agent_no","itm_gekokujo_arquebus_2"),
					(agent_set_wielded_item,":agent_no","itm_gekokujo_arquebus_2"),
				(else_try),
					(eq, ":skirmisher_tier", 3),
					(agent_equip_item,":agent_no","itm_gekokujo_bullets_2"),
					(agent_equip_item,":agent_no","itm_gekokujo_arquebus_3"),
					(agent_set_wielded_item,":agent_no","itm_gekokujo_arquebus_3"),
				(else_try),
					(eq, ":skirmisher_tier", 4),
					(agent_equip_item,":agent_no","itm_gekokujo_bullets_2"),
					(agent_equip_item,":agent_no","itm_gekokujo_arquebus_4"),
					(agent_set_wielded_item,":agent_no","itm_gekokujo_arquebus_4"),
				(try_end),
			(else_try), #on failure, turn them into an archer
				(try_begin),
					(eq, ":skirmisher_tier", 1),
					(agent_equip_item,":agent_no","itm_gekokujo_arrows_1"),
					#randomly select between yumi 1 and 2 at tier 1
					(store_random_in_range, ":yumi_select", 1, 3),
					(try_begin),
						(eq, ":yumi_select", 1),
						(agent_equip_item,":agent_no","itm_gekokujo_yumi_1"),
						(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_1"),
					(else_try),
						(agent_equip_item,":agent_no","itm_gekokujo_yumi_2"),
						(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_2"),
					(try_end),
					#end random select
				(else_try),
					(eq, ":skirmisher_tier", 2),
					(agent_equip_item,":agent_no","itm_gekokujo_arrows_1"),
					(agent_equip_item,":agent_no","itm_gekokujo_yumi_3"),
					(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_3"),
				(else_try),
					(eq, ":skirmisher_tier", 3),
					(agent_equip_item,":agent_no","itm_gekokujo_arrows_2"),
					(agent_equip_item,":agent_no","itm_gekokujo_yumi_4"),
					(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_4"),
				(else_try),
					(eq, ":skirmisher_tier", 4),
					(agent_equip_item,":agent_no","itm_gekokujo_arrows_3"),
					#randomly select between yumi 5 and 6 at tier 4
					(store_random_in_range, ":yumi_select", 1, 3),
					(try_begin),
						(eq, ":yumi_select", 1),
						(agent_equip_item,":agent_no","itm_gekokujo_yumi_5"),
						(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_5"),
					(else_try),
						(agent_equip_item,":agent_no","itm_gekokujo_yumi_6"),
						(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_6"),
					(try_end),
					#end random select
				(try_end),
			(try_end),
		(try_end),
		#re-equip ashigaru skirmishers end
		
		#re-equip ashigaru spearmen start (disabled)
		#these sorry bastards don't know how to select their primary weapons correctly, so no more of this
		#(try_begin),
		#	(is_between, ":troop_no", ashigaru_troops_begin, ashigaru_troops_end), #ashigaru only
		#	(neg|troop_is_guarantee_ranged, ":troop_no"), #melee only
		#	(gt, ":troop_level", 4), #no villagers
		#	
		#	(try_begin), #spearmen
		#		(eq, ":troop_level", 9),
		#		
		#		(agent_unequip_item,":agent_no","itm_gekokujo_tanto_1"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_tanto_2"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_tanto_3"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_yari_bamboo_1"),
		#		
		#		(store_random_in_range, ":secondary_weapon", 0, 3),
		#		(store_add, ":secondary_weapon", "itm_gekokujo_tanto_1", ":secondary_weapon"),
		#		(agent_equip_item,":agent_no",":secondary_weapon"),
		#		(agent_equip_item,":agent_no","itm_gekokujo_yari_bamboo_1"),
		#		(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_bamboo_1"),
		#	(else_try), #trained spearmen
		#		(eq, ":troop_level", 14),
		#		
		#		(agent_unequip_item,":agent_no","itm_gekokujo_wakizashi_1"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_wakizashi_2"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_wakizashi_3"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_4"),
		#	
		#		(store_random_in_range, ":secondary_weapon", 0, 3),
		#		(store_add, ":secondary_weapon", "itm_gekokujo_wakizashi_1", ":secondary_weapon"),
		#		(store_random_in_range, ":primary_weapon", 0, 2),
		#		(store_add, ":primary_weapon", "itm_gekokujo_fukuro_yari_3", ":primary_weapon"),
		#		(agent_equip_item,":agent_no",":secondary_weapon"),
		#		(agent_equip_item,":agent_no",":primary_weapon"),
		#		(agent_set_wielded_item,":agent_no",":primary_weapon"),
		#	(else_try), #veteran spearmen
		#		(eq, ":troop_level", 19),
		#		
		#		(agent_unequip_item,":agent_no","itm_gekokujo_katana_1"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_katana_2"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_katana_3"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_1"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_2"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_yari_1"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_yari_3"),
		#		
		#		(store_random_in_range, ":secondary_weapon", 0, 3),
		#		(store_add, ":secondary_weapon", "itm_gekokujo_katana_1", ":secondary_weapon"),
		#		(agent_equip_item,":agent_no",":secondary_weapon"),
		#		
		#		(store_random_in_range, ":primary_weapon", 0, 4),
		#		(try_begin),
		#			(eq, ":primary_weapon", 0),
		#			(agent_equip_item,":agent_no","itm_gekokujo_fukuro_yari_1"),
		#			(agent_set_wielded_item,":agent_no","itm_gekokujo_fukuro_yari_1"),
		#		(else_try),
		#			(eq, ":primary_weapon", 1),
		#			(agent_equip_item,":agent_no","itm_gekokujo_fukuro_yari_2"),
		#			(agent_set_wielded_item,":agent_no","itm_gekokujo_fukuro_yari_2"),
		#		(else_try),
		#			(eq, ":primary_weapon", 2),
		#			(agent_equip_item,":agent_no","itm_gekokujo_yari_1"),
		#			(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_1"),
		#		(else_try),
		#			(agent_equip_item,":agent_no","itm_gekokujo_yari_3"),
		#			(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_3"),
		#		(try_end),
		#	(else_try), #elite spearmen
		#		(agent_unequip_item,":agent_no","itm_gekokujo_katana_1"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_katana_2"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_katana_3"),
		#		(agent_unequip_item,":agent_no","itm_gekokujo_yari_2"),
		#	
		#		(store_random_in_range, ":secondary_weapon", 0, 3),
		#		(store_add, ":secondary_weapon", "itm_gekokujo_katana_1", ":secondary_weapon"),
		#		(agent_equip_item,":agent_no",":secondary_weapon"),
		#		(agent_equip_item,":agent_no","itm_gekokujo_yari_2"),
		#		(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_2"),
		#	(try_end),
		#(try_end),
		#re-equip ashigaru spearmen end
		
		#equip sashimono start
		(assign, ":sashimono", 0),
		
		(try_begin), #samurai
			(neq, ":faction", -1), #gekokujo 3.1 encounters - required so script doesn't shit bed
			(is_between, ":troop_no", samurai_troops_begin, samurai_troops_end),
			(try_begin), 
				(is_between, ":troop_level", 6, 17), #samurai retainers
				(try_begin),
					(this_or_next|eq, ":agent_party", "p_main_party"),
					(eq, ":faction", "fac_player_supporters_faction"),
					(assign, ":sashimono", "itm_gekokujo_sashimono_2"),
				(else_try),
					(store_add, ":sashimono", "itm_gekokujo_sashimono_uesugi_2", ":offset"),
				(try_end),
			(else_try), 
				(eq, ":troop_level", 21), #samurai officers
				(neg|troop_is_guarantee_ranged, ":troop_no"), #no master archers or gunners
				(try_begin),
					(this_or_next|eq, ":faction", "fac_kingdom_3"), #oda
					(this_or_next|eq, ":faction", "fac_kingdom_4"), #mori
					(this_or_next|eq, ":faction", "fac_kingdom_5"), #takeda
					(this_or_next|eq, ":faction", "fac_kingdom_10"), #nanbu
					(this_or_next|eq, ":faction", "fac_kingdom_12"), #chosokabe
					(this_or_next|eq, ":faction", "fac_kingdom_15"), #shimazu
					(eq, ":faction", "fac_kingdom_18"), #satomi
					(assign,":sashimono","itm_gekokujo_sashimono_3"),
				(else_try),
					(this_or_next|eq, ":faction", "fac_kingdom_1"), #uesugi
					(this_or_next|eq, ":faction", "fac_kingdom_6"), #tokugawa
					(this_or_next|eq, ":faction", "fac_kingdom_7"), #miyoshi
					(this_or_next|eq, ":faction", "fac_kingdom_8"), #amako
					(this_or_next|eq, ":faction", "fac_kingdom_9"), #otomo
					(this_or_next|eq, ":faction", "fac_kingdom_17"), #satake
					(eq, ":faction", "fac_kingdom_20"), #ikko
					(assign,":sashimono","itm_gekokujo_sashimono_4"),
				(else_try),
					#date, asakura, hojo, mogami, ryuzoji, ukita, and player kingdom
					(assign,":sashimono","itm_gekokujo_sashimono_5"),
				(try_end),
			(try_end),
		(else_try), #ashigaru
			(neq, ":faction", -1), #gekokujo 3.1 encounters - required so script doesn't shit bed
			(is_between, ":troop_no", ashigaru_troops_begin, ashigaru_troops_end),
			(try_begin), 
				(eq, ":troop_level", 14), #trained ashigaru
				(neg|troop_is_guarantee_ranged, ":troop_no"), #only spearmen
				(try_begin),
					(this_or_next|eq, ":agent_party", "p_main_party"),
					(eq, ":faction", "fac_player_supporters_faction"),
					(assign, ":sashimono", "itm_gekokujo_sashimono_1"),
				(else_try),
					(store_add, ":sashimono", "itm_gekokujo_sashimono_uesugi_1", ":offset"),
				(try_end),
			(else_try),
				(ge, ":troop_level", 19), #all veteran ashigaru and above
				(try_begin),
					(this_or_next|eq, ":agent_party", "p_main_party"),
					(eq, ":faction", "fac_player_supporters_faction"),
					(assign, ":sashimono", "itm_gekokujo_sashimono_1"),
				(else_try),
					(store_add, ":sashimono", "itm_gekokujo_sashimono_uesugi_1", ":offset"),
				(try_end),
			(try_end),
		(try_end),
		
        #gekokujo 3.1 sashimono texture fix start
        (call_script, "script_troop_agent_set_banner", "tableau_game_troop_label_banner", ":agent_no", ":troop_no"),
        #gekokujo 3.1 sashimono texture fix end
        
		(try_begin),
			(gt, ":sashimono", 0),
			(agent_equip_item,":agent_no",":sashimono", 4),
		(try_end),
		#equip sashimono end
		
		#re-equip date officers start
		(try_begin),
			(eq, ":troop_faction", "fac_kingdom_2"), #date only
			(is_between, ":troop_no", samurai_troops_begin, samurai_troops_end), #samurai only
			(eq, ":troop_level", 21), #officers and master archers/gunners only
			
			#remove all armor items first
			(agent_unequip_item,":agent_no","itm_gekokujo_zunari_h_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yukinoshita_long_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_4_1"),
			
			#roll the dice
			(store_random_in_range, ":armor_seed", 1, 8),
			
			#check the results and assign the new equipment
			(try_begin),
				#result of 7 = red
				(eq, ":armor_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_zunari_h_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_yukinoshita_long_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_4_3"),
			(else_try),
				#result of 5 or 6 = russet
				(this_or_next|eq, ":armor_seed", 5), 
				(eq, ":armor_seed", 6),
				(agent_equip_item,":agent_no","itm_gekokujo_zunari_h_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_yukinoshita_long_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_4_2"),
			(else_try),
				#everything else = black (we just stripped the troop in order to put everything back!)
				(agent_equip_item,":agent_no","itm_gekokujo_zunari_h_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_yukinoshita_long_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_4_1"),
			(try_end),
		(try_end),
		#re-equip date officers end
		
		#random clothes start
		#clothes randomly changed on the fly instead of at the troop level to reduce "loot spam"
		#these troops have a default lootable set of clothes
		#but all of a given set are available to randomly spawn on them
		(assign, ":mens_clothes",0),
		(assign, ":womens_clothes",0),
		(assign, ":hakamas",0),
		
		(try_begin),
			(is_between, ":troop_no", ashigaru_troops_begin, ashigaru_troops_end),
			(eq, ":troop_level", 4), #villagers
			(assign, ":mens_clothes", 1),
		(else_try),
			(this_or_next|eq, ":troop_no", "trp_farmer"), 
			(this_or_next|eq, ":troop_no", "trp_townsman"), 
			(this_or_next|eq, ":troop_no", "trp_looter"), 
			(this_or_next|eq, ":troop_no", "trp_caravan_master"), 
			(this_or_next|eq, ":troop_no", "trp_hired_guard"), 
			(eq, ":troop_no", "trp_bandit"),
			(assign, ":mens_clothes", 1),
		(else_try),
			#same setup as mens_clothes
			(this_or_next|eq, ":troop_no", "trp_peasant_woman"), 
			(eq, ":troop_no", "trp_refugee"),
			(assign, ":womens_clothes", 1),
		(else_try),
			#same setup as mens_clothes
			(this_or_next|eq, ":troop_no", "trp_gekokujo_zunwang_veteran_gunner"), 
			(this_or_next|eq, ":troop_no", "trp_yojimbo"), 
			(this_or_next|eq, ":troop_no", "trp_onnabushi"), 
			(this_or_next|eq, ":troop_no", "trp_ronin"), 
			(this_or_next|eq, ":troop_no", "trp_ronin_wanderer"),
			(eq, ":troop_no", "trp_fort_troop_1_1"), #sado exiles (microfactions)
			(assign, ":hakamas", 1),
		(try_end),		
		
		(try_begin),
			(eq, ":mens_clothes", 1),
			
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_1_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_1_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_1_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_2_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_2_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_2_3"),
			
			#roll the dice
			(store_random_in_range, ":clothes_seed", 1, 7),
			
			#check the results and assign the new equipment
			(try_begin),
				(eq, ":clothes_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_1"),
			(else_try),
				(eq, ":clothes_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_2"),
			(else_try),
				(eq, ":clothes_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_3"),
			(else_try),
				(eq, ":clothes_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_1"),
			(else_try),
				(eq, ":clothes_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_2"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_3"),
			(try_end),
			
		(try_end),
		#END: men's clothes

		#START: women's clothes
		(try_begin),
			(eq, ":womens_clothes", 1),
			
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_3_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_3_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_3_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_3_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_3_5"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_3_6"),
			
			#roll the dice
			(store_random_in_range, ":clothes_seed", 1, 7),
			
			#check the results and assign the new equipment
			(try_begin),
				(eq, ":clothes_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_3_1"),
			(else_try),
				(eq, ":clothes_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_3_2"),
			(else_try),
				(eq, ":clothes_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_3_3"),
			(else_try),
				(eq, ":clothes_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_3_4"),
			(else_try),
				(eq, ":clothes_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_3_5"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_3_6"),
			(try_end),
			
		(try_end),
		#END: women's clothes

		#START: hakamas
		(try_begin),
			(eq, ":hakamas", 1),
			
			(agent_unequip_item,":agent_no","itm_gekokujo_hakama_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_hakama_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_hakama_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_hakama_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_hakama_5"),
			(agent_unequip_item,":agent_no","itm_gekokujo_hakama_6"),
			(agent_unequip_item,":agent_no","itm_gekokujo_haori_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_haori_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_haori_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_haori_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_haori_5"),
			(agent_unequip_item,":agent_no","itm_gekokujo_haori_6"),
			
			#roll the dice
			(store_random_in_range, ":clothes_seed", 1, 13),
			
			#check the results and assign the new equipment
			(try_begin),
				(eq, ":clothes_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_hakama_1"),
			(else_try),
				(eq, ":clothes_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_hakama_2"),
			(else_try),
				(eq, ":clothes_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_hakama_3"),
			(else_try),
				(eq, ":clothes_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_hakama_4"),
			(else_try),
				(eq, ":clothes_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_hakama_5"),
			(else_try),
				(eq, ":clothes_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_hakama_6"),
			(else_try),
				(eq, ":clothes_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_haori_1"),
			(else_try),
				(eq, ":clothes_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_haori_2"),
			(else_try),
				(eq, ":clothes_seed", 9), 
				(agent_equip_item,":agent_no","itm_gekokujo_haori_3"),
			(else_try),
				(eq, ":clothes_seed", 10), 
				(agent_equip_item,":agent_no","itm_gekokujo_haori_4"),
			(else_try),
				(eq, ":clothes_seed", 11), 
				(agent_equip_item,":agent_no","itm_gekokujo_haori_5"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_haori_6"),
			(try_end),
		(try_end),
		#random clothes end
		
		#START: hired_warrior, ikko_arquebus_monk, ikko_yumi_monk, ikko_yari_monk
		#spawn with black versions of all half armors and tatami short armors
		(try_begin),
			(this_or_next|eq, ":troop_no", "trp_hired_warrior"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_arquebus_monk"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_yumi_monk"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_yari_monk"),
			(this_or_next|eq, ":troop_no", "trp_fort_troop_2_1"), #tsushima gunner (microfactions)
			(this_or_next|eq, ":troop_no", "trp_fort_troop_3_1"), #shingi monk gunner (microfactions)
			(eq, ":troop_no", "trp_fort_troop_4_1"), #jimon monk warrior (microfactions)
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_half_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_half_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_half_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_half_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_short_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_short_4"),
			(store_random_in_range, ":armor_seed", 1, 7),#roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":armor_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_half_1"),
			(else_try),
				(eq, ":armor_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_1"),
			(else_try),
				(eq, ":armor_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_4"),
			(else_try),
				(eq, ":armor_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_1"),
			(else_try),
				(eq, ":armor_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_1"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_4"),
			(try_end),
		(try_end),
		#END: hired_warrior, ikko_arquebus_monk, ikko_yumi_monk, ikko_yari_monk
		
		#START: onnabushi_trained
		#spawn with red versions of all half armors and tatami short armors
		(try_begin),
			(eq, ":troop_no", "trp_onnabushi_trained"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_half_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_short_6"),
			(store_random_in_range, ":armor_seed", 1, 7), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":armor_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_half_3"),
			(else_try),
				(eq, ":armor_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_3"),
			(else_try),
				(eq, ":armor_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_6"),
			(else_try),
				(eq, ":armor_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_3"),
			(else_try),
				(eq, ":armor_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_3"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_6"),
			(try_end),
		(try_end),
		#END: onnabushi_trained
		
		#START: ronin_adventurer
		#spawn with russet versions of all half armors and tatami short armors
		(try_begin),
			(eq, ":troop_no", "trp_ronin_adventurer"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_half_5"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_half_2"),
			(store_random_in_range, ":armor_seed", 1, 7), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":armor_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_half_2"),
			(else_try),
				(eq, ":armor_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_2"),
			(else_try),
				(eq, ":armor_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_5"),
			(else_try),
				(eq, ":armor_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_2"),
			(else_try),
				(eq, ":armor_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_2"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_5"),
			(try_end),
		(try_end),
		#END: ronin_adventurer
		
		#START: hired_warrior_veteran, veteran_arquebus_monk, veteran_yumi_monk, ikko_veteran_yari_monk, ikko_naginata_monk
		#spawn with black versions of all short armors
		(try_begin),
			(this_or_next|eq, ":troop_no", "trp_hired_warrior_veteran"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_veteran_arquebus_monk"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_veteran_yumi_monk"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_veteran_yari_monk"),
			(this_or_next|eq, ":troop_no", "trp_gekokujo_ikko_naginata_monk"),
			(this_or_next|eq, ":troop_no", "trp_fort_troop_2_2"), #veteran tsushima gunner (microfactions)
			(this_or_next|eq, ":troop_no", "trp_fort_troop_3_2"), #veteran shingi monk gunner (microfactions)
			(eq, ":troop_no", "trp_fort_troop_4_2"), #veteran jimon monk warrior (microfactions)
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_short_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_short_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_7"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_10"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_4"),
			(store_random_in_range, ":armor_seed", 1, 10), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":armor_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_1"),
			(else_try),
				(eq, ":armor_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_4"),
			(else_try),
				(eq, ":armor_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_1"),
			(else_try),
				(eq, ":armor_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_4"),
			(else_try),
				(eq, ":armor_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_7"),
			(else_try),
				(eq, ":armor_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_10"),
			(else_try),
				(eq, ":armor_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_1"),
			(else_try),
				(eq, ":armor_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_4"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_yukinoshita_short_1"),
			(try_end),
		(try_end),
		#END: hired_warrior_veteran, veteran_arquebus_monk, veteran_yumi_monk, ikko_veteran_yari_monk, ikko_naginata_monk
		
		#START: onnabushi_veteran
		#spawn with red versions of all short armors
		(try_begin),
			(eq, ":troop_no", "trp_onnabushi_veteran"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_6"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yukinoshita_short_3"),
			(store_random_in_range, ":armor_seed", 1, 10), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":armor_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_3"),
			(else_try),
				(eq, ":armor_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_6"),
			(else_try),
				(eq, ":armor_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_3"),
			(else_try),
				(eq, ":armor_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_6"),
			(else_try),
				(eq, ":armor_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_9"),
			(else_try),
				(eq, ":armor_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_12"),
			(else_try),
				(eq, ":armor_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_3"),
			(else_try),
				(eq, ":armor_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_6"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_yukinoshita_short_3"),
			(try_end),
		(try_end),
		#END: onnabushi_veteran
		
		#START: ronin_protector
		#spawn with russet versions of all short armors
		(try_begin),
			(eq, ":troop_no", "trp_ronin_protector"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_5"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_2"),
			(store_random_in_range, ":armor_seed", 1, 10), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":armor_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_2"),
			(else_try),
				(eq, ":armor_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_5"),
			(else_try),
				(eq, ":armor_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_2"),
			(else_try),
				(eq, ":armor_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_5"),
			(else_try),
				(eq, ":armor_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_8"),
			(else_try),
				(eq, ":armor_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_11"),
			(else_try),
				(eq, ":armor_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_2"),
			(else_try),
				(eq, ":armor_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_5"),
			(else_try),
				#(eq, ":armor_seed", 9), 
				(agent_equip_item,":agent_no","itm_gekokujo_yukinoshita_short_2"),
			(try_end),
		(try_end),
		#END: ronin_protector

		#START: brigand
		#spawn with all kimono and red versions of half armors
		(try_begin),
			(eq, ":troop_no", "trp_brigand"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_1_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_3"),
			(store_random_in_range, ":clothes_seed", 1, 12), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":clothes_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_1"),
			(else_try),
				(eq, ":clothes_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_2"),
			(else_try),
				(eq, ":clothes_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_3"),
			(else_try),
				(eq, ":clothes_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_1"),
			(else_try),
				(eq, ":clothes_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_2"),
			(else_try),
				(eq, ":clothes_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_3"),
			(else_try),
				(eq, ":clothes_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_half_3"),
			(else_try),
				(eq, ":clothes_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_3"),
			(else_try),
				(eq, ":clothes_seed", 9), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_6"),
			(else_try),
				(eq, ":clothes_seed", 10), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_3"),
			(else_try),
				(eq, ":clothes_seed", 11), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_3"),
			(else_try),
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_6"),
			(try_end),
		(try_end),
		#END: brigand

		#START: seto_pirate
		#spawn with all kimono and russet versions of half armors
		(try_begin),
			(eq, ":troop_no", "trp_seto_pirate"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_2_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_2"),
			(store_random_in_range, ":clothes_seed", 1, 13), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":clothes_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_1"),
			(else_try),
				(eq, ":clothes_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_2"),
			(else_try),
				(eq, ":clothes_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_3"),
			(else_try),
				(eq, ":clothes_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_1"),
			(else_try),
				(eq, ":clothes_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_2"),
			(else_try),
				(eq, ":clothes_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_3"),
			(else_try),
				(eq, ":clothes_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_half_2"),
			(else_try),
				(eq, ":clothes_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_2"),
			(else_try),
				(eq, ":clothes_seed", 9), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_5"),
			(else_try),
				(eq, ":clothes_seed", 10), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_2"),
			(else_try),
				(eq, ":clothes_seed", 11), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_2"),
			(else_try),
				#(eq, ":clothes_seed", 12), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_5"),
			(try_end),
		(try_end),
		#END: seto_pirate

		#START: woku_pirate
		#spawn with all kimono and black versions of half armors
		(try_begin),
			(eq, ":troop_no", "trp_woku_pirate"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kimono_1_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tatami_short_4"),
			(store_random_in_range, ":clothes_seed", 1, 13), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(eq, ":clothes_seed", 1), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_1"),
			(else_try),
				(eq, ":clothes_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_2"),
			(else_try),
				(eq, ":clothes_seed", 3), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_1_3"),
			(else_try),
				(eq, ":clothes_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_1"),
			(else_try),
				(eq, ":clothes_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_2"),
			(else_try),
				(eq, ":clothes_seed", 6), 
				(agent_equip_item,":agent_no","itm_gekokujo_kimono_2_3"),
			(else_try),
				(eq, ":clothes_seed", 7), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_half_1"),
			(else_try),
				(eq, ":clothes_seed", 8), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_1"),
			(else_try),
				(eq, ":clothes_seed", 9), 
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_half_4"),
			(else_try),
				(eq, ":clothes_seed", 10), 
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_1"),
			(else_try),
				(eq, ":clothes_seed", 11), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_1"),
			(else_try),
				#(eq, ":clothes_seed", 12), 
				(agent_equip_item,":agent_no","itm_gekokujo_tatami_short_4"),
			(try_end),
		(try_end),
		#END: woku_pirate

		#START: kanto_rebel
		#spawn 2/6 spearman, 2/6 samurai, 1/6 skirmisher, 1/6 samurai archer
		(try_begin),
			(eq, ":troop_no", "trp_kanto_rebel"),
			(agent_unequip_item,":agent_no","itm_gekokujo_wakizashi_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_katana_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yari_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_jingasa_9"),
			(agent_unequip_item,":agent_no","itm_gekokujo_suji_o_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_6"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_12"),
			(agent_unequip_item,":agent_no","itm_gekokujo_light_suneate_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_shino_suneate_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_3_3"),
			(store_random_in_range, ":troop_seed", 1, 7), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(this_or_next|eq, ":troop_seed", 1), #spearman
				(eq, ":troop_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_wakizashi_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_jingasa_9"),
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_12"),
				(agent_equip_item,":agent_no","itm_gekokujo_light_suneate_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_1"),
			(else_try),
				(this_or_next|eq, ":troop_seed", 3), #samurai
				(eq, ":troop_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_katana_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_yari_1"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_suji_o_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_6"),
				(agent_equip_item,":agent_no","itm_gekokujo_shino_suneate_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_3_3"),
			(else_try),
				(eq, ":troop_seed", 5), #skirmisher
				(agent_equip_item,":agent_no","itm_gekokujo_tanto_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_arrows_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_yumi_3"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_light_suneate_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_1"),
			(else_try),
				#(eq, ":troop_seed", 6), #samurai archer
				(agent_equip_item,":agent_no","itm_gekokujo_katana_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_arrows_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_yumi_5"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_5"),
				(agent_equip_item,":agent_no","itm_gekokujo_suji_o_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_6"),
				(agent_equip_item,":agent_no","itm_gekokujo_shino_suneate_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_3_3"),
			(try_end),
		(try_end),
		#END: kanto_rebel

		#START: shinano_rebel
		#spawn 2/6 spearman, 3/6 skirmisher, 1/6 samurai
		(try_begin),
			(eq, ":troop_no", "trp_shinano_rebel"),
			(agent_unequip_item,":agent_no","itm_gekokujo_wakizashi_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_katana_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yari_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_jingasa_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_zunari_o_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_11"),
			(agent_unequip_item,":agent_no","itm_gekokujo_light_suneate_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_shino_suneate_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_3_2"),
			(store_random_in_range, ":troop_seed", 1, 7), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(this_or_next|eq, ":troop_seed", 1), #spearman
				(eq, ":troop_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_wakizashi_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_fukuro_yari_4"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_fukuro_yari_4"),
				(agent_equip_item,":agent_no","itm_gekokujo_jingasa_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_11"),
				(agent_equip_item,":agent_no","itm_gekokujo_light_suneate_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_1"),
			(else_try),
				(this_or_next|eq, ":troop_seed", 3), #skirmisher
				(this_or_next|eq, ":troop_seed", 4), 
				(eq, ":troop_seed", 5), 
				(agent_equip_item,":agent_no","itm_gekokujo_tanto_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_arrows_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_yumi_3"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_light_suneate_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_1"),
			(else_try),
				#(eq, ":troop_seed", 6), #samurai
				(agent_equip_item,":agent_no","itm_gekokujo_katana_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_yari_3"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_zunari_o_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_shino_suneate_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_3_2"),
			(try_end),
		(try_end),
		#END: shinano_rebel

		#START: kinai_rebel
		#spawn 2/6 spearman, 2/6 samurai, 1/6 skirmisher, 1/6 berserker
		(try_begin),
			(eq, ":troop_no", "trp_kinai_rebel"),
			(agent_unequip_item,":agent_no","itm_gekokujo_wakizashi_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_katana_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
			(agent_unequip_item,":agent_no","itm_gekokujo_yari_2"),
			(agent_unequip_item,":agent_no","itm_gekokujo_jingasa_4"),
			(agent_unequip_item,":agent_no","itm_gekokujo_kabuto3_o_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_mogami_short_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_okegawa_short_7"),
			(agent_unequip_item,":agent_no","itm_gekokujo_light_suneate_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_shino_suneate_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_1"),
			(agent_unequip_item,":agent_no","itm_gekokujo_tekko_3_1"),
			(store_random_in_range, ":troop_seed", 1, 7), #roll the dice
			(try_begin), #check the results and assign the new equipment
				(this_or_next|eq, ":troop_seed", 1), #spearman
				(eq, ":troop_seed", 2), 
				(agent_equip_item,":agent_no","itm_gekokujo_wakizashi_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_fukuro_yari_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_jingasa_4"),
				(agent_equip_item,":agent_no","itm_gekokujo_okegawa_short_7"),
				(agent_equip_item,":agent_no","itm_gekokujo_light_suneate_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_1"),
			(else_try),
				(this_or_next|eq, ":troop_seed", 3), #samurai
				(eq, ":troop_seed", 4), 
				(agent_equip_item,":agent_no","itm_gekokujo_katana_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_yari_2"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yari_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_kabuto3_o_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_shino_suneate_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_3_1"),
			(else_try),
				(eq, ":troop_seed", 5), #skirmisher
				(agent_equip_item,":agent_no","itm_gekokujo_tanto_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_arrows_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_yumi_3"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_yumi_3"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_half_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_light_suneate_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_1"),
			(else_try),
				#(eq, ":troop_seed", 6), #berserker
				(agent_equip_item,":agent_no","itm_gekokujo_katana_4"),
				(agent_equip_item,":agent_no","itm_gekokujo_konsaibo_2"),
				(agent_set_wielded_item,":agent_no","itm_gekokujo_konsaibo_2"),
				(agent_equip_item,":agent_no","itm_gekokujo_kabuto3_o_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_mogami_short_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_shino_suneate_1"),
				(agent_equip_item,":agent_no","itm_gekokujo_tekko_3_1"),
			(try_end),
		(try_end),
		#END: kinai_rebel

	])
	
#gekokujo 3.1 sabakato switch start
common_gekokujo_sabakato_switch_check = (
  0, 0, 0, 
  [
    (neg|main_hero_fallen),
    (game_key_clicked, gk_toggle_weapon_mode),
    #(key_clicked, key_x)
    (get_player_agent_no, ":player"),
    (agent_get_wielded_item, ":cur_item", ":player", 0),
    (this_or_next|eq, ":cur_item", "itm_gekokujo_sabakato_blunt"),
    (eq, ":cur_item", "itm_gekokujo_sabakato_sharp"),
  ],
  [    
    (get_player_agent_no, ":player"),
    
    (agent_get_wielded_item, ":cur_item", ":player", 0),
    (try_begin),
      (eq, ":cur_item", "itm_gekokujo_sabakato_blunt"),
      (assign, ":new_item", "itm_gekokujo_sabakato_sharp"),
    (else_try),
      (assign, ":new_item", "itm_gekokujo_sabakato_blunt"),
    (try_end),
    
    (agent_unequip_item, ":player", "itm_gekokujo_sabakato_blunt"),
    (agent_unequip_item, ":player", "itm_gekokujo_sabakato_sharp"),
    (agent_equip_item, ":player", ":new_item"),
    (agent_set_wielded_item, ":player", ":new_item"),
  ])
#gekokujo 3.1 sabakato switch end

#gekokujo 2.1 PBO
## Prebattle Orders Begin
prebattle_orders_triggers = [
 (0, 0, ti_once, [(party_slot_ge, "p_main_party", slot_party_prebattle_num_orders, 1)], [
        (get_player_agent_no, ":player_agent"),
        (agent_get_team, ":player_team", ":player_agent"),
		(party_get_slot, ":num_of_orders", "p_main_party", slot_party_prebattle_num_orders),
		(set_show_messages, 0),	 
		(assign, ":delay_count", 0),		
        (try_for_range, ":i", 0, ":num_of_orders"),    
		    (store_add, ":ith_order_slot", ":i", slot_party_prebattle_order_array_begin),
            (party_get_slot, ":order_index", "p_main_party", ":ith_order_slot"),
			(ge, ":order_index", 10), 
			
			#Take 3 digit order index and get component parts: group, type, order
			(store_div, ":ith_order_group", ":order_index", 100),
			(store_mul, ":ith_order_type", ":ith_order_group", 100),
			(val_sub, ":order_index", ":ith_order_type"),
			(store_div, ":ith_order_type", ":order_index", 10),
			(store_mul, ":ith_order", ":ith_order_type", 10),
			(store_sub, ":ith_order", ":order_index", ":ith_order"),

			#Turn type and order into Native order
			(assign, ":delay_order", 0),
			(assign, ":num_repeats", 0),
			(try_begin),
			    (eq, ":ith_order_type", 1), #Start Position: hold, follow, charge; mordr_ 0-2; 3=11 stand ground
				(eq, ":ith_order", 3), 
				(assign, ":ith_order", 11), #Stand Ground
			(else_try),
			    (eq, ":ith_order_type", 2), #Other movement orders: mordr_ 3-8, 
				(try_begin),
				    (is_between, ":ith_order", 5, 7), #5 or 6; Forward/Back 10 Paces
				    (assign, ":delay_order", 1), #To fix bugs with these orders, they are delayed 3 seconds
				    (val_add, ":delay_count", 1),
				(else_try),
				    (store_add, ":ith_repeat_slot", ":ith_order_slot", 60), #30 for partial version
				    (party_get_slot, ":num_repeats", "p_main_party", ":ith_repeat_slot"),
				(try_end),
			(else_try),
			    (eq, ":ith_order_type", 3), #Native Weapon Use orders: mordr_ 9,10,12,13
				(try_begin),
				    (eq, ":ith_order", 0),
					(assign, ":ith_order", 10), #Use Any Weapon
				(else_try),
				    (eq, ":ith_order", 2),
					(assign, ":ith_order", 12), #Hold Fire
				(else_try),
				    (eq, ":ith_order", 3),
					(assign, ":ith_order", 13), #Fire at Will
				(try_end),
			(else_try),
			    (is_between, ":ith_order_type", 5, 7), #5 or 6; Caba Weapon and Shield orders
				(val_add, ":delay_count", 1), #To fix bugs with these orders, they are delayed 3 seconds
			(else_try),
			    (eq, ":ith_order_type", 7), #Caba Skirmish
				(eq, ":ith_order", 1), #Begin Skirmish, any other value would be an error
				(team_set_order_listener, ":player_team", ":ith_order_group"),
				(call_script, "script_order_skirmish_begin_end", skirmish),
				(team_set_order_listener, ":player_team", -1),
			(try_end),
            (try_begin),
			    (is_between, ":ith_order_type", 1, 4),
				(neq, ":delay_order", 1),
				(val_max, ":num_repeats", 1),
				(try_for_range, ":unused", 0, ":num_repeats"),
				    (team_give_order, ":player_team", ":ith_order_group", ":ith_order"),
				(try_end),
			(try_end),			
		(try_end), #End Order Slot Loop	
        (team_set_order_listener, ":player_team", grc_everyone), #Reset	
        (set_show_messages, 1),
		(display_message, "@Everyone, you know what to do. To your positions!", 0xFFDDDD66),
		(try_begin),
		    (eq, ":num_of_orders", 1),
			(party_get_slot, ":first_order", "p_main_party_backup", slot_party_prebattle_order_array_begin),
			(party_set_slot, "p_main_party", slot_party_prebattle_order_array_begin, ":first_order"),
			(party_set_slot, "p_main_party_backup", slot_party_prebattle_order_array_begin, 0),
		(try_end),	
        (try_begin),
            (eq, ":delay_count", 0),
            (party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 0),
		(try_end),
	]),
	
 (3, 0, ti_once, [(party_slot_ge, "p_main_party", slot_party_prebattle_num_orders, 1)], [
        #To fix bugs with Move Forward/Back 10 Paces and Caba Weapon orders
		#these orders are applied separately, after other orders
        (get_player_agent_no, ":player_agent"),
        (agent_get_team, ":player_team", ":player_agent"),
		(party_get_slot, ":num_of_orders", "p_main_party", slot_party_prebattle_num_orders),
		(set_show_messages, 0),	 
        (try_for_range, ":i", 0, ":num_of_orders"),    
		    (store_add, ":ith_order_slot", ":i", slot_party_prebattle_order_array_begin),
            (party_get_slot, ":order_index", "p_main_party", ":ith_order_slot"),
			(ge, ":order_index", 10), 
			
			#Take 3 digit order index and get component parts: group, type, order
			(store_div, ":ith_order_group", ":order_index", 100),
			(store_mul, ":ith_order_type", ":ith_order_group", 100),
			(val_sub, ":order_index", ":ith_order_type"),
			(store_div, ":ith_order_type", ":order_index", 10),
			(this_or_next|is_between, ":ith_order_type", 5, 7), #5 or 6; Caba Weapon and Shield orders
			(eq, ":ith_order_type", 2), #Movement Orders
			(store_mul, ":ith_order", ":ith_order_type", 10),
			(store_sub, ":ith_order", ":order_index", ":ith_order"),
			
			(try_begin),
                (eq, ":ith_order_type", 2),			
                (is_between, ":ith_order", 5, 7), #5 or 6; Only Forward/Back 10 Paces			
			    (store_add, ":ith_repeat_slot", ":ith_order_slot", 60), #30 for partial version
			    (party_get_slot, ":num_repeats", "p_main_party", ":ith_repeat_slot"),
			    (val_max, ":num_repeats", 1),
			    (try_for_range, ":unused", 0, ":num_repeats"),
				    (team_give_order, ":player_team", ":ith_order_group", ":ith_order"),
			    (try_end),
            (else_try),
			    (is_between, ":ith_order_type", 5, 7), #5 or 6; Caba Weapon and Shield orders
				(team_set_order_listener, ":player_team", ":ith_order_group"),
				(call_script, "script_order_weapon_type_switch", ":ith_order"),
				(team_set_order_listener, ":player_team", -1), #Reset
			(try_end),	
		(try_end),		
        (team_set_order_listener, ":player_team", grc_everyone), #Reset			
        (set_show_messages, 1),
		(party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 0),
	]),
 ]
## Prebattle Orders End
## Caba'drin Orders Begin
caba_order_triggers = [
	(ti_before_mission_start, 0, ti_once, [], [
		(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(party_set_slot, "p_main_party_backup", slot_party_gk_order, 0),
		
        (try_for_range, ":i", slot_party_cabadrin_order_d0, slot_party_cabadrin_order_d8 + 1),
	        (party_set_slot, "p_main_party", ":i", 30),
        (try_end),
	]),
	
	(0, 0, 0, [
        (this_or_next|game_key_clicked, gk_group0_hear),
        (this_or_next|game_key_clicked, gk_group1_hear),
        (this_or_next|game_key_clicked, gk_group2_hear),
        (this_or_next|game_key_clicked, gk_group3_hear),
        (this_or_next|game_key_clicked, gk_group4_hear),
        (this_or_next|game_key_clicked, gk_group5_hear),
        (this_or_next|game_key_clicked, gk_group6_hear),
        (this_or_next|game_key_clicked, gk_group7_hear),
        (this_or_next|game_key_clicked, gk_group8_hear),
        (this_or_next|game_key_clicked, gk_everyone_hear),
		(this_or_next|game_key_clicked, gk_reverse_order_group), 
		(game_key_clicked, gk_everyone_around_hear), 
	], [
		(party_set_slot, "p_main_party", slot_party_gk_order, 0),
        (start_presentation, "prsnt_caba_order_display"),
	]),
	
	(ti_escape_pressed, 0, 0, [], [(party_set_slot, "p_main_party", slot_party_gk_order, 0),(is_presentation_active, "prsnt_caba_order_display"),(presentation_set_duration, 0),]),
	
	(0, 0, 0, [(key_clicked, key_f9)], [
	    (neg|party_slot_eq, "p_main_party", slot_party_gk_order, 0),
		(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),
		(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),
		(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),
		(is_presentation_active, "prsnt_caba_order_display"),
		(presentation_set_duration, 0),
		(party_set_slot, "p_main_party", slot_party_gk_order, 0),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_1)], [
		(try_begin),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),
			(party_set_slot, "p_main_party", slot_party_gk_order, gk_order_1),
		(else_try),
			(try_begin),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),	#HOLD		
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(else_try),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),	#ADVANCE
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(else_try),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),	#HOLD FIRE
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(try_end),
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_2)], [
		(try_begin),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),
			(party_set_slot, "p_main_party", slot_party_gk_order, gk_order_2),
		(else_try),
			(try_begin),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),	#FOLLOW
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(else_try),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),	#FALL BACK
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(else_try),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),	#FIRE AT WILL
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(try_end),
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_3)], [
		(try_begin),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),
			(party_set_slot, "p_main_party", slot_party_gk_order, gk_order_3),
		(else_try),
			(try_begin),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),	#CHARGE
			(else_try),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),	#SPREAD OUT
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(else_try),
				(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),	#BLUNT WEAPONS
				(party_set_slot, "p_main_party", slot_party_gk_order, 0),
			(try_end),
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_4)], [
		(try_begin),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),	#STAND GROUND			
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),	#STAND CLOSER
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_3),	#ANY WEAPON
			(call_script, "script_order_set_slot_index", clear),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_5)], [
		(try_begin),
			(party_slot_eq, "p_main_party", slot_party_gk_order, 0),
			(party_set_slot, "p_main_party", slot_party_gk_order, gk_order_5),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_1),	#RETREAT
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),	#MOUNT
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_5),	#One-Hander
			(call_script, "script_order_weapon_type_switch", onehand),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),		
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_6),	#Shield
			(call_script, "script_order_weapon_type_switch", shield),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, k_order_7),	#Begin Skirmish
			(call_script, "script_order_skirmish_begin_end", skirmish),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),    
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_6)], [
	    (try_begin),
			(party_slot_eq, "p_main_party", slot_party_gk_order, 0),
			(party_set_slot, "p_main_party", slot_party_gk_order, gk_order_6),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
		    (party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_2),	#DISMOUNT
		    (party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_5),	#Two-Handers
			(call_script, "script_order_weapon_type_switch", twohands),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_6),	#No Shield
			(call_script, "script_order_weapon_type_switch", noshield),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, k_order_7),	#End Skirmish
			(call_script, "script_order_skirmish_begin_end", end_skirmish),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),    
		(try_end),
	]),

    (0, 0, 0, [(key_clicked, k_order_7)], [ #f7
	    (try_begin),
		    (party_slot_eq, "p_main_party", slot_party_gk_order, 0), 
		    (party_set_slot, "p_main_party", slot_party_gk_order, k_order_7),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_5),	#Polearms
			(call_script, "script_order_weapon_type_switch", polearm),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_6),	#Free Shield
			(call_script, "script_order_weapon_type_switch", free),
			(party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(try_end),
	]),
		
	(0, 0, 0, [(key_clicked, k_order_8)], [ #F8
	    (try_begin),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_5),
		    (call_script, "script_order_weapon_type_switch", ranged),
		    (party_set_slot, "p_main_party", slot_party_gk_order, 0),
		(try_end),
	]),
	
	(0.5, 0, 0, [(call_script, "script_cf_order_skirmish_check")], [(call_script, "script_order_skirmish_skirmish")]), 
 ]
## Caba'drin Orders End

##diplomacy begin
from header_skills import *

dplmc_horse_speed = (
  1, 0, 0, [],
  [
  (eq, "$g_dplmc_horse_speed", 0),
  (try_for_agents, ":agent_no"),
    (agent_is_alive, ":agent_no"),
    (agent_is_human, ":agent_no"),
    (agent_get_horse, ":horse_agent", ":agent_no"),
    (try_begin),
      (ge, ":horse_agent", 0),
      (store_agent_hit_points, ":horse_hp",":horse_agent"),
      (store_sub, ":lost_hp", 100, ":horse_hp"),
      (try_begin),
        (le, ":lost_hp", 15),
        (val_div, ":lost_hp", 2),
        (store_add, ":speed_factor", 100, ":lost_hp"),
      (else_try),
        (val_mul, ":lost_hp", 2),
        (val_div, ":lost_hp", 3),
        (store_sub, ":speed_factor", 115, ":lost_hp"),
      (try_end),
      (agent_get_troop_id, ":agent_troop", ":agent_no"),
      (store_skill_level, ":skl_level", skl_riding, ":agent_troop"),
      (store_mul, ":speed_multi", ":skl_level", 2),
      (val_add, ":speed_multi", 100),
      (val_mul, ":speed_factor", ":speed_multi"),
      (val_div, ":speed_factor", 100),
      (agent_set_horse_speed_factor, ":agent_no", ":speed_factor"),
    (try_end),
  (try_end),
  ])

#gekokujo 3.0 mouselook deathcam start
### MadVader deathcam begin
#common_init_deathcam = (
#   0, 0, ti_once,
#   [],
#   [
#      (assign, "$pop_camera_on", 0),
#      # mouse center coordinates (non-windowed)
#      (assign, "$pop_camera_mouse_center_x", 500),
#      (assign, "$pop_camera_mouse_center_y", 375),
#      # last recorded mouse coordinates
#      (assign, "$pop_camera_mouse_x", "$pop_camera_mouse_center_x"),
#      (assign, "$pop_camera_mouse_y", "$pop_camera_mouse_center_y"),
#      # counts how many cycles the mouse stays in the same position, to determine new center in windowed mode
#      (assign, "$pop_camera_mouse_counter", 0),
#   ]
#)
#
#common_start_deathcam = (
#   0, 4, ti_once, # 4 seconds delay before the camera activates
#   [
#     (main_hero_fallen),
#     (eq, "$pop_camera_on", 0),
#   ],
#   [
#      (get_player_agent_no, ":player_agent"),
#
#      #gekokujo 3.0 enables charge when dead in diplomacy start
#      (agent_get_team, ":player_team", ":player_agent"),	  
#      (try_begin),
#        (eq, "$g_dplmc_charge_when_dead", 1),
#        (team_get_movement_order, ":cur_order", ":player_team", grc_everyone),
#        (neq, ":cur_order", mordr_charge),
#        (team_give_order, ":player_team", grc_everyone, mordr_charge),
#      (try_end),
#	  #gekokujo 3.0 enables charge when dead in diplomacy end
#
#      (agent_get_position, pos1, ":player_agent"),
#      (position_get_x, ":pos_x", pos1),
#      (position_get_y, ":pos_y", pos1),
#      (init_position, pos47),
#      (position_set_x, pos47, ":pos_x"),
#      (position_set_y, pos47, ":pos_y"),
#      (position_set_z_to_ground_level, pos47),
#      (position_move_z, pos47, 250),
#      (mission_cam_set_mode, 1, 0, 0),
#      (mission_cam_set_position, pos47),
#      (assign, "$pop_camera_rotx", 0),
#      (assign, "$pop_camera_on", 1),
#   ]
#)
#
#common_move_deathcam = (
#   0, 0, 0,
#   [
#      (eq, "$pop_camera_on", 1),
#      (this_or_next|key_clicked, key_w),
#      (this_or_next|key_is_down, key_w),
#      (this_or_next|key_clicked, key_s),
#      (this_or_next|key_is_down, key_s),
#      (this_or_next|key_clicked, key_a),
#      (this_or_next|key_is_down, key_a),
#      (this_or_next|key_clicked, key_d),
#      (key_is_down, key_d),
#   ],
#   [
#      (mission_cam_get_position, pos47),
#      (assign, ":move_x", 0),
#      (assign, ":move_y", 0),
#      (try_begin), #forward
#        (this_or_next|key_clicked, key_w),
#        (key_is_down, key_w),
#        (assign, ":move_y", 10),
#      (try_end),
#      (try_begin), #backward
#        (this_or_next|key_clicked, key_s),
#        (key_is_down, key_s),
#        (assign, ":move_y", -10),
#      (try_end),
#      (try_begin), #left
#        (this_or_next|key_clicked, key_a),
#        (key_is_down, key_a),
#        (assign, ":move_x", -10),
#      (try_end),
#      (try_begin), #right
#        (this_or_next|key_clicked, key_d),
#        (key_is_down, key_d),
#        (assign, ":move_x", 10),
#      (try_end),
#      (position_move_x, pos47, ":move_x"),
#      (position_move_y, pos47, ":move_y"),
#      (mission_cam_set_position, pos47),      
#   ]
#)
#
#deathcam_mouse_deadzone = 2 #set this to a positive number (MV: 2 or 3 works well for me, but needs testing on other people's PCs)
#
#common_rotate_deathcam = (
#   0, 0, 0,
#   [
#      (eq, "$pop_camera_on", 1),
#      (neg|is_presentation_active, "prsnt_battle"),
#      (mouse_get_position, pos1),
#      (set_fixed_point_multiplier, 1000),
#      (position_get_x, reg1, pos1),
#      (position_get_y, reg2, pos1),
#      (this_or_next|neq, reg1, "$pop_camera_mouse_center_x"),
#      (neq, reg2, "$pop_camera_mouse_center_y"),
#   ],
#   [
#      # fix for windowed mode: recenter the mouse
#      (assign, ":continue", 1),
#      (try_begin),
#        (eq, reg1, "$pop_camera_mouse_x"),
#        (eq, reg2, "$pop_camera_mouse_y"),
#        (val_add, "$pop_camera_mouse_counter", 1),
#        (try_begin), #hackery: if the mouse hasn't moved for X cycles, recenter it
#          (gt, "$pop_camera_mouse_counter", 50),
#          (assign, "$pop_camera_mouse_center_x", reg1),
#          (assign, "$pop_camera_mouse_center_y", reg2),
#          (assign, "$pop_camera_mouse_counter", 0),
#        (try_end),
#        (assign, ":continue", 0),
#      (try_end),
#      (eq, ":continue", 1), #continue only if mouse has moved
#      (assign, "$pop_camera_mouse_counter", 0), # reset recentering hackery
#      
#      # update recorded mouse position
#      (assign, "$pop_camera_mouse_x", reg1),
#      (assign, "$pop_camera_mouse_y", reg2),
#      
#      (mission_cam_get_position, pos47),
#      (store_sub, ":shift", "$pop_camera_mouse_center_x", reg1), #horizontal shift for pass 0
#      (store_sub, ":shift_vertical", reg2, "$pop_camera_mouse_center_y"), #for pass 1
#      
#      (try_for_range, ":pass", 0, 2), #pass 0: check mouse x movement (left/right), pass 1: check mouse y movement (up/down)
#        (try_begin),
#          (eq, ":pass", 1),
#          (assign, ":shift", ":shift_vertical"), #get ready for the second pass
#        (try_end),
#        (this_or_next|lt, ":shift", -deathcam_mouse_deadzone), #skip pass if not needed (mouse deadzone)
#        (gt, ":shift", deathcam_mouse_deadzone),
#        
#        (assign, ":sign", 1),
#        (try_begin),
#          (lt, ":shift", 0),
#          (assign, ":sign", -1),
#        (try_end),
#        # square root calc
#        (val_abs, ":shift"),
#        (val_sub, ":shift", deathcam_mouse_deadzone), # ":shift" is now 1 or greater
#        (convert_to_fixed_point, ":shift"),
#        (store_sqrt, ":shift", ":shift"),
#        (convert_from_fixed_point, ":shift"),
#        (val_clamp, ":shift", 1, 6), #limit rotation speed
#        (val_mul, ":shift", ":sign"),
#        (try_begin),
#          (eq, ":pass", 0), # rotate around z (left/right)
#          (store_mul, ":minusrotx", "$pop_camera_rotx", -1),
#          (position_rotate_x, pos47, ":minusrotx"), #needed so camera yaw won't change
#          (position_rotate_z, pos47, ":shift"),
#          (position_rotate_x, pos47, "$pop_camera_rotx"), #needed so camera yaw won't change
#        (try_end),
#        (try_begin),
#          (eq, ":pass", 1), # rotate around x (up/down)
#          (position_rotate_x, pos47, ":shift"),
#          (val_add, "$pop_camera_rotx", ":shift"),
#        (try_end),
#      (try_end), #try_for_range ":pass"
#      (mission_cam_set_position, pos47),
#   ]
#)
### MadVader deathcam end
### Zephilinox deathcam begin
common_init_deathcam = (
   0, 0, ti_once,
   [],
   [
        (assign, "$deathcam_on", 0),
        (assign, "$deathcam_death_pos_x", 0),
        (assign, "$deathcam_death_pos_y", 0),
        (assign, "$deathcam_death_pos_z", 0),
        
        (assign, "$deathcam_mouse_last_x", 5000), 
        (assign, "$deathcam_mouse_last_y", 3750),
        
        (assign, "$deathcam_mouse_last_notmoved_x", 5000),
        (assign, "$deathcam_mouse_last_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_x", 5000), #Center screen (10k fixed pos)
        (assign, "$deathcam_mouse_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_counter", 0),
        
        (assign, "$deathcam_total_rotx", 0),
        
        (assign, "$deathcam_sensitivity_x", 400), #4:3 ratio may be best
        (assign, "$deathcam_sensitivity_y", 300), #If modified, change values in common_move_deathcam
        
        (assign, "$deathcam_prsnt_was_active", 0),
   ]
)

common_start_deathcam = (
    0, 1, ti_once, #1 second delay before the camera activates
    [
        (main_hero_fallen),
        (eq, "$deathcam_on", 0),
    ],
    [
        (set_fixed_point_multiplier, 10000),
        (assign, "$deathcam_on", 1),
        
        (display_message, "@You were defeated.", 0xFF2222),
        (display_message, "@Rotate with the mouse, move with standard keys."),
        (display_message, "@Shift/Control for Up/Down, Space Bar to increase speed."),
        (display_message, "@Numpad Plus/Minus to change sensitivity, Home to reset position."),

        (mission_cam_get_position, pos1), #Death pos
        (position_get_x, reg3, pos1),
        (position_get_y, reg4, pos1),
        (position_get_z, reg5, pos1),
        (assign, "$deathcam_death_pos_x", reg3),
        (assign, "$deathcam_death_pos_y", reg4),
        (assign, "$deathcam_death_pos_z", reg5),
        (position_get_rotation_around_z, ":rot_z", pos1),
        
        (init_position, pos47),
        (position_copy_origin, pos47, pos1), #Copy X,Y,Z pos
        (position_rotate_z, pos47, ":rot_z"), #Copying X-Rotation is likely possible, but I haven't figured it out yet
        
        (mission_cam_set_mode, 1, 0, 0), #Manual?

        (mission_cam_set_position, pos47),
        
		#gekokujo 3.0 archers don't charge start
        (team_give_order, 0, grc_infantry, mordr_charge),
        (team_give_order, 1, grc_infantry, mordr_charge),
        (team_give_order, 2, grc_infantry, mordr_charge),
        (team_give_order, 3, grc_infantry, mordr_charge),
		
        (team_give_order, 0, grc_cavalry, mordr_charge),
        (team_give_order, 1, grc_cavalry, mordr_charge),
        (team_give_order, 2, grc_cavalry, mordr_charge),
        (team_give_order, 3, grc_cavalry, mordr_charge),
		
        (team_give_order, 0, grc_heroes, mordr_charge),
        (team_give_order, 1, grc_heroes, mordr_charge),
        (team_give_order, 2, grc_heroes, mordr_charge),
        (team_give_order, 3, grc_heroes, mordr_charge),
        #(team_give_order, 0, grc_everyone, mordr_charge),
        #(team_give_order, 1, grc_everyone, mordr_charge),
        #(team_give_order, 2, grc_everyone, mordr_charge),
        #(team_give_order, 3, grc_everyone, mordr_charge),
		#gekokujo 3.0 archers don't charge end
   ]
)

common_move_deathcam = (
    0, 0, 0,
    [
        (eq, "$deathcam_on", 1),
        (this_or_next|game_key_is_down, gk_move_forward),
        (this_or_next|game_key_is_down, gk_move_backward),
        (this_or_next|game_key_is_down, gk_move_left),
        (this_or_next|game_key_is_down, gk_move_right),
        (this_or_next|key_is_down, key_left_shift),
        (this_or_next|key_is_down, key_left_control),
        (this_or_next|key_is_down, key_numpad_minus),
        (this_or_next|key_is_down, key_numpad_plus),
        (key_clicked, key_home),
    ],
    [   
        (set_fixed_point_multiplier, 10000),
        (mission_cam_get_position, pos47),
        
        (try_begin),
        (key_clicked, key_home),
            (position_set_x, pos47, "$deathcam_death_pos_x"),
            (position_set_y, pos47, "$deathcam_death_pos_y"),
            (position_set_z, pos47, "$deathcam_death_pos_z"),
        (try_end),
        
        (assign, ":move_x", 0),
        (assign, ":move_y", 0),
        (assign, ":move_z", 0),
        
        (try_begin),
        (game_key_is_down, gk_move_forward),
            (val_add, ":move_y", 10),
        (try_end),
        (try_begin),
        (game_key_is_down, gk_move_backward),      
            (val_add, ":move_y", -10),
        (try_end),

        (try_begin),
        (game_key_is_down, gk_move_right),      
            (val_add, ":move_x", 10), 
        (try_end),
        (try_begin),
        (game_key_is_down, gk_move_left),      
            (val_add, ":move_x", -10),
        (try_end),

        (try_begin),
        (key_is_down, key_left_shift),
            (val_add, ":move_z", 10),
        (try_end),
        (try_begin),
        (key_is_down, key_left_control),
            (val_add, ":move_z", -10),
        (try_end),
        
        (try_begin),
        (key_is_down, key_space),
            (val_mul, ":move_x", 4),
            (val_mul, ":move_y", 4),
            (val_mul, ":move_z", 2),
        (try_end),
        
        (position_move_x, pos47, ":move_x"),
        (position_move_y, pos47, ":move_y"),
        (position_move_z, pos47, ":move_z"),
        
        (mission_cam_set_position, pos47),
        
        (try_begin),
        (key_is_down, key_numpad_minus),
        (ge, "$deathcam_sensitivity_x", 4), #Negative check.
        (ge, "$deathcam_sensitivity_y", 3),
            (val_sub, "$deathcam_sensitivity_x", 4),
            (val_sub, "$deathcam_sensitivity_y", 3),
            (store_mod, reg6, "$deathcam_sensitivity_x", 100), #25% increments
            (store_mod, reg7, "$deathcam_sensitivity_y", 75),
            (try_begin),
            (eq, reg6, 0),
            (eq, reg7, 0),
                (assign, reg8, "$deathcam_sensitivity_x"),
                (assign, reg9, "$deathcam_sensitivity_y"),
                (display_message, "@Sensitivity - 25% ({reg8}, {reg9})"),
            (try_end),
        (else_try),
        (key_is_down, key_numpad_plus),
            (val_add, "$deathcam_sensitivity_x", 4),
            (val_add, "$deathcam_sensitivity_y", 3),
            (store_mod, reg6, "$deathcam_sensitivity_x", 100), #25% increments
            (store_mod, reg7, "$deathcam_sensitivity_y", 75),
            (try_begin),
            (eq, reg6, 0),
            (eq, reg7, 0),
                (assign, reg8, "$deathcam_sensitivity_x"),
                (assign, reg9, "$deathcam_sensitivity_y"),
                (display_message, "@Sensitivity + 25% ({reg8}, {reg9})"),
            (try_end),
        (try_end),
   ]
)

common_rotate_deathcam = (
    0, 0, 0,
    [
        (eq, "$deathcam_on", 1),
    ],
    [
        (set_fixed_point_multiplier, 10000), #Extra Precision
        
        (try_begin),
        (this_or_next|is_presentation_active, "prsnt_battle"), #Opened (mouse must move)
        (this_or_next|key_clicked, key_escape), #Menu
        (this_or_next|key_clicked, key_q), #Notes, etc
        (key_clicked, key_tab), #Retreat
        (eq, "$deathcam_prsnt_was_active", 0),
            (assign, "$deathcam_prsnt_was_active", 1),
            (assign, "$deathcam_mouse_last_notmoved_x", "$deathcam_mouse_notmoved_x"),
            (assign, "$deathcam_mouse_last_notmoved_y", "$deathcam_mouse_notmoved_y"),
        (try_end),
        
        (neg|is_presentation_active, "prsnt_battle"),
        
        (mouse_get_position, pos1), #Get and set mouse position
        (position_get_x, reg1, pos1),
        (position_get_y, reg2, pos1),
        
        (mission_cam_get_position, pos47),
        
        (assign, ":continue", 0),
        
        (try_begin),
        (neq, "$deathcam_prsnt_was_active", 1),
            (try_begin), #Check not moved
            (eq, reg1, "$deathcam_mouse_last_x"),
            (eq, reg2, "$deathcam_mouse_last_y"),
            (this_or_next|neq, reg1, "$deathcam_mouse_notmoved_x"),
            (neq, reg2, "$deathcam_mouse_notmoved_y"),
                (val_add, "$deathcam_mouse_notmoved_counter", 1),
                (try_begin), #Notmoved for n cycles
                (ge, "$deathcam_mouse_notmoved_counter", 15),
                    (assign, "$deathcam_mouse_notmoved_counter", 0),
                    (assign, "$deathcam_mouse_notmoved_x", reg1),
                    (assign, "$deathcam_mouse_notmoved_y", reg2),
                (try_end),
            (else_try), #Has moved
                (assign, ":continue", 1),
                (assign, "$deathcam_mouse_notmoved_counter", 0),
            (try_end),
            (assign, "$deathcam_mouse_last_x", reg1), #Next cycle, this pos = last pos
            (assign, "$deathcam_mouse_last_y", reg2),
        (else_try), #prsnt was active
            (try_begin),
            (neq, reg1, "$deathcam_mouse_last_x"), #Is moving
            (neq, reg2, "$deathcam_mouse_last_y"),
                (store_sub, ":delta_x2", reg1, "$deathcam_mouse_last_notmoved_x"), #Store pos difference
                (store_sub, ":delta_y2", reg2, "$deathcam_mouse_last_notmoved_y"),
            (is_between, ":delta_x2", -10, 11), #when engine recenters mouse, there is a small gap
            (is_between, ":delta_y2", -10, 11), #usually 5 pixels, but did 10 to be safe.
                (assign, "$deathcam_prsnt_was_active", 0),
                (assign, "$deathcam_mouse_notmoved_x", "$deathcam_mouse_last_notmoved_x"),
                (assign, "$deathcam_mouse_notmoved_y", "$deathcam_mouse_last_notmoved_y"),
            (else_try),
                (assign, "$deathcam_mouse_notmoved_x", reg1),
                (assign, "$deathcam_mouse_notmoved_y", reg2),
            (try_end),
                (assign, "$deathcam_mouse_last_x", reg1), #Next cycle, this pos = last pos
                (assign, "$deathcam_mouse_last_y", reg2),
        (try_end),
        
        (eq, ":continue", 1), #Else exit
            
        (store_sub, ":delta_x", reg1, "$deathcam_mouse_notmoved_x"), #Store pos difference
        (store_sub, ":delta_y", reg2, "$deathcam_mouse_notmoved_y"),

        (val_mul, ":delta_x", "$deathcam_sensitivity_x"),
        (val_mul, ":delta_y", "$deathcam_sensitivity_y"),
        (val_clamp, ":delta_x", -80000, 80001), #8
        (val_clamp, ":delta_y", -60000, 60001), #6
            
        (store_mul, ":neg_rotx", "$deathcam_total_rotx", -1),
        (position_rotate_x_floating, pos47, ":neg_rotx"), #Reset x axis to initial state
        
        (position_rotate_y, pos47, 90), #Barrel roll by 90 degrees to inverse x/z axis
        (position_rotate_x_floating, pos47, ":delta_x"), #Rotate simulated z axis, Horizontal
        (position_rotate_y, pos47, -90), #Reverse
        
        (position_rotate_x_floating, pos47, "$deathcam_total_rotx"), #Reverse
        
        (position_rotate_x_floating, pos47, ":delta_y"), #Vertical
        (val_add, "$deathcam_total_rotx", ":delta_y"), #Fix yaw
        
        (mission_cam_set_position, pos47),
    ]
)
### Zephilinox deathcam end
#gekokujo 3.0 mouselook deathcam end

#gekokujo 3.0 dplmc_death_camera deprecated
#dplmc_death_camera = (
#  0, 0, 0,
#  [(eq, "$g_dplmc_battle_continuation", 0),
#   (main_hero_fallen),
#   (eq, "$g_dplmc_cam_activated", 1),
#  ],
#  [
#    #(agent_get_look_position, pos1, ":player_agent"),
#
#    (get_player_agent_no, ":player_agent"),
#    (agent_get_team, ":player_team", ":player_agent"),
#    (try_begin),
#      (eq, "$g_dplmc_charge_when_dead", 1),
#      (team_get_movement_order, ":cur_order", ":player_team", grc_everyone),
#      (neq, ":cur_order", mordr_charge),
#      (team_give_order, ":player_team", grc_everyone, mordr_charge),
#    (try_end),
#
#    (mission_cam_get_position, pos1),
#
#    (assign, "$g_camera_rotate_x", 0),
#    (assign, "$g_camera_rotate_y", 0),
#    (assign, "$g_camera_rotate_z", 0),
#    (assign, "$g_camera_x", 0),
#    (assign, "$g_camera_y", 0),
#    (assign, "$g_camera_z", 0),
#
#    (try_begin),
#      (key_is_down, key_a),
#      (mission_cam_set_mode, 1),
#      (val_add, "$g_camera_x", 10),
#    (try_end),
#    (try_begin),
#      (key_is_down, key_d),
#      (mission_cam_set_mode, 1),
#      (val_sub, "$g_camera_x", 10),
#    (try_end),
#    (position_move_x, pos1, "$g_camera_x"),
#
#    (try_begin),
#      (key_is_down, key_w),
#      (mission_cam_set_mode, 1),
#      (val_add, "$g_camera_y", 10),
#    (try_end),
#    (try_begin),
#      (key_is_down, key_s),
#      (mission_cam_set_mode, 1),
#      (val_sub, "$g_camera_y", 10),
#    (try_end),
#    (position_move_y, pos1, "$g_camera_y"),
#
#    (try_begin),
#      (key_is_down, key_numpad_plus),
#      (mission_cam_set_mode, 1),
#      (val_add, "$g_camera_z", 10),
#    (try_end),
#    (try_begin),
#      (key_is_down, key_numpad_minus),
#      (mission_cam_set_mode, 1),
#      (val_sub, "$g_camera_z", 10),
#    (try_end),
#    (position_move_z, pos1, "$g_camera_z"),
#
#    (try_begin),
#      (key_is_down, key_numpad_6),
#      (mission_cam_set_mode, 1),
#      (val_add, "$g_camera_rotate_z", 1),
#    (try_end),
#    (try_begin),
#      (key_is_down, key_numpad_4),
#      (mission_cam_set_mode, 1),
#      (val_sub, "$g_camera_rotate_z", 1),
#    (try_end),
#    (position_rotate_z, pos1, "$g_camera_rotate_z"),
#
#    (try_begin),
#      (key_is_down, key_numpad_1),
#      (mission_cam_set_mode, 1),
#      (val_add, "$g_camera_rotate_y", 1),
#    (try_end),
#    (try_begin),
#      (key_is_down, key_numpad_3),
#      (mission_cam_set_mode, 1),
#      (val_sub, "$g_camera_rotate_y", 1),
#    (try_end),
#    (position_rotate_y, pos1, "$g_camera_rotate_y"),
#
#    (try_begin),
#      (key_is_down, key_numpad_8),
#      (mission_cam_set_mode, 1),
#      (val_add, "$g_camera_rotate_x", 1),
#    (try_end),
#    (try_begin),
#      (key_is_down, key_numpad_2),
#      (mission_cam_set_mode, 1),
#      (val_sub, "$g_camera_rotate_x", 1),
#    (try_end),
#    (position_rotate_x, pos1, "$g_camera_rotate_x"),
#
#    (mission_cam_set_position, pos1),
#
#    (try_begin),
#      (this_or_next|game_key_clicked, gk_view_char),
#      (this_or_next|game_key_clicked, gk_zoom),
#      (game_key_clicked, gk_cam_toggle),
#      (mission_cam_set_mode, 0),
#    (try_end),
#  ])

dplmc_battle_mode_triggers = [
    dplmc_horse_speed,
	#gekokujo 3.0 dplmc_death_camera deprecated
    #dplmc_death_camera,
	common_init_deathcam,
    common_start_deathcam,
    common_move_deathcam,
    common_rotate_deathcam,
	
    #gekokujo 3.0 let's hijack this to make it easier to add triggers to battles
	#gekokujo 3.0 skirmisher weapon distributions
    common_gekokujo_sabakato_switch_check, #gekokujo 3.1 sabakato switch
  ]
##diplomacy end

#gekokujo 3.1 siege improvement start
common_gekokujo_siege_init = (
  ti_before_mission_start, 0, 0, [], 
  [
	(assign, "$gekokujo_gates_total", 0),
    (assign, "$gekokujo_current_gate", 0),
    (assign, "$gekokujo_current_gate_id", 0),
	(assign, "$gekokujo_current_gate_dmg", 0),
    
    (try_begin),
      (eq, "$gekokujo_siege_type", 0), #engineering-based siege
      (assign, "$gekokujo_current_gate_hp", 60),
      (assign, "$gekokujo_first_gate", 2), #first gate is automatically battered
    (else_try),
      (eq, "$gekokujo_siege_type", 1), #agent-based siege
      (assign, "$gekokujo_current_gate_hp", 40), #ninjas weakened the gates from the inside
      (assign, "$gekokujo_first_gate", 1),
    (try_end),
    
    #DEBUG START
	#(assign, "$gekokujo_current_gate_hp", 60), #in the future, gate HP is set on the campaign map
    #(assign, "$gekokujo_first_gate", 1), #in the future, first gate is set on the campaign map
	#DEBUG END
    
	#(set_fixed_point_multiplier, 100),
	
	(scene_prop_get_num_instances, ":num_gates", "spr_gekokujo_c2_gate_large"),  #count number of gates
	(try_for_range, ":gate_no", 0, ":num_gates"), #go through each gate instance
	  (scene_prop_get_instance, ":gate_id", "spr_gekokujo_c2_gate_large", ":gate_no"), #find the gate instance's id
	  (prop_instance_get_variation_id, ":var1", ":gate_id"), #find the instance's gate number (the var1 set in edit mode)
	  (neq, ":var1", 0), #gates with a var1 of 0 (default) are only decorative and should be ignored
	  
	  (try_begin),
	    #(eq, ":var1", 1), #if there are gates at all, we obviously start at the first
        (eq, ":var1", "$gekokujo_first_gate"),
		(eq, "$g_gekokujo_old_siege", 0), #only apply if new-style siege
	    #(assign, "$gekokujo_current_gate", 1), 
	    (assign, "$gekokujo_current_gate", "$gekokujo_first_gate"), 
		(assign, "$gekokujo_current_gate_id", ":gate_id"),
	  (else_try),
		#deactivate all other nondecorative gates so reinforcements can come through
		#(prop_instance_get_position, pos1, ":gate_id"), #absolute position of gate to pos1
		#(prop_instance_get_scale, pos2, ":gate_id"), #get scale of gate to pos2
		#(position_get_scale_x, ":width", pos2), #get scale of x axis to find width
        #(init_position, pos3),
		#(position_set_x, pos3, ":width"), #move pos3 on x axis by width
		#(try_begin),
		#  (gt, ":width", 0), #width was a positive number, it must be the left gate
		#  (position_set_y, pos3, ":width"), #move pos3 on y axis by width
		#  (position_rotate_z, pos1, 90), #rotate pos3 on z axis by 90 degrees
		#(else_try),
		#  #width was a negative number, it must be the right gate
		#  (store_sub, ":width", 0, ":width"), #find the negative of width
		#  (position_set_y, pos3, ":width"), #move pos3 on y axis by the negative of width
		#  (position_rotate_z, pos1, -90), #rotate pos3 on z axis by -90 degrees
		#(try_end),
		#(position_transform_position_to_parent, pos4, pos1, pos3), #get absolute position of pos3 relative from pos1 to pos4
		#(prop_instance_animate_to_position, ":gate_id", pos4, 1), #start with the gate open
        (call_script, "script_gekokujo_open_gate", ":gate_id", 1), #open instantly
	  (try_end),
	  
	  #replace the following with a val_min or val_max as soon as i figure out which is which
	  (try_begin),
	    (gt, ":var1", "$gekokujo_gates_total"),
		(eq, "$g_gekokujo_old_siege", 0), #only apply if new-style siege
	    (assign, "$gekokujo_gates_total", ":var1"),
	  (try_end),
	(try_end),
    
    (try_begin),
      (eq, "$gekokujo_siege_type", 1), #if this is an agent-based siege
      (gt, "$gekokujo_gates_total", 2), #and there are more than 2 gates
      (val_sub, "$gekokujo_gates_total", 1), #the last gate never closes
    (try_end),
  ])

common_gekokujo_siege_gate = (
  5, 0, 0, 
  [
	(gt, "$gekokujo_current_gate", 0),
	#(eq, "$g_gekokujo_old_siege", 0),
  ], 
  [
    #debug start
	#(assign, reg11, "$gekokujo_gates_total"),
	#(assign, reg12, "$gekokujo_current_gate"),
	#(display_message, "@*DEBUG* Gate Check Triggered"),
	#(display_message, "@*DEBUG* Gate Count: {reg11}"),
	#(display_message, "@*DEBUG* Current Gate: {reg12}"),
	#debug end
	
	(set_fixed_point_multiplier, 100),
	
	(try_begin),
	  (lt, "$gekokujo_current_gate_dmg", "$gekokujo_current_gate_hp"), #gate is not yet destroyed
	  
	  (assign, ":gate_dmg", 0),
	  (prop_instance_get_position, pos1, "$gekokujo_current_gate_id"),
	  
	  #attacking agents within 6m of the gate can contribute to battering damage
	  (try_for_agents, ":cur_agent"),
	    (le, ":gate_dmg", 10), #damage capped to 10
	    (agent_is_alive, ":cur_agent"), #dead agents can't batter gates
		
		(agent_get_team, ":cur_agent_team", ":cur_agent"),
		(this_or_next|eq, "$attacker_team", ":cur_agent_team"),
		(eq, "$attacker_team_2", ":cur_agent_team"),
		
		(agent_get_position, pos2, ":cur_agent"),
		(get_distance_between_positions, ":dist", pos1, pos2),
		(try_begin),
		  (lt, ":dist", 600), #within 0-6 meters
		  (val_add, ":gate_dmg", 1), #agents can contribute to damage
		(try_end),
	  (try_end),
	  
	  (val_add, "$gekokujo_current_gate_dmg", ":gate_dmg"), #apply the damage
	  
	  #if the gate was damaged, show a message
	  (try_begin),
	    (gt, ":gate_dmg", 0),
		
		#determine the ordinal form of the current gate's number
		(assign, ":cur_gate", "$gekokujo_current_gate"),
		(try_begin),
		  (eq, ":cur_gate", 1),
		  (str_store_string, s5, "@first"),
		(else_try),
		  (eq, ":cur_gate", 2),
		  (str_store_string, s5, "@second"),
		(else_try),
		  (eq, ":cur_gate", 3),
		  (str_store_string, s5, "@third"),
		(else_try),
		  (eq, ":cur_gate", 4),
		  (str_store_string, s5, "@fourth"),
		(else_try),
		  (eq, ":cur_gate", 5),
		  (str_store_string, s5, "@fifth"),
		(else_try),
		  #let's support gates past the fifth, just in case
		  (str_store_string, s5, "@current"), 
		(try_end),
		
		#determine the % strength left in the gate
	    (store_mul, reg5, "$gekokujo_current_gate_dmg", 100),
		(val_div, reg5, "$gekokujo_current_gate_hp"),
		(val_clamp, reg5, 0, 101),
		(store_sub, reg5, 100, reg5),
		
		#display multiple to make it more eyecatching
		(play_sound, "snd_dummy_hit"),
	    (display_message, "@The attackers have damaged the {s5} gate!", 0xFFDD66),
	    (display_message, "@The {s5} gate is down to {reg5}% strength!", 0xFFDD66),
	  (try_end),
	(try_end),
	
	(try_begin),
	  (ge, "$gekokujo_current_gate_dmg", "$gekokujo_current_gate_hp"), #gate has now been destroyed
	  
	  (assign, ":cur_gate", "$gekokujo_current_gate"),
	  
	  (try_begin),
	    (eq, "$gekokujo_current_gate", "$gekokujo_gates_total"), #this was the final gate	
		(display_message, "@The last gate has been destroyed!", 0xFF2222), #send message 3 times for emphasis
		(display_message, "@The last gate has been destroyed!", 0xFF2222),
		(display_message, "@The last gate has been destroyed!", 0xFF2222),
		(assign, ":next_gate", 0), #don't bother finding a new gate
	  (else_try),
	    (display_message, "@The {s5} gate has been destroyed!", 0xFF2222), #send message 3 times for emphasis
	    (display_message, "@The {s5} gate has been destroyed!", 0xFF2222),
	    (display_message, "@The {s5} gate has been destroyed!", 0xFF2222),
	    (store_add, ":next_gate", ":cur_gate", 1),
	  (try_end),
	  
	  (scene_prop_get_num_instances, ":num_gates", "spr_gekokujo_c2_gate_large"),  #count number of gates
	  (try_for_range, ":gate_no", 0, ":num_gates"), #go through each gate instance
	    (scene_prop_get_instance, ":gate_id", "spr_gekokujo_c2_gate_large", ":gate_no"), #find the gate instance's id
		(prop_instance_get_variation_id, ":var1", ":gate_id"), #find the instance's gate number (the var1 set in edit mode)
		(neq, ":var1", 0), #gates with a var1 of 0 (default) are only decorative and should be ignored
		
		(try_begin),
		  (eq, ":var1", ":cur_gate"), #gates with the current gate number open
		  
		  #(prop_instance_get_position, pos1, ":gate_id"), #absolute position of gate to pos1
		  #(prop_instance_get_scale, pos2, ":gate_id"), #get scale of gate to pos2
		  #(position_get_scale_x, ":width", pos2), #get scale of x axis to find width
          #(init_position, pos3),
		  #(position_set_x, pos3, ":width"), #move pos3 on x axis by width
		  #(try_begin),
		  #  (gt, ":width", 0), #width was a positive number, it must be the left gate
		  #  (position_set_y, pos3, ":width"), #move pos3 on y axis by width
		  #  (position_rotate_z, pos1, 90), #rotate pos3 on z axis by 90 degrees
		  #(else_try),
		  #  #width was a negative number, it must be the right gate
		  #  (store_sub, ":width", 0, ":width"), #find the negative of width
		  #  (position_set_y, pos3, ":width"), #move pos3 on y axis by the negative of width
		  #  (position_rotate_z, pos1, -90), #rotate pos3 on z axis by -90 degrees
		  #(try_end),
		  #(position_transform_position_to_parent, pos4, pos1, pos3), #get absolute position of pos3 relative from pos1 to pos4
		  #(prop_instance_animate_to_position, ":gate_id", pos4, 100), #animate the gate to pos4 in 1 second
          (call_script, "script_gekokujo_open_gate", ":gate_id", 100), #open in 100 seconds
		  
		  (play_sound, "snd_dummy_destroyed"),
		(else_try),
		  (eq, ":var1", ":next_gate"), #gates with the next gate number instantly close up with a clang
		  
		  #(prop_instance_get_position, pos1, ":gate_id"), #absolute position of gate to pos1
		  #(prop_instance_get_scale, pos2, ":gate_id"), #get scale of gate to pos2
		  #(position_get_scale_x, ":width", pos2), #get scale of x axis to find width
          #(init_position, pos3),
		  #(position_set_x, pos3, ":width"), #move pos3 on x axis by width
		  #(try_begin),
		  #  (gt, ":width", 0), #width was a positive number, it must be the left gate
		  #  (store_sub, ":width", 0, ":width"), #find the negative of width
		  #  (position_set_y, pos3, ":width"), #move pos3 on y axis by the negative of width
		  #  (position_rotate_z, pos1, -90), #rotate pos3 on z axis by -90 degrees
		  #(else_try),
		  #  #width was a negative number, it must be the right gate
		  #  (position_set_y, pos3, ":width"), #move pos3 on y axis by width
		  #  (position_rotate_z, pos1, 90), #rotate pos3 on z axis by 90 degrees
		  #(try_end),
		  #(position_transform_position_to_parent, pos4, pos1, pos3), #get absolute position of pos3 relative from pos1 to pos4
		  #(prop_instance_animate_to_position, ":gate_id", pos4, 100), #animate the gate to pos4 in 1 second
          (call_script, "script_gekokujo_close_gate", ":gate_id", 1), #close in 100 seconds          
		  
		  (play_sound, "snd_shield_hit_metal_metal"),
		  
		  (assign, ":next_gate_id", ":gate_id"),
		(try_end),
		
		#the following is old code that makes gates appear/disappear rather than open/close
		#(try_begin),
		#  (eq, ":var1", ":cur_gate"), #gates with the current gate number disappear in a bang
		#  
		#  (prop_instance_get_position, pos1, ":gate_id"),
		#  (position_move_z, pos1, -2000), #raise gate
		#  (prop_instance_set_position, ":gate_id", pos1),
		#  (prop_instance_animate_to_position, ":gate_id", pos1, 1),
		#  
		#  (play_sound, "snd_dummy_destroyed"),
		#(else_try),
		#  (eq, ":var1", ":next_gate"), #gates with the next gate number instantly close up with a clang
		#  
		#  (prop_instance_get_position, pos1, ":gate_id"),
		#  (position_move_z, pos1, 2000), #raise gate
		#  (prop_instance_set_position, ":gate_id", pos1),
		#  (prop_instance_animate_to_position, ":gate_id", pos1, 1),
		#  
		#  (play_sound, "snd_shield_hit_metal_metal"),
		#  
		#  (assign, ":next_gate_id", ":gate_id"),
		#(try_end),
	  (try_end),
	  
	  (assign, "$gekokujo_current_gate_dmg", 0), #reset damage
	  (assign, "$gekokujo_current_gate", ":next_gate"),
	  (try_begin),
	    (neq, "$gekokujo_current_gate", 0),
	    (assign, "$gekokujo_current_gate_id", ":next_gate_id"), 
	  (try_end),
	(try_end),
  ])
  
#common_gekokujo_siege_aggression = (
#  ti_on_agent_spawn, 0, 0, [], 
#  [
#    #this trigger ensures that there will no longer be backwards running
#    (store_trigger_param_1, ":agent_no"),
#    (agent_ai_set_aggressiveness, ":agent_no", 199),
#  ])

#gekokujo 3.1 siege improvement end

multiplayer_server_check_belfry_movement = (
  0, 0, 0, [],
  [
    (multiplayer_is_server),
    (set_fixed_point_multiplier, 100),

    (try_for_range, ":belfry_kind", 0, 2),
      (try_begin),
        (eq, ":belfry_kind", 0),
        (assign, ":belfry_body_scene_prop", "spr_belfry_a"),
      (else_try),
        (assign, ":belfry_body_scene_prop", "spr_belfry_b"),
      (try_end),
    
      (scene_prop_get_num_instances, ":num_belfries", ":belfry_body_scene_prop"),
      (try_for_range, ":belfry_no", 0, ":num_belfries"),
        (scene_prop_get_instance, ":belfry_scene_prop_id", ":belfry_body_scene_prop", ":belfry_no"),
        (prop_instance_get_position, pos1, ":belfry_scene_prop_id"), #pos1 holds position of current belfry 
        (prop_instance_get_starting_position, pos11, ":belfry_scene_prop_id"),

        (store_add, ":belfry_first_entry_point_id", 11, ":belfry_no"), #belfry entry points are 110..119 and 120..129 and 130..139
        (try_begin),
          (eq, ":belfry_kind", 1),
          (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
          (val_add, ":belfry_first_entry_point_id", ":number_of_belfry_a"),
        (try_end),        
                
        (val_mul, ":belfry_first_entry_point_id", 10),
        (store_add, ":belfry_last_entry_point_id", ":belfry_first_entry_point_id", 10),
    
        (try_for_range, ":entry_point_id", ":belfry_first_entry_point_id", ":belfry_last_entry_point_id"),
          (entry_point_is_auto_generated, ":entry_point_id"),
          (assign, ":belfry_last_entry_point_id", ":entry_point_id"),
        (try_end),
        
        (assign, ":belfry_last_entry_point_id_plus_one", ":belfry_last_entry_point_id"),
        (val_sub, ":belfry_last_entry_point_id", 1),
        (assign, reg0, ":belfry_last_entry_point_id"),
        (neg|entry_point_is_auto_generated, ":belfry_last_entry_point_id"),

        (try_begin),
          (get_sq_distance_between_positions, ":dist_between_belfry_and_its_destination", pos1, pos11),
          (ge, ":dist_between_belfry_and_its_destination", 4), #0.2 * 0.2 * 100 = 4 (if distance between belfry and its destination already less than 20cm no need to move it anymore)

          (assign, ":max_dist_between_entry_point_and_belfry_destination", -1), #should be lower than 0 to allow belfry to go last entry point
          (assign, ":belfry_next_entry_point_id", -1),
          (try_for_range, ":entry_point_id", ":belfry_first_entry_point_id", ":belfry_last_entry_point_id_plus_one"),
            (entry_point_get_position, pos4, ":entry_point_id"),
            (get_sq_distance_between_positions, ":dist_between_entry_point_and_belfry_destination", pos11, pos4),
            (lt, ":dist_between_entry_point_and_belfry_destination", ":dist_between_belfry_and_its_destination"),
            (gt, ":dist_between_entry_point_and_belfry_destination", ":max_dist_between_entry_point_and_belfry_destination"),
            (assign, ":max_dist_between_entry_point_and_belfry_destination", ":dist_between_entry_point_and_belfry_destination"),
            (assign, ":belfry_next_entry_point_id", ":entry_point_id"),
          (try_end),

          (try_begin),
            (ge, ":belfry_next_entry_point_id", 0),
            (entry_point_get_position, pos5, ":belfry_next_entry_point_id"), #pos5 holds belfry next entry point target during its path
          (else_try),
            (copy_position, pos5, pos11),    
          (try_end),
        
          (get_distance_between_positions, ":belfry_next_entry_point_distance", pos1, pos5),
        
          #collecting scene prop ids of belfry parts
          (try_begin),
            (eq, ":belfry_kind", 0),
            #belfry platform_a
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
            #belfry platform_b
            (scene_prop_get_instance, ":belfry_platform_b_scene_prop_id", "spr_belfry_platform_b", ":belfry_no"),
          (else_try),
            #belfry platform_a
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
          (try_end),
    
          #belfry wheel_1
          (store_mul, ":wheel_no", ":belfry_no", 3),
          (try_begin),
            (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
            (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),    
            (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
            (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
          (try_end),
          (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
          #belfry wheel_2
          (val_add, ":wheel_no", 1),
          (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
          #belfry wheel_3
          (val_add, ":wheel_no", 1),
          (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),

          (init_position, pos17),
          (position_move_y, pos17, -225),
          (position_transform_position_to_parent, pos18, pos1, pos17),
          (position_move_y, pos17, -225),
          (position_transform_position_to_parent, pos19, pos1, pos17),

          (assign, ":number_of_agents_around_belfry", 0),
          (get_max_players, ":num_players"),
          (try_for_range, ":player_no", 0, ":num_players"),
            (player_is_active, ":player_no"),
            (player_get_agent_id, ":agent_id", ":player_no"),
            (ge, ":agent_id", 0),
            (agent_get_team, ":agent_team", ":agent_id"),
            (eq, ":agent_team", 1), #only team2 players allowed to move belfry (team which spawns outside the castle (team1 = 0, team2 = 1))
            (agent_get_horse, ":agent_horse_id", ":agent_id"),
            (eq, ":agent_horse_id", -1),
            (agent_get_position, pos2, ":agent_id"),
            (get_sq_distance_between_positions_in_meters, ":dist_between_agent_and_belfry", pos18, pos2),

            (lt, ":dist_between_agent_and_belfry", multi_distance_sq_to_use_belfry), #must be at most 10m * 10m = 100m away from the player
            (neg|scene_prop_has_agent_on_it, ":belfry_scene_prop_id", ":agent_id"),
            (neg|scene_prop_has_agent_on_it, ":belfry_platform_a_scene_prop_id", ":agent_id"),

            (this_or_next|eq, ":belfry_kind", 1), #there is this_or_next here because belfry_b has no platform_b
            (neg|scene_prop_has_agent_on_it, ":belfry_platform_b_scene_prop_id", ":agent_id"),
    
            (neg|scene_prop_has_agent_on_it, ":belfry_wheel_1_scene_prop_id", ":agent_id"),#can be removed to make faster
            (neg|scene_prop_has_agent_on_it, ":belfry_wheel_2_scene_prop_id", ":agent_id"),#can be removed to make faster
            (neg|scene_prop_has_agent_on_it, ":belfry_wheel_3_scene_prop_id", ":agent_id"),#can be removed to make faster
            (neg|position_is_behind_position, pos2, pos19),
            (position_is_behind_position, pos2, pos1),
            (val_add, ":number_of_agents_around_belfry", 1),        
          (try_end),

          (val_min, ":number_of_agents_around_belfry", 16),

          (try_begin),
            (scene_prop_get_slot, ":pre_number_of_agents_around_belfry", ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing),
            (scene_prop_get_slot, ":next_entry_point_id", ":belfry_scene_prop_id", scene_prop_next_entry_point_id),
            (this_or_next|neq, ":pre_number_of_agents_around_belfry", ":number_of_agents_around_belfry"),
            (neq, ":next_entry_point_id", ":belfry_next_entry_point_id"),

            (try_begin),
              (eq, ":next_entry_point_id", ":belfry_next_entry_point_id"), #if we are still targetting same entry point subtract 
              (prop_instance_is_animating, ":is_animating", ":belfry_scene_prop_id"),
              (eq, ":is_animating", 1),

              (store_mul, ":sqrt_number_of_agents_around_belfry", "$g_last_number_of_agents_around_belfry", 100),
              (store_sqrt, ":sqrt_number_of_agents_around_belfry", ":sqrt_number_of_agents_around_belfry"),
              (val_min, ":sqrt_number_of_agents_around_belfry", 300),
              (assign, ":distance", ":belfry_next_entry_point_distance"),
              (val_mul, ":distance", ":sqrt_number_of_agents_around_belfry"),
              (val_div, ":distance", 100), #100 is because of fixed_point_multiplier
              (val_mul, ":distance", 4), #multiplying with 4 to make belfry pushing process slower, 
                                                                 #with 16 agents belfry will go with 4 / 4 = 1 speed (max), with 1 agent belfry will go with 1 / 4 = 0.25 speed (min)    
            (try_end),

            (try_begin),
              (ge, ":belfry_next_entry_point_id", 0),

              #up down rotation of belfry's next entry point
              (init_position, pos9),
              (position_set_y, pos9, -500), #go 5.0 meters back
              (position_set_x, pos9, -300), #go 3.0 meters left
              (position_transform_position_to_parent, pos10, pos5, pos9), 
              (position_get_distance_to_terrain, ":height_to_terrain_1", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at left part of belfry
      
              (init_position, pos9),
              (position_set_y, pos9, -500), #go 5.0 meters back
              (position_set_x, pos9, 300), #go 3.0 meters right
              (position_transform_position_to_parent, pos10, pos5, pos9), 
              (position_get_distance_to_terrain, ":height_to_terrain_2", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at right part of belfry

              (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
              (val_mul, ":height_to_terrain", 100), #because of fixed point multiplier

              (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 2 degrees. #ac sonra
              (init_position, pos20),    
              (position_rotate_x_floating, pos20, ":rotate_angle_of_next_entry_point"),
              (position_transform_position_to_parent, pos23, pos5, pos20),

              #right left rotation of belfry's next entry point
              (init_position, pos9),
              (position_set_x, pos9, -300), #go 3.0 meters left
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
              (init_position, pos9),
              (position_set_x, pos9, 300), #go 3.0 meters left
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
              (store_sub, ":height_to_terrain_1", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

              (init_position, pos9),
              (position_set_x, pos9, -300), #go 3.0 meters left
              (position_set_y, pos9, -500), #go 5.0 meters forward
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
              (init_position, pos9),
              (position_set_x, pos9, 300), #go 3.0 meters left
              (position_set_y, pos9, -500), #go 5.0 meters forward
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
              (store_sub, ":height_to_terrain_2", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

              (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),    
              (val_mul, ":height_to_terrain", 100), #100 is because of fixed_point_multiplier
              (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 25 degrees. 
              (val_mul, ":rotate_angle_of_next_entry_point", -1),

              (init_position, pos20),
              (position_rotate_y_floating, pos20, ":rotate_angle_of_next_entry_point"),
              (position_transform_position_to_parent, pos22, pos23, pos20),
            (else_try),
              (copy_position, pos22, pos5),      
            (try_end),
              
            (try_begin),
              (ge, ":number_of_agents_around_belfry", 1), #if there is any agents pushing belfry

              (store_mul, ":sqrt_number_of_agents_around_belfry", ":number_of_agents_around_belfry", 100),
              (store_sqrt, ":sqrt_number_of_agents_around_belfry", ":sqrt_number_of_agents_around_belfry"),
              (val_min, ":sqrt_number_of_agents_around_belfry", 300),
              (val_mul, ":belfry_next_entry_point_distance", 100), #100 is because of fixed_point_multiplier
              (val_mul, ":belfry_next_entry_point_distance", 3), #multiplying with 3 to make belfry pushing process slower, 
                                                                 #with 9 agents belfry will go with 3 / 3 = 1 speed (max), with 1 agent belfry will go with 1 / 3 = 0.33 speed (min)    
              (val_div, ":belfry_next_entry_point_distance", ":sqrt_number_of_agents_around_belfry"),
              #calculating destination coordinates of belfry parts
              #belfry platform_a
              (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos1, pos6),
              (position_transform_position_to_parent, pos8, pos22, pos7),
              (prop_instance_animate_to_position, ":belfry_platform_a_scene_prop_id", pos8, ":belfry_next_entry_point_distance"),    
              #belfry platform_b
              (try_begin),
                (eq, ":belfry_kind", 0),
                (prop_instance_get_position, pos6, ":belfry_platform_b_scene_prop_id"),
                (position_transform_position_to_local, pos7, pos1, pos6),
                (position_transform_position_to_parent, pos8, pos22, pos7),
                (prop_instance_animate_to_position, ":belfry_platform_b_scene_prop_id", pos8, ":belfry_next_entry_point_distance"),
              (try_end),
              #wheel rotation
              (store_mul, ":belfry_wheel_rotation", ":belfry_next_entry_point_distance", -25),
              #(val_add, "$g_belfry_wheel_rotation", ":belfry_wheel_rotation"),
              (assign, "$g_last_number_of_agents_around_belfry", ":number_of_agents_around_belfry"),

              #belfry wheel_1
              #(prop_instance_get_starting_position, pos13, ":belfry_wheel_1_scene_prop_id"),
              (prop_instance_get_position, pos13, ":belfry_wheel_1_scene_prop_id"),
              (prop_instance_get_position, pos20, ":belfry_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos20, pos13),
              (position_transform_position_to_parent, pos21, pos22, pos7),
              (prop_instance_rotate_to_position, ":belfry_wheel_1_scene_prop_id", pos21, ":belfry_next_entry_point_distance", ":belfry_wheel_rotation"),
      
              #belfry wheel_2
              #(prop_instance_get_starting_position, pos13, ":belfry_wheel_2_scene_prop_id"),
              (prop_instance_get_position, pos13, ":belfry_wheel_2_scene_prop_id"),
              (prop_instance_get_position, pos20, ":belfry_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos20, pos13),
              (position_transform_position_to_parent, pos21, pos22, pos7),
              (prop_instance_rotate_to_position, ":belfry_wheel_2_scene_prop_id", pos21, ":belfry_next_entry_point_distance", ":belfry_wheel_rotation"),
      
              #belfry wheel_3
              (prop_instance_get_position, pos13, ":belfry_wheel_3_scene_prop_id"),
              (prop_instance_get_position, pos20, ":belfry_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos20, pos13),
              (position_transform_position_to_parent, pos21, pos22, pos7),
              (prop_instance_rotate_to_position, ":belfry_wheel_3_scene_prop_id", pos21, ":belfry_next_entry_point_distance", ":belfry_wheel_rotation"),

              #belfry main body
              (prop_instance_animate_to_position, ":belfry_scene_prop_id", pos22, ":belfry_next_entry_point_distance"),    
            (else_try),
              (prop_instance_is_animating, ":is_animating", ":belfry_scene_prop_id"),
              (eq, ":is_animating", 1),

              #belfry platform_a
              (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
              #belfry platform_b
              (try_begin),
                (eq, ":belfry_kind", 0),
                (prop_instance_stop_animating, ":belfry_platform_b_scene_prop_id"),
              (try_end),
              #belfry wheel_1
              (prop_instance_stop_animating, ":belfry_wheel_1_scene_prop_id"),
              #belfry wheel_2
              (prop_instance_stop_animating, ":belfry_wheel_2_scene_prop_id"),
              #belfry wheel_3
              (prop_instance_stop_animating, ":belfry_wheel_3_scene_prop_id"),
              #belfry main body
              (prop_instance_stop_animating, ":belfry_scene_prop_id"),
            (try_end),
        
            (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing, ":number_of_agents_around_belfry"),    
            (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_next_entry_point_id, ":belfry_next_entry_point_id"),
          (try_end),
        (else_try),
          (le, ":dist_between_belfry_and_its_destination", 4),
          (scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
      
          (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 1),    

          (try_begin),
            (eq, ":belfry_kind", 0),
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
          (else_try),
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
          (try_end),
    
          (prop_instance_get_starting_position, pos0, ":belfry_platform_a_scene_prop_id"),
          (prop_instance_animate_to_position, ":belfry_platform_a_scene_prop_id", pos0, 400),    
        (try_end),
      (try_end),
    (try_end),
    ])

multiplayer_server_spawn_bots = (
  0, 0, 0, [],
  [
    (multiplayer_is_server),
    (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
    (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
    (try_begin),
      (gt, ":total_req", 0),

      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

        (team_get_score, ":team_1_score", 0),
        (team_get_score, ":team_2_score", 1),

        (store_add, ":current_round", ":team_1_score", ":team_2_score"),
        (eq, ":current_round", 0),

        (store_mission_timer_a, ":round_time"),
        (val_sub, ":round_time", "$g_round_start_time"),
        (lt, ":round_time", 20),

        (assign, ":rounded_game_first_round_time_limit_past", 0),
      (else_try),
        (assign, ":rounded_game_first_round_time_limit_past", 1),
      (try_end),
    
      (eq, ":rounded_game_first_round_time_limit_past", 1),
    
      (store_random_in_range, ":random_req", 0, ":total_req"),
      (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
      (try_begin),
        (lt, ":random_req", 0),
        #add to team 1
        (assign, ":selected_team", 0),
      (else_try),
        #add to team 2
        (assign, ":selected_team", 1),
      (try_end),

      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),

        (store_mission_timer_a, ":round_time"),
        (val_sub, ":round_time", "$g_round_start_time"),

        (try_begin),
          (le, ":round_time", 20),
          (assign, ":look_only_actives", 0),
        (else_try),
          (assign, ":look_only_actives", 1),
        (try_end),
      (else_try),
        (assign, ":look_only_actives", 1),
      (try_end),
    
      (call_script, "script_multiplayer_find_bot_troop_and_group_for_spawn", ":selected_team", ":look_only_actives"),
      (assign, ":selected_troop", reg0),
      (assign, ":selected_group", reg1),

      (team_get_faction, ":team_faction", ":selected_team"),
      (assign, ":num_ai_troops", 0),
      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
        (eq, ":ai_troop_faction", ":team_faction"),
        (val_add, ":num_ai_troops", 1),
      (try_end),

      (assign, ":number_of_active_players_wanted_bot", 0),

      (get_max_players, ":num_players"),
      (try_for_range, ":player_no", 0, ":num_players"),
        (player_is_active, ":player_no"),
        (player_get_team_no, ":player_team_no", ":player_no"),
        (eq, ":selected_team", ":player_team_no"),

        (assign, ":ai_wanted", 0),
        (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
        (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
          (player_slot_ge, ":player_no", ":bot_type_wanted_slot", 1),
          (assign, ":ai_wanted", 1),
          (assign, ":end_cond", 0), 
        (try_end),

        (ge, ":ai_wanted", 1),

        (val_add, ":number_of_active_players_wanted_bot", 1),
      (try_end),

      (try_begin),
        (this_or_next|ge, ":selected_group", 0),
        (eq, ":number_of_active_players_wanted_bot", 0),

        (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
        (try_begin),
          (ge, ":has_item", 0),
          (assign, ":is_horseman", 1),
        (else_try),
          (assign, ":is_horseman", 0),
        (try_end),

        (try_begin),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

          (store_mission_timer_a, ":round_time"),
          (val_sub, ":round_time", "$g_round_start_time"),

          (try_begin),
            (lt, ":round_time", 20), #at start of game spawn at base entry point
            (try_begin),
              (eq, ":selected_team", 0),
              (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 1, ":is_horseman"), 
            (else_try),
              (assign, reg0, multi_initial_spawn_point_team_2),
            (try_end),
          (else_try),
            (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
          (try_end),
        (else_try),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
      
          (try_begin),
            (eq, ":selected_team", 0),
            (assign, reg0, 0),
          (else_try),
            (assign, reg0, 32),
          (try_end),
        (else_try),
          (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
        (try_end),
      
        (store_current_scene, ":cur_scene"),
        (modify_visitors_at_site, ":cur_scene"),
        (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", ":selected_group"),
        (assign, "$g_multiplayer_ready_for_spawning_agent", 0),

        (try_begin),
          (eq, ":selected_team", 0),
          (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
        (else_try),
          (eq, ":selected_team", 1),
          (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
        (try_end),
      (try_end),
    (try_end),    
    ])

multiplayer_server_manage_bots = (
  3, 0, 0, [],
  [
    (multiplayer_is_server),
    (try_for_agents, ":cur_agent"),
      (agent_is_non_player, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_get_group, ":agent_group", ":cur_agent"),
      (try_begin),
        (neg|player_is_active, ":agent_group"),
        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
      (else_try),
        (player_get_team_no, ":leader_team_no", ":agent_group"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (neq, ":leader_team_no", ":agent_team"),
        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
      (try_end),
    (try_end),
    ])

multiplayer_server_check_polls = (
  1, 5, 0,
  [
    (multiplayer_is_server),
    (eq, "$g_multiplayer_poll_running", 1),
    (eq, "$g_multiplayer_poll_ended", 0),
    (store_mission_timer_a, ":mission_timer"),
    (store_add, ":total_votes", "$g_multiplayer_poll_no_count", "$g_multiplayer_poll_yes_count"),
    (this_or_next|eq, ":total_votes", "$g_multiplayer_poll_num_sent"),
    (gt, ":mission_timer", "$g_multiplayer_poll_end_time"),
    (call_script, "script_cf_multiplayer_evaluate_poll"),
    ],
  [
    (assign, "$g_multiplayer_poll_running", 0),
    (try_begin),
      (this_or_next|eq, "$g_multiplayer_poll_to_show", 0), #change map
      (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
      (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_poll_value_to_show", 1),
      (call_script, "script_game_set_multiplayer_mission_end"),
    (try_end),
    ])
    
multiplayer_server_check_end_map = ( 
  1, 0, 0, [],
  [
    (multiplayer_is_server),
    #checking for restarting the map
    (assign, ":end_map", 0),
    (try_begin),
      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
      (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
    
      (try_begin),
        (eq, "$g_round_ended", 1),

        (store_mission_timer_a, ":seconds_past_till_round_ended"),
        (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
        (store_sub, ":multiplayer_respawn_period_minus_one", "$g_multiplayer_respawn_period", 1),
        (ge, ":seconds_past_till_round_ended", ":multiplayer_respawn_period_minus_one"),
  
        (store_mission_timer_a, ":mission_timer"),    
        (try_begin),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
          (assign, ":reduce_amount", 90),
        (else_try),
          (assign, ":reduce_amount", 120),
        (try_end),
    
        (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
        (store_sub, ":game_max_seconds_min_n_seconds", ":game_max_seconds", ":reduce_amount"), #when round ends if there are 60 seconds to map change time then change map without completing exact map time.
        (gt, ":mission_timer", ":game_max_seconds_min_n_seconds"),
        (assign, ":end_map", 1),
      (try_end),
      
      (eq, ":end_map", 1),
    (else_try),
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #battle mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #fight and destroy mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege), #siege mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #in headquarters mod game cannot limited by time, only can be limited by score.
      (store_mission_timer_a, ":mission_timer"),
      (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
      (gt, ":mission_timer", ":game_max_seconds"),
      (assign, ":end_map", 1),
    (else_try),
      #assuming only 2 teams in scene
      (team_get_score, ":team_1_score", 0),
      (team_get_score, ":team_2_score", 1),
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #for not-headquarters mods
        (try_begin),
          (this_or_next|ge, ":team_1_score", "$g_multiplayer_game_max_points"),
          (ge, ":team_2_score", "$g_multiplayer_game_max_points"),
          (assign, ":end_map", 1),
        (try_end),
      (else_try),
        (assign, ":at_least_one_player_is_at_game", 0),
        (get_max_players, ":num_players"),
        (try_for_range, ":player_no", 0, ":num_players"),
          (player_is_active, ":player_no"),
          (player_get_agent_id, ":agent_id", ":player_no"),
          (ge, ":agent_id", 0),
          (neg|agent_is_non_player, ":agent_id"),
          (assign, ":at_least_one_player_is_at_game", 1),
          (assign, ":num_players", 0),
        (try_end),
    
        (eq, ":at_least_one_player_is_at_game", 1),

        (this_or_next|le, ":team_1_score", 0), #in headquarters game ends only if one team has 0 score.
        (le, ":team_2_score", 0),
        (assign, ":end_map", 1),
      (try_end),
    (try_end),
    (try_begin),
      (eq, ":end_map", 1),
      (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
      (call_script, "script_game_set_multiplayer_mission_end"),           
    (try_end),
    ])

multiplayer_once_at_the_first_frame = (
  0, 0, ti_once, [], [
    (start_presentation, "prsnt_multiplayer_welcome_message"),
    ])

multiplayer_battle_window_opened = (
  ti_battle_window_opened, 0, 0, [], [
    (start_presentation, "prsnt_multiplayer_team_score_display"),
    ])


common_battle_mission_start = (
  ti_before_mission_start, 0, 0, [],
  [
    (team_set_relation, 0, 2, 1),
    (team_set_relation, 1, 3, 1),
    (call_script, "script_change_banners_and_chest"),
    ])

common_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (eq, "$g_battle_won", 1),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0),
#gekokujo 3.0 mouselook death cam start
    (else_try),
      (eq, "$pin_player_fallen", 1),
      (call_script, "script_simulate_retreat", 0, 0, 0),
      (assign, "$g_battle_result", -1),
      (set_mission_result, -1),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission, 0),
    (else_try),
      (eq, "$deathcam_on", 1),
      (question_box,"str_do_you_want_to_retreat"),
#gekokujo 3.0 mouselook death cam end
#gekokujo 3.0 diplomacy deathcam deprecated start
#    ##diplomacy begin
#    (else_try),
#      (eq, "$g_dplmc_battle_continuation", 0),
#      ##diplomacy start+ Import Caba`drin's battle continuation fix
#      (this_or_next|main_hero_fallen),   #CABA EDIT/FIX FOR DEATH CAM
#      ##diplomacy end+
#      (eq, "$pin_player_fallen", 1),
#      (question_box,"str_do_you_want_to_retreat"),
###      (call_script, "script_simulate_retreat", 5, 20),
###      (str_store_string, s5, "str_retreat"),
###      (call_script, "script_count_mission_casualties_from_agents"),
###      (set_mission_result, -1),
###      (finish_mission,0),
#    ##diplomacy end
#gekokujo 3.0 diplomacy deathcam deprecated end
    (else_try),
      (call_script, "script_cf_check_enemies_nearby"),
      (question_box,"str_do_you_want_to_retreat"),
    (else_try),
      (display_message,"str_can_not_retreat"),
    (try_end),
    ])

common_battle_init_banner = (
  ti_on_agent_spawn, 0, 0, [],
  [
    (store_trigger_param_1, ":agent_no"),
    (agent_get_troop_id, ":troop_no", ":agent_no"),
    (call_script, "script_troop_agent_set_banner", "tableau_game_troop_label_banner", ":agent_no", ":troop_no"),
  ])


common_arena_fight_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (question_box,"str_give_up_fight"),
    ])

common_custom_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (neq, "$g_battle_result", 0),
      (call_script, "script_custom_battle_end"),
      (finish_mission),
    (else_try),
      (question_box,"str_give_up_fight"),
    (try_end),
    ])

from header_skills import *
bodyguard_triggers = [
 (ti_after_mission_start, 0, ti_once, [(neq, "$g_mt_mode", tcm_disguised)], #condition for not sneaking in; to exclude prison-breaks, etc change to (eq, "$g_mt_mode", tcm_default")
   [
    #gekokujo 3.0 microfactions! start
	#disable this if we're going into a fort, since it double-spawns there for some weird reason
	#(neg|party_slot_eq, "$current_town", slot_party_type, spt_fort),
    #gekokujo 3.0 microfactions! end
	
    #Get number of bodyguards
    (store_skill_level, ":leadership", skl_leadership, "trp_player"),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (val_div, ":leadership", 3),
    (val_div, ":renown", 400),
    (store_add, ":max_guards", ":renown", ":leadership"),
    (val_min, ":max_guards", 4),
   
    #gekokujo 3.1 ninja bodyguards start
    #we have to disable this to allow mandatory ninja bodyguards
    #(ge, ":max_guards", 1),
    #gekokujo 3.1 ninja bodyguards end

    #Get player info
    (get_player_agent_no, ":player"),
    (agent_get_team, ":playerteam", ":player"),
    (agent_get_horse, ":use_horse", ":player"), #If the player spawns with a horse, the bodyguard will too.

    #Prepare Scene/Mission Template
    (assign, ":entry_point", 0),
    (assign, ":mission_tpl", 0),
    (try_begin),        
        #gekokujo 3.1 crimes start
        (gt, "$gekokujo_encounter_mode", 0),
        (assign, ":entry_point", 0), #First Attacker's Entry
        (assign, ":mission_tpl", "mt_gekokujo_encounter"), 
        #gekokujo 3.1 crimes end
    (else_try),
		(party_slot_eq, "$current_town", slot_party_type, spt_village),
        (assign, ":entry_point", 11), #Village Elder's Entry
        (assign, ":mission_tpl", "mt_village_center"),
    (else_try),
		#gekokujo 3.0 microfactions! start #forget this crap
		(party_slot_eq, "$current_town", slot_party_type, spt_fort), 
        (assign, ":entry_point", 12), #Deputy's Entry
        (assign, ":mission_tpl", "mt_village_center"),
		#gekokujo 3.0 microfactions! end
    (else_try),
        (this_or_next|eq, "$talk_context", tc_prison_break),
        (this_or_next|eq, "$talk_context", tc_escape),
        (eq, "$talk_context", tc_town_talk),
        (assign, ":entry_point", 24), #Prison Guard's Entry
        (try_begin),
            (party_slot_eq, "$current_town", slot_party_type, spt_castle),
            (assign, ":mission_tpl", "mt_castle_visit"),
        (else_try),
            (assign, ":mission_tpl", "mt_town_center"),
        (try_end),
    (else_try),
        (eq, "$talk_context", tc_tavern_talk),
        (assign, ":entry_point", 17), #First NPC Tavern Entry
    (try_end),
    (try_begin),
        (neq, "$talk_context", tc_tavern_talk),
        (gt, ":use_horse", 0),
        (mission_tpl_entry_set_override_flags, ":mission_tpl", ":entry_point", 0),
    (try_end),
    (store_current_scene, ":cur_scene"),
    (modify_visitors_at_site, ":cur_scene"),  
   
    #Find and Spawn Bodyguards
    (assign, ":bodyguard_count", 0),   
    (party_get_num_companion_stacks, ":num_of_stacks", "p_main_party"),
    (try_for_range, ":i", 0, ":num_of_stacks"),
        (party_stack_get_troop_id, ":troop_id", "p_main_party", ":i"),
        (neq, ":troop_id", "trp_player"),
        (troop_is_hero, ":troop_id"),
        (neg|troop_is_wounded, ":troop_id"),
        (val_add, ":bodyguard_count", 1),
                
        (try_begin), #For prison-breaks
            (this_or_next|eq, "$talk_context", tc_escape),
            (eq, "$talk_context", tc_prison_break),      
            (troop_set_slot, ":troop_id", slot_troop_will_join_prison_break, 1),
        (try_end),

        (add_visitors_to_current_scene, ":entry_point", ":troop_id", 1),

        (eq, ":bodyguard_count", ":max_guards"),
        (assign, ":num_of_stacks", 0), #Break Loop       
    (try_end), #Stack Loop
	
	#gekokujo 3.1 ninja bodyguards start
    #minimum of two ninjas are always allowed, but 4 bodyguards total is still max
    (try_begin),
      (eq, ":max_guards", 0),
      (val_add, ":max_guards", 2), 
    (else_try),
      (eq, ":max_guards", 1),
      (val_add, ":max_guards", 1), 
    (try_end),
    
	#male/female agents/experienced agents are added AFTER companions, no matter the order
	(party_get_num_companion_stacks, ":num_of_stacks", "p_main_party"),
	(try_for_range, ":i", 0, ":num_of_stacks"),
		(lt, ":bodyguard_count", ":max_guards"), #only bother if we're not yet at capacity
		(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i"),
		(this_or_next|eq, ":troop_id", "trp_yojimbo"),
		(this_or_next|eq, ":troop_id", "trp_hired_agent"),
		(this_or_next|eq, ":troop_id", "trp_hired_agent_experienced"),
		(this_or_next|eq, ":troop_id", "trp_female_agent"),
		(eq, ":troop_id", "trp_female_agent_experienced"),
		
		(party_stack_get_size, ":num_agents", "p_main_party", ":i"),
		(party_stack_get_num_wounded, ":wounded_agents", "p_main_party", ":i"),
		
		(val_sub, ":num_agents", ":wounded_agents"), #number of available agents
		(store_sub, ":max_agents", ":max_guards", ":bodyguard_count"), #how many we can actually spawn
		(try_begin),
			(gt, ":num_agents", ":max_agents"), #if there are more agents available than we can spawn
			(assign, ":num_agents", ":max_agents"), #change available to the lower number
		(try_end),
		
		(val_add, ":bodyguard_count", ":num_agents"),
		
		(try_begin), #For prison-breaks
			(this_or_next|eq, "$talk_context", tc_escape),
			(eq, "$talk_context", tc_prison_break),
			(troop_set_slot, ":troop_id", slot_troop_will_join_prison_break, 1),
		(try_end),
		
		(add_visitors_to_current_scene, ":entry_point", ":troop_id", ":num_agents"),
		
		#so they spawn correctly, we need to assign the counts to global vars
		(try_begin),
			(eq, ":troop_id", "trp_yojimbo"),
			(assign, "$gekokujo_bodyguard_yojimbo", ":num_agents"),
		(else_try),
			(eq, ":troop_id", "trp_hired_agent"),
			(assign, "$gekokujo_bodyguard_hired_agents", ":num_agents"),
		(else_try),
			(eq, ":troop_id", "trp_hired_agent_experienced"),
			(assign, "$gekokujo_bodyguard_hired_agents_experienced", ":num_agents"),
		(else_try),
			(eq, ":troop_id", "trp_female_agent"),
			(assign, "$gekokujo_bodyguard_female_agents", ":num_agents"),
		(else_try),
			(eq, ":troop_id", "trp_female_agent_experienced"),
			(assign, "$gekokujo_bodyguard_female_agents_experienced", ":num_agents"),
		(try_end),
		
		(eq, ":bodyguard_count", ":max_guards"),
		(assign, ":num_of_stacks", 0), #Break Loop    
	(try_end),
	#gekokujo 3.1 ninja bodyguards end
	
    (gt, ":bodyguard_count", 0), #If bodyguards spawned...
    (set_show_messages, 0),   
    #gekokujo 3.1 random encounters start
    #automatic charge in encounter_mode 1 and 3, since you have no idea where your enemy is
    #(team_give_order, ":playerteam", 8, mordr_follow), #Division 8 to avoid potential conflicts
    (try_begin),
      (gt, "$gekokujo_encounter_mode", 0),
      (team_give_order, ":playerteam", 8, mordr_charge),
    (else_try),
      (team_give_order, ":playerteam", 8, mordr_follow), #Division 8 to avoid potential conflicts
    (try_end),
    #gekokujo 3.1 random encounters end
    (set_show_messages, 1),   
   ]),   

 (ti_on_agent_spawn, 0, 0, [], 
   [
    (store_trigger_param_1, ":agent"),
    (agent_get_troop_id, ":troop", ":agent"),
    (neq, ":troop", "trp_player"),
	
	#gekokujo 3.1 ninja bodyguards start
	#the way this was originally written only allowed heroes to spawn correctly
    #(troop_is_hero, ":troop"),
    #(main_party_has_troop, ":troop"),
	(assign, ":is_bodyguard", 0),
	
	(try_begin),
		(troop_is_hero, ":troop"),
		(main_party_has_troop, ":troop"),
		(assign, ":is_bodyguard", 1),
	(else_try),
		(eq, ":troop", "trp_yojimbo"),
		(gt, "$gekokujo_bodyguard_yojimbo", 0),
		(val_sub, "$gekokujo_bodyguard_yojimbo", 1),
		(assign, ":is_bodyguard", 1),
	(else_try),
		(eq, ":troop", "trp_hired_agent"),
		(gt, "$gekokujo_bodyguard_hired_agents", 0),
		(val_sub, "$gekokujo_bodyguard_hired_agents", 1),
		(assign, ":is_bodyguard", 1),
	(else_try),
		(eq, ":troop", "trp_hired_agent_experienced"),
		(gt, "$gekokujo_bodyguard_hired_agents_experienced", 0),
		(val_sub, "$gekokujo_bodyguard_hired_agents_experienced", 1),
		(assign, ":is_bodyguard", 1),
	(else_try),
		(eq, ":troop", "trp_female_agent"),
		(gt, "$gekokujo_bodyguard_female_agents", 0),
		(val_sub, "$gekokujo_bodyguard_female_agents", 1),
		(assign, ":is_bodyguard", 1),
	(else_try),
		(eq, ":troop", "trp_female_agent_experienced"),
		(gt, "$gekokujo_bodyguard_female_agents_experienced", 0),
		(val_sub, "$gekokujo_bodyguard_female_agents_experienced", 1),
		(assign, ":is_bodyguard", 1),
	(try_end),
	
	(eq, ":is_bodyguard", 1),
	#gekokujo 3.1 ninja bodyguards end
    
    (get_player_agent_no, ":player"),
    (agent_get_team, ":playerteam", ":player"),
    (agent_get_position,pos1,":player"),        
    
    (agent_set_team, ":agent", ":playerteam"),
    (agent_set_division, ":agent", 8),
    (agent_add_relation_with_agent, ":agent", ":player", 1),
    (agent_set_is_alarmed, ":agent", 1),
    (store_random_in_range, ":shift", 1, 3),
    (val_mul, ":shift", 100),
    (position_move_y, pos1, ":shift"),
    (store_random_in_range, ":shift", 1, 3),
    (store_random_in_range, ":shift_2", 0, 2),
    (val_mul, ":shift_2", -1),
    (try_begin),
        (neq, ":shift_2", 0),
        (val_mul, ":shift", ":shift_2"),
    (try_end),
    (position_move_x, pos1, ":shift"),
    (agent_set_position, ":agent", pos1),
	
	#gekokujo 3.1 ninja bodyguards start
	#copy over ninja disguises from common_gekokujo_equip

	
	#gekokujo 3.0 ninja bodyguards end
   ]),
  
 (ti_on_agent_killed_or_wounded, 0, 0, [],
   [
    (store_trigger_param_1, ":dead_agent"),
	(store_trigger_param_3, ":is_wounded"),
        
    (agent_get_troop_id, ":troop", ":dead_agent"),
    (neq, ":troop", "trp_player"),
	 
	#gekokujo 3.1 ninja bodyguards start
	#the way this was originally written only wounded heroes
    #(troop_is_hero, ":troop"),
    #(main_party_has_troop, ":troop"),
    #(party_wound_members, "p_main_party", ":troop", 1),
	(main_party_has_troop, ":troop"),
	(try_begin),
		(troop_is_hero, ":troop"),
		(party_wound_members, "p_main_party", ":troop", 1),
	(else_try),
		(agent_is_ally, ":dead_agent"),
		(eq, ":is_wounded", 1),
		(party_wound_members, "p_main_party", ":troop", 1),
	(else_try),
		(agent_is_ally, ":dead_agent"),
		(eq, ":is_wounded", 0),
		(party_remove_members, "p_main_party", ":troop", 1),
	(try_end),
	#gekokujo 3.1 ninja bodyguards end
   ]),
   
   common_gekokujo_sabakato_switch_check, #gekokujo 3.1 sabakato switch
 ]

custom_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 2),
#gekokujo 3.0 diplomacy deathcam deprecated start
#    ##diplomacy begin
#    (this_or_next|eq, "$g_dplmc_battle_continuation", 0),
#    (neg|main_hero_fallen, 0),
#    ##diplomacy end
#gekokujo 3.0 diplomacy deathcam deprecated end
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign, "$g_battle_won",1),
    (assign, "$g_battle_result", 1),
    ],
  [
    (call_script, "script_custom_battle_end"),
    (finish_mission, 1),
    ])

custom_battle_check_defeat_condition = (
  1, 4,
##diplomacy begin
  0,
##diplomacy end
  [
    (main_hero_fallen),
#gekokujo 3.0 diplomacy deathcam deprecated start
#    ##diplomacy begin
#    (try_begin),
#      (eq, "$g_dplmc_battle_continuation", 0),
#      (assign, ":num_allies", 0),
#      (try_for_agents, ":agent"),
#       (agent_is_ally, ":agent"),
#       (agent_is_alive, ":agent"),
#       (val_add, ":num_allies", 1),
#      (try_end),
#      (gt, ":num_allies", 0),
#      (try_begin),
#        (eq, "$g_dplmc_cam_activated", 0),
#        #(store_mission_timer_a, "$g_dplmc_main_hero_fallen_seconds"),
#        (assign, "$g_dplmc_cam_activated", 1),
#        (display_message, "@You have been knocked out by the enemy. Watch your men continue the fight without you or press Tab to retreat."),
#		#gekokujo 3.0 mouselook deathcam no more control message
#        #(display_message, "@To watch the fight you can use 'w, a, s, d, numpad_+/numpad_-' to move and 'numpad_1,2,3,4,6,8' to rotate the cam."),
#      (try_end),
#  (else_try),
#    ##diplomacy end
#gekokujo 3.0 diplomacy deathcam deprecated end
    (assign,"$g_battle_result",-1),
#gekokujo 3.0 diplomacy deathcam deprecated start
#    ##diplomacy begin
#    (try_end),
#    ##diplomacy end
#gekokujo 3.0 diplomacy deathcam deprecated end
    ],
  [
    (call_script, "script_custom_battle_end"),
    (finish_mission),
    ])

common_battle_victory_display = (
  10, 0, 0, [],
  [
    (eq,"$g_battle_won",1),
    (display_message,"str_msg_battle_won"),
    ])

common_siege_question_answered = (
  ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$pin_player_fallen", 0),
     (get_player_agent_no, ":player_agent"),
     (agent_get_team, ":agent_team", ":player_agent"),
     (try_begin),
       (neq, "$attacker_team", ":agent_team"),
       (neq, "$attacker_team_2", ":agent_team"),
       (str_store_string, s5, "str_siege_continues"),
       (call_script, "script_simulate_retreat", 8, 15, 0),
     (else_try),
       (str_store_string, s5, "str_retreat"),
       (call_script, "script_simulate_retreat", 5, 20, 0),
     (try_end),
     (call_script, "script_count_mission_casualties_from_agents"),
     (finish_mission,0),
     ])

common_custom_battle_question_answered = (
   ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$g_battle_result", -1),
     (call_script, "script_custom_battle_end"),
     (finish_mission),
     ])

common_custom_siege_init = (
  0, 0, ti_once, [],
  [
    (assign, "$g_battle_result", 0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

common_siege_init = (
  0, 0, ti_once, [],
  [
    (assign,"$g_battle_won",0),
    (assign,"$defender_reinforcement_stage",0),
    (assign,"$attacker_reinforcement_stage",0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

common_music_situation_update = (
  30, 0, 0, [],
  [
    (call_script, "script_combat_music_set_situation_with_culture"),
    ])

common_siege_ai_trigger_init = (
  0, 0, ti_once,
  [
    (assign, "$defender_team", 0),
    (assign, "$attacker_team", 1),
    (assign, "$defender_team_2", 2),
    (assign, "$attacker_team_2", 3),
    ], [])

common_siege_ai_trigger_init_2 = (
  0, 0, ti_once,
  [
    (set_show_messages, 0),
    (entry_point_get_position, pos10, 10),
    (try_for_range, ":cur_group", 0, grc_everyone),
      (neq, ":cur_group", grc_archers),
      (team_give_order, "$defender_team", ":cur_group", mordr_hold),
      (team_give_order, "$defender_team", ":cur_group", mordr_stand_closer),
      (team_give_order, "$defender_team", ":cur_group", mordr_stand_closer),
      (team_give_order, "$defender_team_2", ":cur_group", mordr_hold),
      (team_give_order, "$defender_team_2", ":cur_group", mordr_stand_closer),
      (team_give_order, "$defender_team_2", ":cur_group", mordr_stand_closer),
    (try_end),
    (team_give_order, "$defender_team", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team", grc_everyone, pos10),
    (team_give_order, "$defender_team_2", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team_2", grc_everyone, pos10),
    (set_show_messages, 1),
    ], [])

common_siege_ai_trigger_init_after_2_secs = (
  0, 2, ti_once, [],
  [
    (try_for_agents, ":agent_no"),
      (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
    (try_end),
    ])

common_siege_defender_reinforcement_check = (
  3, 0, 5, [],
  [(lt, "$defender_reinforcement_stage", 7),
   (store_mission_timer_a,":mission_time"),
   (ge,":mission_time",10),
   (store_normalized_team_count,":num_defenders",0),
   (lt,":num_defenders",8),
   (add_reinforcements_to_entry,4, 7),
   (val_add,"$defender_reinforcement_stage",1),
   #gekokujo - defender reinforcements always charge
   #(try_begin),
   #  (gt, ":mission_time", 300), #5 minutes, don't let small armies charge
   #  (get_player_agent_no, ":player_agent"),
   #  (agent_get_team, ":player_team", ":player_agent"),
   #  (neq, ":player_team", "$defender_team"), #player should be the attacker
   #  (neq, ":player_team", "$defender_team_2"), #player should be the attacker
   #  (ge, "$defender_reinforcement_stage", 2),
   #  (set_show_messages, 0),
   #  (team_give_order, "$defender_team", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
   #  (team_give_order, "$defender_team_2", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
   #  (team_give_order, "$defender_team", grc_cavalry, mordr_charge), #AI desperate charge:cavalry!!!
   #  (team_give_order, "$defender_team_2", grc_cavalry, mordr_charge), #AI desperate charge:cavalry!!!
   #  (set_show_messages, 1),
   #  (ge, "$defender_reinforcement_stage", 4),
   #  (set_show_messages, 0),
   #  (team_give_order, "$defender_team", grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
   #  (team_give_order, "$defender_team_2", grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
   #  (set_show_messages, 1),
   #(try_end),
   (team_give_order, "$defender_team", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
   (team_give_order, "$defender_team_2", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
   (team_give_order, "$defender_team", grc_cavalry, mordr_charge), #AI desperate charge:cavalry!!!
   (team_give_order, "$defender_team_2", grc_cavalry, mordr_charge), #AI desperate charge:cavalry!!!
   ])

common_siege_defender_reinforcement_archer_reposition = (
  2, 0, 0,
  [
    (gt, "$defender_reinforcement_stage", 0),
    ],
  [
    (call_script, "script_siege_move_archers_to_archer_positions"),
    ])

common_siege_attacker_reinforcement_check = (
  1, 0, 5,
  [
    (lt,"$attacker_reinforcement_stage",5),
    (store_mission_timer_a,":mission_time"),
    (ge,":mission_time",10),
    (store_normalized_team_count,":num_attackers",1),
    (lt,":num_attackers",6)
    ],
  [
    (add_reinforcements_to_entry, 1, 8),
    (val_add,"$attacker_reinforcement_stage", 1),
    ])

common_siege_attacker_do_not_stall = (
  5, 0, 0, [],
  [ #Make sure attackers do not stall on the ladders...
    (try_for_agents, ":agent_no"),
      (agent_is_human, ":agent_no"),
      (agent_is_alive, ":agent_no"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (this_or_next|eq, ":agent_team", "$attacker_team"),
      (eq, ":agent_team", "$attacker_team_2"),
      (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
    (try_end),
    ])

common_battle_check_friendly_kills = (
  2, 0, 0, [],
  [
    (call_script, "script_check_friendly_kills"),
    ])

common_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    ##gekokujo 3.1 jacobhinds overhauled morale and routing start
    (call_script, "script_all_enemies_routed"),
    (this_or_next|eq, reg0, 0),
    ##gekokujo 3.1 jacobhinds overhauled morale and routing end
    (all_enemies_defeated, 5),
#gekokujo 3.0 diplomacy deathcam deprecated start
#    ##diplomacy begin
#    (this_or_next|eq, "$g_dplmc_battle_continuation", 0),
#    (neg|main_hero_fallen),
#    ##diplomacy end
#gekokujo 3.0 diplomacy deathcam deprecated end
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$g_battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_play_victorious_sound"),
    ],
  [
    (call_script, "script_count_mission_casualties_from_agents"),
    (finish_mission, 1),
    ])

common_battle_victory_display = (
  10, 0, 0, [],
  [
    (eq,"$g_battle_won",1),
    (display_message,"str_msg_battle_won"),
    ])

common_siege_refill_ammo = (
  120, 0, 0, [],
  [#refill ammo of defenders every two minutes.
    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":cur_agent"),
      (neq, ":cur_agent", ":player_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
##      (agent_is_defender, ":cur_agent"),
      (agent_get_team, ":agent_team", ":cur_agent"),
      (this_or_next|eq, ":agent_team", "$defender_team"),
      (eq, ":agent_team", "$defender_team_2"),
      (agent_refill_ammo, ":cur_agent"),
    (try_end),
    ])

#gekokujo 3.0 mouselook death cam start
common_siege_check_defeat_condition = (
    1, 4, ti_once,
    [
        (main_hero_fallen),
        (assign, ":pteam_alive", 0), 
        (try_for_agents, ":agent"), #Check players team is dead
            (neq, ":pteam_alive", 1), #Break loop
            (agent_is_ally, ":agent"),
            (agent_is_alive, ":agent"),
            (assign, ":pteam_alive", 1),
        (try_end),
        (eq, ":pteam_alive", 0),
    ],
    [
        (assign, "$pin_player_fallen", 1),
        (display_message, "@Press TAB to end the battle."),
    ]
)
#gekokujo 3.0 mouselook death cam end
#gekokujo 3.0 diplomacy deathcam deprecated start
#common_siege_check_defeat_condition = (
#  1, 4,
###diplomacy begin
#  0,
###diplomacy end
#  [
#    (main_hero_fallen)
#    ],
#  [
#    ##diplomacy begin
#    (try_begin),
#      (eq, "$g_dplmc_battle_continuation", 0),
#      (assign, ":num_allies", 0),
#      (try_for_agents, ":agent"),
#       (agent_is_ally, ":agent"),
#       (agent_is_alive, ":agent"),
#       (val_add, ":num_allies", 1),
#      (try_end),
#      (gt, ":num_allies", 0),
#      (try_begin),
#        (eq, "$g_dplmc_cam_activated", 0),
#        #(store_mission_timer_a, "$g_dplmc_main_hero_fallen_seconds"),
#        (assign, "$g_dplmc_cam_activated", 1),
#        (display_message, "@You have been knocked out by the enemy. Watch your men continue the fight without you or press Tab to retreat."),
#		#gekokujo 3.0 mouselook deathcam no more control message
#        #(display_message, "@To watch the fight you can use 'w, a, s, d, numpad_+/numpad_-' to move and 'numpad_1,2,3,4,6,8' to rotate the cam."),
#      (try_end),
#    (else_try),
#    ##diplomacy end
#    (assign, "$pin_player_fallen", 1),
#    (get_player_agent_no, ":player_agent"),
#    (agent_get_team, ":agent_team", ":player_agent"),
#    (try_begin),
#      (neq, "$attacker_team", ":agent_team"),
#      (neq, "$attacker_team_2", ":agent_team"),
#      (str_store_string, s5, "str_siege_continues"),
#      (call_script, "script_simulate_retreat", 8, 15, 0),
#    (else_try),
#      (str_store_string, s5, "str_retreat"),
#      (call_script, "script_simulate_retreat", 5, 20, 0),
#    (try_end),
#    (assign, "$g_battle_result", -1),
#    (set_mission_result,-1),
#    (call_script, "script_count_mission_casualties_from_agents"),
#    (finish_mission,0),
#    ##diplomacy begin
#    (try_end),
#    ##diplomacy end
#    ])
#gekokujo 3.0 diplomacy deathcam deprecated end

# common_battle_order_panel = (
  # 0, 0, 0, [],
  # [
    # (game_key_clicked, gk_view_orders),
    # ##diplomacy begin
    # (neg|main_hero_fallen),
    # ##diplomacy end
    # (neg|is_presentation_active, "prsnt_battle"),
    # (start_presentation, "prsnt_battle"),
    # ])

# common_battle_order_panel_tick = (
  # 0.1, 0, 0, [],
  # [
    # (is_presentation_active, "prsnt_battle"),
    # (call_script, "script_update_order_panel_statistics_and_map"),
    # ])
common_battle_order_panel =(
  0, 0, ti_once, [],
  [
    (neg|is_presentation_active, "prsnt_mini_map"),
    (start_presentation, "prsnt_mini_map"),
  ])

common_battle_order_panel_tick = (
  0, 0, 0, [],
  [
    (try_begin),
      (neg|is_presentation_active, "prsnt_battle"),
      (neg|is_presentation_active, "prsnt_mini_map"),
      (start_presentation, "prsnt_mini_map"),
    (try_end),
    (try_begin),
      (is_presentation_active, "prsnt_battle"),
      (call_script, "script_update_order_panel_statistics_and_map"),
    (else_try),
      (is_presentation_active, "prsnt_mini_map"),
      (call_script, "script_update_order_panel_map"),
    (try_end),
    ])    

common_battle_inventory = (
  ti_inventory_key_pressed, 0, 0, [],
  [
    (display_message,"str_use_baggage_for_inventory"),
    ])

common_inventory_not_available = (
  ti_inventory_key_pressed, 0, 0,
  [
    (display_message, "str_cant_use_inventory_now"),
    ], [])

common_siege_init_ai_and_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_siege_init_ai_and_belfry"),
    ], [])

common_siege_move_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_cf_siege_move_belfry"),
    ], [])

common_siege_rotate_belfry = (
  0, 2, ti_once,
  [
    (call_script, "script_cf_siege_rotate_belfry_platform"),
    ],
  [
    (assign, "$belfry_positioned", 3),
    ])

common_siege_assign_men_to_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_cf_siege_assign_men_to_belfry"),
    ], [])


tournament_triggers = [
  (ti_before_mission_start, 0, 0, [], [
      #gekokujo 3.0 arena spectators start
	  (try_for_range, ":spectator", 40, 50),
		(store_random_in_range, ":spectator_troop", 0, 8),
		(try_begin),
		  (eq, ":spectator_troop", 0),
		  (assign, ":spectator_troop", "trp_novice_fighter"),
		(else_try),
		  (eq, ":spectator_troop", 1),
		  (assign, ":spectator_troop", "trp_regular_fighter"),
		(else_try),
		  (eq, ":spectator_troop", 2),
		  (assign, ":spectator_troop", "trp_veteran_fighter"),
		(else_try),
		  (eq, ":spectator_troop", 3),
		  (assign, ":spectator_troop", "trp_novice_fighter"),
		(else_try),
		  (eq, ":spectator_troop", 4),
		  (assign, ":spectator_troop", "trp_onnabushi"),
		(else_try),
		  (eq, ":spectator_troop", 5),
		  (assign, ":spectator_troop", "trp_onnabushi_trained"),
		(else_try),
		  (eq, ":spectator_troop", 6),
		  (assign, ":spectator_troop", "trp_onnabushi_veteran"),
		(else_try),
		  (assign, ":spectator_troop", "trp_onnabushi_elite"),
		(try_end),
		(set_visitor, ":spectator", ":spectator_troop"),
	  (try_end),
      #gekokujo 3.0 arena spectators end
      (call_script, "script_change_banners_and_chest"),
      (assign, "$g_arena_training_num_agents_spawned", 0)
    ]),
	
  #gekokujo 3.0 everyone gets a pair of tabi in the arena, even though they ought to be barefoot
  (ti_on_agent_spawn, 0, 0, [], [
      (try_for_agents, ":agent_no"),
	    (agent_equip_item, ":agent_no", "itm_gekokujo_tabi"),
      (try_end),
    ]),
	
  (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
  
  (ti_tab_pressed, 0, 0, [],
   [(try_begin),
      (eq, "$g_mt_mode", abm_visit),
      (set_trigger_result, 1),
    (else_try),
      (question_box,"str_give_up_fight"),
    (try_end),
    ]),
	
  (ti_question_answered, 0, 0, [],
   [(store_trigger_param_1,":answer"),
    (eq,":answer",0),
    (try_begin),
      (eq, "$g_mt_mode", abm_tournament),
      (call_script, "script_end_tournament_fight", 0),
    (else_try),
      (eq, "$g_mt_mode", abm_training),
      (get_player_agent_no, ":player_agent"),
      (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),#use this for conversation
    (try_end),
    (finish_mission,0),
    ]),

  #(ti_after_mission_start, 5, ti_once, [], [
  (1, 0, ti_once, [], [
      (eq, "$g_mt_mode", abm_visit),
      (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
      (store_current_scene, reg(1)),
      (scene_set_slot, reg(1), slot_scene_visited, 1),
      (mission_enable_talk),
      #(get_player_agent_no, ":player_agent"),
      (assign, ":team_set", 0),
      (try_for_agents, ":agent_no"),
		#gekokujo 3.0 arena spectator half-assed hack (sigh) start
        #(neq, ":agent_no", ":player_agent"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        #(is_between, ":troop_id", regular_troops_begin, regular_troops_end),
		(eq, ":troop_id", "trp_stupid_asshole"),
		#gekokujo 3.0 arena spectator half-assed hack (sigh) end
        (eq, ":team_set", 0),
        (agent_set_team, ":agent_no", 1),
        (assign, ":team_set", 1),
      (try_end),
    ]),
##
##  (0, 0, 0, [],
##   [
##      #refresh hit points for arena visit trainers
##      (eq, "$g_mt_mode", abm_visit),
##      (get_player_agent_no, ":player_agent"),
##      (try_for_agents, ":agent_no"),
##        (neq, ":agent_no", ":player_agent"),
##        (agent_get_troop_id, ":troop_id", ":agent_no"),
##        (is_between, ":troop_id", regular_troops_begin, regular_troops_end),
##        (agent_set_hit_points, ":agent_no", 100),
##      (try_end),
##    ]),
  
##      (1, 4, ti_once, [(eq, "$g_mt_mode", abm_fight),
##                       (this_or_next|main_hero_fallen),
##                       (num_active_teams_le,1)],
##       [
##           (try_begin),
##             (num_active_teams_le,1),
##             (neg|main_hero_fallen),
##             (assign,"$arena_fight_won",1),
##             #Fight won, decrease odds
##             (assign, ":player_odds_sub", 0),
##             (try_begin),
##               (ge,"$arena_bet_amount",1),
##               (store_div, ":player_odds_sub", "$arena_win_amount", 2),
##             (try_end),
##             (party_get_slot, ":player_odds", "$g_encountered_party", slot_town_player_odds),
##             (val_add, ":player_odds_sub", 5),
##             (val_sub, ":player_odds", ":player_odds_sub"),
##             (val_max, ":player_odds", 250),
##             (party_set_slot, "$g_encountered_party", slot_town_player_odds, ":player_odds"),
##           (else_try),
##             #Fight lost, increase odds
##             (assign, ":player_odds_add", 0),
##             (try_begin),
##               (ge,"$arena_bet_amount",1),
##               (store_div, ":player_odds_add", "$arena_win_amount", 2),
##             (try_end),
##             (party_get_slot, ":player_odds", "$g_encountered_party", slot_town_player_odds),
##             (val_add, ":player_odds_add", 5),
##             (val_add, ":player_odds", ":player_odds_add"),
##             (val_min, ":player_odds", 4000),
##             (party_set_slot, "$g_encountered_party", slot_town_player_odds, ":player_odds"),
##           (try_end),
##           (store_remaining_team_no,"$arena_winner_team"),
##           (assign, "$g_mt_mode", abm_visit),
##           (party_get_slot, ":arena_mission_template", "$current_town", slot_town_arena_template),
##           (set_jump_mission, ":arena_mission_template"),
##           (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
##           (modify_visitors_at_site, ":arena_scene"),
##           (reset_visitors),
##           (set_visitor, 35, "trp_veteran_fighter"),
##           (set_visitor, 36, "trp_hired_warrior_veteran"),
##           (set_jump_entry, 50),
##           (jump_to_scene, ":arena_scene"),
##           ]),
  
  (0, 0, ti_once, [],
   [
     (eq, "$g_mt_mode", abm_tournament),
     (play_sound, "snd_arena_ambiance", sf_looping),
     (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
     ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_tournament),
                   (this_or_next|main_hero_fallen),
                   (num_active_teams_le, 1)],
   [
       (try_begin),
         (neg|main_hero_fallen),
         (call_script, "script_end_tournament_fight", 1),
         (call_script, "script_play_victorious_sound"),
         (finish_mission),
       (else_try),
         (call_script, "script_end_tournament_fight", 0),
         (finish_mission),
       (try_end),
       ]),

  (ti_battle_window_opened, 0, 0, [], [(eq, "$g_mt_mode", abm_training),(start_presentation, "prsnt_arena_training")]),
  
  (0, 0, ti_once, [], [(eq, "$g_mt_mode", abm_training),
                       (assign, "$g_arena_training_max_opponents", 40),
                       (assign, "$g_arena_training_num_agents_spawned", 0),
                       (assign, "$g_arena_training_kills", 0),
                       (assign, "$g_arena_training_won", 0),
                       (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
                       ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_training),
                   (store_mission_timer_a, ":cur_time"),
                   (gt, ":cur_time", 3),
                   (assign, ":win_cond", 0),
                   (try_begin),
                     (ge, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),#spawn at most 40 agents
                     (num_active_teams_le, 1),
                     (assign, ":win_cond", 1),
                   (try_end),
                   (this_or_next|eq, ":win_cond", 1),
                   (main_hero_fallen)],
   [
       (get_player_agent_no, ":player_agent"),
       (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),#use this for conversation
       (assign, "$g_arena_training_won", 0),
       (try_begin),
         (neg|main_hero_fallen),
         (assign, "$g_arena_training_won", 1),#use this for conversation
       (try_end),
       (assign, "$g_mt_mode", abm_visit),
       (set_jump_mission, "mt_arena_melee_fight"),
       (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
       (modify_visitors_at_site, ":arena_scene"),
       (reset_visitors),
	   #gekokujo 3.0 arena spectator half-assed hack (sigh) start
       #(set_visitor, 35, "trp_veteran_fighter"),
       #(set_visitor, 36, "trp_hired_warrior_veteran"),
	   (store_random_in_range, ":fighter_1", 16, 24),
	   (store_random_in_range, ":fighter_2", 24, 32),
       (set_visitor, ":fighter_1", "trp_stupid_asshole"),
       (set_visitor, ":fighter_2", "trp_stupid_asshole"),
	   #gekokujo 3.0 arena spectator half-assed hack (sigh) end
       (set_jump_entry, 50),
       (jump_to_scene, ":arena_scene"),
       ]),


  (0.2, 0, 0,
   [
       (eq, "$g_mt_mode", abm_training),
       (assign, ":num_active_fighters", 0),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 ,7),
         (val_add, ":num_active_fighters", 1),
       (try_end),
       (lt, ":num_active_fighters", 7),
       (neg|main_hero_fallen),
       (store_mission_timer_a, ":cur_time"),
       (this_or_next|ge, ":cur_time", "$g_arena_training_next_spawn_time"),
       (this_or_next|lt, "$g_arena_training_num_agents_spawned", 6),
       (num_active_teams_le, 1),
       (lt, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),
      ],
    [
       (assign, ":added_troop", "$g_arena_training_num_agents_spawned"),
       (store_div,  ":added_troop", "$g_arena_training_num_agents_spawned", 6),
       (assign, ":added_troop_sequence", "$g_arena_training_num_agents_spawned"),
       (val_mod, ":added_troop_sequence", 6),
       (val_add, ":added_troop", ":added_troop_sequence"),
       (val_min, ":added_troop", 9),
       (val_add, ":added_troop", "trp_arena_training_fighter_1"),
       (assign, ":end_cond", 10000),
       (get_player_agent_no, ":player_agent"),
       (agent_get_position, pos5, ":player_agent"),
       (try_for_range, ":unused", 0, ":end_cond"),
         (store_random_in_range, ":random_entry_point", 32, 40),
         (neq, ":random_entry_point", "$g_player_entry_point"), # make sure we don't overwrite player
         (entry_point_get_position, pos1, ":random_entry_point"),
         (get_distance_between_positions, ":dist", pos5, pos1),
         (gt, ":dist", 900), #must be at least 9 meters away from the player
         (assign, ":end_cond", 0),
       (try_end),
       (add_visitors_to_current_scene, ":random_entry_point", ":added_troop", 1),
       (store_add, ":new_spawned_count", "$g_arena_training_num_agents_spawned", 1),
       (store_mission_timer_a, ":cur_time"),
       (store_add, "$g_arena_training_next_spawn_time", ":cur_time", 14),
       (store_div, ":time_reduction", ":new_spawned_count", 3),
       (val_sub, "$g_arena_training_next_spawn_time", ":time_reduction"),
       ]),

  (0, 0, 0,
   [
       (eq, "$g_mt_mode", abm_training)
       ],
    [
       (assign, ":max_teams", 6),
       (val_max, ":max_teams", 1),
       (get_player_agent_no, ":player_agent"),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_slot_eq, ":agent_no", slot_agent_arena_team_set, 0),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 ,7),
         (try_begin),
           (eq, ":agent_no", ":player_agent"),
           (agent_set_team, ":agent_no", 6), #player is always team 6.
         (else_try),
           (store_random_in_range, ":selected_team", 0, ":max_teams"),
          # find strongest team
           (try_for_range, ":t", 0, 6),
             (troop_set_slot, "trp_temp_array_a", ":t", 0),
           (try_end),
           (try_for_agents, ":other_agent_no"),
             (agent_is_human, ":other_agent_no"),
             (agent_is_alive, ":other_agent_no"),
             (neq, ":agent_no", ":player_agent"),
             (agent_slot_eq, ":other_agent_no", slot_agent_arena_team_set, 1),
             (agent_get_team, ":other_agent_team", ":other_agent_no"),
             (troop_get_slot, ":count", "trp_temp_array_a", ":other_agent_team"),
             (val_add, ":count", 1),
             (troop_set_slot, "trp_temp_array_a", ":other_agent_team", ":count"),
           (try_end),
           (assign, ":strongest_team", 0),
           (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", 0),
           (try_for_range, ":t", 1, 6),
             (troop_slot_ge, "trp_temp_array_a", ":t", ":strongest_team_count"),
             (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", ":t"),
             (assign, ":strongest_team", ":t"),
           (try_end),
           (store_random_in_range, ":rand", 5, 100),
           (try_begin),
             (lt, ":rand", "$g_arena_training_num_agents_spawned"),
             (assign, ":selected_team", ":strongest_team"),
           (try_end),
           (agent_set_team, ":agent_no", ":selected_team"),
         (try_end),
         (agent_set_slot, ":agent_no", slot_agent_arena_team_set, 1),
         (try_begin),
           (neq, ":agent_no", ":player_agent"),
           (val_add, "$g_arena_training_num_agents_spawned", 1),
         (try_end),
       (try_end),
       ]),
  ]


##split modules begin
from module_mission_templates_town_village import mission_templates_town_village
from module_mission_templates_siege import mission_templates_siege
from module_mission_templates_field_battle import mission_templates_field_battle
from module_mission_templates_arena_training import mission_templates_arena_training
from module_mission_templates_tutorial import mission_templates_tutorial
from module_mission_templates_multiplayer import mission_templates_multiplayer
from module_mission_templates_core_misc import mission_templates_core_misc
##split modules end

mission_templates = mission_templates_town_village + mission_templates_siege + mission_templates_field_battle + mission_templates_arena_training + mission_templates_tutorial + mission_templates_multiplayer + mission_templates_core_misc

# modmerger_start version=201 type=4
try:
    component_name = "mission_templates"
    var_set = { "mission_templates":mission_templates,"multiplayer_server_check_belfry_movement":multiplayer_server_check_belfry_movement,"multiplayer_server_spawn_bots":multiplayer_server_spawn_bots,"multiplayer_server_manage_bots":multiplayer_server_manage_bots,"multiplayer_server_check_polls":multiplayer_server_check_polls,"multiplayer_server_check_end_map":multiplayer_server_check_end_map,"multiplayer_once_at_the_first_frame":multiplayer_once_at_the_first_frame,"multiplayer_battle_window_opened":multiplayer_battle_window_opened,"common_battle_mission_start":common_battle_mission_start,"common_battle_tab_press":common_battle_tab_press,"common_battle_init_banner":common_battle_init_banner,"common_arena_fight_tab_press":common_arena_fight_tab_press,"common_custom_battle_tab_press":common_custom_battle_tab_press,"custom_battle_check_victory_condition":custom_battle_check_victory_condition,"custom_battle_check_defeat_condition":custom_battle_check_defeat_condition,"common_battle_victory_display":common_battle_victory_display,"common_siege_question_answered":common_siege_question_answered,"common_custom_battle_question_answered":common_custom_battle_question_answered,"common_custom_siege_init":common_custom_siege_init,"common_siege_init":common_siege_init,"common_music_situation_update":common_music_situation_update,"common_siege_ai_trigger_init":common_siege_ai_trigger_init,"common_siege_ai_trigger_init_2":common_siege_ai_trigger_init_2,"common_siege_ai_trigger_init_after_2_secs":common_siege_ai_trigger_init_after_2_secs,"common_siege_defender_reinforcement_check":common_siege_defender_reinforcement_check,"common_siege_defender_reinforcement_archer_reposition":common_siege_defender_reinforcement_archer_reposition,"common_siege_attacker_reinforcement_check":common_siege_attacker_reinforcement_check,"common_siege_attacker_do_not_stall":common_siege_attacker_do_not_stall,"common_battle_check_friendly_kills":common_battle_check_friendly_kills,"common_battle_check_victory_condition":common_battle_check_victory_condition,"common_battle_victory_display":common_battle_victory_display,"common_siege_refill_ammo":common_siege_refill_ammo,"common_siege_check_defeat_condition":common_siege_check_defeat_condition,"common_battle_order_panel":common_battle_order_panel,"common_battle_order_panel_tick":common_battle_order_panel_tick,"common_battle_inventory":common_battle_inventory,"common_inventory_not_available":common_inventory_not_available,"common_siege_init_ai_and_belfry":common_siege_init_ai_and_belfry,"common_siege_move_belfry":common_siege_move_belfry,"common_siege_rotate_belfry":common_siege_rotate_belfry,"common_siege_assign_men_to_belfry":common_siege_assign_men_to_belfry,"tournament_triggers":tournament_triggers, }
    from modmerger import modmerge
    modmerge(var_set, component_name)
except:
    raise
# modmerger_end
