var canv, c
window.addEventListener("load", () => {
    canv = document.querySelector("canvas")
    c = canv.getContext("2d")
    
    const resize = ()=> {
        canv.width  = window.innerWidth
        canv.height = window.innerHeight
    }
    resize()
    document.addEventListener("resize", resize)
    
    init()
})

var pos = new Complex(0,0),
    mandlebrotOrder = 2,
    func = mandlebrot,
    interpretIndex = 0,
    colorTypes = ["standard", "polar", "real", "imag", "angle"],
    interpret = "standard",
    juliaSeed = new Complex(0,0),
    zoomFactor = .69,
    movespeed = .12,
    depth = 100,
    prec,
    xrange = 4, 
    yrange,
    colorSpread = 1

const CONTROLS = [
    "WASD: Move View",
    "+-: Zoom",
    "[]: Change Depth Value",
    "Space: Cycle Projection Types",
    "Alt: Cycle Set Types",
    "IJKL: Move Julia Seed", 
    "OP: Change Set Power",
    "--"
].join("\n")

// Program
function init() {
    // Controls
    console.log(CONTROLS)

    window.addEventListener("keydown", e => {
        console.log(e.key)
        switch(e.key) {
            // order
            case "p": mandlebrotOrder++; break
            case "o": mandlebrotOrder--; break

            case "Alt":
                if( func == mandlebrot ) {
                    func = julia
                } else {func = mandlebrot}

            // Zoom
            case "=": // +
                xrange *= zoomFactor
                scrRatio = canv.height / canv.width,
                yrange = xrange * scrRatio
                // colorPerPoint(func, interpret)
                break
                
            case "-":
                xrange /= zoomFactor
                scrRatio = canv.height / canv.width,
                yrange = xrange * scrRatio
                // colorPerPoint(func, interpret)
                break

            //Move
            case "w":
                pos = Complex.add(pos, new Complex(0, -yrange * movespeed))
                // colorPerPoint(func, interpret)
                break

            case "a":
                pos = Complex.add(pos, new Complex(-xrange * movespeed, 0))
                // colorPerPoint(func, interpret)
                break

            case "s":
                pos = Complex.add(pos, new Complex(0, yrange * movespeed))
                // colorPerPoint(func, interpret)
                break

            case "d":
                pos = Complex.add(pos, new Complex(xrange * movespeed, 0))
                // colorPerPoint(func, interpret)
                break


            //Move Julia Seed
            case "i":
                juliaSeed = Complex.add(juliaSeed, new Complex(0, -.01))
                break

            case "j":
                juliaSeed = Complex.add(juliaSeed, new Complex(-.01, 0))
                break

            case "k":
                juliaSeed = Complex.add(juliaSeed, new Complex(0, .01))
                break

            case "l":
                juliaSeed = Complex.add(juliaSeed, new Complex(.01, 0))
                break

            // case "q":
            //     colorPerPoint(func, interpret)
            //     break

            // Change Depth
            case "[":
                depth -= 20
                // colorPerPoint(func, interpret)
                break
            case "]":
                depth += 20
                // colorPerPoint(func, interpret)
                break

            case " ":
                interpretIndex++
                if(interpretIndex >= colorTypes.length) interpretIndex = 0
                interpret = colorTypes[interpretIndex]
                colorPerPoint(func, interpret)
                break

        }
        colorPerPoint(func, interpret)


        console.clear()
        console.log([
            "Coloring: " + interpret,
            "Set Power: " + mandlebrotOrder,
            "Position: " + pos.toString(),
            "Set Type: " + func.name,
            "Julia Seed: " + juliaSeed.toString(),
            "Depth: " + depth,
            "Viewport Width: " + xrange
        ].join("\n"))
        console.log(CONTROLS)
    })

    scrRatio = canv.height / canv.width,
    yrange = xrange * scrRatio

    prec = canv.width/2
    colorPerPoint(func, interpret)
}

function colorPerPoint(func, interpretType) {
    // loops the points and runs a 
    // function that returns a color to draw

    let inc = xrange/prec
    for(let x = -xrange/2; x < xrange/2; x += inc) {
        for(let y = -yrange/2; y < yrange/2; y += inc) {
            let position = Complex.add(new Complex(x, y), pos)
            result = func(position)
            c.fillStyle = interpretColor(result, interpretType)

            // unit length
            let tx = x/ (xrange/2)
            let ty = y/ (yrange/2)

            // scale to screen
            tx *= canv.width/2
            ty *= canv.height/2

            // move to center
            tx += canv.width/2
            ty += canv.height/2

            size = canv.width / prec
            c.fillRect(tx, ty, size, size)
        }
    }
}

function mandlebrot(c) {
    // returns mandlebrot coloring at point z
    let z = 0,
        iterations = 0

    for(let i = 0; i < depth; i++) {
        z = Complex.add(Complex.pow(z, mandlebrotOrder), c)
        // if(Complex.abs(z) > 2) {
        
        // vary limit from |z| > 2 to between 1 and 2 for interesting results 
        if(z.real**2 + z.imag**2 > 2**2) { // slightly faster, no sqrt
            iterations = i 
            break
        }
    }

    return {
        iterations: iterations,
        finalZ: z
    }
}

function julia(z) {
    let iterations = 0

    for(let i = 0; i < depth; i++) {
        z = Complex.add(Complex.pow(z, mandlebrotOrder), juliaSeed)
        if(Complex.abs(z) > 2) {
            iterations = i 
            break
        }
    }

    return {
        iterations: iterations,
        finalZ: z
    }
}

function color(hue) {
    let h = hue*colorSpread
    return `hsl(${h},70%,60%)`
}

function interpretColor(res, type) {
    switch(type) {
        case "standard":
            if(Complex.abs(res.finalZ) <= 2) return "black"
            return color(res.iterations * 10)
            
        case "polar":
            return color(Complex.abs(res.finalZ) * 60)

        case "real":
            return color(res.finalZ.real * 60)

        case "imag":
            return color(res.finalZ.imag * 60)

        case "angle":
            return color(res.finalZ.angle() * 50)
    }
}
