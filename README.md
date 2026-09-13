![](https://github.com/hasii2011/code-ally-basic/blob/master/developer/agpl-license-web-badge-version-2-256x48.png "AGPL")

[![CI](https://github.com/hasii2011/py-force-directed-layout/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/hasii2011/py-force-directed-layout/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/pyforcedirectedlayout.svg)](https://badge.fury.io/py/pyforcedirectedlayout)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/hasii2011/py-force-directed-layout/graphs/commit-activity)


# Introduction
This project is the Python implementation of Brad Smith's article on [A Forced-Directed Diagram Layout Algorithm](https://www.brad-smith.info/blog/archives/129).  There were a few 
bumps on the road to get Brad's code manually converted from a Microsoft graphics platform to a pseudo-platform independent platform like [wxPython](https://wxpython.org) 
running on Mac OS.  I will not go into detail on what those bumps were.  But I want to make sure and document those [here](https://hsanchezii.wordpress.com).



# Details

## Install in your virtual environment

```bash
pip install pyforcedirectedlayout
```

## Configuration details

### These drive the algorithm

| Parameter       | Default Value | Description                                                                                     |
|-----------------|---------------|-------------------------------------------------------------------------------------------------|
| damping         | 0.1           | Value between 0 and 1 that slows the motion of the nodes during layout.                         |
| springLength    | 100           | Value in pixels representing the length of the imaginary springs that run along the connectors. |
| maxIterations   | 500           | Maximum number of iterations before the algorithm terminates                                    |
| attractionForce | 0.1           | The spring value                                                                                |
| repulsionForce  | 10000         | The repulsion value                                                                             |

### Randomize the layout

| Parameter | Default Value     | Description |
|-----------|:------------------|-------------|
| minPoint  | Point(x=10, y=10) |             |
| maxPoint  | Point(x=60, y=60) |             |

### Early Termination


| Parameter                | Default Value | Description                                                                                                               |
|--------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------|
| minimumTotalDisplacement | 10            |                                                                                                                           |
| stopCount                | 15            | Stop execution after this many number of iterations where the `totalDisplacement` is less that `minimumTotalDisplacement` |

## Developer Notes

This project uses [buildlackey](https://github.com/hasii2011/buildlackey) for day-to-day development builds

___

# Note
For all kinds of problems, requests, enhancements, bug reports, etc., drop me an e-mail.
Written by <a href="mailto:humberto.a.sanchez.ii@gmail.com?subject=Hello Humberto">Humberto A. Sanchez II</a>  ©2026


[Copilot Statement](https://github.com/hasii2011/code-ally-basic/wiki/GitHub-Copilot).
