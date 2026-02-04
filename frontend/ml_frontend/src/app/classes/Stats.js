'use client'


// props: 
//  AttributeStates 
//  selected attribute states for graph drawing
export default function Stats(props) {
  const attributes = ["temperature","humidity","light","elevation","curves","road_size","road_texture","incline","traffic"]

  const colors = {
    "temperature": "#FF6B6B",      // pastel red
    "humidity": "#FFB6B9",         // soft pink
    "light": "#FFD6A5",            // pastel orange
    "elevation": "#FDFFB6",        // pastel yellow
    "curves": "#CAFFBF",           // pastel green
    "road_size": "#9BF6FF",        // pastel cyan
    "road_texture": "#A0C4FF",     // pastel blue
    "incline": "#66BB6A",          // pastel violet
    "traffic": "#FFC6FF",          // pastel magenta
  }




  function draw_data(data){
    let attributes = [...props.AttributeStates[0]]
    attributes.includes(data) == false ? attributes.push(data) : attributes.splice(attributes.indexOf(data), 1)
    props.AttributeStates[1](attributes)
  }


  function get_attributes() {
    // function from chat gpt
    const stats = [...attributes]
    const data = []

    const rowCols = [3, 3, 3] 
    const bottomRowItems = 3  

    rowCols.forEach((cols, rowIndex) => {
      const rowItems = []
      const itemsInRow =
        rowIndex === 2 ? bottomRowItems : cols 

      for (let i = 0; i < itemsInRow && stats.length; i++) {
        const item = stats.shift()
        rowItems.push(
          <div key={`item-${rowIndex}-${i}`} className="grid grid-rows-1 grid-cols-2 gap-28"> 
            <div
              className={props.AttributeStates[0].includes(item) == false && props.StartTest == false ? "cursor-pointer text-md text-white hover:text-green-200 select-none"  : props.StartTest == false ?  "cursor-pointer text-md font-bold text-green-300 hover:text-violet-300 select-none" : props.AttributeStates[0].includes(item) == false ? "text-md text-white disabled select-none cursor-default" : "text-md font-bold disabled select-none cursor-default"}
              onClick={props.StartTest == false ?  () => draw_data(item) : null}
              style={{ color:  props.AttributeStates[0].includes(item) == true && props.StartTest == true && colors[item]}}
            >
              {item}
            </div>
            <div>
              {props.DrawData && props.StartTest == true && props.AttributeStates[0].includes(item) == true ? isNaN(props.DrawData[item]) ? props.DrawData[item] : props.DrawData[item].toFixed(2) : null} 
            </div>
            
          </div>
        )
      }

      while (rowItems.length < cols) {
        rowItems.push(<div key={`empty-${rowIndex}-${rowItems.length}`} />)
      }

      data.push(
        <div
          key={`row-${rowIndex}`}
          className={`grid grid-rows-1 grid-cols-${cols} gap-22 place-items-center`}
        >
          {rowItems}
        </div>
      )
    })

    return <div className="grid grid-rows-3 w-4/5 ml-18 h-full place-items-center">{data}</div>
  }




  return (
    <div>
      {get_attributes()}
    </div>
  )
}