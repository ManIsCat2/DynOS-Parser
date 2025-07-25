# dynos.py

import struct

FUNCTION_CODE = 0x434E5546
POINTER_CODE = 0x52544E50
LUA_VAR_CODE = 0x5641554C
TEX_REF_CODE = 0x52584554

F32VTX_SENTINEL_0 = 0x3346
F32VTX_SENTINEL_1 = 0x5632
F32VTX_SENTINEL_2 = 0x5854

# Define the data types
DATA_TYPE_NONE = 0
DATA_TYPE_LIGHT = 1
DATA_TYPE_TEXTURE=2
DATA_TYPE_VERTEX=3
DATA_TYPE_DISPLAY_LIST=4
DATA_TYPE_GEO_LAYOUT=5
DATA_TYPE_ANIMATION_VALUE=6
DATA_TYPE_ANIMATION_INDEX=7
DATA_TYPE_ANIMATION=8
DATA_TYPE_ANIMATION_TABLE=9
DATA_TYPE_GFXDYNCMD=10
DATA_TYPE_COLLISION=11
DATA_TYPE_LEVEL_SCRIPT=12
DATA_TYPE_MACRO_OBJECT=13
DATA_TYPE_TRAJECTORY=14
DATA_TYPE_MOVTEX=15
DATA_TYPE_MOVTEXQC=16
DATA_TYPE_ROOMS=17
DATA_TYPE_LIGHT_T=18
DATA_TYPE_AMBIENT_T=19
DATA_TYPE_TEXTURE_LIST=20
DATA_TYPE_TEXTURE_RAW=21
DATA_TYPE_BEHAVIOR_SCRIPT=22
DATA_TYPE_UNUSED=23
DATA_TYPE_LIGHT_0=24

