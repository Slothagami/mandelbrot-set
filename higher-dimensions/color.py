def hsv_to_rgb(h, s, v): # takes percent values
    # https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion (Tcll's Answer)
    if s == 0: 
        v *= 255
        return (v, v, v)

    i = int(h * 6) # XXX assume int() truncates!
    f = (h * 6) - i

    p = int(255 * (v * (1 - s)))
    q = int(255 * (v * (1 - s * f)))
    t = int(255 * (v * (1 - s * (1 - f))))
    
    v *= 255
    i %= 6

    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)
