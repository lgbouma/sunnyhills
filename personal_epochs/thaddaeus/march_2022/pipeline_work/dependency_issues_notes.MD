# dependency hell notes
* When numpy version > 1.22, numba has an issue (numpy version needs to be < 1.22)
    * which module needs numba? 
* However, when numpy is set to a 1.21 version, e.g. 1.21.5, then the numpy.core.multiarray fails to import. 
    * seems like batman uses this