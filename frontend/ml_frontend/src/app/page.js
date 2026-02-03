'use client'
import {useEffect, useState} from "react"
import "./shapes.css"
import Draw from "./classes/Draw"
import Stats from "./classes/Stats"

export default function Home() {
  const defaults = {}
  const [DrawValue, setDrawValue] = useState(0)
  const [DrawColor, setDrawColor] = useState("red")
  const [DrawData, setDrawData] = useState("red")
  const [PreviousDrawValue, setPreviousDrawValue] = useState(0)
  const [RunTest, setRunTest] = useState(false)
  const [TestTrigger, setTestTrigger] = useState(false)
  const [X_Interval, setX_Interval] = useState(10)
  const [Counter, setCounter] = useState(-1)
  const [CurrentToken, setCurrentToken] = useState(0)
  const [OriginalToken, setOriginalToken] = useState(0)
  const [MapData, setMapData] = useState(0)
  const [MapText, setMapText] = useState("")
  const [Data, setData] = useState("")
  const [Seeds, setSeeds] = useState("")
  const [ShowForm, setShowForm] = useState(true)
  const [ShowAbout, setShowAbout] = useState(false)
  const [ShowData, setShowData] = useState(false)
  const [ShowExample, setShowExample] = useState(false)
  const [ShowCode, setShowCode] = useState(false)
  const [SeedText, setSeedText] = useState("")
  const classes = ["font-bold", ""]
  const [LinkText, setLinkText] = useState(classes[0])
  const [ReceiveTrip, setReceiveTrip] = useState(false)
  const [LoadedTrip, setLoadedTrip] = useState(true)
  const [Pause, setPause] = useState(false)
  const [StartTest, setStartTest] = useState(false)
  const [DisplayCreated, setDisplayCreated] = useState(false)
  const attributes = ["temperature","humidity","light","elevation","curves","road_size","road_texture","incline","traffic","potential_hazard","weather_type"]
  const [SelectedAttributes, setSelectedAttributes] = useState([attributes[0]])
  const [DrawClasses, setDrawClasses] = useState([<Draw Value={DrawValue} PreviousValue={PreviousDrawValue} Counter={Counter} Color={DrawColor} RunTestState={[RunTest, setRunTest]}/>])
                  // <Draw Value={DrawValue} PreviousValue={PreviousDrawValue} Counter={Counter} Color={DrawColor} RunTestState={[RunTest, setRunTest]}/>
  const content = {
    "form": setShowForm,
    "data": setShowData,
    "about": setShowAbout
  }


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
  "potential_hazard": "#8E7BC8", // soft coral
  "weather_type": "#FFC75F"      // light peach
}


  useEffect(()=>{
    send_api("start")
    get_attributes()
  }, [])


  useEffect(()=>{
    if(TestTrigger == true){
      setRunTest(true)
      setTestTrigger(false)
      StartTest == false ? setStartTest(true) : null
    } 
  }, [TestTrigger])


  useEffect(()=>{
    if(Data){
      set_seeds()
      change_map(0)
      !OriginalToken ? setOriginalToken(Data["token"]) : null
      setCurrentToken(Data["token"])
      setX_Interval(Data.test.environment[0].range[1]/100)
      initialize_draw()
    }
  }, [Data])


  useEffect(()=>{
    ReceiveTrip == true ? adjust_trip() : null
  }, [ReceiveTrip])


  useEffect(()=>{
    Seeds ? setSeedText(Seeds["0"]) : null
  }, [Seeds])


  useEffect(()=>{
    while(StartTest == true && Counter < 100){
      const timeoutId = setTimeout(() => {
          if(Pause != true){ 
            run_session()
          }
      }, 500)

      return () => clearTimeout(timeoutId)
    }
  }, [StartTest, Counter])


  function draw_value(value){
    if(value < 1){
      value = value * 100
    }
    return 400 - value
  }


  function show_content(show){
    let terms = ["form", "data", "about"]
    for(let i=0; i<terms.length; i++){
      content[terms[i]](show == terms[i] ? true : false)
    }
    // show == "data" ? redraw() : null
  }


  function full_seed(){
    return Data ? '["user_176551",' + JSON.stringify(Data["seed"][0]) + ']' : ""
  }


  function short_seed(){
    return Data ? '["user_176551",' + JSON.stringify(Data["seed"][0]["s"]) + ']' : ""
  }


  function tiny_seed(){
    return "N/A"
  }


  function raw_seed(){
    return "N/A"
  }


  function seed_text(type){
    type == "0" ? setLinkText(classes[0]) : setLinkText(classes[1]) 
    setSeedText(Seeds[type])
  }


  function set_seeds(){
    setSeeds({"0" : [full_seed(), full_seed().length + ` bytes`],
    "1" : [short_seed(), short_seed().length + ` bytes`],
    "2" : [tiny_seed(),  ``],
    "3" : [raw_seed(), ``]})
  }


  async function send_api(path) {
    // const res = await fetch(`https://stateshaper-ml-backend.vercel.app/api/` + path, {
    const res = await fetch("http://localhost:8000/api/" + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: JSON.stringify({"token": 1, "environment": Data ? Data.test.environment : []}) })
    });
    const data = await res.json()
    
    if(path != "trip" && path != "reset"){
      setData(data.response)
      setDrawData(data.response.test.environment[0].data)
    }

    if(path == "trip"){
      setDrawData(data.response.test.data)
      setReceiveTrip(true)
    }   

    if(path == "reset"){
      setLoadedTrip(true)
    }   

    console.log("data in " + path)
    console.log(data.response)
  }


  function get_name(name){
    name = name.split("_")
    let string = ""
    for(let word of name){
      string = string + capitalize(word) + " "
    }
    string = string.slice(0, string.length-1)
    return string
  }


  function capitalize(word){
    return word[0].toUpperCase() + word.slice(1)
  }


  function get_range(range){
    return range[0].toString().length > 1 ? range[0] + " - " + range[1] : range[0] + "  - " + range[1]
  }


  function change_map(current){
    try{
      reset_trip()
      setX_Interval(Data.test.environment[current].range[1]/100)
      setDrawData(Data.test.environment[current].data)
      setMapText(Data.test.environment.map((item, i) => (
        <div className="grid grid-cols-2 gap-8" key={i}>
          <div className="flex items-center cursor-pointer z-99" onClick={e => change_map(i)}>
          <div className={map_text(Data.test.environment[current].environment, item.environment)}>{item.environment}</div>
          </div>
          <div className="font-mono whitespace-pre flex items-center">
            mi. {get_range(item.range)}
          </div>
        </div>
      )))
      setMapData(Object.keys(Data.test.environment[current].data).map((item, i) => (
        <div className="grid w-full grid-rows-1 grid-cols-2 gap-8 text-lg" key={i}>
          <div>
            {get_name(item)}
          </div>
          <div className={!Data.test.environment[current].data[item].toString().includes(".") ? "whitespace-pre italic" : "whitespace-pre"}>
            {Data.test.environment[current].data[item]}
          </div>
        </div>
      )))
    }catch{
      setMapData("")
    }
  }


  function map_text(map, data){
    return map == data ? "text-green-200 hover:text-green-300" : "hover:text-violet-200"
  }
 

  function run_session(){
    Counter == 0 ? setCounter(1) : null
    Counter < 100 ? send_api("trip") : null
  }


  function adjust_trip(){
    setReceiveTrip(false)
    let counter = Counter
    // let value = DrawValue
    counter++

    // counter % 2 == 0 ? value-=Math.round((Math.random() * 20)) : counter % 3 == 0 ? value+=Math.round((Math.random() * 70)) : value-=Math.round((Math.random() * 15))
    setCounter(counter)
    console.log("\ndraw data in adjust trip")
    console.log(DrawData)
    try{
      setDrawValue(draw_value(DrawData[SelectedAttributes[0]]))
      console.log("\ndraw value set")
      console.log(SelectedAttributes[0])
      console.log(draw_value(DrawData[SelectedAttributes[0]]))
    }catch{
      console.log("\nunable to set draw value")
    }
    
    setTestTrigger(true)
  }

    
  function reset_trip(){
    setLoadedTrip(false)
    setReceiveTrip(false)
    setCounter(-1)
    setDrawValue(null)
    setTestTrigger(false)
    setStartTest(false)
    send_api("reset")
  }
  

  function initialize_draw(){
    setDrawValue(draw_value(DrawData.temperature))
    setPreviousDrawValue(draw_value(DrawData.temperature))
  }


  function get_attributes() {
    // function from chat gpt
    const stats = [...attributes]
    const data = []

    const rowCols = [4, 4, 4] 
    const bottomRowItems = 3  

    rowCols.forEach((cols, rowIndex) => {
      const rowItems = []
      const itemsInRow =
        rowIndex === 2 ? bottomRowItems : cols 

      for (let i = 0; i < itemsInRow && stats.length; i++) {
        const item = stats.shift()
        rowItems.push(
          <div
            key={`item-${rowIndex}-${i}`}
            className={SelectedAttributes.includes(item) == false ? "cursor-pointer text-md text-white hover:text-green-200"  : "cursor-pointer text-md font-bold text-green-300 hover:text-violet-200"}
            onClick={() => draw_data(item)}
          >
            {item}
          </div>
        )
      }

      while (rowItems.length < cols) {
        rowItems.push(<div key={`empty-${rowIndex}-${rowItems.length}`} />)
      }

      data.push(
        <div
          key={`row-${rowIndex}`}
          className={`grid grid-rows-1 grid-cols-${cols} gap-8`}
        >
          {rowItems}
        </div>
      )
    })

    return <div className="grid grid-rows-3 w-full h-full">{data}</div>
  }



  function draw_display(){
    let classes = []
    let data = null

    
    for(let value of SelectedAttributes){
      data = {
        "value": null,
        "prev_value": null,
        "counter": null,
        "color": null,
      }
      data.value = draw_value(DrawData[value])
      data.prev_value = draw_value(DrawData[value])
      data.counter = Counter
      data.color = colors[value]

      // classes.push(<div key={classes.length}><Draw Value={data.value} PreviousValue={data.prev_value} Counter={data.counter} Color={data.color} RunTestState={[RunTest, setRunTest]}/></div>)
      classes.push(data)
    }
    console.log("\ndraw classes")
    console.log(classes)
    // setDisplayCreated(true)
    return classes
  }



  return (
    <div className="flex grid grid-auto-rows dark:bg-black h-screen min-h-screen fixed bg-[#02082c] font-mono">
      <style>
        {`
          .dot-scrollbar::-webkit-scrollbar {
            width: 12px;
          }
          .dot-scrollbar::-webkit-scrollbar-track {
            background: transparent;
          }
          .dot-scrollbar::-webkit-scrollbar-thumb {
            background-color: gray;
            border-radius: 50%;
            border: 3px solid transparent;
          }
          .dot-scrollbar::-webkit-scrollbar-thumb:hover {
            background-color: gray;
          }
        `}
      </style>
      <div className="grid grid-rows-1 place-items-center text-3xl mt-8 text-gray-200 font-bold">
        <div>
          Stateshaper ML Training Demo
        </div>   
      </div>
      <div className="grid grid-cols-2 grid-rows-2 place-items-center h-4/5 mt-32 text-gray-200 min-w-full tatic">
        <div className="grid gap-8 h-full static place-items-center">
          <div className="grid grid-rows-1 grid-cols-3 w-128 text-gray-200 text-xl cursor-pointer place-items-center">
            <a className={ShowForm ? "font-bold text-2xl" : ""} onClick={()=>show_content("form")}>Trip</a>
            <a className={ShowData ? "font-bold text-2xl" : ""} onClick={()=>show_content("data")}>Run</a>
            <a className={ShowAbout ? "font-bold text-2xl" : ""} onClick={()=>show_content("about")}>About</a>
          </div>
          <div>
            <div className={ShowForm ? "grid grid-rows-3 max-w-[800px] h-140 place-items-center overflow-y-auto mt-20 p-4 dot-scrollbar static" : "hidden"} style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
              <div className="grid grid-rows-1 grid-cols-3 gap-4 w-full text-xl mr-auto mt-24">
                <div>
                  Derived From: 
                </div>
                <div>
                  {Data.token}
                </div>
                <div className="grid grid-rows-1 grid-cols-2 self-end right-0 ml-auto gap-8 px-8">
                    <button className={Data ? Data["token"] != OriginalToken ? "w-20 h-12 px-4 py-1 bg-blue-600 rounded-2xl cursor-pointer text-4xl hover:bg-gray-300 hover:text-blue-700 select-none z-99" : "disabled select-none w-20 h-12 px-4 py-1 bg-gray-600 rounded-2xl cursor-none text-4xl" : null} onClick={e => send_api("reverse")} disabled={Data ? Data["token"] == OriginalToken : false}>
                      &larr;
                    </button>
                    <button className="w-20 h-12 px-4 py-1 bg-blue-600 rounded-2xl cursor-pointer px-2 text-4xl hover:bg-gray-300 hover:text-blue-700 select-none z-99"  onClick={e => send_api("forward")}>
                      &rarr;
                    </button>
                </div>
              </div>
            <div className="grid grid-rows-1 grid-cols-2 w-full h-24 text-xl mt-36 static">
              <div className="grid w-full grid-rows-2 grid-cols-1">
                <div>
                  <b>Car:</b>
                </div>   
                <div className="text-blue-400 text-2xl mt-4">
                  <i>{Data ? get_name(Data.test.vehicle.name) : null}</i>
                </div>
              </div>
              <div className="grid w-full grid-rows-2 grid-cols-1">
                <div className="grid grid-rows-1 grid-cols-2">
                  <div>
                    <b>Maps:</b> 
                  </div>
                </div>
                <div className="mt-4">
                  {Data ? MapText :null}
                </div>
              </div>
            </div>
            <div className="grid grid-rows-2 grid-cols-1 gap-24 w-full text-lg mt-36">
                <div className="grid w-full grid-rows-1 grid-cols-1 justify-self-start mt-auto top-0 static">
                  {/* <b className="text-xl">Data:</b> <i></i> */}
                </div>
                <div className="grid grid-rows-1 grid-cols-2">
                  <div>
                    {Data ? Object.keys(Data.test.vehicle).map((item, i) => (
                      <div key={i}>
                        {i > 0 ?
                        <div className="grid w-full grid-rows-1 grid-cols-2 gap-8">
                          <div>
                            {capitalize(item)}
                          </div>
                          <div className="whitespace-pre">
                            {Data.test.vehicle[item]}
                          </div>
                        </div>
                        : null}
                      </div>
                    )):null}
                  </div>
                  <div>
                    {Data ? MapData : null}
                  </div>
                </div>
            </div>
            </div>
            <div className={ShowData ? "grid grid-rows-3 max-w-[800px] h-150 place-items-center overflow-y-auto  p-4 dot-scrollbar static gap-28" : "hidden"} style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>

                {/* <div className="w-full h-full" dangerouslySetInnerHTML={{ __html: get_attributes() }} /> */}
                <div>
                  {/* {get_attributes()} */}
                  <Stats AttributeStates={[SelectedAttributes, setSelectedAttributes]} StartTest={StartTest} Counter={Counter}/>
                </div>

                

              <div className="mt-12 w-180 h-100 bg-gray-400">
                {LoadedTrip && DrawClasses ? 
                  // <Draw Value={DrawValue} PreviousValue={PreviousDrawValue} Counter={Counter} Color={DrawColor} RunTestState={[RunTest, setRunTest]}/>
                  <div>
                    {Data ? draw_display().map((data, i) => (
                      <Draw Value={data.value} PreviousValue={data.prev_value} Counter={data.counter} Color={data.color} RunTestState={[RunTest, setRunTest]} key={i}/>
                    )) : null}
                  </div>
                : null}
              </div>
              <div className={Counter < 100 ? "mt-16 px-4 py-2 ml-auto w-32 h-12 bg-blue-900 rounded-lg text-xl text-white cursor-pointer hover:bg-blue-800 select-none" : "mt-16 px-3 py-2 ml-auto w-32 h-12 bg-gray-600 rounded-lg text-xl text-white cursor-none disabled select-none"}  onClick={e => run_session()}>
                {Counter < 100 ? "Run Test" : "Finished!"}
              </div>
            </div>
            <div className={ShowAbout ? "grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-[740px] gap-6 overflow-y-auto dot-scrollbar p-6 text-lg" : "hidden"} style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
          {/* <div className="grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-[740px] gap-6 overflow-y-auto dot-scrollbar p-6 text-lg" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}> */}
            <div>
              An unlimited amount of training data for machine learning can be created and stored using <i>Stateshaper</i>. The ability for the engine to derive synthetic data by tokenizing its numeric output allows for a wide range of test values to be used. Each test can be stored and re-created at any time from the small seed formats seen to the right of the screen. 
            </div>
            <div>  
              If the test variations created aren't good enough, output can be adjusted in the plugin file by using the current token as a base to derive test values from. This particular example shows how <i>Stateshaper</i> can be used to run road simulations to help train the AI in self-driving cars. Theoretically, all possible test scenarios can be brute-force tested based on the deterministic nature of the program. If needed, the parameter values for the main class and corresponding plugin file can be modified for a particular use.
            </div>
            <div>
              Once run, these tests can be stored using almost no space. Any simulation can be revisited at any time. Consider that one prototype for a self-driving car may have several versions. Each version created can have millions of possible AI training sessions conducted before the car begins testing on the road. The data needed for this can take up many terabytes of space. Storing this data can be important for many reasons such as further research, version comparison, and regulatory reasons to name a few. Using <i>Stateshaper</i> in this case can reduce database related costs in this instance by over 99%. This includes storage, bandwidth and electricity consumption. 
            </div>
            <div>
              ML Training is only one of the many uses for this program. It is currently available as a Python package and Github repository. 
            </div>
            <div className="mt-8 grid grid-cols-1 gap-4 grid-rows-2 place-items-center">
              <code>pip install stateshaper</code>
              <a className="underline hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper" target="_blank">https://www.github.com/jgddesigns/stateshaper</a>
            </div>
            <div className="mt-4">
              Other uses can include, but are not limited to, smart home scheduling, gaming NPC behavior, content generation, graphic assets and store inventories. 
            </div>
            </div>
          </div>

        </div>

        <div className="grid w-3/4 place-items-center h-full static">
          <div className="grid grid-auto-rows mt-12">
            <div className="text-bold text-lg">
              Seed State Format
            </div>
            <div className="italic mt-4">
              Once a profile is created, the student profile and study plan is compressed into Seed State format. The quiz questions adjust over time based on the student's answers. 
            </div>
            <div className="grid grid-rows-1 grid-cols-4 place-items-center cursor-pointer text-gray-200 mt-8">
              <a id="0" className={LinkText} onClick={(e) => seed_text(e.target.id)}>
                Full State
              </a>
              <a id="1" className="hover:font-bold hover:text-gray-300 cursor-pointer" onMouseOver={(e) => seed_text(e.target.id)} onMouseOut={(e) => seed_text("0")}>
                Short State
              </a>
              <a id="2" className="hover:font-bold hover:text-gray-300 cursor-pointer" onMouseOver={(e) => seed_text(e.target.id)} onMouseOut={(e) => seed_text("0")}>
                Tiny State
              </a>
              <a id="3" className="hover:font-bold hover:text-gray-300 cursor-pointer" onMouseOver={(e) => seed_text(e.target.id)} onMouseOut={(e) => seed_text("0")}>
                Raw State
              </a>
            </div>
            <div className="grid grid-rows-2 grid-cols-1 gap-8 w-3/4 h-32 min-h-32 static mt-8 bold text-gray-700 p-4 rounded bg-gray-200">
              <code>
                {SeedText ? SeedText[0] : ""}
              </code>
              <code className="mt-3">
                {SeedText ? SeedText[1] : ""}
              </code>
            </div>
            <div className="italic mt-8">
              The above strings are all that is needed to generate a student's profile. For sensitive data, some values can be stored in environment variables. Tiny State and Raw State format are not required for this type of use because no personalized data is selected from the original dataset. 
            </div>
            <div className="italic mt-8">
              For other applications, a plugin file is required to coordinate Stateshaper output with the app's frontend and backend logic. Some plugins will be released along with the package. Custom plugins can also be written. 
            </div>
          </div>

        </div>
      </div>
      <div className={!ShowCode ? "text-white text-2xl hover:font-bold bottom-6 right-192 ml-auto absolute hover:text-gray-300 cursor-pointer" : "text-2xl font-bold bottom-6 right-192 ml-auto absolute text-gray-300 cursor-pointer"} onMouseEnter={e=>setShowCode(true)} onClick={e=>setShowCode(false)}>
        CODE
      </div>
      <div className="text-white text-2xl hover:font-bold bottom-6 right-12 ml-auto absolute hover:text-gray-300 cursor-pointer" onMouseEnter={e=>setShowExample(true)} onMouseLeave={e=>setShowExample(false)}>
        EXAMPLE ONLY
      </div>
      <div className={!ShowCode ? "text-white text-2xl hover:font-bold bottom-6 right-192 ml-auto absolute hover:text-gray-300 cursor-pointer" : "text-2xl font-bold bottom-6 right-192 ml-auto absolute text-gray-300 cursor-pointer"} onMouseEnter={e=>setShowCode(true)} onClick={e=>setShowCode(false)}>
        CODE
      </div>
      <div className="text-white text-2xl hover:font-bold bottom-6 right-12 ml-auto absolute hover:text-gray-300 cursor-pointer" onMouseEnter={e=>setShowExample(true)} onMouseLeave={e=>setShowExample(false)}>
        EXAMPLE ONLY
      </div>
      {ShowCode ?
        <div className="text-white p-4 py-5 bottom-18 right-192 ml-auto absolute w-128 h-24 rounded-lg bg-blue-600 overflow-x-auto overflow-y-hidden">
        <div className="text-md ">
          <span className="font-bold">Github:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic px-2" href="https://www.github.com/jgddesigns/stateshaper/tree/graphics_demo" target="_blank">https://www.github.com/jgddesigns/stateshaper/tree/ml_demo</a>
        </div>
        </div>
      : null}
      {ShowExample ?
        <div className="text-white p-4 bottom-18 right-12 ml-auto absolute w-128 h-24 rounded-lg bg-blue-600">
        <div className="text-lg font-bold">
          Sample app, real logic. 
        </div>
        <div className="text-md mt-2">
          Intended to showcase the tool's capabilities.
        </div>
        </div>
      : null}
    </div>
  )
}