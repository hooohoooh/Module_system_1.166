# ============================================================
# IRONSIGHT CODE COLLECTION
# Source: Mount & Blade: Between Republics mod
# ============================================================

# ============================================================
# iron_sight_runtime (module_mission_templates.py:711-797)
# Main runtime logic for ironsight mode
# ============================================================
iron_sight_runtime = (
0, 0, 0, [], [
#(display_message, "@debug iron_sight_runtime begin"),
(eq, "$ironsight_enabled", 1),
(get_player_agent_no, ":player"),
(agent_get_wielded_item, ":item", ":player"),
(agent_get_animation, ":animation", ":player", 1),
	(try_begin),
	(this_or_next|eq, ":animation", "anim_bolt_shot_straightpull"),
	(this_or_next|eq, ":animation", "anim_bolt_action_shot"),
	(this_or_next|eq, ":animation", "anim_release_crossbow"),
	(this_or_next|eq, ":animation", "anim_release_musket"),
	(this_or_next|eq, ":animation", "anim_ready_crossbow"),
	(eq, ":animation", "anim_ready_musket"),
	(is_camera_in_first_person),
	(neg|game_key_clicked, gk_cam_toggle),
		(try_begin),
		(eq, "$ironsight_mode", 0),
		(assign, "$ironsight_mode", 1),
		(assign, "$ironsight_timer", 4),
		(assign, "$ironsight_timer2", 9999999),
		(assign, "$ironsight_aux", 0),
		(assign, "$ironsight_aux2", 0),
		(try_end),
	(else_try),
	(eq, "$ironsight_mode", 1),
	(assign, "$ironsight_mode", 0),
	(mission_cam_set_mode, 0, 300, 0),
	(try_end),
	(try_begin),
	(eq, "$ironsight_mode", 1),
		(try_begin),
		(gt, "$ironsight_timer", 0),
			(try_begin),
			(eq, "$ironsight_aux2", 1),
			(assign, "$ironsight_aux2", 0),
			(mission_cam_set_mode, 0, 300, 0),
			(try_end),
		(else_try),
			(try_begin),
			(eq, "$ironsight_aux2", 0),
			(assign, "$ironsight_aux2", 1),
			(mission_cam_set_mode, 1, 0, 0),
			(try_end),
		(this_or_next|eq, ":animation", "anim_bolt_shot_straightpull"),
		(this_or_next|eq, ":animation", "anim_lever_action_shot"),
		(eq, ":animation", "anim_bolt_action_shot"),
		(agent_get_bone_position, pos1, ":player", 14, 1),
		(position_rotate_y, pos1, -90),
		(position_move_y, pos1, -44),
		(position_move_z, pos1, 9),
		(mission_cam_set_position, pos1),
		(else_try),
		(agent_get_bone_position, pos1, ":player", 19, 1),
		(position_rotate_y, pos1, -90),
		(position_move_y, pos1, -10),
		(position_move_z, pos1, 9),
			(try_begin),
			(is_between, ":item", "itm_lmg_lewis", "itm_lmg_hotchkiss1909_m"),
			(position_move_z, pos1, 5, 0),
			(try_end),
		(mission_cam_set_position, pos1),
		(try_end),
		(try_begin),
		(this_or_next|eq, ":animation", "anim_bolt_shot_straightpull"),
		(this_or_next|eq, ":animation", "anim_lever_action_shot"),
		(eq, ":animation", "anim_bolt_action_shot"),
			(try_begin),
			(eq, "$ironsight_aux", 0),
			(assign, "$ironsight_aux", 1),
			(assign, "$ironsight_timer2", 3),
			(try_end),
		(else_try),
		(assign, "$ironsight_aux", 0),
		(val_clamp, "$ironsight_timer", 0, 5),
		(try_end),
		(try_begin),
		(this_or_next|eq, ":animation", "anim_bolt_shot_straightpull"),
		(this_or_next|eq, ":animation", "anim_lever_action_shot"),
		(eq, ":animation", "anim_bolt_action_shot"),
		(eq, "$ironsight_timer2", 0),
		(assign, "$ironsight_timer", 14),
		(assign, "$ironsight_timer2", 9999999),
		(try_end),
	(try_end),
#(display_message, "@debug iron_sight_runtime end"),
])

# ============================================================
# iron_sight_100ms (module_mission_templates.py:799-812)
# Timer decrement logic for ironsight
# ============================================================
iron_sight_100ms = (
0.1, 0, 0, [],
[
#(display_message, "@debug iron_sight_100ms begin"),
	(try_begin),
	(gt, "$ironsight_timer", 0),
	(val_sub, "$ironsight_timer", 1),
	(try_end),
	(try_begin),
	(gt, "$ironsight_timer2", 0),
	(val_sub, "$ironsight_timer2", 1),
	(try_end),
#(display_message, "@debug iron_sight_100ms end"),
])

