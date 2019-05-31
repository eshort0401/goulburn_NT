import numpy as np

def test_ewan(U, PH, z0=0, z1=15000, dz=1000):
    
    Z = np.arange(z0,z1+dz,dz)

    U_interp = np.empty((
        5,
        np.size(Z),
       5,5
    ))*np.nan
    U_ar = U.U.values
    Z_ar = PH.geopotential.values/9.80665

    for i in range(5):
        for j in range(5):
            for k in range(5):
                
                U_interp[k,:,i,j] = np.interp(Z, Z_ar[k,:,i,j], U_ar[k,:,i,j], left=np.nan, right=np.nan)
                
    return U_interp
