#!/usr/bin/env python
import os, sys, json

template ={
    'name': "GEO",
    'mother': 'air_box',
    'index': None,
    'valid_begin': [0, 0],
    'valid_end': [0, 0],
    'type': None,
    'size': None,
    'material': None,
    'color': [1.0, 1.0, 1.0, 0.5],
}

mm = 1.
cm = 10.
m = 1000.

def main():
    world_length = 4*m
    air_box_length = 3*m
    absorber_length = 20*cm

    hodos_z = [-61*cm-6*cm - 6*cm, -6*cm, 24*cm, 124*cm]
    cells_z = [0, 6*cm, 12*cm, 18*cm]
    opSheets_z = [-3*cm, 3*cm, 9*cm, 15*cm, 21*cm]

    world = build({
        'index': 'world',
        'mother': '',
        'type': 'box',
        'size': [world_length/2, world_length/2, world_length/2],
        'material': 'air',
        'drawstyle': 'wireframe',
        'invisible': 1
    })

    air_box = build({
        'index': 'air_box',
        'mother': 'world',
        'type': 'box',
        'size': [air_box_length/2, air_box_length/2, air_box_length/2],
        'material': 'air',
        'drawstyle': 'wireframe',
        # 'invisible': 1
    })

    virtual_target = build({
        'index': 'virtual_target',
        'type': 'box',
        'size': [5*cm/2, 5*cm/2, 0.01*mm/2],
        'position': [0., 0., -90*cm],
        'material': 'air',
        'color': [1.0, 1.0, 1.0, 0.5],
        'drawstyle': 'wireframe',
    })

    counter1 = build({
        'index': 'counter1',
        'type': 'box',
        'size': [1*cm/2, 1*cm/2, 2*mm/2],
        'position': [0., 0., -80*cm],
        'material': 'polystyrene',
        'color': [1.0, 1.0, 1.0, 0.5],
    })

    counter2 = build({
        'index': 'counter2',
        'type': 'box',
        'size': [1.4*cm/2, 1.4*cm/2, 2*mm/2],
        'position': [0., 0., -80*cm+3*mm],
        'material': 'polystyrene',
        'color': [1.0, 1.0, 1.0, 0.5],
    })

    veto = build({
        'index': 'veto',
        'type': 'box',
        'size': [20*cm/2, 20*cm/2, 0.5*cm/2],
        'position': [0., 0., -8*cm],
        'material': 'polystyrene',
        'color': [1.0, 1.0, 1.0, 0.5],
    })

    veto_hole = build({
        'index': 'veto_hole',
        'mother': 'veto',
        'type': 'box',
        'size': [2*cm/2, 2*cm/2, 0.5*cm/2],
        'position': [0., 0., 0.],
        'material': 'air',
        'color': [0.0, 0.0, 0.0, 0.5],
    })

    absorber = build({
        'index': 'absorber',
        'type': 'box',
        'size': [32*cm/2, 32*cm/2, absorber_length/2],
        'position': [0., 0., hodos_z[1] - 6*cm - absorber_length/2],
        'material': 'hdpe',
        'color': [1.0, 0.0, 1.0, 0.5],
    })

    platform = build({
        'index': 'platform',
        'type': 'box',
        'size': [30*cm/2, 12.7*mm/2, 32*cm/2],
        'position': [0., -54.*mm/2-12.7*mm/2, 9*cm], # 2" pmt is larger than cuvette height
        'material': 'aluminum',
        'color': [0.5, 0.5, 0.5, 0.3],
    })

    pmts = build({
        'index': 'pmts',
        'enable': 1,
        'type': 'pmtarray',
        'pmt_model': "r11065",
        'pmt_detector_type': "idpmt",
        'sensitive_detector': "/mydet/pmt/inner",
        'efficiency_correction': 1.000,
        'pos_table': "PMTINFO",
        'orientation': "manual",
    })

    cuvettes = []
    for i in range(4):
        x = 12.5*mm
        y = 45.*mm
        z = 12.5*mm
        one = build({
            'index': "cuvette%i" % (i+1,),
            'type': "box",
            'size': [x/2, y/2, z/2],
            'position': [0.0, 0.0, cells_z[i]],
            'material': "pyrex",
            'color': [0.0, 1.0, 0.0, 0.5],
        })
        cuvettes.append(one)

    wblss = []
    for i in range(4):
        x = 10.0*mm
        y = 42.5*mm
        z = 10.0*mm
        one = build({
            'index': "wbls%i" % (i+1,),
            'mother': "cuvette%i" % (i+1,),
            'type': "box",
            'size': [x/2, y/2, z/2],
            'position': [0.0, 0.0, 0.0],
            'material': "wbls_1pct",
            'color': [0.0, 0.0, 1.0, 0.5],
        })
        wblss.append(one)

    hodos = []
    for i in range(4):
        x = 2.0*cm
        y = 2.0*cm
        z = 0.5*cm
        if (i==3):  # last hodo
            x = 5.0*cm
            y = 5.0*cm
        one = build({
            'index': "hodo%i" % (i+1,),
            'type': "box",
            'size': [x/2, y/2, z/2],
            'position': [0.0, 0.0, hodos_z[i]],
            'material': "polystyrene",
            'color': [1.0, 0.0, 0.0, 0.5],
        })
        hodos.append(one)

    opSheets = []
    for i in range(5):
        x = 32.0*cm
        y = 16.0*cm
        z = 0.016*mm
        one = build({
            'index': "opSheet%i" % (i+1,),
            'type': "box",
            'size': [x/2, y/2, z/2],
            'position': [0.0, y/2-45*mm/2, opSheets_z[i]],
            'material': "aluminum",
            'color': [0.0, 1.0, 1.0, 0.3],
        })
        opSheets.append(one)


    write(
        world,
        air_box,
        virtual_target,
        counter1,
        counter2,
        veto,
        veto_hole,
        absorber,
        platform,
        pmts,
        *(cuvettes + wblss + opSheets + hodos)
    )


def build(d):
    t = {}
    t.update(template)
    t.update(d)
    return t

def write(*objs):
    f = open('/home/vagrant/app/rat-pac/data/NSRL16A/NSRL16A.geo', 'w')
    for o in objs:
        json.dump(o, f, indent=4)
        f.write('\n')

    f.close()

if __name__ == "__main__":
    main()