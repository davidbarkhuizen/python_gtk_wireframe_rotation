import math

class Point2D(object):
    def __init__(self, x=None,y=None):
        self.x = x
        self.y = y

class Point3D(object):
    def __init__(self, x=None,y=None,z=None):
        self.x = x
        self.y = y
        self.z = z        

class Rot(object):
    
    rad_const = math.pi / 180.0  
    
    def rad(self, theta):
        return theta * Rot.rad_const    
        
    def __init__(self):
        
        self.sin_table = []
        self.cos_table = []
        
        for d in range(360):
            self.sin_table.append(math.sin(self.rad(d)))
            self.cos_table.append(math.cos(self.rad(d)))
        
        for i in [1]: # points            
            self.points = []        
            for i in range(24):
                self.points.append(Point3D())

            self.points[0].x =  10.0 
            self.points[0].z =   4.0
            self.points[1].x =   4.0
            self.points[1].z =  10.0
            self.points[2].x =  -4.0 
            self.points[2].z =  10.0
            self.points[3].x = -10.0 
            self.points[3].z =   4.0
            self.points[4].x = -10.0 
            self.points[4].z =  -4.0
            self.points[5].x =  -4.0 
            self.points[5].z = -10.0
            self.points[6].x =   4.0 
            self.points[6].z = -10.0
            self.points[7].x =  10.0 
            self.points[7].z =  -4.0

            for i in range(8):
                self.points[i].y = 30.0

            for i in range(8, 16):
                self.points[i].x = self.points[i - 8].x
                self.points[i].z = self.points[i - 8].z
                self.points[i].y = -30.0

            self.points[16].x =  20.0
            self.points[16].z =  20.0
            self.points[17].x = -20.0
            self.points[17].z =  20.0
            self.points[18].x = -20.0
            self.points[18].z = -20.0
            self.points[19].x =  20.0
            self.points[19].z = -20.0

            for i in range(16, 20):
                self.points[i].y = 30.0

            for i in range(20, 24):
                self.points[i].x = self.points[i - 4].x
                self.points[i].z = self.points[i - 4].z
                self.points[i].y = -30.0        
            
        
        self.x_off = 320.0
        self.y_off = 240.0
        self.z_off = 50.0

        self.z_deg = 0
        self.x_deg = 0
        self.y_deg = 0
            
    def flatten(self, cube):
        '''
        320 : 200 => 1 : 5 / 8 |  a.r of 4 : 3, height = 4 / 3 of width, therefore
        x : y => 1 : 5 / 6
        '''
        
        n = len(self.points)
        
        x_scale = 100.0
        y_scale = 100.0 # 83.0
        
        flat = []        
        for i in range(n):
            x = cube[i].x
            y = cube[i].y
            z = self.z_off - cube[i].z
            nx = int(self.x_off + (x / z * x_scale))
            ny = int(self.y_off + (y / z * y_scale))
            flat.append(Point2D(nx, ny))
            
        return flat


    def rotate(self, points, z, x, y):
        '''
        to rotate a point (oX, oY) through Alpha radians, counter-clockwise, about
        the z axis:
        nX = [Cos(Alpha) * oX] - [Sin(Alpha) * oY]
        nY = [Sin(Alpha) * oX] + [Cos(Alpha) * oY]
        '''
        
        rotated = []
        for i in range(len(points)):
            oX = points[i].x
            oY = points[i].y
            oZ = points[i].z

            # about z axis 
            nX = (self.cos_table[z] * oX) - (self.sin_table[z] * oY)
            nY = (self.sin_table[z] * oX) + (self.cos_table[z] * oY)
            oX = nX 
            oY = nY

            # about x axis 
            nZ = (self.cos_table[x] * oZ) - (self.sin_table[x] * oY)
            nY = (self.sin_table[x] * oZ) + (self.cos_table[x] * oY)
            oZ = nZ

            # about y axis 
            nX = (self.cos_table[y] * oX) - (self.sin_table[y] * oZ)
            nZ = (self.sin_table[y] * oX) + (self.cos_table[y] * oZ)

            rotated.append(Point3D(x=nX, y=nY, z=nZ))
            
        return rotated

    def draw_to_pixmap(self, points, pixmap, gc, style):
        '''
        '''
        # pixmap.draw_line(self.gc, x, y, self.w/2, self.h/2)  

        #  octal inlay flush with end plate 
        for i in range(7):
            pixmap.draw_line(gc, points[i].x, points[i].y, points[i + 1].x, points[i + 1].y)
        
        pixmap.draw_line(gc, points[7].x, points[7].y, points[0].x, points[0].y)

        # connections between octal inlays'pipe' 
        for i in range(8):
            pixmap.draw_line(gc, points[i].x, points[i].y, points[i + 8].x, points[i + 8].y)

        #  octal inlay flush with end plate 
        for i in range(8, 15):
            pixmap.draw_line(gc, points[i].x, points[i].y, points[i + 1].x, points[i + 1].y)
        
        pixmap.draw_line(gc, points[15].x, points[15].y, points[8].x, points[8].y)

        #  end plate of column 
        for i in range(16, 19):
            pixmap.draw_line(gc, points[i].x, points[i].y, points[i + 1].x, points[i + 1].y)
            
        pixmap.draw_line(gc, points[19].x, points[19].y, points[16].x, points[16].y)

        #  end plate of column 
        for i in range(20, 23):
            pixmap.draw_line(gc, points[i].x, points[i].y, points[i + 1].x,points[i + 1].y)
        
        pixmap.draw_line(gc, points[23].x, points[23].y, points[20].x, points[20].y)


    def iterate(self, pixmap, gc, style):
        '''
        '''
        rotated = self.rotate(self.points, self.z_deg, self.x_deg, self.y_deg)
        flattened = self.flatten(rotated)
        self.draw_to_pixmap(flattened, pixmap, gc, style)
        
    def move(self, x, y, z):
        
        self.z_deg = self.z_deg + int(z)
        self.x_deg = self.x_deg + int(y)
        self.y_deg = self.y_deg - int(x)       
        
        self.shake()

    def shake(self):

        if (self.z_deg >= 360):
            self.z_deg = self.z_deg - 360
        if (self.z_deg < 0):
            self.z_deg = self.z_deg + 360
        
        if (self.x_deg >= 360):
            self.x_deg = self.x_deg - 360
        if (self.x_deg < 0):
            self.x_deg = self.x_deg + 360

        if (self.y_deg >= 360):
            self.y_deg = self.y_deg - 360
        if (self.y_deg < 0):
            self.y_deg = self.y_deg + 360
