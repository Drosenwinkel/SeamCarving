import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):

    """returns a list of coordinates corresponding to the lowest-energy vertical
seam to remove, e.g. [(5, 0), (5, 1), (4, 2), (5, 3), (6, 4)]."""



    def best_seam(self, dp=True):

        energy_memo ={}
        point_memo={}

        for j in range(self.height):
            for i in range(self.width):

                #first row
                if(j==0):
                    energy_memo[(i,j)] = self.energy(i,j)
                else:

                    #if leftmost
                    if(i==0):
                        if(energy_memo[(i,j-1)] < energy_memo[(i+1,j-1)] ):
                            point_memo[(i,j)] = (i,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i,j-1)]
                        else:
                            point_memo[(i,j)] = (i+1,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i+1,j-1)]

                    elif(i==self.width-1):

                        if(energy_memo[(i,j-1)] < energy_memo[(i-1,j-1)]):
                            point_memo[(i,j)] = (i,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i,j-1)]
                        else:
                            point_memo[(i,j)] = (i-1,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i-1,j-1)]

                    else:

                        if(energy_memo[(i-1,j-1)] < energy_memo[(i,j-1)] and energy_memo[(i-1,j-1)] < energy_memo[(i+1,j-1)]):
                            point_memo[(i,j)] = (i-1,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i-1,j-1)]
                        elif(energy_memo[(i-1,j-1)] > energy_memo[(i,j-1)] and energy_memo[(i,j-1)] < energy_memo[(i+1,j-1)]):
                            point_memo[(i,j)] = (i,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i,j-1)]
                        else:
                            point_memo[(i,j)] = (i+1,j-1)
                            energy_memo[(i,j)] = self.energy(i,j) + energy_memo[(i+1,j-1)]

        seam = []
        min_index_last_row=-1;
        min = energy_memo[(0,self.height-1)]+1
        for i in range(self.width):
            if(energy_memo[(i,self.height-1)] < min):
                min = energy_memo[(i,self.height-1)]
                min_index_last_row=i

        previous = (min_index_last_row,self.height-1)
        seam.append(previous)

        while(point_memo.has_key(previous)):

            seam.append(point_memo[previous])
            previous = point_memo[previous]



        return seam[::-1]


    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
