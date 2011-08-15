#!/usr/bin/python
import os, sys
sys.path.append('..')
import rpythonic
rpythonic.set_pypy_root( '../../pypy' )
################################
rpy = rpythonic.RPython()

@rpy.bind()							# declare arg types is optional if,
def add( a=1, b=1000 ):			# keyword defaults are given
	return a+b

@rpy.bind(a=float, b=float)
def sub( a, b ):
	return a-b

@rpy.bind( values=[float] )	# lists not working yet
def test_R( values ):
	print( 'entering test_R' )
	x = []
	for i in range(10):
		print(i)
		r = R(); x.append( r )
		for v in values: r.append( v )
		print( r.values )


class R(object):
	def __init__(self):
		self.values = []
	def append( self, value ):
		self.values.append( value )


rpy.cache('test1', refresh=1)					# only compiles if cache is dirty

############### testing ##############

print add( 100, 9 )
print add( 1, 99 )
print sub( 1.0, .8 )		# opps, TODO fixme: 3219623024

test_R( [.1, .2, .3] )

