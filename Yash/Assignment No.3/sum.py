from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.rank

send_buf = []

if rank == 0:
    arr = np.array([12,21241,5131,1612251,161,6,161,1613,161363,12616,367,8363])
    arr.shape = (3, 4)
    send_buf = arr

v = comm.scatter(send_buf, root=0)
print("Local sum at rank {0}: {1}".format(comm.rank, np.sum(v)))

recvbuf = comm.reduce(v, root=0)
if comm.rank == 0:
    global_sum = np.sum(recvbuf)
    print("Global sum: "+ str(global_sum)) 
