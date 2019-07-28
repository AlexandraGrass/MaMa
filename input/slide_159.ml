let rec f = fun x y -> 
  if y <= 1 
    then x 
    else f ( x * y ) ( y - 1 ) in 
      f 1