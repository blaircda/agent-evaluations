import numpy as np
import csv
rng = np.random.default_rng(seed=42)

def get_irr(cashflow):
    """
    Attempts to find Internal Rate of Return (IRR) of a cashflow stream
    Transforms ``cashflow`` into a polynomial in discount factor and finds all real, positive roots
    Returns IRR = 1/d - 1 where d is a root

    Parameters
    ----------
    cashflow: array_like of floats or ints
        Cash-flow stream

    Returns
    -------
    float or ndarray
    """
    p = np.polynomial.Polynomial(cashflow) # make polynomial
    d = p.roots() # get roots
    real = np.isclose(d.imag, 0) # mask for real roots
    d = d.real[real] # select real roots
    d = d[d>0] # select positive real roots
    irr = 1/d - 1
    return irr

def generate_flows(Nflows, flow_length, max_outlay = 10, min_outlay = 1, max_inflow = 10, min_inflow = 1):
    """
    Randomly generates Nflows flows of length flow_length
    Saves to file output as csv

    Parameters
    ---------
    Nflows: int
        Number of flows
    flow_length: int
        Length of flows
    max_outlay: int or float
        Maximum initial outlay.
    min_outlay: int or float
        Minimum initial outlay
    max_inflow: int or float
        Maximum inflow at any point of the flow
    min_inflow: int or float
        Minimum inflow at any point of the flow
        
    Returns
    -------
    None
    """
    outlays = rng.integers(-max_outlay,-min_outlay+1,(Nflows,1))
    inflows = rng.integers(min_inflow, max_inflow+1,(Nflows,flow_length-1))
    flows = np.concatenate((outlays, inflows), axis=1)

    np.savetxt("flows.csv", flows, fmt="%d", delimiter=",")
    irrs = [get_irr(row) for row in flows]
    np.savetxt("irrs.csv", irrs, fmt="%.6f")

def generate_mixed_flows(Nflows, flow_length, max_outlay = 10, min_outlay = 1, max_abs_flow=10):
    """
    Randomly generates Nflows flows of length flow_length
    Saves to file output as csv

    Parameters
    ---------
    Nflows: int
        Number of flows
    flow_length: int
        Length of flows
    max_outlay: int or float
        Maximum initial outlay.
    min_outlay: int or float
        Minimum initial outlay
    max_abs_flow: int or float
        Maximum flow in OR out at any point of the flow
        
    Returns
    -------
    None
    """
    outlays = rng.integers(-max_outlay,-min_outlay+1,(Nflows,1))
    inflows = rng.integers(-max_abs_flow, max_abs_flow+1,(Nflows,flow_length-1))
    flows = np.concatenate((outlays, inflows), axis=1)
    
    with open('mixed_flows.csv', 'w') as flowfile, open('mixed_irrs.csv', 'w') as irrfile:
        flowwriter = csv.writer(flowfile)
        irrwriter = csv.writer(irrfile)
        for c in flows:
            irr = get_irr(c)
            flowwriter.writerow(c)
            irrwriter.writerow([f"{x:.6f}" for x in irr])

if __name__ == '__main__':
    generate_flows(10, 5)
    generate_mixed_flows(10,5)
