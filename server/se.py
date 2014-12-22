from ladon.ladonizer import ladonize

class Calculator(object):
  """
  This service does the math, and serves as example for new potential Ladon users.
  """
  @ladonize(int,int,rtype=int)
  def add(self,a,b):
    """
    Add two integers together and return the result

    @param a: 1st integer
    @param b: 2nd integer
    @rtype: The result of the addition
    """
    return a+b