#!/usr/bin/env python
import os, sys, json

template ={
    'name': "GEO",
    'mother': 'air_box',
    'index': None,
    'valid_begin': [0, 0],
    'valid_end': [0, 0],
    'type': None,
    'material': None,
    'color': [1.0, 1.0, 1.0, 0.5],
}

mm = 1.
cm = 10.
m = 1000.
inch = 25.4

def main():
    world_length = 4*m
    dark_box_length = 2.5*m
    dark_box_thickness = 3*cm
    air_box_length = dark_box_length - 2*dark_box_thickness

    tank_offset = [0, 0, 0.15*m]
    acrylic_material = 'acrylic_uvt'
    acrylic_color =  [1.0, 1.0, 0.0, 0.5]
    filling_material = 'water'
    filling_color = [0.0, 1.0, 0.0, 0.5]

    acrylic_thickness = 25.4*mm
    acrylic_wall_inner_radius = 0.995*m/2
    acrylic_wall_outer_radius = acrylic_wall_inner_radius+acrylic_thickness
    acrylic_wall_height = 1.25*m

    teflon_wall_gap = 12.5*mm
    teflon_wall_thickness = 1./8*inch
    teflon_wall_outer_radius = acrylic_wall_inner_radius - teflon_wall_gap
    teflon_wall_inner_radius = teflon_wall_outer_radius - teflon_wall_thickness
    teflon_wall_height = acrylic_wall_height

    acrylic_lid_outer_radius = 1.150*m/2
    acrylic_lid_thickness = acrylic_thickness
    side_hole_offset = -0.2937*m  # x-axis
    port_inner_radius = 0.1778*m/2
    port_outer_radius = 0.2032*m/2
    port_height = 0.12*m
    port_flange_outer_radius = 0.2762*m/2
    port_position_z = acrylic_wall_height/2+acrylic_lid_thickness+port_height/2
    overflow_height = port_height / 2
    overflow_position_z = acrylic_wall_height/2+acrylic_lid_thickness+overflow_height/2

    frame_thickness = 3.8*cm/2
    frame_platform_height = 0.7*m
    frame_platform_dimension = [1.3*m/2, 1.3*m/2, frame_thickness/2]
    frame_bar_group_dimension =  add([-frame_thickness, -frame_thickness, 0], frame_platform_dimension)
    frame_bar_dimension = [frame_bar_group_dimension[0], frame_thickness/2, frame_thickness/2]
    frame_bar_spacing = 0.2*m
    frame_color = [0.0, 1.0, 1.0, 0.2]


    world = build({
        'index': 'world',
        'mother': '',
        'type': 'box',
        'size': [world_length/2, world_length/2, world_length/2],
        'material': 'air',
        'drawstyle': 'wireframe',
        'invisible': 1
    })

    dark_box = build({
        'index': 'dark_box',
        'mother': 'world',
        'type': 'box',
        'size': [dark_box_length/2, dark_box_length/2, dark_box_length/2],
        'material': 'cardboard',
        'drawstyle': 'wireframe',
        # 'invisible': 1
    })

    air_box = build({
        'index': 'air_box',
        'mother': 'dark_box',
        'type': 'box',
        'size': [air_box_length/2, air_box_length/2, air_box_length/2],
        'material': 'air',
        'drawstyle': 'wireframe',
        # 'invisible': 1
    })

    acrylic_wall = build({
        'index': "acrylic_wall",
        'type': "tube",
        'r_max': acrylic_wall_outer_radius,
        'r_min': acrylic_wall_inner_radius,
        'size_z': acrylic_wall_height/2,
        'position': add([0.0, 0.0, 0.0], tank_offset) ,
        'material': acrylic_material,
        'color': acrylic_color,
    })

    center_detector = build({
        'index': "cd",
        'type': "tube",
        'r_max': acrylic_wall_inner_radius,
        'size_z': acrylic_wall_height/2,
        'position': add([0.0, 0.0, 0.0], tank_offset) ,
        'material': filling_material,
        'color': filling_color,
    })

    teflon_wall = build({
        'index': "teflon_wall",
        'mother': "cd",
        'type': "tube",
        'r_max': teflon_wall_outer_radius,
        'r_min': teflon_wall_inner_radius,
        'size_z': teflon_wall_height/2,
        'position': [0.0, 0.0, 0.0],
        'material': "ptfe",
        'color': [1.0, 1.0, 1.0, 0.3],
    })

    acrylic_bottom = build({
        'index': "acrylic_bottom",
        'type': "tube",
        'r_max': acrylic_wall_outer_radius,
        'size_z': acrylic_thickness/2,
        'position': add([0.0, 0.0, -acrylic_wall_height/2 - acrylic_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    acrylic_flange = build({
        'index': "acrylic_flange",
        'type': "tube",
        'r_max': acrylic_lid_outer_radius,
        'r_min': acrylic_wall_outer_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': add([0.0, 0.0, acrylic_wall_height/2 - acrylic_lid_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    acrylic_lid = build({
        'index': "acrylic_lid",
        'type': "tube",
        'r_max': acrylic_lid_outer_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': add([0.0, 0.0, acrylic_wall_height/2 + acrylic_lid_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    center_hole = build({
        'index': "center_hole",
        'mother': "acrylic_lid",
        'type': "tube",
        'r_max': port_inner_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': [0.0, 0.0, 0.0],
        'material': filling_material,
        'color': filling_color,
    })

    side_hole = build({
        'index': "side_hole",
        'mother': "acrylic_lid",
        'type': "tube",
        'r_max': port_inner_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': [side_hole_offset, 0.0, 0.0],
        'material': filling_material,
        'color': filling_color,
    })

    center_port_wall = build({
        'index': "center_port_wall",
        'type': "tube",
        'r_max': port_outer_radius,
        'r_min': port_inner_radius,
        'size_z': port_height/2,
        'position': add([0.0, 0.0, port_position_z], tank_offset) ,
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    side_port_wall = build({
        'index': "side_port_wall",
        'type': "tube",
        'r_max': port_outer_radius,
        'r_min': port_inner_radius,
        'size_z': port_height/2,
        'position': add([side_hole_offset, 0.0, port_position_z], tank_offset) ,
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    center_port_flange = build({
        'index': "center_port_flange",
        'type': "tube",
        'r_max': port_flange_outer_radius,
        'r_min': port_outer_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': add([0.0, 0.0, port_position_z+port_height/2-acrylic_lid_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    side_port_flange = build({
        'index': "side_port_flange",
        'type': "tube",
        'r_max': port_flange_outer_radius,
        'r_min': port_outer_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': add([side_hole_offset, 0.0, port_position_z+port_height/2-acrylic_lid_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    center_port_lid = build({
        'index': "center_port_lid",
        'type': "tube",
        'r_max': port_flange_outer_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': add([0.0, 0.0, port_position_z+port_height/2+acrylic_lid_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    side_port_lid = build({
        'index': "side_port_lid",
        'type': "tube",
        'r_max': port_flange_outer_radius,
        'size_z': acrylic_lid_thickness/2,
        'position': add([side_hole_offset, 0.0, port_position_z+port_height/2+acrylic_lid_thickness/2], tank_offset),
        'material': acrylic_material,
        'color':  acrylic_color,
    })

    center_overflow = build({
        'index': "center_overflow",
        'type': "tube",
        'r_max': port_inner_radius,
        'size_z': overflow_height/2,
        'position': add([0.0, 0.0, overflow_position_z], tank_offset),
        'material': filling_material,
        'color':  filling_color,
    })

    side_overflow = build({
        'index': "side_overflow",
        'type': "tube",
        'r_max': port_inner_radius,
        'size_z': overflow_height/2,
        'position': add([side_hole_offset, 0.0, overflow_position_z], tank_offset),
        'material': filling_material,
        'color':  filling_color,
    })

    frame_platform = build({
        'index': 'frame_platform',
        'type': 'box',
        'size': frame_platform_dimension,
        'position': add([0.0, 0.0, -acrylic_wall_height/2 - acrylic_thickness - frame_bar_dimension[2]], tank_offset),
        'material': 'aluminum',
        'color': frame_color,
    })

    frame_bar_group = build({
        'index': 'frame_bar_group',
        'mother': 'frame_platform',
        'type': 'box',
        'size': frame_bar_group_dimension,
        'material': 'air',
        'color': [0.0, 0.0, 0.0, 0.2],
    })

    # NOTE: the "replica" method assumes no gaps replicas fill up the entire mother volume, not useful here
    frame_bar = []
    N = 6
    for i in range(N):
        frame_bar.append(build({
            'index': 'frame_bar_%i' % (i,),
            'mother': 'frame_bar_group',
            'type': 'box',
            'size': frame_bar_dimension,
            'position': [0.0, frame_bar_spacing*(-(N-1.0)/2+i), 0.0],
            'material': 'aluminum',
            # 'replicas': 6,
            # 'replica_axis': 'y',
            # 'replica_spacing': frame_bar_spacing,
            'color': frame_color,
        }))

    frame_bottom_dimension = [(frame_bar_spacing*5+frame_thickness)/2, (frame_bar_spacing*5+frame_thickness)/2, frame_thickness/2]
    frame_bottom = build({
        'index': 'frame_bottom',
        'type': 'box',
        'size': frame_bottom_dimension,
        'position': add([0.0, 0.0, -acrylic_wall_height/2 - acrylic_thickness - frame_platform_height + frame_thickness/2], tank_offset),
        'material': 'aluminum',
        'color': frame_color,
    })

    frame_bottom_cut = build({
        'index': 'frame_bottom_cut',
        'mother': 'frame_bottom',
        'type': 'box',
        'size': add([-frame_thickness, -frame_thickness, 0], frame_bottom_dimension),
        'material': 'air',
        'color': [0.0, 0.0, 0.0, 0.2],
    })

    frame_bottom_bar = build({
        'index': 'frame_bottom_bar',
        'mother': 'frame_bottom_cut',
        'type': 'box',
        'size': [frame_thickness/2, frame_bottom_dimension[1]-frame_thickness/2, frame_thickness/2],
        'material': 'aluminum',
        'color': frame_color,
    })

    frame_leg_left_group = build({
        'index': 'frame_leg_left_group',
        'type': 'box',
        'size': [frame_thickness/2, frame_platform_dimension[1], (frame_platform_height-frame_thickness*2)/2],
        'position': add([-frame_bottom_dimension[0]+frame_thickness/2, 0.0, -acrylic_wall_height/2 - acrylic_thickness - frame_platform_height/2], tank_offset),
        'material': 'air',
        'drawstyle': 'wireframe',
        'invisible': 1,
    })

    frame_leg_left = []
    for i in range(N):
        frame_leg_left.append(build({
            'index': 'frame_leg_left_%i' % (i,),
            'mother': 'frame_leg_left_group',
            'type': 'box',
            'size': [frame_thickness/2, frame_thickness/2, (frame_platform_height-frame_thickness*2)/2],
            'position': [0.0, frame_bar_spacing*(-(N-1.0)/2+i), 0.0],
            'material': 'aluminum',
            'color': frame_color,
        }))

    frame_leg_center_group = build({
        'index': 'frame_leg_center_group',
        'type': 'box',
        'size': [frame_thickness/2, frame_platform_dimension[1], (frame_platform_height-frame_thickness*2)/2],
        'position': add([0.0, 0.0, -acrylic_wall_height/2 - acrylic_thickness - frame_platform_height/2], tank_offset),
        'material': 'air',
        'drawstyle': 'wireframe',
        'invisible': 1,
    })

    frame_leg_center = []
    for i in range(N):
        frame_leg_center.append(build({
            'index': 'frame_leg_center_%i' % (i,),
            'mother': 'frame_leg_center_group',
            'type': 'box',
            'size': [frame_thickness/2, frame_thickness/2, (frame_platform_height-frame_thickness*2)/2],
            'position': [0.0, frame_bar_spacing*(-(N-1.0)/2+i), 0.0],
            'material': 'aluminum',
            'color': frame_color,
        }))

    frame_leg_right_group = build({
        'index': 'frame_leg_right_group',
        'type': 'box',
        'size': [frame_thickness/2, frame_platform_dimension[1], (frame_platform_height-frame_thickness*2)/2],
        'position': add([frame_bottom_dimension[0]-frame_thickness/2, 0.0, -acrylic_wall_height/2 - acrylic_thickness - frame_platform_height/2], tank_offset),
        'material': 'air',
        'drawstyle': 'wireframe',
        'invisible': 1,
    })

    frame_leg_right = []
    for i in range(N):
        frame_leg_right.append(build({
            'index': 'frame_leg_right_%i' % (i,),
            'mother': 'frame_leg_right_group',
            'type': 'box',
            'size': [frame_thickness/2, frame_thickness/2, (frame_platform_height-frame_thickness*2)/2],
            'position': [0.0, frame_bar_spacing*(-(N-1.0)/2+i), 0.0],
            'material': 'aluminum',
            'color': frame_color,
        }))

    pmts = build({
        'index': "pmts",
        'enable': 1,
        'type': "pmtarray",
        'pmt_model': "r7723",
        'pmt_detector_type': "idpmt",
        'sensitive_detector': "/mydet/pmt/inner",
        'efficiency_correction': 1.000,
        'pos_table': "PMTINFO",
        'orientation': "manual",
    })

    other_objects = frame_bar + frame_leg_left + frame_leg_center + frame_leg_right
    write(
        world,
        dark_box,
        air_box,
        acrylic_wall,
        center_detector,
        teflon_wall,
        acrylic_bottom,
        acrylic_flange,
        acrylic_lid,
        center_hole,
        side_hole,
        center_port_wall,
        side_port_wall,
        center_port_flange,
        side_port_flange,
        center_port_lid,
        side_port_lid,
        center_overflow,
        side_overflow,
        pmts,
        frame_platform,
        frame_bar_group,
        frame_bottom,
        frame_bottom_cut,
        frame_bottom_bar,
        frame_leg_left_group,
        frame_leg_center_group,
        frame_leg_right_group,
        *other_objects
    )

    # write PMT info
    pmt_bot_z = -acrylic_wall_height/2 - acrylic_thickness + tank_offset[2]
    pmt_top_z = acrylic_wall_height/2 + acrylic_lid_thickness + tank_offset[2]
    pmt_info = {
        'name': "PMTINFO",
        'valid_begin': [0, 0],
        'valid_end': [0, 0],
        'x': [-400.0, -200.0, 0.0, 300.0, -200.0, 200.0],
        'y': [0.0]*4 + [-200.0,   0.0],
        'z': [pmt_bot_z]*4 + [pmt_top_z]*2,
        'dir_x': [0.0]*6,
        'dir_y': [0.0]*6,
        'dir_z': [1.0]*4 + [-1.0]*2,
        'type': [0]*6,
    }
    f = open('/home/vagrant/app/rat-pac/data/BNL1ton/PMTINFO.ratdb', 'w')
    json.dump(pmt_info, f, indent=4)
    f.write('\n')
    f.close()

def add(x, y):
    return [a + b for a, b in zip(x, y)]

def build(d):
    t = {}
    t.update(template)
    t.update(d)
    return t


def write(*objs):
    f = open('/home/vagrant/app/rat-pac/data/BNL1ton/BNL1ton.geo', 'w')
    for o in objs:
        json.dump(o, f, indent=4)
        f.write('\n')

    f.close()

if __name__ == "__main__":
    main()