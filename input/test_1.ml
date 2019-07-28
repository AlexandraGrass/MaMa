let rec x = fun a -> 1 
  and y = fun b -> 
    let rec z0 = fun c -> c 
      and z1 = fun d -> d in 
        z1 1 
  and z = fun a -> a in 
    ((x 2) + (y 2))