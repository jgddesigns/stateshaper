'use client'
import {useEffect, useState} from "react"


// props: Value, PreviousValue, Counter, Y_Interval, RunTestState
export default function Draw(props) {
    const [Line, setLine] = useState(null)
    const [Calculations, setCalculations] = useState(null)
    const [X_Interval, setX_Interval] = useState(7.19)
    const [PreviousValue, setPreviousValue] = useState(400)
    const [CurrentValue, setCurrentValue] = useState(0)
    const [Color, setColor] = useState("red")



    useEffect(()=>{
        try{
           props.X_Interval ? setX_Interval(props.X_Interval) : null
        }catch{}
        
        try{
            props.Color ? setColor(props.Color) : null
        }catch{}
        setLine(null)
    }, [])


    useEffect(()=>{
        props.RunTestState[0] == true && props.Counter <= 100 ? calculate() : null
    }, [props.RunTestState])


    useEffect(()=>{
        Calculations != null ? draw_line() : null
    }, [Calculations])


    function calculate(){
        console.log("counter")
        console.log(props.Counter)
        console.log("value")
        console.log(props.Value)

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
        <svg width="725" height="400">
            {Line ? 
                Line.map(item =>
                    item  
                )
            : null}
        </svg>
    </div>
  )
}