sDynosBuiltinFuncs = [
    'geo_mirror_mario_set_alpha',
    'geo_switch_mario_stand_run',
    'geo_switch_mario_eyes',
    'geo_mario_tilt_torso',
    'geo_mario_head_rotation',
    'geo_switch_mario_hand',
    'geo_mario_hand_foot_scaler',
    'geo_switch_mario_cap_effect',
    'geo_switch_mario_cap_on_off',
    'geo_mario_rotate_wing_cap_wings',
    'geo_switch_mario_hand_grab_pos',
    'geo_render_mirror_mario',
    'geo_mirror_mario_backface_culling',
    'geo_update_projectile_pos_from_parent',
    'geo_update_layer_transparency',
    'geo_switch_anim_state',
    'geo_switch_area',
    'geo_camera_main',
    'geo_camera_fov',
    'geo_envfx_main',
    'geo_skybox_main',
    'geo_wdw_set_initial_water_level',
    'geo_movtex_pause_control',
    'geo_movtex_draw_water_regions',
    'geo_movtex_draw_nocolor',
    'geo_movtex_draw_colored',
    'geo_movtex_draw_colored_no_update',
    'geo_movtex_draw_colored_2_no_update',
    'geo_movtex_update_horizontal',
    'geo_movtex_draw_colored_no_update',
    'geo_painting_draw',
    'geo_painting_update',
    'geo_exec_inside_castle_light',
    'geo_exec_flying_carpet_timer_update',
    'geo_exec_flying_carpet_create',
    'geo_exec_cake_end_screen',
    'geo_cannon_circle_base',
    'geo_move_mario_part_from_parent',
    'geo_bits_bowser_coloring',
    'geo_update_body_rot_from_parent',
    'geo_switch_bowser_eyes',
    'geo_switch_tuxie_mother_eyes',
    'geo_update_held_mario_pos',
    'geo_snufit_move_mask',
    'geo_snufit_scale_body',
    'geo_scale_bowser_key',
    "geo_rotate_coin",
    'geo_offset_klepto_held_object',
    'geo_switch_peach_eyes',

    # Co-op specific
    'geo_mario_set_player_colors',
    'geo_movtex_draw_water_regions_ext',
    'lvl_init_or_update',
    'geo_choose_area_ext',

    # Behaviors
    'bhv_cap_switch_loop',
    'bhv_tiny_star_particles_init',
    'bhv_grindel_thwomp_loop',
    'bhv_koopa_shell_underwater_loop',
    'bhv_door_init',
    'bhv_door_loop',
    'bhv_star_door_loop',
    'bhv_star_door_loop_2',
    'bhv_mr_i_loop',
    'bhv_mr_i_body_loop',
    'bhv_mr_i_particle_loop',
    'bhv_piranha_particle_loop',
    'bhv_giant_pole_loop',
    'bhv_pole_init',
    'bhv_pole_base_loop',
    'bhv_thi_huge_island_top_loop',
    'bhv_thi_tiny_island_top_loop',
    'bhv_king_bobomb_loop',
    'bhv_bobomb_anchor_mario_loop',
    'bhv_beta_chest_bottom_init',
    'bhv_beta_chest_bottom_loop',
    'bhv_beta_chest_lid_loop',
    'bhv_bubble_wave_init',
    'bhv_bubble_maybe_loop',
    'bhv_bubble_player_loop',
    'bhv_water_air_bubble_init',
    'bhv_water_air_bubble_loop',
    'bhv_particle_init',
    'bhv_particle_loop',
    'bhv_water_waves_init',
    'bhv_small_bubbles_loop',
    'bhv_fish_group_loop',
    'bhv_cannon_base_loop',
    'bhv_cannon_barrel_loop',
    'bhv_cannon_base_unused_loop',
    'bhv_chuckya_loop',
    'bhv_chuckya_anchor_mario_loop',
    'bhv_rotating_platform_loop',
    'bhv_wf_breakable_wall_loop',
    'bhv_kickable_board_loop',
    'bhv_tower_door_loop',
    'bhv_wf_rotating_wooden_platform_init',
    'bhv_wf_rotating_wooden_platform_loop',
    'bhv_fading_warp_loop',
    'bhv_warp_loop',
    'bhv_white_puff_exploding_loop',
    'bhv_spawned_star_init',
    'bhv_spawned_star_loop',
    'bhv_coin_init',
    'bhv_coin_loop',
    'bhv_coin_inside_boo_loop',
    'bhv_coin_formation_init',
    'bhv_coin_formation_spawn_loop',
    'bhv_coin_formation_loop',
    'bhv_temp_coin_loop',
    'bhv_coin_sparkles_loop',
    'bhv_golden_coin_sparkles_loop',
    'bhv_wall_tiny_star_particle_loop',
    'bhv_pound_tiny_star_particle_loop',
    'bhv_pound_tiny_star_particle_init',
    'bhv_punch_tiny_triangle_loop',
    'bhv_punch_tiny_triangle_init',
    'bhv_tumbling_bridge_platform_loop',
    'bhv_tumbling_bridge_loop',
    'bhv_elevator_init',
    'bhv_elevator_loop',
    'bhv_water_mist_loop',
    'bhv_water_mist_spawn_loop',
    'bhv_water_mist_2_loop',
    'bhv_pound_white_puffs_init',
    'bhv_ground_sand_init',
    'bhv_ground_snow_init',
    'bhv_wind_loop',
    'bhv_unused_particle_spawn_loop',
    'bhv_ukiki_cage_star_loop',
    'bhv_ukiki_cage_loop',
    'bhv_bitfs_sinking_platform_loop',
    'bhv_bitfs_sinking_cage_platform_loop',
    'bhv_ddd_moving_pole_loop',
    'bhv_platform_normals_init',
    'bhv_tilting_inverted_pyramid_loop',
    'bhv_squishable_platform_loop',
    'bhv_beta_moving_flames_spawn_loop',
    'bhv_beta_moving_flames_loop',
    'bhv_rr_rotating_bridge_platform_loop',
    'bhv_flamethrower_loop',
    'bhv_flamethrower_flame_loop',
    'bhv_bouncing_fireball_loop',
    'bhv_bouncing_fireball_flame_loop',
    'bhv_bowser_shock_wave_loop',
    'bhv_flame_mario_loop',
    'bhv_black_smoke_mario_loop',
    'bhv_black_smoke_bowser_loop',
    'bhv_black_smoke_upward_loop',
    'bhv_beta_fish_splash_spawner_loop',
    'bhv_spindrift_loop',
    'bhv_tower_platform_group_init',
    'bhv_tower_platform_group_loop',
    'bhv_wf_sliding_tower_platform_loop',
    'bhv_wf_elevator_tower_platform_loop',
    'bhv_wf_solid_tower_platform_loop',
    'bhv_snow_leaf_particle_spawn_init',
    'bhv_tree_snow_or_leaf_loop',
    'bhv_piranha_plant_bubble_loop',
    'bhv_piranha_plant_waking_bubbles_loop',
    'bhv_purple_switch_loop',
    'bhv_hidden_object_loop',
    'bhv_breakable_box_loop',
    'bhv_pushable_loop',
    'bhv_init_room',
    'bhv_small_water_wave_loop',
    'bhv_yellow_coin_init',
    'bhv_yellow_coin_loop',
    'bhv_squarish_path_moving_loop',
    'bhv_squarish_path_parent_init',
    'bhv_squarish_path_parent_loop',
    'bhv_heave_ho_loop',
    'bhv_heave_ho_throw_mario_loop',
    'bhv_ccm_touched_star_spawn_loop',
    'bhv_unused_poundable_platform',
    'bhv_beta_trampoline_top_loop',
    'bhv_beta_trampoline_spring_loop',
    'bhv_jumping_box_loop',
    'bhv_boo_cage_init',
    'bhv_boo_cage_loop',
    'bhv_bowser_key_init',
    'bhv_bowser_key_loop',
    'bhv_grand_star_init',
    'bhv_grand_star_loop',
    'bhv_beta_boo_key_loop',
    'bhv_alpha_boo_key_loop',
    'bhv_bullet_bill_init',
    'bhv_bullet_bill_loop',
    'bhv_white_puff_smoke_init',
    'bhv_bowser_tail_anchor_init',
    'bhv_bowser_tail_anchor_loop',
    'bhv_bowser_init',
    'bhv_bowser_loop',
    'bhv_bowser_body_anchor_init',
    'bhv_bowser_body_anchor_loop',
    'bhv_bowser_flame_spawn_loop',
    'bhv_tilting_bowser_lava_platform_init',
    'bhv_falling_bowser_platform_loop',
    'bhv_blue_bowser_flame_init',
    'bhv_blue_bowser_flame_loop',
    'bhv_flame_floating_landing_init',
    'bhv_flame_floating_landing_loop',
    'bhv_blue_flames_group_loop',
    'bhv_flame_bouncing_init',
    'bhv_flame_bouncing_loop',
    'bhv_flame_moving_forward_growing_init',
    'bhv_flame_moving_forward_growing_loop',
    'bhv_flame_bowser_init',
    'bhv_flame_bowser_loop',
    'bhv_flame_large_burning_out_init',
    'bhv_blue_fish_movement_loop',
    'bhv_tank_fish_group_loop',
    'bhv_checkerboard_elevator_group_init',
    'bhv_checkerboard_elevator_group_loop',
    'bhv_checkerboard_platform_init',
    'bhv_checkerboard_platform_loop',
    'bhv_bowser_key_unlock_door_loop',
    'bhv_bowser_key_course_exit_loop',
    'bhv_invisible_objects_under_bridge_init',
    'bhv_invisible_objects_under_bridge_loop',
    'bhv_water_level_pillar_init',
    'bhv_water_level_pillar_loop',
    'bhv_ddd_warp_loop',
    'bhv_moat_grills_loop',
    'bhv_rotating_clock_arm_loop',
    'bhv_ukiki_init',
    'bhv_ukiki_loop',
    'bhv_lll_sinking_rock_block_loop',
    'bhv_lll_moving_octagonal_mesh_platform_loop',
    'bhv_lll_rotating_block_fire_bars_loop',
    'bhv_lll_rotating_hex_flame_loop',
    'bhv_lll_wood_piece_loop',
    'bhv_lll_floating_wood_bridge_loop',
    'bhv_volcano_flames_loop',
    'bhv_lll_rotating_hexagonal_ring_loop',
    'bhv_lll_sinking_rectangular_platform_loop',
    'bhv_lll_sinking_square_platforms_loop',
    'bhv_koopa_shell_loop',
    'bhv_koopa_shell_flame_loop',
    'bhv_tox_box_loop',
    'bhv_piranha_plant_loop',
    'bhv_lll_bowser_puzzle_piece_loop',
    'bhv_lll_bowser_puzzle_loop',
    'bhv_tuxies_mother_loop',
    'bhv_small_penguin_loop',
    'bhv_fish_spawner_loop',
    'bhv_fish_loop',
    'bhv_wdw_express_elevator_loop',
    'bhv_bub_spawner_loop',
    'bhv_bub_loop',
    'bhv_exclamation_box_init',
    'bhv_exclamation_box_loop',
    'bhv_rotating_exclamation_box_loop',
    'bhv_sound_spawner_init',
    'bhv_bowsers_sub_loop',
    'bhv_sushi_shark_loop',
    'bhv_sushi_shark_collision_loop',
    'bhv_jrb_sliding_box_loop',
    'bhv_ship_part_3_loop',
    'bhv_sunken_ship_part_loop',
    'bhv_white_puff_1_loop',
    'bhv_white_puff_2_loop',
    'bhv_blue_coin_switch_loop',
    'bhv_hidden_blue_coin_loop',
    'bhv_openable_cage_door_loop',
    'bhv_openable_grill_loop',
    'bhv_water_level_diamond_loop',
    'bhv_init_changing_water_level_loop',
    'bhv_tweester_sand_particle_loop',
    'bhv_tweester_loop',
    'bhv_merry_go_round_boo_manager_loop',
    'bhv_animated_texture_loop',
    'bhv_boo_in_castle_loop',
    'bhv_boo_with_cage_init',
    'bhv_boo_with_cage_loop',
    'bhv_boo_init',
    'bhv_big_boo_loop',
    'bhv_courtyard_boo_triplet_init',
    'bhv_boo_loop',
    'bhv_boo_boss_spawned_bridge_loop',
    'bhv_bbh_tilting_trap_platform_loop',
    'bhv_haunted_bookshelf_loop',
    'bhv_merry_go_round_loop',
    'bhv_play_music_track_when_touched_loop',
    'bhv_beta_bowser_anchor_loop',
    'bhv_static_checkered_platform_loop',
    'bhv_castle_floor_trap_init',
    'bhv_castle_floor_trap_loop',
    'bhv_floor_trap_in_castle_loop',
    'bhv_sparkle_spawn_loop',
    'bhv_scuttlebug_loop',
    'bhv_scuttlebug_spawn_loop',
    'bhv_whomp_loop',
    'bhv_water_splash_spawn_droplets',
    'bhv_water_droplet_loop',
    'bhv_water_droplet_splash_init',
    'bhv_bubble_splash_init',
    'bhv_idle_water_wave_loop',
    'bhv_shallow_water_splash_init',
    'bhv_wave_trail_shrink',
    'bhv_strong_wind_particle_loop',
    'bhv_sl_snowman_wind_loop',
    'bhv_sl_walking_penguin_loop',
    'bhv_menu_button_init',
    'bhv_menu_button_loop',
    'bhv_menu_button_manager_init',
    'bhv_menu_button_manager_loop',
    'bhv_act_selector_star_type_loop',
    'bhv_act_selector_init',
    'bhv_act_selector_loop',
    'bhv_moving_yellow_coin_init',
    'bhv_moving_yellow_coin_loop',
    'bhv_moving_blue_coin_init',
    'bhv_moving_blue_coin_loop',
    'bhv_blue_coin_sliding_jumping_init',
    'bhv_blue_coin_sliding_loop',
    'bhv_blue_coin_jumping_loop',
    'bhv_seaweed_init',
    'bhv_seaweed_bundle_init',
    'bhv_bobomb_init',
    'bhv_bobomb_loop',
    'bhv_bobomb_fuse_smoke_init',
    'bhv_bobomb_buddy_init',
    'bhv_bobomb_buddy_loop',
    'bhv_cannon_closed_init',
    'bhv_cannon_closed_loop',
    'bhv_whirlpool_init',
    'bhv_whirlpool_loop',
    'bhv_jet_stream_loop',
    'bhv_homing_amp_init',
    'bhv_homing_amp_loop',
    'bhv_circling_amp_init',
    'bhv_circling_amp_loop',
    'bhv_butterfly_init',
    'bhv_butterfly_loop',
    'bhv_hoot_init',
    'bhv_hoot_loop',
    'bhv_beta_holdable_object_init',
    'bhv_beta_holdable_object_loop',
    'bhv_object_bubble_init',
    'bhv_object_bubble_loop',
    'bhv_object_water_wave_init',
    'bhv_object_water_wave_loop',
    'bhv_explosion_init',
    'bhv_explosion_loop',
    'bhv_bobomb_bully_death_smoke_init',
    'bhv_bobomb_explosion_bubble_init',
    'bhv_bobomb_explosion_bubble_loop',
    'bhv_respawner_loop',
    'bhv_small_bully_init',
    'bhv_bully_loop',
    'bhv_big_bully_init',
    'bhv_big_bully_with_minions_init',
    'bhv_big_bully_with_minions_loop',
    'bhv_jet_stream_ring_spawner_loop',
    'bhv_jet_stream_water_ring_init',
    'bhv_jet_stream_water_ring_loop',
    'bhv_manta_ray_water_ring_init',
    'bhv_manta_ray_water_ring_loop',
    'bhv_bowser_bomb_loop',
    'bhv_bowser_bomb_explosion_loop',
    'bhv_bowser_bomb_smoke_loop',
    'bhv_celebration_star_init',
    'bhv_celebration_star_loop',
    'bhv_celebration_star_sparkle_loop',
    'bhv_star_key_collection_puff_spawner_loop',
    'bhv_lll_drawbridge_spawner_init',
    'bhv_lll_drawbridge_spawner_loop',
    'bhv_lll_drawbridge_loop',
    'bhv_small_bomp_init',
    'bhv_small_bomp_loop',
    'bhv_large_bomp_init',
    'bhv_large_bomp_loop',
    'bhv_wf_sliding_platform_init',
    'bhv_wf_sliding_platform_loop',
    'bhv_moneybag_init',
    'bhv_moneybag_loop',
    'bhv_moneybag_hidden_loop',
    'bhv_bob_pit_bowling_ball_init',
    'bhv_bob_pit_bowling_ball_loop',
    'bhv_free_bowling_ball_init',
    'bhv_free_bowling_ball_loop',
    'bhv_bowling_ball_init',
    'bhv_bowling_ball_loop',
    'bhv_generic_bowling_ball_spawner_init',
    'bhv_generic_bowling_ball_spawner_loop',
    'bhv_thi_bowling_ball_spawner_loop',
    'bhv_rr_cruiser_wing_init',
    'bhv_rr_cruiser_wing_loop',
    'bhv_spindel_init',
    'bhv_spindel_loop',
    'bhv_ssl_moving_pyramid_wall_init',
    'bhv_ssl_moving_pyramid_wall_loop',
    'bhv_pyramid_elevator_init',
    'bhv_pyramid_elevator_loop',
    'bhv_pyramid_elevator_trajectory_marker_ball_loop',
    'bhv_pyramid_top_init',
    'bhv_pyramid_top_loop',
    'bhv_pyramid_top_fragment_init',
    'bhv_pyramid_top_fragment_loop',
    'bhv_pyramid_pillar_touch_detector_loop',
    'bhv_waterfall_sound_loop',
    'bhv_volcano_sound_loop',
    'bhv_castle_flag_init',
    'bhv_birds_sound_loop',
    'bhv_ambient_sounds_init',
    'bhv_sand_sound_loop',
    'bhv_castle_cannon_grate_init',
    'bhv_snowmans_bottom_init',
    'bhv_snowmans_bottom_loop',
    'bhv_snowmans_head_init',
    'bhv_snowmans_head_loop',
    'bhv_snowmans_body_checkpoint_loop',
    'bhv_big_boulder_init',
    'bhv_big_boulder_loop',
    'bhv_big_boulder_generator_loop',
    'bhv_wing_cap_init',
    'bhv_wing_vanish_cap_loop',
    'bhv_metal_cap_init',
    'bhv_metal_cap_loop',
    'bhv_normal_cap_init',
    'bhv_normal_cap_loop',
    'bhv_vanish_cap_init',
    'bhv_collect_star_init',
    'bhv_collect_star_loop',
    'bhv_star_spawn_init',
    'bhv_star_spawn_loop',
    'bhv_hidden_red_coin_star_init',
    'bhv_hidden_red_coin_star_loop',
    'bhv_red_coin_init',
    'bhv_red_coin_loop',
    'bhv_bowser_course_red_coin_star_loop',
    'bhv_hidden_star_init',
    'bhv_hidden_star_loop',
    'bhv_hidden_star_trigger_loop',
    'bhv_ttm_rolling_log_init',
    'bhv_rolling_log_loop',
    'bhv_lll_rolling_log_init',
    'bhv_1up_common_init',
    'bhv_1up_walking_loop',
    'bhv_1up_running_away_loop',
    'bhv_1up_sliding_loop',
    'bhv_1up_init',
    'bhv_1up_loop',
    'bhv_1up_jump_on_approach_loop',
    'bhv_1up_hidden_loop',
    'bhv_1up_hidden_trigger_loop',
    'bhv_1up_hidden_in_pole_loop',
    'bhv_1up_hidden_in_pole_trigger_loop',
    'bhv_1up_hidden_in_pole_spawner_loop',
    'bhv_controllable_platform_init',
    'bhv_controllable_platform_loop',
    'bhv_controllable_platform_sub_loop',
    'bhv_breakable_box_small_init',
    'bhv_breakable_box_small_loop',
    'bhv_sliding_snow_mound_loop',
    'bhv_snow_mound_spawn_loop',
    'bhv_floating_platform_loop',
    'bhv_arrow_lift_loop',
    'bhv_orange_number_init',
    'bhv_orange_number_loop',
    'bhv_manta_ray_init',
    'bhv_manta_ray_loop',
    'bhv_falling_pillar_init',
    'bhv_falling_pillar_loop',
    'bhv_falling_pillar_hitbox_loop',
    'bhv_jrb_floating_box_loop',
    'bhv_decorative_pendulum_init',
    'bhv_decorative_pendulum_loop',
    'bhv_treasure_chest_ship_init',
    'bhv_treasure_chest_ship_loop',
    'bhv_treasure_chest_jrb_init',
    'bhv_treasure_chest_jrb_loop',
    'bhv_treasure_chest_init',
    'bhv_treasure_chest_loop',
    'bhv_treasure_chest_bottom_init',
    'bhv_treasure_chest_bottom_loop',
    'bhv_treasure_chest_top_loop',
    'bhv_mips_init',
    'bhv_mips_loop',
    'bhv_yoshi_init',
    'bhv_koopa_init',
    'bhv_koopa_update',
    'bhv_koopa_race_endpoint_update',
    'bhv_pokey_update',
    'bhv_pokey_body_part_update',
    'bhv_swoop_update',
    'bhv_fly_guy_update',
    'bhv_goomba_init',
    'bhv_goomba_update',
    'bhv_goomba_triplet_spawner_update',
    'bhv_chain_chomp_update',
    'bhv_chain_chomp_chain_part_update',
    'bhv_wooden_post_update',
    'bhv_chain_chomp_gate_init',
    'bhv_chain_chomp_gate_update',
    'bhv_wiggler_update',
    'bhv_wiggler_body_part_update',
    'bhv_enemy_lakitu_update',
    'bhv_camera_lakitu_init',
    'bhv_camera_lakitu_update',
    'bhv_cloud_update',
    'bhv_cloud_part_update',
    'bhv_spiny_update',
    'bhv_monty_mole_init',
    'bhv_monty_mole_update',
    'bhv_monty_mole_hole_update',
    'bhv_monty_mole_rock_update',
    'bhv_platform_on_track_init',
    'bhv_platform_on_track_update',
    'bhv_track_ball_update',
    'bhv_seesaw_platform_init',
    'bhv_seesaw_platform_update',
    'bhv_ferris_wheel_axle_init',
    'bhv_ferris_wheel_platform_update',
    'bhv_water_bomb_spawner_update',
    'bhv_water_bomb_update',
    'bhv_water_bomb_shadow_update',
    'bhv_ttc_rotating_solid_init',
    'bhv_ttc_rotating_solid_update',
    'bhv_ttc_pendulum_init',
    'bhv_ttc_pendulum_update',
    'bhv_ttc_treadmill_init',
    'bhv_ttc_treadmill_update',
    'bhv_ttc_moving_bar_init',
    'bhv_ttc_moving_bar_update',
    'bhv_ttc_cog_init',
    'bhv_ttc_cog_update',
    'bhv_ttc_pit_block_init',
    'bhv_ttc_pit_block_update',
    'bhv_ttc_elevator_init',
    'bhv_ttc_elevator_update',
    'bhv_ttc_2d_rotator_init',
    'bhv_ttc_2d_rotator_update',
    'bhv_ttc_spinner_update',
    'bhv_mr_blizzard_init',
    'bhv_mr_blizzard_update',
    'bhv_mr_blizzard_snowball',
    'bhv_sliding_plat_2_init',
    'bhv_sliding_plat_2_loop',
    'bhv_rotating_octagonal_plat_init',
    'bhv_rotating_octagonal_plat_loop',
    'bhv_animates_on_floor_switch_press_init',
    'bhv_animates_on_floor_switch_press_loop',
    'bhv_activated_back_and_forth_platform_init',
    'bhv_activated_back_and_forth_platform_update',
    'bhv_recovery_heart_loop',
    'bhv_water_bomb_cannon_loop',
    'bhv_bubble_cannon_barrel_loop',
    'bhv_unagi_init',
    'bhv_unagi_loop',
    'bhv_unagi_subobject_loop',
    'bhv_dorrie_update',
    'bhv_haunted_chair_init',
    'bhv_haunted_chair_loop',
    'bhv_mad_piano_update',
    'bhv_flying_bookend_loop',
    'bhv_bookend_spawn_loop',
    'bhv_haunted_bookshelf_manager_loop',
    'bhv_book_switch_loop',
    'bhv_fire_piranha_plant_init',
    'bhv_fire_piranha_plant_update',
    'bhv_small_piranha_flame_loop',
    'bhv_fire_spitter_update',
    'bhv_fly_guy_flame_loop',
    'bhv_snufit_loop',
    'bhv_snufit_balls_loop',
    'bhv_horizontal_grindel_init',
    'bhv_horizontal_grindel_update',
    'bhv_eyerok_boss_init',
    'bhv_eyerok_boss_loop',
    'bhv_eyerok_hand_loop',
    'bhv_klepto_init',
    'bhv_klepto_update',
    'bhv_bird_update',
    'bhv_racing_penguin_init',
    'bhv_racing_penguin_update',
    'bhv_penguin_race_finish_line_update',
    'bhv_penguin_race_shortcut_check_update',
    'bhv_coffin_spawner_loop',
    'bhv_coffin_loop',
    'bhv_clam_loop',
    'bhv_skeeter_update',
    'bhv_skeeter_wave_update',
    'bhv_swing_platform_init',
    'bhv_swing_platform_update',
    'bhv_donut_platform_spawner_update',
    'bhv_donut_platform_update',
    'bhv_ddd_pole_init',
    'bhv_ddd_pole_update',
    'bhv_red_coin_star_marker_init',
    'bhv_triplet_butterfly_update',
    'bhv_bubba_loop',
    'bhv_intro_lakitu_loop',
    'bhv_intro_peach_loop',
    'bhv_end_birds_1_loop',
    'bhv_end_birds_2_loop',
    'bhv_intro_scene_loop',
    'bhv_dust_smoke_loop',
    'bhv_yoshi_loop',
    'bhv_volcano_trap_loop',

    # mario_misc.h
    'bhv_toad_message_init',
    'bhv_toad_message_loop',
    'bhv_unlock_door_star_init',
    'bhv_unlock_door_star_loop',

    # Other
    'load_object_collision_model',
    'obj_set_secondary_camera_focus',

    # Menu related
    'lvl_intro_update',
    'geo_intro_super_mario_64_logo',
    'geo_intro_tm_copyright',
    'geo_intro_regular_backdrop',
    'geo_draw_mario_head_goddard',

    # Custom
    'bhv_blue_coin_number_loop',
    'bhv_blue_coin_switch_init',
    'bhv_star_number_loop',
    'spawn_star_number',
    'bhv_ferris_wheel_platform_init',
    'geo_mario_cap_display_list',
]

