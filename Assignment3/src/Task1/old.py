from timeit import default_timer as timer
import sys
from array import array
import matplotlib.pyplot as plt
import numpy as np

scalar = 2.0

def get_copy_size(STREAM_ARRAY_SIZE):
    return (2 * np.nbytes[float] * STREAM_ARRAY_SIZE)

def get_add_size(STREAM_ARRAY_SIZE):
    return (2 * np.nbytes[float] * STREAM_ARRAY_SIZE)

def get_scale_size(STREAM_ARRAY_SIZE):
    return (3 * np.nbytes[float] * STREAM_ARRAY_SIZE)

def get_triad_size(STREAM_ARRAY_SIZE):
    return (3 * np.nbytes[float] * STREAM_ARRAY_SIZE)


def run_stream_test(type,debug,STREAM_ARRAY_SIZE):
    times = [0.0]*4
    # List 
    if type=="l":
        a = [1.0]*STREAM_ARRAY_SIZE
        b = [2.0]*STREAM_ARRAY_SIZE
        c = [0.0]*STREAM_ARRAY_SIZE
        
        ## Calculate time to do operations:

        # copy
        times[0] = timer()
        c[:] = a[:]
        times[0] = timer() - times[0]

        # scale
        times[1] = timer()
        b = [scalar * x for x in c]
        times[1] = timer() - times[1]
        
        # add
        times[2] = timer()
        c = [x + y for x, y in zip(a, b)]
        times[2] = timer() - times[2]

        # triad
        times[3] = timer()
        a = [x + scalar * y for x, y in zip(b, c)]
        times[3] = timer() - times[3]
    # Array
    else:
        a = array('f', [1.0] * STREAM_ARRAY_SIZE)
        b = array('f', [2.0] * STREAM_ARRAY_SIZE)
        c = array('f', [0.0] * STREAM_ARRAY_SIZE)
        # Copy
        times[0] = timer()
        c[:] = a[:]
        times[0] = timer() - times[0]

        # Scale
        times[1] = timer()
        b = array('d', [scalar * x for x in c])
        times[1] = timer() - times[1]
        
        # Add
        times[2] = timer()
        c = array('d', [x + y for x, y in zip(a, b)])
        times[2] = timer() - times[2]

        # Triad
        times[3] = timer()
        a = array('d', [x + scalar * y for x, y in zip(b, c)])
        times[3] = timer() - times[3]


    # Get the amount of data moved
    copy = get_copy_size(STREAM_ARRAY_SIZE)
    add = get_add_size(STREAM_ARRAY_SIZE)
    scale = get_scale_size(STREAM_ARRAY_SIZE)
    triad = get_triad_size(STREAM_ARRAY_SIZE)


    # Calculate bandwidth
    copyStream = 1.0e-09 * (copy/times[0])
    addStream = 1.0e-09 * (add/times[1])
    scaleStream = 1.0e-09 * (scale/times[2])
    triadStream = 1.0e-09 * (triad/times[3])

    total = copyStream + addStream + scaleStream + triadStream

    if debug:
        print("Copy GB/s:",copyStream)
        print("Add GB/s:",addStream)
        print("Scale GB/s:",scaleStream)
        print("Triad GB/s:",triadStream)
        
    # Return
    return [copyStream,addStream,scaleStream,triadStream]


if __name__ == "__main__":
    x = [i * 10_000 + 10_000 for i in range(100_000) if i * 10_000 + 10_000 <= 100_000]
    y3 = [[],[],[],[]]
    y4 = [[],[],[],[]]

    for val in x:
        data3 = run_stream_test("l", False, val)
        data4 = run_stream_test("array", False, val)
        y3[0].append(data3[0])
        y3[1].append(data3[1])
        y3[2].append(data3[2])
        y3[3].append(data3[3])
        y4[0].append(data4[0])
        y4[1].append(data4[1])
        y4[2].append(data4[2])
        y4[3].append(data4[3])

    # Ugly code for adding to plots
    # Please ignore 


    fig, axs = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
    fig.suptitle('List & Array comparison')
    axs[0, 0].plot(x,y3[0],label="List")
    axs[0, 0].set_title('Copy')
    axs[0, 1].plot(x,y3[1],label="List")
    axs[0, 1].set_title('Add')
    axs[1, 0].plot(x,y3[2],label="List")
    axs[1, 0].set_title('Scale')
    axs[1, 1].plot(x,y3[3],label="List")
    axs[1, 1].set_title('Triad')
    axs[0, 0].plot(x,y4[0],label="Array")
    axs[0, 1].plot(x,y4[1],label="Array")
    axs[1, 0].plot(x,y4[2],label="Array")
    axs[1, 1].plot(x,y4[3],label="Array")
    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].legend()

    # Set common labels

    fig.text(0.5, 0.04, 'N', ha='center', va='center')
    fig.text(0.06, 0.5, 'GB/s', ha='center', va='center', rotation='vertical')

    plt.show()