# ============================================================
# player_accuracy_modifier (module_mission_templates.py:1801-1815)
# Accuracy modifier based on ironsight mode
# ============================================================
player_accuracy_modifier = (
0, 0, 0, [],
[
#(display_message, "@debug player_accuracy_modifier begin"),
(get_player_agent_no, ":player"),
(agent_is_active, ":player"),
(agent_is_alive, ":player"),
	(try_begin),
	(eq, "$ironsight_mode", 1),
	(agent_set_accuracy_modifier, ":player", 500),
	(else_try),
	(agent_set_accuracy_modifier, ":player", 85),
	(try_end),
#(display_message, "@debug player_accuracy_modifier end"),
])

# ============================================================
# Iron Sight Menu Action (module_game_menus.py:3110-3122)
# Camp menu option to toggle ironsight mode
# ============================================================
# ("enable_ironsight",
#  [], "Toggle ironsight mode.",
#  [
iron_sight_menu_action = [
	(try_begin),
	(eq, "$ironsight_enabled", 1),
	(assign, "$ironsight_enabled", 0),
	(display_message, "@Ironsight mode disabled."),
	(else_try),
	(assign, "$ironsight_enabled", 1),
	(display_message, "@Ironsight mode enabled."),
	(try_end),
]
#  ])

# ============================================================
# Initialization (module_scripts.py:76-77)
# Initial values for ironsight variables
# ============================================================
iron_sight_initialization = [
(assign, "$ironsight_enabled", 0),
(assign, "$ironsight_mode", 0),
]

# ============================================================
# Battle Start Reset (module_mission_templates.py:5148)
# Reset ironsight mode at battle start
# ============================================================
battle_start_iron_sight_reset = [
(assign, "$ironsight_mode", 0),
]

# ============================================================
# Crossbow Ironsight Toggle (module_mission_templates.py:2323-2350)
# Crossbow-specific ironsight/firing toggle logic
# Note: This is part of a larger trigger, shown here with full context
# ============================================================
# Parent trigger context (lines 2311-2322):
# (eq, hlod_gunplay, 1),
# (eq, "$aerial_view_state", 0),
# (get_player_agent_no, ":player"),
# (agent_is_active, ":player"),
# (agent_is_alive, ":player"),
# (store_mission_timer_a_msec, ":mission_timer"),
# (agent_set_accuracy_modifier, ":player", 500),              
# (agent_set_slot, ":player", slot_agent_gun_automatic_on, 2),
# (agent_get_wielded_item, ":wornitem", ":player"),
# (is_between, ":wornitem", "itm_tutorial_spear", "itm_fumo_cirno"),
# (item_get_slot, ":rpm", ":wornitem", slot_item_rpm),
# (eq, ":rpm", 0),

crossbow_ironsight_toggle = [
    (try_begin),
       (item_get_type, ":type", ":wornitem"),
       (eq, ":type", itp_type_crossbow),
       (agent_slot_eq, ":player", slot_agent_gun_aim_on, 0),       
	   (game_key_clicked, gk_defend),
       (neg|game_key_is_down, gk_attack),
       (assign, "$ironsight_enabled", 1),       
       (display_message, "@Projectile firing enabled"),  
   	   (agent_set_accuracy_modifier, ":player", 500),              
       (agent_set_slot, ":player", slot_agent_gun_aim_on, 1),
       (try_begin),
        (agent_get_animation, ":aimanim", ":player", 1),
        (assign, ":aimanim", "anim_ready_crossbow"),
        (agent_set_animation, ":player", ":aimanim", 1),   
       (try_end),
    (else_try),
       (agent_slot_eq, ":player", slot_agent_gun_aim_on, 1), 
	   (game_key_clicked, gk_defend),
       (neg|game_key_is_down, gk_attack),
       (assign, "$ironsight_enabled", 0),
       (mission_cam_set_mode, 0, 300, 0),       
       (display_message, "@Projectile firing disabled"),
   	   (agent_set_accuracy_modifier, ":player", 500),              
       (agent_set_slot, ":player", slot_agent_gun_aim_on, 0), 
       (agent_set_animation, ":player", "anim_YuriCancelAnimation", 1),
       (agent_set_slot, ":player", slot_agent_gun_automatic_on, 2),       
    (else_try),
       (agent_get_ammo, ":ammo", ":player", 1),    
	   (gt, ":ammo", 0),    
       (agent_slot_eq, ":player", slot_agent_gun_aim_on, 0),
       (gt, ":mission_timer", 1650),
       (game_key_is_down, gk_attack), 
       (assign, "$ignore_script_game_missile_launch", 0),              
       (agent_get_bone_position, pos10, ":player", 18, 1),
       (agent_get_look_position, pos11, ":player"),
       (position_copy_rotation, pos10, pos11),
    (try_end),
]

# ============================================================
# Slot Constants (module_constants.py)
# ============================================================
# slot_item_aim_loop_animation (module_constants.py:706, 712)
slot_item_aim_loop_animation = 43

# slot_agent_gun_aim_on (module_constants.py:794)
slot_agent_gun_aim_on = 47

# slot_agent_gun_automatic_on (module_constants.py:795)
slot_agent_gun_automatic_on = 48