class BinFile:
    def __init__(self, file=None, filename="", ro=True):
        self.mOffset = 0
        self.mFile = file
        self.mFileName = filename
        self.mReadOnly = ro
        self.mData = None
        self.mSize = 0
    def Offset(self):
        return self.mOffset
    def SetOffset(self, offset):
        self.mOffset = offset
    def OpenR(self, name):
        self.mFile = open(name, "rb")
        self.mFileName = name
        self.mReadOnly = True
        self.mFile.seek(0, 2)  # Move to end of file
        self.mSize = self.mFile.tell()
        self.mFile.seek(0)  # Reset to start
        self.mData = self.mFile.read(self.mSize)
        self.mOffset = 0
        return self
    def OpenW(self, name):
        self.mFile = open(name, "wb")
        self.mReadOnly = False
        self.mFileName = name
        self.mOffset = 0
        self.mFile.seek(0)
        return self
    def Close(self):
        if self.mFile:
            self.mFile.close()
        self.mFile = None
        self.mSize = 0
        self.mData = None
        self.mFileName = ""
    def Read(self, size):
        self.mFile.seek(self.mOffset)
        result = self.mFile.read(size)
        self.mOffset += size
        return result
    def Write(self, buf, size=1):
        if not self.mReadOnly:
            self.mFile.seek(self.mOffset)
            if type(buf) == int:
                result = self.mFile.write(int(buf).to_bytes())
            elif type(buf) == str:
                result = self.mFile.write(buf.encode("ascii"))
            else:
                result = self.mFile.write(buf)
            self.mOffset += size
            return result
    def ReadFloat(self):
        float_bytes = self.Read(4)
        return struct.unpack('<f', float_bytes)[0]
    def ReadInt16(self):
        int16_bytes = self.Read(2)
        return struct.unpack('<h', int16_bytes)[0]
    def ReadInt8(self):
        byte_value = self.Read(1)
        return int.from_bytes(byte_value, 'little')
    def Skip(self, amount):
        self.mOffset += amount

