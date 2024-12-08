"""
Author: Richard Naud
"""

from math import erf
from numpy import arange, zeros, where, transpose, array, argmin

def SpatiallyIntegratedKernel(xranged,sigma,sprime):
  vint = erf((xranged+sprime)/sigma)-erf((xranged-sprime)/sigma)
  return vint

def StimRecurr(theta,sigma_ee,Aee,Aie,Aei,Aii,I,Ilims=(0,600),dI=500,xlims=(0,600),ds=.1,dt=0.01,T=2): # time in unit of tau
  I0range = arange(Ilims[0],Ilims[1],dI)
  xranged = arange(xlims[0],xlims[1],ds)
  ranget = arange(0,T,dt)

  sprimenew = zeros(len(I0range))
  sprimenew_i = zeros(len(I0range))
  sprime_norec = zeros(len(I0range))

  V = zeros((len(xranged),len(I0range)))
  V_i = zeros((len(xranged),len(I0range)))

  sprimemat = zeros((len(ranget),len(I0range)))
  sprimemat_i = zeros((len(ranget),len(I0range)))
  
  for I0 in I0range:
    I0ind = where(I0==I0range)[0]
    V0 = I(0,I0)
    sprime_norec[I0ind] = argmin(abs(theta- I(xranged,I0) ))*ds
    sprimenew[I0ind] = sprime_norec[I0ind]  # no disynaptic activation
    sprimemat[0,I0ind] =sprimenew[I0ind]*1.0
    countiter=0
    V[:,I0ind]= transpose(array([I(xranged,I0)]))
    for t in ranget:
        vsyn_e= transpose(array([SpatiallyIntegratedKernel(xranged,sigma_ee,sprimenew[I0ind])]))
        vsyn_i= transpose(array([SpatiallyIntegratedKernel(xranged,sigma_ee,sprimenew_i[I0ind])])) # same sigmas for the moment

        V[:,I0ind] += dt*(-V[:,I0ind]+Aee*vsyn_e-Aie*vsyn_i)

        vsyn_e= transpose(array([SpatiallyIntegratedKernel(xranged,sigma_ee,sprimenew[I0ind])])) # same sigmas for the moment
        vsyn_i= transpose(array([SpatiallyIntegratedKernel(xranged,sigma_ee,sprimenew_i[I0ind])])) # same sigmas for the moment

        V_i[:,I0ind] += dt*(-V_i[:,I0ind]+Aei*vsyn_e-Aii*vsyn_i)

        if sum(V[:,I0ind]>theta)>0:
          sprimenew[I0ind] = argmin(abs(theta-V[:,I0ind]))*ds   
        else:
          sprimenew[I0ind]=0
          
        sprimemat[where(t==ranget)[0],I0ind] =sprimenew[I0ind]*1.0

        if sum(V_i[:,I0ind]>theta)>0:
          sprimenew_i[I0ind] = argmin(abs(theta-V_i[:,I0ind]))*ds  
        else:
          sprimenew_i[I0ind]   

        sprimemat_i[where(t==ranget)[0],I0ind] =sprimenew_i[I0ind]*1.0
  return sprimemat,sprimemat_i,sprime_norec,V,V_i,xranged,I0range

print(StimRecurr(100,100,100,100,100,100,arange(0,600)))