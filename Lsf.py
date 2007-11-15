import Numeric
import LinearAlgebra

def lsf(data, a, n):
	xmat=setxmat(data, a, n)
	yvec=setyvec(data, n)
	return LinearAlgebra.linear_least_squares(xmat, yvec)

def setxmat(data, a, n):
	xmat=Numeric.zeros((n+1,n+1), Numeric.Float64)
	dat64=Numeric.array(data, Numeric.Float64)

	m=len(data)
	
	for i in range(0, n+1):
		for j in range(0, n+1):
			if a[j] == 0:
				xmat[i][j] = 0.0
			else:
				q=i+j
			
				if q == 0:
					xmat[i][j]=m
				else:
					for k in range(0, m):
						if dat64[k][0] == 0.0:
							xmat[i][j] = xmat[i][j] + 1.0
						else:
							xmat[i][j] = xmat[i][j]+dat64[k][0]**q
	
	return xmat
	
def setyvec(data, n):
	yvec=Numeric.zeros(n+1, Numeric.Float64)
	dat64=Numeric.array(data, Numeric.Float64)

	m=len(data)
	for i in range(0, n+1):
		for k in range(0, m):
			q=i
			if q == 0:
				yvec[i]=yvec[i]+dat64[k][1]
			else:
				yvec[i]=yvec[i]+dat64[k][1]*dat64[k][0]**q

	return yvec
