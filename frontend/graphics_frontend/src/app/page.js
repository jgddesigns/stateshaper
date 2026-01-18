'use client'
import {useEffect, useState} from "react"
import "./shapes.css"

export default function Home() {
  const [CurrentToken, setCurrentToken] = useState(0)
  const [OriginalToken, setOriginalToken] = useState(0)
  const [Data, setData] = useState("")
  const [Seeds, setSeeds] = useState("")
  const [ShowForm, setShowForm] = useState(true)
  const [ShowAbout, setShowAbout] = useState(false)
  const [ShowExample, setShowExample] = useState(false)
  const [ShowCode, setShowCode] = useState(false)
  const [SeedText, setSeedText] = useState("")
  const classes = ["font-bold", ""]
  const [LinkText, setLinkText] = useState(classes[0])
  const [ShapesData, setShapesData] = useState(null)
  const [Shapes, setShapes] = useState(null)


  const grid_size = 25

  const colors = ["bg-red-400","bg-blue-400","bg-green-400","bg-yellow-400","bg-orange-400","bg-purple-400","bg-pink-400","bg-cyan-400","bg-lime-400","bg-teal-400","bg-emerald-400","bg-indigo-400"]
  const text = ["text-red-400","text-blue-400","text-green-400","text-yellow-400","text-orange-400","text-purple-400","text-pink-400","text-cyan-400","text-lime-400","text-teal-400","text-emerald-400","text-indigo-400"]

  const content = {
    "form" : setShowForm,
    "about":  setShowAbout
  }


  useEffect(()=>{
    send_api("forward")
  }, [])


  useEffect(()=>{
    if(Data){
      set_seeds()
      set_shapes()
      !OriginalToken ? setOriginalToken(Data["token"]) : null
      setCurrentToken(Data["token"])

    }
  }, [Data])


  useEffect(()=>{
    Seeds ? setSeedText(Seeds["0"]) : null
  }, [Seeds])


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
    let shapes = new_shapes()
    
    for(let item of Object.keys(Data["shapes"])){
      shapes[get_pos(Data["shapes"][item]["pos"]["x"], Data["shapes"][item]["pos"]["y"])] = Data["shapes"][item]
    }
    setShapesData(shapes)
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
    let terms = ["form", "about", "tests"]
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
    const res = await fetch(`https://stateshaper-graphics-backend.vercel.app/api/` + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "" })
    });
    const data = await res.json()
    setData(data["response"])
  }



  return (
    <div className="flex grid grid-auto-rows dark:bg-black h-screen min-h-screen fixed bg-[#02082c]">
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
          Stateshaper Graphics Demo
        </div>   
      </div>
      <div className="grid grid-cols-2 grid-rows-2 place-items-center h-4/5 mt-32 text-gray-200 min-w-full tatic">
        <div className="grid gap-8 h-full static place-items-center">
          <div className="grid grid-rows-1 grid-cols-2 w-128 text-gray-200 text-xl cursor-pointer place-items-center">
            <a className={ShowForm ? "font-bold text-2xl" : ""} onClick={()=>show_content("form")}>Draw</a>
            <a className={ShowAbout ? "font-bold text-2xl" : ""} onClick={()=>show_content("about")}>About</a>
          </div>
          {ShowForm ?
          <div className="grid max-w-[800px] h-140 place-items-center  overflow-y-auto mt-20 p-4 dot-scrollbar static" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div className="ml-auto px-12 grid grid-cols-3 grid-rows-1 max-w-[750px] gap-34 place-items-center mr-10">
              <div className={OriginalToken == CurrentToken ? "w-28 h-12 bg-gray-600 text-black rounded px-5 py-3 cursor-none mr-auto disabled select-none" : "w-28 h-12 bg-blue-600 text-white rounded px-5 py-3 cursor-pointer hover:text-gray-300 mr-auto select-none"} onClick={OriginalToken != CurrentToken ? ()=>send_api("reverse") : null}>
                Prior Map
              </div>
              <div className="grid grid-cols-1 grid-rows-2 place-items-center">
                <div className="">
                  Derived From
                </div>
                <div className="mt-1">
                    {CurrentToken}
                </div>
              </div>
              <div className="w-28 h-12 bg-blue-600 text-white rounded px-5 py-2 cursor-pointer grid-rows-1 grid-cols-2 hover:text-gray-300 ml-auto select-none" onClick={e=>send_api("forward")}>
                <div>
                  Next Map 
                </div>
                <div className="text-2xl justify-self-center mt-[-12px]">
                  {'\u{221E}'}
                </div>
              </div>
            </div>
            {Shapes ?
              <div className="grid grid-rows-5 grid-cols-1 mt-24 max-w-[700px] p-4 self-start gap-32">
                {Array.from({ length: 5 }).map((_, index) => {
                  const start = index * 5
                  const row_shapes = Shapes.slice(start, start + 5)
                  return (
                    <div
                      key={index}
                      className="grid grid-rows-1 grid-cols-5 gap-4 min-w-[600px] h-32 place-items-center"
                    >
                      {row_shapes.map((shape, cols) => (
                        <div key={cols} className={shape}>
                          {shape}
                        </div>
                      ))}
                    </div>
                  )
                })}
              </div>
            : null}
          </div>
          : 
          <div className="grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-[740px] gap-6 overflow-y-auto dot-scrollbar p-6 text-lg" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div>
              Implementing <i>Stateshaper</i> here allows for graphics to be drawn on the screen by using the token output to derive each graphic's attributes. This is a basic example that can be expanded upon up to the most detailed textures needed (such as modern video games or CGI). The key here is that this can be done from just a few bytes of memory. The limits are only what the GPU can handle and how detailed the code is. The output is not literally infinite (based on mathematical rules) but can come close depending on how large of a mod value is set.
            </div>
            <div>  
              Potentially, an entire map can be built using these methods without storing any of the sprites in static memory. The graphics can be seemingly random, or mapped exactly as needed depending on the token output from <i>Stateshaper</i>. For more detailed applications, the token output can be modified within the package's source code by altering its morph function or passing custom class parameters. This can also be achieved within the methods written in the plugin file connecting to a specific app.
            </div>
            <div>
              Once a plugin file is written that defines rules for the graphics, the values can be passed into your application and used to generate on-screen content. The plugin file can be easily connected to the Stateshaper engine and used to generate your data at any time. Examples for creating a plugin like this can be found in the <i>Stateshaper</i> GitHub repository:
            </div>
            <div className="mt-4 underline">
              <a className="hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper" target="_blank">https://www.github.com/jgddesigns/stateshaper</a>
            </div>
            <div className="mt-4">
              Other uses can include, but are not limited to, smart home scheduling, gaming NPC behavior, content generation, ML training, and store inventories. 
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
      {ShowCode ?
        <div className="text-white p-4 bottom-18 right-192 ml-auto absolute w-128 h-36 rounded-lg bg-blue-600">
        <div className="text-md ">
          <span className="font-bold">Frontend:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper_graphics_frontend" target="_blank">https://www.github.com/jgddesigns/stateshaper_graphics_frontend</a>
        </div>
        <div className="text-md mt-2">
          <span className="font-bold">Backend:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper_graphics_backend" target="_blank">https://www.github.com/jgddesigns/stateshaper_graphics_backend</a>
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