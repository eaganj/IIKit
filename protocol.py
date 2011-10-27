# -*- coding: utf-8 -*-
#
# IIKit -- the Instrumental Interaction Toolkit
# Copyright 2009-2011, Université Paris-Sud
# by James R. Eagan (code at my last name dot me)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with this program.  
# If not, see <http://www.gnu.org/licenses/>.

import jre.debug

class Protocol(object):
    kind = []
    signature = []
    
    # FIXME: bindings are currently memoized by object class, which means that a class' objects can either
    # always conform or never conform; conformance can not change over time, e.g. as its state changes.
    _bindings = {}
    
    @classmethod
    def objectConforms(cls, obj):
        # TODO: implement binding support
        # We can't short-circuit in WILD because all iStar objects are of the same class but have different
        # sets of attributes.
        # result = cls._bindings.get(obj.__class__, None)
        # if result is not None:
        #     return result
            
        for k in cls.kind:
            if isinstance(obj, k):
                cls._bindings[obj.__class__] = True
                return True 
        
        # Object does not match any type signatures.  Try method signatures instead.
        for signature in cls.signature:
            for method in signature:
                if not hasattr(obj, method):
                    break
            else:
                cls._bindings[obj.__class__] = True
                return True # signature matches
                    
        # No matching signature found.
        cls._bindings[obj.__class__] = False
        return False
    
    def bindObject(self, obj):
        # TODO : implement proper binding support
        return obj

__all__ = ('Protocol',)

if __name__ == '__main__':
    from jre.compat import namedtuple
    class Point(Protocol):
        signature = [ 'x y'.split(), ]
    
    class Rect(Protocol):
        signature = [ 'x y width height'.split() ]
    
    point = namedtuple('Point', 'x, y')(1, 2)
    rect = namedtuple('Rect', 'x y width height')(1, 2, 3, 4)
    
    assert Point.objectConforms(point)
    assert Point.objectConforms(rect)
    assert Rect.objectConforms(rect)
    assert not Rect.objectConforms(point)