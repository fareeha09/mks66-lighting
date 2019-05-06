import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    #light[0]=[0.5,0.75,1]
    A = calculate_ambient(ambient, areflect) 
    D = calculate_diffuse(light, dreflect, normal)
    S = calculate_specular(light, sreflect, view, normal)
	
    #light[COLOR]= limit_color(light[COLOR])
    #print A
    #print D
    #print S
    a=[]
    for i in range(len(light[COLOR])):
        a.append(int(A[i]+D[i]+S[i]))	
	
    return a
	
def calculate_ambient(alight, areflect): #ambient = A * K
    a = [] 
    for i in range(len(alight)):
        a.append(alight[i] * areflect[i])
	
    return a
	
def calculate_diffuse(light, dreflect, normal):
    #diffuse = P * Kd * (N dot L)
	#print normal
	L = normalize(light[LOCATION])
	N = normalize(normal)
	
	#for i in range(3):
	#	print(normalize(normal))
	#	print(normalize(light[LOCATION]))
	
	#print N
	#print L
	
	dot = dot_product(N, L)
	a = []
	
	for i in range(len(light[COLOR])):
		a.append(light[COLOR][i] * dreflect[i] * dot)
		if a[i]<0:
			a[i]=0
	return a
	

def calculate_specular(light, sreflect, view, normal):
    #specular = P * Ks * [((2(N dot L)) N - L) dot V]^x
	L = normalize( light[LOCATION] )
	N = normalize(normal)
	V = normalize(view)
	#print N
	dot = dot_product(N, L)
	
	R = []
	for i in range(3):
		R.append(2 * (dot * N[i]) - L[i])
	
	a = []
	for i in range(len(light[COLOR])):
		a.append(light[COLOR][i] * sreflect[i] * math.pow((dot_product( R , V)), SPECULAR_EXP))
		if a[i]<0:
			a[i]=0
	
	return a
	
def limit_color(color):
    for i in range(len(color)):
		if (color[i] < 0):
			color[i]= 0
		elif (color[i] > 255):
			color[i]= 255
    return color
	
#vector functions
#normalize vector, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
		#print vector[i]
		vector[i] = (vector[i] / magnitude)
		#print vector[i]
	
	#print vector 
    return vector

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
