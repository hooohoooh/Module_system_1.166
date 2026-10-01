# -*- coding: UTF-8 -*-
# split feature file: simple_triggers - module
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end
from module_constants import *

simple_triggers_economy_trade = [
	
(24, 
[
    (try_for_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
      (faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),

	  (store_sub, ":divisor", 140, "$player_right_to_rule"),
	  (val_div, ":divisor", 14),
	  (val_max, ":divisor", 1),
	  
      (store_div, ":faction_morale_div_10", ":faction_morale", ":divisor"), #10 is the base, down to 2 for 100 rtr     
      (val_sub, ":faction_morale", ":faction_morale_div_10"),           

      (faction_set_slot, ":kingdom_no",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),
]),
  #Pay day.
  (24 * 7,
   [
     ##diplomacy begin
     (store_current_hours, "$g_next_pay_time"),
     (val_add, "$g_next_pay_time", 24 * 7),
     ##diplomacy end
     (assign, "$g_presentation_lines_to_display_begin", 0),
     (assign, "$g_presentation_lines_to_display_end", 15),
     (assign, "$g_apply_budget_report_to_gold", 1),
     (try_begin),
       (eq, "$g_infinite_camping", 0),
       (start_presentation, "prsnt_budget_report"),
        ##diplomacy begin
        (try_begin),
          (gt, "$g_player_debt_to_party_members", 5000),
          (call_script, "script_add_notification_menu", "mnu_dplmc_deserters",20,0),
        (try_end),
        ##diplomacy end
     (try_end),
    ]),
  # Oath fulfilled -- ie, mercenary contract expired?
  (24,
   [
      (le, "$auto_menu", 0),
      (gt, "$players_kingdom", 0),
      (neq, "$players_kingdom", "fac_player_supporters_faction"),
      (eq, "$player_has_homage", 0),
	  
	  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	  
	  #A player bound to a kingdom by marriage will not have the contract expire. This should no longer be the case, as I've counted wives as having homage, but is in here as a fallback
	  (assign, ":player_has_marriage_in_faction", 0),
	  (try_begin),
		(is_between, ":player_spouse", active_npcs_begin, active_npcs_end),
		(store_faction_of_troop, ":spouse_faction", ":player_spouse"),
		(eq, ":spouse_faction", "$players_kingdom"),
	    (assign, ":player_has_marriage_in_faction", 1),
	  (try_end),
	  (eq, ":player_has_marriage_in_faction", 0),
	  
      (store_current_day, ":cur_day"),
      (gt, ":cur_day", "$mercenary_service_next_renew_day"),
      (jump_to_menu, "mnu_oath_fulfilled"),
    ]),
  # Party Morale: Move morale towards target value.
  (24,
   [
      (call_script, "script_get_player_party_morale_values"),
      (assign, ":target_morale", reg0),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (store_sub, ":dif", ":target_morale", ":cur_morale"),
      (store_div, ":dif_to_add", ":dif", 5),
      (store_mul, ":dif_to_add_correction", ":dif_to_add", 5),
      (try_begin),#finding ceiling of the value
        (neq, ":dif_to_add_correction", ":dif"),
        (try_begin),
          (gt, ":dif", 0),
          (val_add, ":dif_to_add", 1),
        (else_try),
          (val_sub, ":dif_to_add", 1),
        (try_end),
      (try_end),
      (val_add, ":cur_morale", ":dif_to_add"),
      (party_set_morale, "p_main_party", ":cur_morale"),      
    ]),
  #Adding net incomes to heroes (once a week)
  #Increasing debts to heroes by 1% (once a week)
  #Adding net incomes to centers (once a week)
  (24*7,
   [
		##diplomacy start+ Save register
		(assign, ":save_reg0", reg0),
		##Change to support kingdom ladies
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	   (try_for_range, ":troop_no", heroes_begin, heroes_end),
	     (this_or_next|is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	   ##diplomacy end+
         (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),#Increasing debt
         (val_mul, ":cur_debt", 101),
         (val_div, ":cur_debt", 100),
         (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
         (call_script, "script_calculate_hero_weekly_net_income_and_add_to_wealth", ":troop_no"),#Adding net income
       (try_end),

	   ##diplomacy start+
	   (store_current_hours, ":two_weeks_ago"),
	   (val_sub, ":two_weeks_ago", 24 * 14),
	   ##diplomacy end+

       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         #If non-player center, adding income to wealth
         (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
		 ##diplomacy start+
		 #Defer the ownership check so attrition can still occur for unowned centers.
		 #Give a slight grace period first, though.
		 (neg|party_slot_eq, ":center_no", slot_town_lord, 0),
		 (this_or_next|party_slot_ge, ":center_no", dplmc_slot_center_last_transfer_time, ":two_weeks_ago"),
			(party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
		 (this_or_next|ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 ##diplomacy end+
		 (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
         (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
         (store_mul, ":added_wealth", ":prosperity", 15),
         (val_add, ":added_wealth", 700),
         (try_begin),
           (party_slot_eq, ":center_no", slot_party_type, spt_town),
           (val_mul, ":added_wealth", 3),
           (val_div, ":added_wealth", 2),
         (try_end),
         (val_add, ":cur_wealth", ":added_wealth"),
         (call_script, "script_calculate_weekly_party_wage", ":center_no"),
         (val_sub, ":cur_wealth", reg0),
		 ##diplomacy start+ Allow attrition to occur
		 (try_begin),
			(lt, ":cur_wealth", 0),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
			(assign, ":cur_weekly_wage", reg0),
			(store_party_size_wo_prisoners, ":garrison_size", ":center_no"),
			(call_script, "script_party_get_ideal_size", ":center_no"),#This script has been modified to support this use
			(val_mul, reg0, 5),
			(val_div, reg0, 4),
			(ge, ":garrison_size", reg0),

			(store_sub, ":percent_under", 0, ":cur_wealth"),
			(val_mul, ":percent_under", 100),
			(val_div, ":percent_under", ":cur_weekly_wage"),
			(val_div, ":percent_under", 5), #Max 20 percent (won't take garrison below ideal size)
			(call_script, "script_party_inflict_attrition", ":center_no", ":percent_under", 1),
		 (try_end),
		 (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
		 ##diplomacy end+
         (val_max, ":cur_wealth", 0),
         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
       (try_end),
	   ##diplomacy end+
	   (assign, reg0, ":save_reg0"),
	   ##diplomacy end+
    ]),
  #Hiring men with hero wealths (once a day)
  #Hiring men with center wealths (once a day)
  (24,
   [
     ##diplomacy start+
     ##change to allow promoted kingdom ladies to hire troops
     #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
     (try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
     ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (ge, ":party_no", 1),
       (party_is_active, ":party_no"),
       (party_get_attached_to, ":cur_attached_party", ":party_no"),
       (is_between, ":cur_attached_party", centers_begin, centers_end),
       (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege
                       
       (store_faction_of_party, ":party_faction", ":party_no"),
       (try_begin),
         (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
         (eq, ":party_faction", "$players_kingdom"),        
		 #gekokujo 3.0 more reinforcements start
         (assign, ":num_hiring_rounds", 2), 
         #(assign, ":num_hiring_rounds", 1),  
		 #gekokujo 3.0 more reinforcements end     
         (store_random_in_range, ":random_value", 0, 2),   
         (val_add, ":num_hiring_rounds", ":random_value"),
       (else_try),
         (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
         (try_begin),
           (eq, ":reduce_campaign_ai", 0), #hard (2x reinforcing)
		   #gekokujo 3.0 more reinforcements start
           (assign, ":num_hiring_rounds", 3),
           #(assign, ":num_hiring_rounds", 2),
		   #gekokujo 3.0 more reinforcements end
         (else_try),
           (eq, ":reduce_campaign_ai", 1), #medium (1x or 2x reinforcing)
		   #gekokujo 3.0 more reinforcements start
           (assign, ":num_hiring_rounds", 2), 
           #(assign, ":num_hiring_rounds", 1), 
		   #gekokujo 3.0 more reinforcements end      
           (store_random_in_range, ":random_value", 0, 2),  
           (val_add, ":num_hiring_rounds", ":random_value"),
         (else_try),
           (eq, ":reduce_campaign_ai", 2), #easy (1x reinforcing)
		   #gekokujo 3.0 more reinforcements start
           (assign, ":num_hiring_rounds", 2),      
           #(assign, ":num_hiring_rounds", 1),          
		   #gekokujo 3.0 more reinforcements end
         (try_end),                
       (try_end), 
       
       (try_begin),
         (faction_slot_eq,  ":party_faction", slot_faction_marshall, ":troop_no"),
         (val_add, ":num_hiring_rounds", 1),
       (try_end),
                
       (try_for_range, ":unused", 0, ":num_hiring_rounds"),         
         (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men with current wealth        
       (try_end),  
     (try_end),
       
     (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
       (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
       (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.       
       (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege
		 
       (store_faction_of_party, ":center_faction", ":center_no"),
       (try_begin),
         (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
         (eq, ":center_faction", "$players_kingdom"),        
         (assign, ":reinforcement_cost", reinforcement_cost_moderate),
       (else_try),
         (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
         (assign, ":reinforcement_cost", reinforcement_cost_moderate),
         (try_begin), 
           (eq, ":reduce_campaign_ai", 0), #hard (1x or 2x reinforcing)
           (assign, ":reinforcement_cost", reinforcement_cost_hard),
		   #gekokujo 3.0 more reinforcements start
           #(store_random_in_range, ":num_hiring_rounds", 0, 2),
           #(val_add, ":num_hiring_rounds", 1),
           (store_random_in_range, ":num_hiring_rounds", 0, 4),
           (val_add, ":num_hiring_rounds", 2),
		   #gekokujo 3.0 more reinforcements end
         (else_try), 
           (eq, ":reduce_campaign_ai", 1), #moderate (1x reinforcing)
           (assign, ":reinforcement_cost", reinforcement_cost_moderate),
		   #gekokujo 3.0 more reinforcements start
           #(assign, ":num_hiring_rounds", 1),
           (store_random_in_range, ":num_hiring_rounds", 0, 4),
           (assign, ":num_hiring_rounds", 1),
		   #gekokujo 3.0 more reinforcements end
         (else_try), 
           (eq, ":reduce_campaign_ai", 2), #easy (none or 1x reinforcing)
           (assign, ":reinforcement_cost", reinforcement_cost_easy),
		   #gekokujo 3.0 more reinforcements start
           #(store_random_in_range, ":num_hiring_rounds", 0, 2),
           (store_random_in_range, ":num_hiring_rounds", 0, 4),
		   #gekokujo 3.0 more reinforcements end
         (try_end),           
       (try_end),
       
       (try_for_range, ":unused", 0, ":num_hiring_rounds"), 		 
         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
         (assign, ":hiring_budget", ":cur_wealth"),
         (val_div, ":hiring_budget", 2),
         (gt, ":hiring_budget", ":reinforcement_cost"),       
         (call_script, "script_cf_reinforce_party", ":center_no"),       
         (val_sub, ":cur_wealth", ":reinforcement_cost"),
         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
       (try_end),  
     (try_end),

     #this is moved up from below , from a 24 x 15 slot to a 24 slot
     (try_for_range, ":center_no", centers_begin, centers_end),
       #(neg|is_between, ":center_no", castles_begin, castles_end),
       (store_random_in_range, ":random", 0, 30),
       (le, ":random", 10),
	   
       (call_script, "script_get_center_ideal_prosperity", ":center_no"),
       (assign, ":ideal_prosperity", reg0),
       (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),       
       (try_begin),
	     (eq, ":random", 0), #with 3% probability it will gain +10/-10 prosperity even it has higher prosperity than its ideal prosperity.
         (try_begin),
           (store_random_in_range, ":random", 0, 2),
           (try_begin),
             (eq, ":random", 0),
             (neg|is_between, ":center_no", castles_begin, castles_end), #castles always gain positive prosperity from surprise income to balance their prosperity.
             (call_script, "script_change_center_prosperity", ":center_no", -10),
             (val_add, "$newglob_total_prosperity_from_convergence", -10),
           (else_try),     
             (call_script, "script_change_center_prosperity", ":center_no", 10),
             (val_add, "$newglob_total_prosperity_from_convergence", 10),
           (try_end),
         (try_end),
	   (else_try),
         (gt, ":prosperity", ":ideal_prosperity"),		 
         (call_script, "script_change_center_prosperity", ":center_no", -1),
         (val_add, "$newglob_total_prosperity_from_convergence", -1),
       (else_try),
         (lt, ":prosperity", ":ideal_prosperity"),		 
         (call_script, "script_change_center_prosperity", ":center_no", 1),
         (val_add, "$newglob_total_prosperity_from_convergence", 1),
	   (try_end),
     (try_end),	   	   	   
	 
	 #gekokujo 3.0 microfactions! start
	 #we're hijacking this trigger to refresh forts
	 #when a fort isn't player-owned, the timer represents how long until a suppressed fort has a chance at respawn
	 #an ACTIVE non-player-owned fort should have its timer at -1, since 0 just means it is trying to be active
	 #when a fort is player-owned, the timer represents how long until a player can recruit or produce
	 #player-owned forts are always active
	 (try_for_range, ":center_no", forts_begin, forts_end),
	   #countdown
	   (try_begin),
	     (party_slot_ge, ":center_no", slot_fort_timer, 1), #don't mess with a fort already at 0 (or below)
	     (party_get_slot, ":timer", ":center_no", slot_fort_timer),
		 (val_sub, ":timer", 1),
		 (party_set_slot, ":center_no", slot_fort_timer, ":timer"), #count down by 1
		 ##debug start
		 #(str_store_party_name, s8, ":center_no"),
		 #(assign, reg9, ":timer"),
		 #(display_log_message, "@{s8} Timer: of the {reg9}"),
		 #debug end
	   (try_end),
	   
	   #put out the fire
	   (try_begin),
	     (party_slot_ge, ":center_no", slot_fort_fire, 1), #is there a fire?
		 (party_clear_particle_systems, ":center_no"),
	     (party_set_slot, ":center_no", slot_fort_fire, 0),
		 (try_begin),
		   (party_slot_eq, ":center_no", slot_fort_type, sft_village), #ainu village
		   (party_set_icon, ":center_no", "icon_village_snow_deserted_a"),
		 (else_try),
		   (party_set_icon, ":center_no", "icon_village_deserted_a"),
		 (try_end),
	   (try_end),
	   
	   #restoration
	   (try_begin),
	     (party_slot_eq, ":center_no", slot_fort_timer, 0), #countdown reached 0
	     (party_slot_eq, ":center_no", slot_fort_captured, 0), #the player doesn't own it
		 
		 #restore the icon
		 #(party_set_flags, ":center_no", pf_disabled, 0), 
		 #(party_set_flags, ":center_no", pf_always_visible, 1),
		 (try_begin),
		   (this_or_next|party_slot_eq, ":center_no", slot_fort_type, sft_mansion),
		   (party_slot_eq, ":center_no", slot_fort_type, sft_castle),
		   (party_set_icon, ":center_no", "icon_mansion"),
		 (else_try),
		   (party_slot_eq, ":center_no", slot_fort_type, sft_temple),
		   (party_set_icon, ":center_no", "icon_temple"),
		 (else_try),
		   (party_slot_eq, ":center_no", slot_fort_type, sft_village),
		   (party_set_icon, ":center_no", "icon_village_snow_a"),
		 (try_end),
		 
	     #restores the garrison for newly reactivated forts
		 (try_begin),
		   (party_get_num_companions, ":store_no", ":center_no"),
		   (eq, ":store_no", 0),
		 
		   (try_begin),
		     (party_slot_eq, ":center_no", slot_fort_type, sft_village), #ainu villages don't get mercenaries
		     (store_random_in_range, ":rand_recruits", 15, 62), #15 to 61, so that there will always be at least 15 of each
		     (store_sub, ":rand_bandits", 76, ":rand_recruits"),
		     (assign, ":rand_melee", 0),
		   (else_try),
		     (store_random_in_range, ":rand_recruits", 10, 41), #10 to 40, so that there will always be at least 10 of each
		     (store_sub, ":rand_bandits", 50, ":rand_recruits"),
		     (store_random_in_range, ":rand_melee", 5, 22), #5 to 21, so that there will always be at least 5 of each
		     (store_sub, ":rand_ranged", 26, ":rand_melee"),
		   (try_end),

		   (party_get_slot, ":recruit", ":center_no", slot_fort_recruit_type),
		   (party_get_slot, ":bandit", ":center_no", slot_fort_bandit_type),
		   (party_add_members, ":center_no", ":recruit", ":rand_recruits"),
		   (party_add_members, ":center_no", ":bandit", ":rand_bandits"),

		   (try_begin),
		     (neq, ":rand_melee", 0),
		     (party_add_members, ":center_no", "trp_hired_warrior", ":rand_melee"),
		     (party_add_members, ":center_no", "trp_hired_gunner", ":rand_ranged"),
		   (try_end),
		 (try_end), #end the garrison refresh
	   (try_end), #end the restoration of the fort
	 (try_end),
	 #gekokujo 3.0 microfactions! end
    ]),
  # Refresh merchant inventories
   (168,
   [
      (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
      (try_end),
    ]),
  #Refreshing village defenders
  #Clearing slot_village_player_can_not_steal_cattle flags
   (48,
   [
      (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (party_set_slot, ":village_no", slot_village_player_can_not_steal_cattle, 0),
      (try_end),
    ]),
  # Refresh number of cattle in villages
  (24 * 7,
   [
     (try_for_range, ":village_no", centers_begin, centers_end),
	   (neg|is_between, ":village_no", castles_begin, castles_end),
	   (party_get_slot, ":num_cattle", ":village_no", slot_center_head_cattle),
	   (party_get_slot, ":num_sheep", ":village_no", slot_center_head_sheep),
	   (party_get_slot, ":num_acres", ":village_no", slot_center_acres_pasture),
	   (val_max, ":num_acres", 1),
	   
	   (store_mul, ":grazing_capacity", ":num_cattle", 400),
	   (store_mul, ":sheep_addition", ":num_sheep", 200),
	   (val_add, ":grazing_capacity", ":sheep_addition"),
	   (val_div, ":grazing_capacity", ":num_acres"),
	   
	   (store_random_in_range, ":random_no", 0, 100),
	   (try_begin), #Disaster
	     (eq, ":random_no", 0),#1% chance of epidemic - should happen once every two years
		 (val_min, ":num_cattle", 10),
		 
        (try_begin),
#          (eq, "$cheat_mode", 1),
#          (str_store_party_name, s1, ":village_no"),
#          (display_message, "@{!}Cattle in {s1} are exterminated due to famine."),
           ##diplomacy start+ Add display message for the player's own fiefs
		   #(store_distance_to_party_from_party, ":dist", "p_main_party", ":village_no"),
		   #(this_or_next|lt, ":dist", 30),
	          (gt, "$g_player_chamberlain", 0),
		   (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
		   (party_get_slot, reg4, ":village_no", slot_center_head_cattle),
		   (val_sub, reg4, ":num_cattle"),
		   (gt, reg4, 0),
		   (str_store_party_name_link, s4, ":village_no"),
		   (display_log_message, "@A livestock epidemic has killed {reg4} cattle in {s4}."),
		   ##diplomacy end+
        (try_end),
		 
       (else_try), #Overgrazing
         (gt, ":grazing_capacity", 100),
		
         (val_mul, ":num_sheep", 90), #10% decrease at number of cattles
         (val_div, ":num_sheep", 100),
		
         (val_mul, ":num_cattle", 90), #10% decrease at number of sheeps
         (val_div, ":num_cattle", 100),
		 
       (else_try), #superb grazing
         (lt, ":grazing_capacity", 30),

         (val_mul, ":num_cattle", 120), #20% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (val_add, ":num_cattle", 1),
		
         (val_mul, ":num_sheep", 120), #20% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (val_add, ":num_sheep", 1),
		
       (else_try), #very good grazing
         (lt, ":grazing_capacity", 60),

         (val_mul, ":num_cattle", 110), #10% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (val_add, ":num_cattle", 1),
		
         (val_mul, ":num_sheep", 110), #10% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (val_add, ":num_sheep", 1),

       (else_try), #good grazing
         (lt, ":grazing_capacity", 100),
         (lt, ":random_no", 50),

         (val_mul, ":num_cattle", 105), #5% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (try_begin), #if very low number of cattles and there is good grazing then increase number of cattles also by one
           (le, ":num_cattle", 20),
           (val_add, ":num_cattle", 1),
         (try_end),
		
         (val_mul, ":num_sheep", 105), #5% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (try_begin), #if very low number of sheeps and there is good grazing then increase number of sheeps also by one
           (le, ":num_sheep", 20),
           (val_add, ":num_sheep", 1),
         (try_end),		
       (try_end),

       (party_set_slot, ":village_no", slot_center_head_cattle, ":num_cattle"),
       (party_set_slot, ":village_no", slot_center_head_sheep, ":num_sheep"),	  	  	  
     (try_end),
    ]),
   #Accumulate taxes
   (24 * 7,
   [
      #Adding earnings to town lords' wealths.
      #Moved to troop does business
      #(try_for_range, ":center_no", centers_begin, centers_end),
      #  (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      #  (neq, ":town_lord", "trp_player"),
      #  (is_between, ":town_lord", active_npcs_begin, active_npcs_end),
      #  (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
      #  (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      #  (troop_get_slot, ":troop_wealth", ":town_lord", slot_troop_wealth),
      #  (val_add, ":troop_wealth", ":accumulated_rents"),
      #  (val_add, ":troop_wealth", ":accumulated_tariffs"),
      #  (troop_set_slot, ":town_lord", slot_troop_wealth, ":troop_wealth"),				
      #  (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
      #  (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
      #  (try_begin),
      #    (eq, "$cheat_mode", 1),
      #    (assign, reg1, ":troop_wealth"),
      #    (add_troop_note_from_sreg, ":town_lord", 1, "str_current_wealth_reg1", 0),
      #  (try_end),
      #(try_end),
            
	  #Collect taxes for another week
      (try_for_range, ":center_no", centers_begin, centers_end),
        (try_begin),
          (party_slot_ge, ":center_no", slot_town_lord, 0), #unassigned centers do not accumulate rents	  
        
          (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),		  
		
          (assign, ":cur_rents", 0),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (try_begin),
              (party_slot_eq, ":center_no", slot_village_state, svs_normal),
              (assign, ":cur_rents", 1200),
            (try_end),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_castle),
            (assign, ":cur_rents", 1200),
          (else_try),  
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign, ":cur_rents", 2400),
          (try_end),
		
          (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity), #prosperty changes between 0..100     
          (store_add, ":multiplier", 20, ":prosperity"), #multiplier changes between 20..120
          (val_mul, ":cur_rents", ":multiplier"), 
          (val_div, ":cur_rents", 120),#Prosperity of 100 gives the default values
          
          (try_begin),
            (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            
            (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
            (try_begin),
              (eq, ":reduce_campaign_ai", 0), #hard (less money from rents)
              (val_mul, ":cur_rents", 3),
              (val_div, ":cur_rents", 4),
            (else_try),
              (eq, ":reduce_campaign_ai", 1), #medium (normal money from rents)
              #same
            (else_try),
              (eq, ":reduce_campaign_ai", 2), #easy (more money from rents)
              (val_mul, ":cur_rents", 4),
              (val_div, ":cur_rents", 3),
            (try_end),                
          (try_end),  
                    
          (val_add, ":accumulated_rents", ":cur_rents"), #cur rents changes between 23..1000
          
                    ##diplomacy begin
          (try_begin),
            (str_store_party_name, s6, ":center_no"),

            (party_get_slot, ":tax_rate", ":center_no", dplmc_slot_center_taxation),
            (neq, ":tax_rate", 0),
            (store_div, ":rent_change", ":accumulated_rents", 100),
            (val_mul, ":rent_change", ":tax_rate"),

            (try_begin), #debug
              (eq, "$cheat_mode", 1),
              (assign, reg0, ":tax_rate"),
              (display_message, "@{!}DEBUG : tax rate in {s6}: {reg0}"),
              (assign, reg0, ":accumulated_rents"),
              (display_message, "@{!}DEBUG : accumulated_rents  in {s6}: {reg0}"),
              (assign, reg0, ":rent_change"),
              (display_message, "@{!}DEBUG : rent_change in {s6}: {reg0}  in {s6}"),
            (try_end),

            (val_add, ":accumulated_rents", ":rent_change"),

            (val_div, ":tax_rate", -25),

            (call_script, "script_change_center_prosperity", ":center_no", ":tax_rate"),

            (try_begin),
              (lt, ":tax_rate", 0), #double negative values
              (val_mul, ":tax_rate", 2),

              (try_begin), #debug
                (eq, "$cheat_mode", 1),
                (assign, reg0, ":tax_rate"),
                (display_message, "@{!}DEBUG : tax rate after modi in {s6}: {reg0}"),
              (try_end),

              (try_begin),
                (this_or_next|is_between, ":center_no", villages_begin, villages_end),
                (is_between, ":center_no", towns_begin, towns_end),
                (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),

                (try_begin), #debug
                  (eq, "$cheat_mode", 1),
                  (assign, reg0, ":center_relation"),
                  (display_message, "@{!}DEBUG : center relation: {reg0}"),
                (try_end),

                (le, ":center_relation", -5),
                (store_random_in_range, ":random",-100, 0),
                (gt, ":random", ":center_relation"),

                (neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
                (display_message, "@Riot in {s6}!"),
                (party_set_slot, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"), #trp_peasant_woman used to simulate riot
                (call_script, "script_change_center_prosperity", ":center_no", -1),
                (call_script, "script_add_notification_menu", "mnu_dplmc_notification_riot", ":center_no", 0),

                #add additional troops
                (store_character_level, ":player_level", "trp_player"),
                (store_div, ":player_leveld2", ":player_level", 2),
                (store_mul, ":player_levelx2", ":player_level", 2),
                (try_begin),
                  (is_between, ":center_no", villages_begin, villages_end),
                  (store_random_in_range, ":random",0, ":player_level"),
                  (party_add_members, ":center_no", "trp_hired_warrior", ":random"),
                  (store_random_in_range, ":random", 0, ":player_leveld2"),
                  (party_add_members, ":center_no", "trp_hired_warrior_veteran", ":random"),
                (else_try),
                  (party_set_banner_icon, ":center_no", 0),
                  (party_get_num_companion_stacks, ":num_stacks",":center_no"),
                  (try_for_range, ":i_stack", 0, ":num_stacks"),
                    (party_stack_get_size, ":stack_size",":center_no",":i_stack"),
                    (val_div, ":stack_size", 2),
                    (party_stack_get_troop_id, ":troop_id", ":center_no", ":i_stack"),
                    (party_remove_members, ":center_no", ":troop_id", ":stack_size"),
                  (try_end),
                  (store_random_in_range, ":random",":player_leveld2", ":player_levelx2"),
                  (party_add_members, ":center_no", "trp_townsman", ":random"),
                  (store_random_in_range, ":random",0, ":player_level"),
                  (party_add_members, ":center_no", "trp_hired_guard", ":random"),
                (try_end),
              (end_try),
            (try_end),
            (call_script, "script_change_player_relation_with_center", ":center_no", ":tax_rate"),
          (try_end),

          (try_begin), #no taxes for infested villages and towns
            (party_slot_ge, ":center_no", slot_village_infested_by_bandits, 1),
            (assign,":accumulated_rents", 0),
          (try_end),
          ##diplomacy end
          
          (party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
        (try_end),
        
		(try_begin),
		  (is_between, ":center_no", villages_begin, villages_end),
		  (party_get_slot, ":bound_castle", ":center_no", slot_village_bound_center),
		  (party_slot_ge, ":bound_castle", slot_town_lord, 0), #unassigned centers do not accumulate rents	  
		  (is_between, ":bound_castle", castles_begin, castles_end),
		  (party_get_slot, ":accumulated_rents", ":bound_castle", slot_center_accumulated_rents), #castle's accumulated rents
		  (val_add, ":accumulated_rents", ":cur_rents"), #add village's rent to castle rents
		  (party_set_slot, ":bound_castle", slot_center_accumulated_rents, ":accumulated_rents"),
		(try_end),		
      (try_end),
    ]),
  # Spawn merchant caravan parties
##  (3,
##   [
##       (try_for_range, ":troop_no", merchants_begin, merchants_end),
##         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_merchant),
##         (troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
##         (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),
##
##         (call_script, "script_cf_create_merchant_party", ":troop_no"),
##       (try_end),
##    ]),

  # Spawn village farmer parties
  (24,
   [
       (try_for_range, ":village_no", villages_begin, villages_end),
         (party_slot_eq, ":village_no", slot_village_state, svs_normal),
         (party_get_slot, ":farmer_party", ":village_no", slot_village_farmer_party),
         (this_or_next|eq, ":farmer_party", 0),
         (neg|party_is_active, ":farmer_party"),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 60),
         (call_script, "script_create_village_farmer_party", ":village_no"),
         (party_set_slot, ":village_no", slot_village_farmer_party, reg0),
#         (str_store_party_name, s1, ":village_no"),
#         (display_message, "@Village farmers created at {s1}."),
       (try_end),
    ]),
  
   (72,
   [
  # Updating trade good prices according to the productions
       (call_script, "script_update_trade_good_prices"),
 # Updating player odds
       (try_for_range, ":cur_center", centers_begin, centers_end),
         (party_get_slot, ":player_odds", ":cur_center", slot_town_player_odds),
         (try_begin),
           (gt, ":player_odds", 1000),
           (val_mul, ":player_odds", 95),
           (val_div, ":player_odds", 100),
           (val_max, ":player_odds", 1000),
         (else_try),
           (lt, ":player_odds", 1000),
           (val_mul, ":player_odds", 105),
           (val_div, ":player_odds", 100),
           (val_min, ":player_odds", 1000),
         (try_end),
         (party_set_slot, ":cur_center", slot_town_player_odds, ":player_odds"),
       (try_end),
    ]),
  #Troop AI: Merchants thinking
  (8,
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
         (party_is_in_any_town, ":party_no"),

         (store_faction_of_party, ":merchant_faction", ":party_no"),
         (faction_get_slot, ":num_towns", ":merchant_faction", slot_faction_num_towns),
         (try_begin),
           (le, ":num_towns", 0),
           (remove_party, ":party_no"),
         (else_try),
           (party_get_cur_town, ":cur_center", ":party_no"),
           
           (store_random_in_range, ":random_no", 0, 100),                               
           
           (try_begin),
             (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
             
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (try_begin),
               (eq, ":reduce_campaign_ai", 0), #hard (less money from tariffs)
               (assign, ":tariff_succeed_limit", 35),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #medium (normal money from tariffs)
               (assign, ":tariff_succeed_limit", 45),
             (else_try),
               (eq, ":reduce_campaign_ai", 2), #easy (more money from tariffs)
               (assign, ":tariff_succeed_limit", 60),
             (try_end),                
           (else_try),  
             (assign, ":tariff_succeed_limit", 45),
           (try_end),
                      
           (lt, ":random_no", ":tariff_succeed_limit"),                  

           (assign, ":can_leave", 1),
           (try_begin),
             (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
             (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
             (assign, ":can_leave", 0),
           (try_end),
           (eq, ":can_leave", 1),

           (assign, ":do_trade", 0),
           (try_begin),
             (party_get_slot, ":cur_ai_state", ":party_no", slot_party_ai_state),
             (eq, ":cur_ai_state", spai_trading_with_town),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),
             (assign, ":do_trade", 1),
           (try_end),

           (assign, ":target_center", -1),
           
           (try_begin), #Make sure escorted caravan continues to its original destination.
             (eq, "$caravan_escort_party_id", ":party_no"),
             (neg|party_is_in_town, ":party_no", "$caravan_escort_destination_town"),
             (assign, ":target_center", "$caravan_escort_destination_town"),
           (else_try),
		     ##diplomacy start+ added third parameter "-1" to use the town's location
             (call_script, "script_cf_select_most_profitable_town_at_peace_with_faction_in_trade_route", ":cur_center", ":merchant_faction",
				-1),
			 ##diplomacy end+
             (assign, ":target_center", reg0),
           (try_end),
           (is_between, ":target_center", towns_begin, towns_end),
           (neg|party_is_in_town, ":party_no", ":target_center"),
       
           (try_begin),
             (eq, ":do_trade", 1),
             (str_store_party_name, s7, ":cur_center"),             
             (call_script, "script_do_merchant_town_trade", ":party_no", ":cur_center"),
           (try_end),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":target_center"),
           (party_set_flags, ":party_no", pf_default_behavior, 0),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
         (try_end),
       (try_end),
    ]),
 #Increase castle food stores
  (2,
   [
   ##diplomacy start+ Change to vary with village prosperity
   (try_begin),
       (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
       ##OLD:
       #unaltered block begin
       (try_for_range, ":center_no", castles_begin, castles_end),
         (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #castle is not under siege
         (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
         (val_add, ":center_food_store", 100),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (val_min, ":center_food_store", ":food_store_limit"),
         (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
       #unaltered block end
   (else_try),
       ##NEW:
       (try_for_range, ":village_no", villages_begin, villages_end),
          (neg|party_slot_ge, ":village_no", slot_center_is_besieged_by, 0),
          (party_slot_eq, ":village_no", slot_village_state, svs_normal),
          (party_get_slot, ":center_no", ":village_no", slot_village_bound_center),
          (is_between, ":center_no", castles_begin, castles_end),
          (neg|party_slot_ge, ":center_no", slot_center_is_besieged_by, 0),
          (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
          (party_get_slot, reg0, ":village_no", slot_town_prosperity),
          (val_add, reg0, 75),
          (val_mul, reg0, 100),#base addition is 100
          (val_add, reg0, 62),
          (val_div, reg0, 125),#plus or minus 40%
          (val_add, ":center_food_store", reg0),
          (call_script, "script_center_get_food_store_limit", ":center_no"),
          (assign, ":food_store_limit", reg0),
          (val_min, ":center_food_store", ":food_store_limit"),
          (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
   (try_end),
   ]),
  # Setting item modifiers for food
  (24,
   [
     (troop_get_inventory_capacity, ":inv_size", "trp_player"),
     (try_for_range, ":i_slot", 0, ":inv_size"),
       (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
       (this_or_next|eq, ":item_id", "itm_cattle_meat"),
       (this_or_next|eq, ":item_id", "itm_chicken"),
		(eq, ":item_id", "itm_pork"),
		
       (troop_get_inventory_slot_modifier, ":modifier", "trp_player", ":i_slot"),
       (try_begin),
         (ge, ":modifier", imod_fresh),
         (lt, ":modifier", imod_rotten),
         (val_add, ":modifier", 1),
         (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", ":modifier"),
       (else_try),
         (lt, ":modifier", imod_fresh),
         (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", imod_fresh),
       (try_end),
     (try_end),
    ]),
  
  # Adding mercenary troops to the towns
  (72,
   [
     (call_script, "script_update_mercenary_units_of_towns"),
     #NPC changes begin
     # removes   (call_script, "script_update_companion_candidates_in_taverns"),
     #NPC changes end
     (call_script, "script_update_ransom_brokers"),
     (call_script, "script_update_tavern_travellers"),
     (call_script, "script_update_tavern_minstrels"),
     (call_script, "script_update_booksellers"),
     (call_script, "script_update_villages_infested_by_bandits"),
	 #Gekokujo Update Cities for Recruitment
     (try_for_range, ":center_no", centers_begin, centers_end),
       (call_script, "script_update_volunteer_troops_in_village", ":center_no"),
     (try_end),
	 #Gekokujo Do Not Update Tavern Recruitment
     (try_for_range, ":village_no", villages_begin, villages_end),
       (call_script, "script_update_npc_volunteer_troops_in_village", ":village_no"),
     (try_end),
    ]),
  (24,
   [	
    (call_script, "script_update_other_taverngoers"),
	]),
  # Adding tournaments to towns
  # Adding bandits to towns and villages
  (24,
   [(assign, ":num_active_tournaments", 0),
    (try_for_range, ":center_no", towns_begin, towns_end),
      (party_get_slot, ":has_tournament", ":center_no", slot_town_has_tournament),
      (try_begin),
        (eq, ":has_tournament", 1),#tournament ended, simulate
        (call_script, "script_fill_tournament_participants_troop", ":center_no", 0),
        (call_script, "script_sort_tournament_participant_troops"),#may not be needed
        (call_script, "script_get_num_tournament_participants"),
        (store_sub, ":needed_to_remove_randomly", reg0, 1),
        (call_script, "script_remove_tournament_participants_randomly", ":needed_to_remove_randomly"),
        (call_script, "script_sort_tournament_participant_troops"),
        (troop_get_slot, ":winner_troop", "trp_tournament_participants", 0),
        (try_begin),
          (is_between, ":winner_troop", active_npcs_begin, active_npcs_end),
          (str_store_troop_name_link, s1, ":winner_troop"),
          (str_store_party_name_link, s2, ":center_no"),
          (display_message, "@{s1} has won the tournament at {s2}."),
          (call_script, "script_change_troop_renown", ":winner_troop", 20),
        (try_end),
      (try_end),
      (val_sub, ":has_tournament", 1),
      (val_max, ":has_tournament", 0),
      (party_set_slot, ":center_no", slot_town_has_tournament, ":has_tournament"),
      (try_begin),
        (gt, ":has_tournament", 0),
        (val_add, ":num_active_tournaments", 1),
      (try_end),
    (try_end),
    
    (try_for_range, ":center_no", centers_begin, centers_end),
      (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
      (party_slot_eq, ":center_no", slot_party_type, spt_village),
      (party_get_slot, ":has_bandits", ":center_no", slot_center_has_bandits),
      (try_begin),
        (le, ":has_bandits", 0),
        (assign, ":continue", 0),
        (try_begin),
          (check_quest_active, "qst_deal_with_night_bandits"),
          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, ":center_no"),
          (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
          (assign, ":continue", 1),
        (else_try),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", 3),
          (assign, ":continue", 1),
        (try_end),
        (try_begin),
          (eq, ":continue", 1),
          (store_random_in_range, ":random_no", 0, 3),
          (try_begin),
            (eq, ":random_no", 0),
            (assign, ":bandit_troop", "trp_bandit"),
          (else_try),
            (eq, ":random_no", 1),
			#gekokujo set new bandit types
            #(assign, ":bandit_troop", "trp_woku_pirate"),
            (assign, ":bandit_troop", "trp_brigand"),
          (else_try),
            #(assign, ":bandit_troop", "trp_shinano_rebel"),
            (assign, ":bandit_troop", "trp_kanto_rebel"),
          (try_end),
          (party_set_slot, ":center_no", slot_center_has_bandits, ":bandit_troop"),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s1, ":center_no"),
            (display_message, "@{!}{s1} is infested by bandits (at night)."),
          (try_end),
        (try_end),
      (else_try),
        (try_begin),
          (assign, ":random_chance", 40),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign, ":random_chance", 20),
          (try_end),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":random_chance"),
          (party_set_slot, ":center_no", slot_center_has_bandits, 0),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s1, ":center_no"),
            (display_message, "@{s1} is no longer infested by bandits (at night)."),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
	
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
		
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	  (is_between, ":faction_object", towns_begin, towns_end),
	  
	  (party_slot_ge, ":faction_object", slot_town_has_tournament, 1),
	  #continue holding tournaments during the feast
      (party_set_slot, ":faction_object", slot_town_has_tournament, 2),
    (try_end),
	
	(try_begin),
	  #gekokujo feasts - make them more rare
      (lt, ":num_active_tournaments", 3),
      (store_random_in_range, ":random_no", 0, 100),
      #Add new tournaments with a 30% chance if there are less than 3 tournaments going on
      #(lt, ":random_no", 30),
	  (lt, ":random_no", 6), #gekokujo there are 3.33x as many factions and 1.45x as many cities
      (store_random_in_range, ":random_town", towns_begin, towns_end),
      (store_random_in_range, ":random_days", 12, 15),
      (party_set_slot, ":random_town", slot_town_has_tournament, ":random_days"),
      (try_begin),
        (eq, "$cheat_mode", 1),
        (str_store_party_name, s1, ":random_town"),
        (display_message, "@{!}{s1} is holding a tournament."),
      (try_end),
    (try_end),
    ]),
  (3,
[
	(assign, "$g_player_tournament_placement", 0),
]),
    
  # Spawn some bandits.
  (36,
   [
       (call_script, "script_spawn_bandits"),
    ]),
# Removing cattle herds if they are way out of range
  (12, [(try_for_parties, ":cur_party"),
          (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
          (store_distance_to_party_from_party, ":dist",":cur_party", "p_main_party"),
          (try_begin),
            (gt, ":dist", 30),
            (remove_party, ":cur_party"),
            (try_begin),
              #Fail quest if the party is the quest party
              (check_quest_active, "qst_move_cattle_herd"),
              (neg|check_quest_concluded, "qst_move_cattle_herd"),
              (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
              (call_script, "script_fail_quest", "qst_move_cattle_herd"),
            (end_try),
          (else_try),
            (gt, ":dist", 10),
            (party_set_slot, ":cur_party", slot_cattle_driven_by_player, 0),
            (party_set_ai_behavior, ":cur_party", ai_bhvr_hold),
          (try_end),
        (try_end),
    ]),
  (24,
   [
	  # Setting food bonuses in every 6 hours again and again because of a bug (we could not find its reason) which decreases especially slot_item_food_bonus slots of items to 0.
	  #Staples
      (item_set_slot, "itm_bread", slot_item_food_bonus, 8), #brought up from 4
      (item_set_slot, "itm_grain", slot_item_food_bonus, 2), #new - can be boiled as porridge
	  
	  #Fat sources - preserved
      (item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 4),
      (item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
      (item_set_slot, "itm_cheese", slot_item_food_bonus, 5),
      (item_set_slot, "itm_sausages", slot_item_food_bonus, 5),
      (item_set_slot, "itm_butter", slot_item_food_bonus, 4), #brought down from 8

	  #Fat sources - perishable
      (item_set_slot, "itm_chicken", slot_item_food_bonus, 8), #brought up from 7
      (item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7), #brought down from 7
      (item_set_slot, "itm_pork", slot_item_food_bonus, 6), #brought down from 6
	  
	  #Produce
      (item_set_slot, "itm_raw_olives", slot_item_food_bonus, 1),
      (item_set_slot, "itm_cabbages", slot_item_food_bonus, 2),
      (item_set_slot, "itm_raw_grapes", slot_item_food_bonus, 3),
      (item_set_slot, "itm_apples", slot_item_food_bonus, 4), #brought down from 5

	  #Sweet items
      (item_set_slot, "itm_raw_date_fruit", slot_item_food_bonus, 4), #brought down from 8
      (item_set_slot, "itm_honey", slot_item_food_bonus, 6), #brought down from 12
      
      (item_set_slot, "itm_wine", slot_item_food_bonus, 5),
      (item_set_slot, "itm_ale", slot_item_food_bonus, 4),
   ]),
  # Constable training
   (24,
   [
   (eq, "$g_player_constable", "trp_dplmc_constable"),
   (is_between, "$g_constable_training_center", walled_centers_begin, walled_centers_end),
   (party_slot_eq, "$g_constable_training_center", slot_town_lord, "trp_player"),

   (store_skill_level, ":trainer_level", skl_trainer, "trp_player"),
   (val_add, ":trainer_level", 4),
   (store_div, ":xp_gain", ":trainer_level", 2),

   (try_for_parties, ":party_no"),
    (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
    (eq, ":party_no", "$g_constable_training_center"),

    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),

    (assign, ":trained", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (eq, ":trained", 0),
      (party_stack_get_troop_id, ":troop_id", ":party_no", ":i_stack"),
      (neg|troop_is_hero, ":troop_id"),

      (troop_get_upgrade_troop, ":upgrade_troop", ":troop_id" , "$g_constable_training_type"),
      (try_begin),
       (le, ":upgrade_troop", 0),
       (troop_get_upgrade_troop, ":upgrade_troop", ":troop_id", 0),
      (try_end),

      #only proceed if troop is upgradable
      (gt, ":upgrade_troop", 0),

      (store_character_level, ":troop_level", ":troop_id"),
      (assign, ":troop_limit" , 6),

      (try_begin),
        (eq, "$g_constable_training_improved", 1),
        (assign, ":troop_limit" , 10),
        (try_begin),
          (le, ":troop_level", 6),
          (val_add, ":xp_gain", 2), #more recruits are trained during improved training
        (try_end),
      (try_end),

      (le, ":troop_level", ":troop_limit"),

      (party_count_members_of_type,":cur_number",":party_no",":troop_id"),
      (val_min, ":xp_gain", ":cur_number"),

      (call_script, "script_game_get_upgrade_cost", ":troop_id"),
      (store_mul, ":upgrade_cost", ":xp_gain", reg0),

      (try_begin),
        (eq, "$g_constable_training_improved", 1),
        (val_add, ":upgrade_cost", 10), #+10 mon during improved training
      (try_end),

      (store_troop_gold, ":gold", "trp_household_possessions"),
      (try_begin),
        (lt, ":gold", ":upgrade_cost"),
        (store_div, ":money_limit", ":gold", reg0),
        (val_min, ":xp_gain", ":money_limit"),
        (store_mul, ":upgrade_cost", ":xp_gain", reg0),
        (display_message, "@Not enough money in treasury to upgrade troops."),
      (try_end),

      (party_remove_members,":party_no",":troop_id",":xp_gain"),
      (party_add_members, ":party_no", ":upgrade_troop", ":xp_gain"),

      (call_script, "script_dplmc_withdraw_from_treasury", ":upgrade_cost"),

      (assign, reg5, ":xp_gain"),
      (str_store_troop_name, s6, ":troop_id"),
      (str_store_troop_name, s7, ":upgrade_troop"),
      (str_store_party_name, s8, ":party_no"),
      (display_message, "@Your army inspector upgraded {reg5} {s6} to {s7} in {s8}"),
      (assign, ":trained", 1),
    (try_end),
   (try_end),
    ]),
  # Patrol wages
   (24 * 7,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_patrol),



      (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
      (eq, ":ai_state", spai_patrolling_around_center),

      (try_begin),
		(party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
        (assign, ":total_wage", 0),
        (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
          (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
          (call_script, "script_game_get_troop_wage", ":stack_troop", 0),
          (val_mul, reg0, ":stack_size"),
          (val_add, ":total_wage", reg0),
        (try_end),
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (try_begin),
          (lt, ":gold", ":total_wage"),
          (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
          (str_store_party_name, s6, ":target_party"),
          (display_log_message, "@Your soldiers patrolling {s6} disbanded because you can't pay the wages!", 0xFF0000),
          (remove_party, ":party_no"),
        (try_end),
      (try_end),
    (try_end),
    ]),
]
