The script runme.py generates a movie of a firing dentate gyrus granule cell.

The cell morphology was taken from NeuroMorpho.Org (see below). Hodgin-Huxley
ion channels were inserted in the soma and axon. The cell fires due to current
injected into its soma.

The script has been tested in Ubuntu 14.04. It requires the ImageMagick image
conversion tools, avconv (available via "sudo apt-get install libav-tools"),
and the NEURON simulator (http://neuron.yale.edu).

As this simulation uses squid ion channels in a mammalian cell, it should not
be viewed as a realistic model; instead, consider this code as an example of
how to generate a video with NEURON and as a crude example of action potential
propagation.




This simulation uses the Dentate Gyrus Granule Cell n275 from

http://neuromorpho.org/neuroMorpho/neuron_info.jsp?neuron_name=n275

(The corresponding file n275.swc is included in the archive for reference, but
is not directly used in the simulation. The NEURON translated version, n275.hoc
is used instead.)


See:

Cannon, R. C., Turner, D. A., Pyapali, G. K., & Wheal, H. V. (1998). An on-line archive of reconstructed hippocampal neurons. Journal of neuroscience methods, 84(1), 49-54.

Ascoli, G. A., Donohue, D. E., & Halavi, M. (2007). NeuroMorpho. Org: a central resource for neuronal morphologies. The Journal of Neuroscience, 27(35), 9247-9251.
