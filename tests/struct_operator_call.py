import lib


def bind_test(gen):
	gen.start('my_test')

	lib.bind_defaults(gen)

	# inject test code in the wrapper
	gen.insert_code('''\
struct simple_struct {
	simple_struct(int _v) : v(_v) {}

	simple_struct operator-(const simple_struct &b) { return simple_struct(v - b.v); }
	simple_struct operator+(const simple_struct &b) { return simple_struct(v + b.v); }
	simple_struct operator/(const simple_struct &b) { return simple_struct(v / b.v); }
	simple_struct operator*(const simple_struct &b) { return simple_struct(v * b.v); }

	simple_struct operator+(int k) { return simple_struct(v + k); }
	simple_struct operator/(int k) { return simple_struct(v / k); }
	simple_struct operator*(int k) { return simple_struct(v * k); }
	simple_struct operator-(int k) { return simple_struct(v - k); }

	void operator-=(const simple_struct &b) { v -= b.v; }
	void operator+=(const simple_struct &b) { v += b.v; }
	void operator/=(const simple_struct &b) { v /= b.v; }
	void operator*=(const simple_struct &b) { v *= b.v; }

	void operator-=(int k) { v -= k; }
	void operator+=(int k) { v += k; }
	void operator/=(int k) { v /= k; }
	void operator*=(int k) { v *= k; }

	bool operator==(int k) const { return k == v; }
	bool operator==(const simple_struct &b) const { return b.v == v; }
	bool operator!=(int k) const { return k != v; }
	bool operator!=(const simple_struct &b) const { return b.v != v; }

	int v;
};
''', True, False)

	simple_struct = gen.begin_class('simple_struct')
	gen.bind_constructor(simple_struct, ['int v'])
	gen.bind_arithmetic_ops_overloads(simple_struct, ['-', '+', '/', '*'], [
		('simple_struct', ['simple_struct b'], {"bound_name": "SimpleStruct"}),
		('simple_struct', ['int k'], {"bound_name": "Int"})
	])
	gen.bind_inplace_arithmetic_ops_overloads(simple_struct, ['-=', '+=', '/=', '*='], [
		(['simple_struct b'], {"bound_name": "SimpleStruct"}),
		(['int k'], {"bound_name": "Int"})
	])
	gen.bind_comparison_ops_overloads(simple_struct, ['==', '!='], [
		(['simple_struct b'], []),
		(['int k'], [])
	])
	gen.bind_member(simple_struct, 'int v')
	gen.end_class(simple_struct)

	gen.finalize()
	return gen.get_output()


test_python = '''\
import my_test

a, b = my_test.simple_struct(4), my_test.simple_struct(8)

s = a + b
assert s.v == 12
s += b
assert s.v == 20
s += 4
assert s.v == 24

s = s / 4
assert s.v == 6
s /= 3
assert s.v == 2
s += a
assert s.v == 6

s = s * a
assert s.v == 24
s *= 2
assert s.v == 48

s = s - b
assert s.v == 40
s -= 32
assert s.v == 8

c = a * 2
assert c == b
assert a != b
'''

test_lua = '''\
my_test = require "my_test"

a, b = my_test.simple_struct(4), my_test.simple_struct(8)

s = a + b
assert(s.v == 12)
s = s + b
assert(s.v == 20)
s = s + 4
assert(s.v == 24)

s = s / 4
assert(s.v == 6)
s = s / 3
assert(s.v == 2)
s = s + a
assert(s.v == 6)

s = s * a
assert(s.v == 24)
s = s * 2
assert(s.v == 48)

s = s - b
assert(s.v == 40)
s = s - 32
assert(s.v == 8)

c = a * 2
assert(c == b)
assert(a ~= b)
'''

test_go = """\
package mytest

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Test ...
func Test(t *testing.T) {
	a, b := NewSimpleStruct(4), NewSimpleStruct(8)

	s := a.AddSimpleStruct(b)
	assert.Equal(t, s.GetV(), int32(12), "should be the same.")
	s.InplaceAddSimpleStruct(b)
	assert.Equal(t, s.GetV(), int32(20), "should be the same.")
	s.InplaceAddInt(4)
	assert.Equal(t, s.GetV(), int32(24), "should be the same.")

	s = s.DivInt(4)
	assert.Equal(t, s.GetV(), int32(6), "should be the same.")
	s.InplaceDivInt(3)
	assert.Equal(t, s.GetV(), int32(2), "should be the same.")
	s.InplaceAddSimpleStruct(a)
	assert.Equal(t, s.GetV(), int32(6), "should be the same.")

	s = s.MulSimpleStruct(a)
	assert.Equal(t, s.GetV(), int32(24), "should be the same.")
	s.InplaceMulInt(2)
	assert.Equal(t, s.GetV(), int32(48), "should be the same.")

	s = s.SubSimpleStruct(b)
	assert.Equal(t, s.GetV(), int32(40), "should be the same.")
	s.InplaceSubInt(32)
	assert.Equal(t, s.GetV(), int32(8), "should be the same.")

	c := a.MulInt(2)
	assert.True(t, c.Eq(b), "should be the same.")
	assert.True(t, a.Ne(b), "should be the same.")
}
"""

test_rust = '''\
use my_test::*;

#[test]
fn test() {
	let a = simple_struct::new(4);
	let b = simple_struct::new(8);

	let mut s = a.add_simple_struct(&b);
	assert_eq!(s.get_v(), 12, "should be the same.");
	s.inplace_add_simple_struct(&b);
	assert_eq!(s.get_v(), 20, "should be the same.");
	s.inplace_add_int(4);
	assert_eq!(s.get_v(), 24, "should be the same.");

	s = s.div_int(4);
	assert_eq!(s.get_v(), 6, "should be the same.");
	s.inplace_div_int(3);
	assert_eq!(s.get_v(), 2, "should be the same.");
	s.inplace_add_simple_struct(&a);
	assert_eq!(s.get_v(), 6, "should be the same.");

	s = s.mul_simple_struct(&a);
	assert_eq!(s.get_v(), 24, "should be the same.");
	s.inplace_mul_int(2);
	assert_eq!(s.get_v(), 48, "should be the same.");

	s = s.sub_simple_struct(&b);
	assert_eq!(s.get_v(), 40, "should be the same.");
	s.inplace_sub_int(32);
	assert_eq!(s.get_v(), 8, "should be the same.");

	let c = a.mul_int(2);
	assert!(c.eq(&b), "should be the same.");
	assert!(!a.ne(&b), "should be the same.");
}
'''