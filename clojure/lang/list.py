from clojure.lang.primitives import Obj, BoolObj, IntObj
from clojure.lang.symbol import Symbol
from clojure.lang.afn import AFn

import sys

class List(Obj):
   def __init__(self, head, tail = None, count = 1):
       self.head = head
       self.tail = tail
       self.count = count
   def cons(self, other):
       if self.count == 0:
           return List(other)
       return List(other, self, self.count + 1)
   def rest(self):
       return self.tail
   def first(self):
       return self.head
   def length(self):
   	   return IntObj(self.count)
   	   
   def get_item(self, idx):
       h = self
       for x in range(idx):
           h = h.rest()
       return h.head
   
   def __len__(self):
       return self.count
   
   def __getslice__(self, i, k):
       if k == sys.maxint:
           h = self
           for x  in range(i):
               h = self.rest()
           return h
       v = []
       h = self
       for x in range(i):
           h = self.rest()
       for x in range(k-i):
           v.append(h.head)
       return List.from_list(v)
       
   @staticmethod
   def from_list(lst):
       last = None
       count = 1
       for x in range(len(lst)-1, -1, -1):
           last = List(lst[x], last, count)
           count += 1
       return last
   
   def to_list(self):
       lst = [None] * self.count
       idx = 0
       list = self
       while list is not None:
           lst[idx] = list.head
           idx += 1
           list = list.tail
       return lst
   
   def __repr__(self):
       s = []
       s.append("(")
       h = self
       while h is not None:
           s.append(h.head.__repr__())
           h = h.rest()
       s.append(")")
       return " ".join(s)
   def evaluate(self):
   	   from clojure.jit.jit import jitdriver
   	   from clojure.lang.var import _Globals
   	   jitdriver.jit_merge_point(form = self, frames = _Globals._frames )
   	   f = self.first().evaluate()
   	   args = []
   	   h = self.rest()
   	   return f.apply(h)
       
       
   
class EmptyList(Obj):
   def __init__(self):
       pass
   def cons(self, head):
       return List(head)
   def rest(self):
       raise Exception("Can't get rest from empty list")
   def first(self):
       raise Exception("EmptyList")
   def __len__(self):
       return 0     
   def length(self):
   	   return IntObj(0)    	   
   	   
   	   
class Cons_List(AFn):
	def invoke2(self, x, lst):
		return lst.cons(x)
		

def init_vars():
	from clojure.lang.var import Var
	conslist = Var(Symbol.from_string("cons_list*"), Cons_List())
	
init_vars()
	
