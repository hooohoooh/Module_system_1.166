reserved_variables = [
  # marshall_selection presentation (election simple trigger disabled; see module_simple_triggers)
  "g_presentation_marshall_selection_1_vote",
  "g_presentation_marshall_selection_2_vote",
  "g_presentation_marshall_selection_max_renown_1",
  "g_presentation_marshall_selection_max_renown_2",
  "g_presentation_marshall_selection_max_renown_1_troop",
  "g_presentation_marshall_selection_max_renown_2_troop",
  "g_presentation_marshall_selection_ended",
  # gatling variables
  "ym_56",
  "ym_44",
  # zhenyinghebing variables
  "g_merge_faction_1",
  "g_merge_faction_2",
  "g_merge_faction_3",
  "g_merge_faction_4",
  "g_faction_merge_done",
  # troop detail view presentation variables
  "g_presentation_obj_troop_detail_close",
  "g_presentation_obj_troop_detail_back",
  # troop tree overlay counter
  "g_troop_tree_overlay_count",
]
# modmerger_start version=201 type=4
try:
    component_name = "variables"
    var_set = { "reserved_variables":reserved_variables, }
    from modmerger import modmerge
    modmerge(var_set, component_name)
except:
    raise
# modmerger_end
