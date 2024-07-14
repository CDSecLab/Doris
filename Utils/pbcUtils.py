from pypbc import Element, G1, Zr
from .cfg import pairing
from .cryptoUtils import prf
from Crypto.Util.number import long_to_bytes, bytes_to_long


class pbcUtil:
    def __init__(self) -> None:
        self.g = self._gen_g()

    # Generate the primitive root(g) randomly
    def _gen_g(self):
        return Element.random(pairing, G1)

    # Map the string(m) onto the order of the group(Zr)
    def prfToZr(self, k: bytes, m: str) -> Element:
        c = prf(k, m)
        return Element.from_hash(pairing, Zr, c)

    # pow(g,n)
    def gToPower(self, n: Element) -> Element:
        return Element(pairing, G1, self.g**n)

    # pow(g,n*m)
    def gToPower2(self, n: Element, m: Element) -> Element:
        return Element(pairing, G1, self.g**(n*m))

    # Convert the elements in Zr to bytes type
    def Zr2Bytes(self, ele: Element) -> bytes:
        return long_to_bytes(int(str(ele), 16))

    # Convert bytes type data to element in Zr
    def bytes2Zr(self, bstr: bytes) -> Element:
        return Element(pairing, Zr, value=bytes_to_long(bstr))

    # n*m
    def mul2Zr(self, n: Element, m: Element) -> Element:
        return Element(pairing, Zr, n*m)

    # pow(n,m)
    def pow(self, n: Element, m: Element) -> Element:
        return Element(pairing, G1, n**m)
