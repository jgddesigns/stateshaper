'use client'
import {useEffect, useState} from "react"
import "./shapes.css"

export default function Home() {
  const [CurrentToken, setCurrentToken] = useState(0)
  const [OriginalToken, setOriginalToken] = useState(0)
  const [CurrentMap, setCurrentMap] = useState(0)
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
  const [ShapesData, setShapesData] = useState(null)
  const [Shapes, setShapes] = useState(null)
  const [Line, setLine] = useState(<svg></svg>)


  const grid_size = 25

  const colors = ["bg-red-400","bg-blue-400","bg-green-400","bg-yellow-400","bg-orange-400","bg-purple-400","bg-pink-400","bg-cyan-400","bg-lime-400","bg-teal-400","bg-emerald-400","bg-indigo-400"]
  const text = ["text-red-400","text-blue-400","text-green-400","text-yellow-400","text-orange-400","text-purple-400","text-pink-400","text-cyan-400","text-lime-400","text-teal-400","text-emerald-400","text-indigo-400"]

  const content = {
    "form" : setShowForm,
    "data" : setShowData,
    "about":  setShowAbout
  }


  useEffect(()=>{
    send_api("forward")
  }, [])


  useEffect(()=>{
    if(Data){
      console.log(Data) 
      set_seeds()
      change_map(0)
      setLine(draw_line())
      !OriginalToken ? setOriginalToken(Data["token"]) : null
      setCurrentToken(Data["token"])

    }
  }, [Data])


  useEffect(()=>{
    Seeds ? setSeedText(Seeds["0"]) : null
  }, [Seeds])


  useEffect(()=>{
    CurrentMap ? setChangeMap(true) : null
  }, [CurrentMap])


  useEffect(()=>{
    ShapesData ? draw_shapes() : null
  }, [ShapesData])




  function draw_shapes(){
    let shapes = []
    for(let item of ShapesData){
      if(item != ""){
        let shape_class = item["shape"] + " " + colors[item["color"]]  + " " + text[item["color"]] + " w-" + item["size"]["width"] + " h-" + item["size"]["height"] + " justify-self-center self-center select-none"
        shapes.push(shape_class)
      }else{
        shapes.push("w-32 h-64 justify-self-center self-center text-[#02082c] select-none")
      }
    }
    setShapes(shapes)
  }


  function set_shapes(){
    // let shapes = new_shapes()
    
    // for(let item of Object.keys(Data["shapes"])){
    //   shapes[get_pos(Data["shapes"][item]["pos"]["x"], Data["shapes"][item]["pos"]["y"])] = Data["shapes"][item]
    // }
    // setShapesData(shapes)
  }


  function new_shapes(){
    let shapes = []
    while(shapes.length < grid_size){
      shapes.push("")
    }
    return shapes
  }


  function get_pos(x, y){
    return ((x+1)*(y+1)) - 1
  }


  function show_content(show){
    let terms = ["form", "data", "about"]
    for(let i=0; i<terms.length; i++){
      content[terms[i]](show == terms[i] ? true : false)
    }
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
      body: JSON.stringify({ message: "" })
    });
    const data = await res.json()
    setData(data["response"])
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
    }catch{setMapData("")}
  }


  function map_text(map, data){
    return map == data ? "text-green-200 hover:text-green-300" : "hover:text-violet-200"
  }
 

  function draw_line(){
    return <svg width="400" height="400">
            <path
              d="M 20 100 Q 200 180 200 100"
              stroke="red"
              strokeWidth="2"
              fill="none"
            />
          </svg>
  }

  function run_session(){

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
          {ShowForm ?
          <div className="grid grid-rows-3 max-w-[800px] h-140 place-items-center overflow-y-auto mt-20 p-4 dot-scrollbar static" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div className="grid grid-rows-1 grid-cols-2 w-full text-xl mt-12 static">
              <div className="grid w-full grid-rows-2 grid-cols-1">
                <div>
                  <b>Car:</b>
                </div>   
                <div className="text-2xl text-blue-400 mt-4">
                  <i>{Data ? get_name(Data.test.vehicle.name) : null}</i>
                </div>
              </div>
              <div className="grid w-full grid-rows-2 grid-cols-1">
                <div className="grid grid-rows-1 grid-cols-2">
                  <div>
                    <b>Maps:</b> 
                  </div>
                </div>
                <div>
                  {Data ? MapText :null}
                </div>
              </div>
            </div>
            <div className="grid grid-rows-2 grid-cols-1 gap-24 w-full text-lg mt-150">
                <div className="grid w-full grid-rows-1 grid-cols-1 justify-self-start mt-auto top-0 static">
                  <b className="text-xl">Data:</b> <i></i>
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
              <div className="grid grid-rows-1 grid-cols-3 gap-4 w-full text-xl mr-auto mt-24">
                <div>
                  Derived From: 
                </div>
                <div>
                  {Data.token}
                </div>
                <div className="grid grid-rows-1 grid-cols-2 self-end right-0 ml-auto gap-8 px-8">
                    <div className={Data ? Data["token"] != OriginalToken ? "w-20 h-12 px-4 py-1 bg-blue-600 rounded-2xl cursor-pointer text-4xl hover:bg-gray-300 hover:text-blue-700" : "w-20 h-12 px-4 py-1 bg-gray-600 rounded-2xl cursor-none text-4xl" : null}>
                      &larr;
                    </div>
                    <div className="w-20 h-12 px-4 py-1 bg-blue-600 rounded-2xl cursor-pointer px-2 text-4xl hover:bg-gray-300 hover:text-blue-700">
                      &rarr;
                    </div>
                </div>
              </div>
            </div>
          </div>
          : 
          ShowData ?
          <div className="grid grid-rows-1 max-w-[800px] h-140 place-items-center overflow-y-auto mt-12 p-4 dot-scrollbar static" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
              <div className="mt-4 px-4 py-2 ml-auto w-24 h-12 bg-blue-900 rounded-lg text-xl text-white cursor-pointer hover:bg-blue-800" onClick={e => run_sesion()}>
                Begin
              </div>
              <div className="mt-12 w-180 h-100 bg-gray-200">
                  {Line}
              </div>
          </div>
          : 
          <div className="grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-[740px] gap-6 overflow-y-auto dot-scrollbar p-6 text-lg" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
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
        }
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
        <div className="text-white p-4 py-5 bottom-18 right-192 ml-auto absolute w-128 h-24 rounded-lg bg-blue-600">
        <div className="text-md ">
          <span className="font-bold">Github:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper/tree/graphics_demo" target="_blank">https://www.github.com/jgddesigns/stateshape/tree/ml_demo</a>
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