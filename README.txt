Complicated "let" statements are supported:
	"(let (a (let (b 5) (+ b 6))) (* 3 a))" returns 33

Arithmetic functions (+, -, *, /) support negative numbers:
	"(+ 3 -7)" returns -4

Arithmetic functions (+, -, *, /) support more than 2 terms:
	"(let (a 4) (+ a -2 7))" returns 9
	"(- 10 1 2 3 4)" returns 0
	"(/ 10 1 2 3 4)" returns 0.416666666667