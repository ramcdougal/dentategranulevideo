# linux only movie generation of a firing dentate gyrus granule cell

try:
    from neuron import h, gui
except:
    print('This simulation requires NEURON with Python support.')
    print('See: http://neuron.yale.edu')
    import sys
    sys.exit()

# setup directories
import os
try:
    os.makedirs('images')
except:
    os.system('rm -fr images')
    os.makedirs('images')

# load the morphology
h.load_file('n275.hoc')

# setup the discretization
for sec in h.allsec():
    sec.nseg = 21

# add ion channels
for sec in h.allsec():
    if 'dend' not in sec.name():
        sec.insert('hh')


# setup graphics
ps = h.PlotShape(0)
ps.size(-416.826, 396.319, -486.465, 472.666)
ps.variable('v')
ps.view(-416.826, -486.465, 813.145, 959.13, 151, 52, 559.68, 660.16)
h.fast_flush_list.append(ps)
ps.exec_menu('Shape Plot')
ps.exec_menu('Show Diam')
h.graphList[0].append(ps)

# initialize simulation
h.finitialize(-65)

# setup current pulses to trigger APs
fire_times = [0, 15, 23, 31]
iclamps = []
for time in fire_times:
    iclamp = h.IClamp(h.soma[0](0.5))
    iclamp.delay = time
    iclamp.amp = 2
    iclamp.dur = 0.5
    iclamps.append(iclamp)

image_count = 0
save_every = 10

def savefig():
    global image_count
    filename = 'images/%04.2f.ps' % h.t
    ps.printfile(filename)
    # fatten the lines in the image to make it easier to see
    lines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == '0 setlinewidth':
                line = '5 setlinewidth'
            lines.append(line)
    # now rewrite the file with the thicker linewidth
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    # now convert it to a png
    png_filename = 'images/image%04d.png' % image_count
    image_count += 1
    os.system('convert %s -crop 558x660+0+0 %s' % (filename, png_filename))

# stop time
stop_time = 45

#
# run the simulation, storing the values
#

segs = []
for sec in h.allsec():
    segs.extend([seg for seg in sec])

values = []
advance_count = 0
while h.t < stop_time:
    h.fadvance()
    if advance_count % save_every == 0:
        values.append([seg.v for seg in segs])
    advance_count += 1
    print(h.t)

#
# now fatten everything up (so we can see it) and save the graphics
# note: handle the soma differently by scaling in all directions not just diam
#
scale = 5
import numpy
for sec in h.allsec():
    if 'soma' not in sec.name():
        for i in range(sec.n3d()):
            d = sec.diam3d(i)
            sec.pt3dchange(i, d * scale)
    elif 'soma' in sec.name():
        x, y, z, diam = [], [], [], []
        for i in range(sec.n3d()):
            x.append(sec.x3d(i))
            y.append(sec.y3d(i))
            z.append(sec.z3d(i))
            diam.append(sec.diam3d(i))
        sec.pt3dclear()
        x, y, z, diam = scale * numpy.array(x), scale * numpy.array(y), scale * numpy.array(z), scale * numpy.array(diam)
        i = int(len(x) / 2)
        midptx, midpty, midptz = x[i], y[i], z[i]
        x -= midptx / 2.
        y -= midpty / 2.
        z -= midptz / 2.
        for xpt, ypt, zpt, diampt in zip(x, y, z, diam):
            sec.pt3dadd(xpt, ypt, zpt, diampt)



# begin with a full rotation for 40 frames
for i in range(40):
    ps.rotate(0, 0, 0, 0, 6.283 / 40., 0)
    h.doNotify()
    savefig()

# for each stored value set: apply, then save a picture
for i, value in enumerate(values):
    for v, s in zip(value, segs):
        s.v = v
    if i < 40:
        ps.rotate(0, 0, 0, 0, 6.283 / 40., 0)
    h.doNotify()
    savefig()
    print('i = %d' % i)

# convert the pictures to a video
os.system('rm -f movie.mp4')
os.system('avconv -qscale 5 -r 20 -b 9600 -i images/image%04d.png movie.mp4')
