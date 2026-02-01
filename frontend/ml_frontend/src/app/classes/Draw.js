'use client'
import {useEffect, useState} from "react"


// props: Value, PreviousValue, Counter, X_Interval, RunTestState
export default function Draw(props) {
    const defaults = {"interval": 7.19, "max_x": 725, "max_y": 400}
    const colors = {
        "steel_blue": "#6B8EAD",
        "soft_teal": "#7FA6A0",
        "lavender": "#9A7AA0",
        "moss_green": "#8FAF7A",
        "magenta": "#C97BBE",
        "slate_blue": "#7C9EB2",
        "rose": "#9C6B6B",
        "sea_green": "#6F8F7D",
        "periwinkle": "#8B7AAE",
        "teal": "#5F8A8B"
    }

    const [Line, setLine] = useState(null)
    const [Calculations, setCalculations] = useState(null)

    const [X_Interval, setX_Interval] = useState(defaults.interval)
    const [PreviousValue, setPreviousValue] = useState(defaults.max_y)
    const [CurrentValue, setCurrentValue] = useState(0)
    const [Color, setColor] = useState(colors.rose)



    useEffect(()=>{
        props.Counter < 1 ? setLine(null) : null
        console.log(Line)
    }, [])


    useEffect(()=>{
        props.RunTestState[0] == true && props.Counter < 100 ? calculate() : null
    }, [props.RunTestState])


    useEffect(()=>{
        Calculations != null ? draw_line() : null
    }, [Calculations])


    function calculate(){
        console.log("counter")
        console.log(props.Counter)
        console.log("value")
        console.log(props.Value)
        console.log("line")
        console.log(Line)

        props.Counter < 1 ? setLine(null) : null
        if(((props.Counter - 1) * X_Interval) < 719){
            setPreviousValue(props.Value)
            setCurrentValue(props.Value)

            let prev_x = props.Counter > 0 ? (props.Counter - 1) * X_Interval : (props.Counter * X_Interval)
            prev_x > 719 ? prev_x = 719 : null

            let x = ((props.Counter + 1) * X_Interval)  
            x > 719 ? x = 719 : null

            let prev_y = props.Counter > 0 ? PreviousValue : props.Value
            prev_y < 0 ? prev_y = 0 : null

            let y = props.Value
            y < 0 ? y = 0 : null

            setCalculations({
                "prev_x": prev_x,
                "x": x,
                "prev_y": prev_y,
                "y": y
            })

            props.RunTestState[1](false)
        }else{

        }
    }


    function draw_line(){
        let line = Line ? Line.map(item =>
            item = item
        ) : []
        console.log("\ncalculations for drawing")
        console.log(Calculations)
        console.log(Color)
        line.push(
            <line
                x1={Calculations.prev_x}
                y1={Calculations.prev_y}
                x2={Calculations.x}
                y2={Calculations.y}
                stroke={Color}
                strokeWidth="2"
                key={props.Counter}
            />
        )
        setLine(line)
        setCalculations(null)
    }



  return (
    <div>
        <svg width={defaults.max_x} height={defaults.max_y}>
            {Line ? 
                Line.map(item =>
                    item  
                )
            : null}
        </svg>
    </div>
  )
}