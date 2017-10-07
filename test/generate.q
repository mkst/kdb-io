/script to generate simple, nested and compressed dummy databases

/ 1000 atoms per list
sz:1000;

-1"writing down atoms";

`:data/atoms/a set 1b;
`:data/atoms/b set 0Ng;
`:data/atoms/c set "x"$"a";
`:data/atoms/d set 1024h;
`:data/atoms/e set 1024i;
`:data/atoms/f set 1024;
`:data/atoms/g set 10e;
`:data/atoms/h set 10f;
`:data/atoms/i set "a";
`:data/atoms/j set `abc;
`:data/atoms/k set .z.p;
`:data/atoms/l set `month$.z.p;
`:data/atoms/m set `date$.z.p;
`:data/atoms/n set `datetime$.z.p;
`:data/atoms/o set first(1?.z.p)-1?.z.p;
`:data/atoms/p set `minute$.z.p;
`:data/atoms/q set `second$.z.p;
`:data/atoms/r set `time$.z.p;

-1"writing down lists";

`:data/lists/a set sz#1b;
`:data/lists/b set sz#0Ng;
`:data/lists/c set sz#"x"$"a";
`:data/lists/d set sz#1024h;
`:data/lists/e set sz#1024i;
`:data/lists/f set sz#1024;
`:data/lists/g set sz#10e;
`:data/lists/h set sz#10f;
`:data/lists/i set sz#"a";
`:data/lists/j set sz#`abc;
`:data/lists/k set sz#.z.p;
`:data/lists/l set sz#`month$.z.p;
`:data/lists/m set sz#`date$.z.p;
`:data/lists/n set sz#`datetime$.z.p;
`:data/lists/o set sz#first(1?.z.p)-1?.z.p;
`:data/lists/p set sz#`minute$.z.p;
`:data/lists/q set sz#`second$.z.p;
`:data/lists/r set sz#`time$.z.p;

/100k rows in simple or compressed column
sz:100000;

simple:([]
  a:sz?01b;
  b:sz?0Ng;
  c:"x"$sz?255;
  d:sz?1024h;
  e:sz?1024i;
  f:sz?1024;
  g:sz?10e;
  h:sz?10f;
  i:sz?.Q.a;
  j:sz?`a`b`c`d`e;
  k:sz?.z.p;
  l:`month$sz?.z.p;
  m:`date$sz?.z.p;
  n:`datetime$sz?.z.p;
  o:(sz?.z.p)-sz?.z.p;
  p:`minute$sz?.z.p;
  q:`second$sz?.z.p;
  r:`time$sz?.z.p);

-1"writing down simple";

`:data/simple/ set .Q.en[`:data] simple;

sz:1000; / 1k nested rows

nested:update a:{ (first 1+1?sz)?01b } each i from sz#simple;
nested:update b:{ (first 1+1?sz)?0Ng } each i from nested;
nested:update c:{ "x"$(first 1+1?sz)?255 } each i from nested;
nested:update d:{ (first 1+1?sz)?1024h } each i from nested;
nested:update e:{ (first 1+1?sz)?1024i } each i from nested;
nested:update f:{ (first 1+1?sz)?1024 } each i from nested;
nested:update g:{ (first 1+1?sz)?10e } each i from nested;
nested:update h:{ (first 1+1?sz)?10f } each i from nested;
nested:update i:{ (first 1+1?sz)?.Q.a } each i from nested;
/nested:update j:{ (first 1+1?sz)?`a`b`c`d`e } each i from nested; / FIXME: write down nested syms
nested:update k:{ (first 1+1?sz)?.z.p } each i from nested;
nested:update l:{ `month$(first 1+1?sz)?.z.p } each i from nested;
nested:update m:{ `date$(first 1+1?sz)?.z.p } each i from nested;
nested:update n:{ `datetime$(first 1+1?sz)?.z.p } each i from nested;
nested:update o:{ (first 1+1?sz)?(sz?.z.p)-sz?.z.p } each i from nested;
nested:update p:{ `minute$(first 1+1?sz)?.z.p } each i from nested;
nested:update q:{ `second$(first 1+1?sz)?.z.p } each i from nested;
nested:update e:{ `time$(first 1+1?sz)?.z.p } each i from nested;

/ sort by k
nested:`k xasc nested;

-1"writing down nested";

`:data/nested/ set .Q.en[`:data] nested;

-1"writing down compressed";
/ enable compression
.z.zd:18 2 6;
`:data/compressed/ set .Q.en[`:data] simple;

exit 0