class String:
    def __init__(self, buffer=""):
        self.buffer = buffer
    def Read(self, binfile: BinFile):
        sizeofname = int.from_bytes(binfile.Read(1), 'little')
        self.buffer = binfile.Read(sizeofname).decode()
    def Write(self, binfile: BinFile):
        sizeofname = len(self.buffer)
        binfile.Write(sizeofname, 1)
        binfile.Write(self.buffer, sizeofname)
    def begin(self):
        return self.buffer
    
def ReadName(binfile: BinFile) -> String:
    name = String()
    name.Read(binfile)
    return name

def ReadBytes(binfile:BinFile, bytes:int):
    return int.from_bytes(binfile.Read(bytes), 'little')

def DynosGetFuncNameFromIndex(index):
    if (index >= 0 and index < len(sDynosBuiltinFuncs)): return sDynosBuiltinFuncs[index]

def DynosPointerRead(val, binfile, cannull=False):
    if val == FUNCTION_CODE: 
        funcindex = ReadBytes(binfile, 4)
        return DynosGetFuncNameFromIndex(funcindex)
    elif val == POINTER_CODE: 
        ptrname = ReadName(binfile)
        ptrdata = ReadBytes(binfile, 4)
        return ptrname
    if cannull:
        return "NULL"
    else:
        return None