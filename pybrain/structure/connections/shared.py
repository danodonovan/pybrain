__author__ = 'Tom Schaul, tom@idsia.ch'

from pybrain.structure.parametercontainer import ParameterContainer
from connection import Connection
from pybrain.utilities import Named
from full import FullConnection


class OwnershipViolation(Exception):
    """ Exception raised when one attempts to write-access the parameters of the 
        SharedConnection, instead of its mother. """


class MotherConnection(ParameterContainer, Named):
    """ The container for the shared parameters of connections (just a container with a constructor, actually). """
    
    nbparams = None
    
    # TODO: maybe all sibling connections should register themselves here?
    def __init__(self, nbparams, std = 1., name = None):
        self.name = name
        self.setArgs(nbparams = nbparams)
        self.initParams(nbparams, std)
            

class SharedConnection(Connection):
    """  A shared connection can link different couples of modules, with a single set of parameters. """
    
    mother = None
    
    def __init__(self, mother, *args, **kwargs):
        Connection.__init__(self, *args, **kwargs)
        self._replaceParamsByMother(mother)
        
    def _replaceParamsByMother(self, mother):
        self.setArgs(mother = mother)
        self.paramdim = self.mother.paramdim
            
    def initParams(self, *args): raise OwnershipViolation
    def getParameters(self): return self.mother.getParameters()
    def _setParameters(self, *args): raise OwnershipViolation    
    def getDerivatives(self): return self.mother.getDerivatives()
    def _setDerivatives(self, *args): raise OwnershipViolation
    def resetDerivatives(self): raise OwnershipViolation
    
    def _getName(self):
        return self.mother.name if self._name is None else self._name

    def _setName(self, newname):
        self._name = newname
        
    name = property(_getName, _setName)
    
        
class SharedFullConnection(SharedConnection, FullConnection): 
    """ shared version of FullConnection """
    
    def _forwardImplementation(self, inbuf, outbuf):
        FullConnection._forwardImplementation(self, inbuf, outbuf)
    
    def _backwardImplementation(self, outerr, inerr, inbuf):
        FullConnection._backwardImplementation(self, outerr, inerr, inbuf)
    