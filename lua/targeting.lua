local function table_has_value(t, val)
	for i, v in pairs(t) do
		if i == val then
			return true
		end
	end
	return false
end

function gettarget()
	g = dofile("get_agent_data.lua") -- Load file
	
	local target_table = {}
	for agent in game.agentsI() do
		if is_alive_human_agent(agent) then
			target = get_look_target(agent)
			if is_alive_human_agent(target) then
				if not table_has_value(target_table, agent) then
					target_table[agent] = 0
					game.agent_clear_scripted_mode(agent)
					game.agent_set_speed_limit(agent, 100)
					game.set_party_battle_mode(0)
					--print("u did it")
				end
				if table_has_value(target_table, target) then
					target_table[target] = target_table[target] + 1
				else
					target_table[target] = 1
				end
			end
		end
	end
	
	--print("Target table size: " .. #target_table)
	
	for agent in game.agentsI() do
		target = get_look_target(agent)
		enemy_amount = get_num_cached_enemies(agent)
		if #target_table > 0 then
			for x=1, enemy_amount do
				enemy = get_cached_enemy(x, agent)
				if (target_table[enemy] ~= nil) and (target_table[enemy] < 2) then
					game.agent_set_look_target_agent(agent, enemy)
					break
				end
			end
		end
	end
	
	
	-- for agent in game.agentsI() do
		-- target = get_look_target(agent)
	    -- pos_agent, pos_target = get_agent_position(agent), get_agent_position(target)
		-- distance = get_distance_between_positions(pos_agent, pos_target)
		-- if distance < 2500 then 
			-- game.agent_clear_scripted_mode(agent)
			-- print("clear scripted mode")
		-- end
	-- end
	
end



-- function idiot()
	-- dofile("data/position_data.lua") -- Load file
	-- dofile("data/agent_player_data.lua")
	
	-- for agent in game.agentsI() do
		-- if is_alive_human_agent(agent) then
			-- agent_pos = get_agent_position(agent) 
			-- x_pos, y_pos = position_get_x(agent_pos), position_get_y(agent_pos)
			-- --pos1, pos2 = get_scene_boundaries(preg1, preg2) --pos1 = min, pos2 = max 
			-- --x = position_get_x(pos2)
			-- --y = position_get_y(pos2)
			-- distancex = 1000 - x_pos
			-- distancey = 1000 - y_pos
			-- if x_pos < 2000 then
				-- game.agent_fade_out(0, agent)
			-- end
			-- if y_pos < 2000 then
				-- game.agent_fade_out(0, agent)
			-- end
			-- if distancex < 2000 then
				-- game.agent_fade_out(0, agent)
			-- end
			-- if distancey < 2000 then
				-- game.agent_fade_out(0, agent)
			-- end
		-- end
	-- end
-- end