# Approximation of QoE rating distributions

In the context of QoE management, network and service providers commonly rely on models that map system QoS conditions (e.g., system response time, packet loss, etc.) to estimated end user QoE values. Observable QoS conditions in the system may be assumed to follow a certain distribution, meaning that different end users will experience different conditions. On the other hand, drawing from the results of subjective user studies, we know that user diversity leads to distributions of user scores for any given test conditions (in this case referring to the QoS parameters of interest). Our previous studies have shown that to correctly derive various QoE metrics (e.g., Mean Opinion Score (MOS), quantiles, probability of users rating 'good or better', etc.) in a system under given conditions, there is a need to consider rating distributions obtained from user studies, which are often times not available. In the paper [QoEMAN2020] we extend these findings to show how to approximate user rating distributions given a QoS-to-MOS mapping function and second order statistics. Such a user rating distribution may then be combined with a QoS distribution observed in a system to finally derive corresponding distributions of QoE scores.

## Python Script: Approximation of the QoE distribution with a Beta distribution
A basic script is provided which approximates a QoE distribution with a Beta distribution for given MOS and SOS parameter. In addition an example script is provided to illustrate the usage of the basic functions.

## Investigators
The investigators in this research are
* Tobias Hoßfeld (tobias.hossfeld@uni-wuerzburg.de), Professor and head of [Chair of Communication Networks, University of Würzburg](http://www.comnet.informatik.uni-wuerzburg.de/)
* Poul E. Heegaard
* Martin Varela
* Lea Skorin-Kapov
* Markus Fiedler (markus.fiedler@bth.se), Professor and responsible for the area of media technology at [Blekinge Institute of Technology](http://www.bth.se/)

## Copyright Notice
This tool is published under the license: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Permission is hereby granted, without written agreement and without license or royalty fees, to use, copy, modify, and distribute this tool and its documentation for any purpose, provided that the copyright notice in its entirety appear in all copies of this tool, and the original source of this tool is acknowledged in any publication that reports research using this tool. If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

Originial source: The following paper is to be cited in the bibliography whenever the tool is used. 
* **[QoEMAN2020]** Tobias Hossfeld, Poul E. Heegaard, Martin Varela, Lea Skorin-Kapov, Markus Fiedler. "From QoS Distributions to QoE Distributions: a System's Perspective". Accepted for publication in the 4th International Workshop on Quality of Experience Management (QoE Management 2020), featured by IEEE Conference on Network Softwarization (IEEE NetSoft 2020), Ghent, Belgium.
