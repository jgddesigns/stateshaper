'use client'
import {useEffect, useState} from "react";


export default function Home() {
  const ad_count = 3

  const attributes_map = {
    "sports": 0,
    "writing": 0, 
    "fitness": 0,
    "movies": 0,
    "cooking": 0,
    "science": 0, 
    "travel": 0,
    "animals": 0, 
    "crafts": 0, 
    "history": 0,
  }

  const [Attributes, setAttributes] = useState(attributes_map)
  const [Data, setData] = useState("")
  const [Seeds, setSeeds] = useState("")
  const [Ads, setAds] = useState([])
  const [NewAds, setNewAds] = useState(false)
  const [Loaded, setLoaded] = useState(false)
  const [ShowInterests, setShowInterests] = useState(true)
  const [SeedText, setSeedText] = useState("")
  const classes = ["font-bold", ""]
  const [LinkText, setLinkText] = useState(classes[0])
  const [ShowExample, setShowExample] = useState(false)
  const [ShowCode, setShowCode] = useState(false)


  useEffect(()=>{
    send_api("start")
    setLoaded(true)
  }, [])


  useEffect(()=>{
    set_seeds()
  }, [Data])


  useEffect(()=>{
    setSeedText(Seeds["0"])
  }, [Seeds])


  useEffect(()=>{
    if(!NewAds){
      show_ads()
      setNewAds(true)
    }
  }, [NewAds])


  function seed_text(type){
    type == "0" ? setLinkText(classes[0]) : setLinkText(classes[1]) 
    setSeedText(Seeds[type])
  }


  function adjust_values(e){
    let value = e.target.value.replace(/[^0-9]/g, '') 
    parseInt(value) > 100 ? value = 100 : null
    parseInt(value) < 0 ? value = 0 : null
    document.getElementById(e.target.id).value = value
    let temp_arr = Attributes
    temp_arr[e.target.id] = value
    setAttributes(temp_arr)
  }


  function show_ads(){
    let temp_arr = Ads
    let new_arr = []
    let place = 0
    while(new_arr.length < ad_count){
      place = Math.floor(Math.random() * temp_arr.length)
      new_arr.push(temp_arr[place])
      temp_arr.splice(place, 1)
    }
    setAds(new_arr)
  }


  function show_interests(condition){
    setShowInterests(condition)
  }


  function full_seed(){
    return Data ? '["user_176551",' + JSON.stringify(Data) + ']' : ""
  }


  function short_seed(){
    return Data ? '["user_176551",' + JSON.stringify(Data["state"]) + ',' + JSON.stringify(Data["vocab"]) + ']' : ""
  }


  function tiny_seed(){
    return Data ? Data["vocab"][0] : ""
  }


  function raw_seed(){
    return Data ? Data["vocab"][1] : ""
  }


  function set_seeds(){
    setSeeds({"0" : [full_seed(), `~225 bytes`],
    "1" : [short_seed(), `~65 bytes`],
    "2" : [tiny_seed(),  `~` + tiny_seed().length + ` bytes`],
    "3" : [raw_seed(), `~` + raw_seed().length + ` bytes`]})
  }


  async function send_api(path) {
    const res = await fetch(`https://trypython.vercel.app/api/` + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: JSON.stringify(Attributes) })
    });

    const data = await res.json();
    setData(data.response["seed"])
    setNewAds(false)  
    setAds(data.response["ads"])
    setAttributes(data.response["ratings"])
  }


  return (
    <div className="flex grid grid-auto-rows dark:bg-black h-screen min-h-screen fixed bg-[#02082c]">
      <div className="grid grid-rows-1 place-items-center text-3xl mt-8 text-gray-200 font-bold">
        <div>
          Stateshaper Ads Demo
        </div>   
      </div>
      <div className="grid grid-cols-2 grid-rows-2 place-items-center h-4/5 mt-32 text-gray-200">
        <div className="grid gap-8 h-full static place-items-center">
          <div className="grid grid-rows-1 grid-cols-2 w-128 text-gray-200 text-xl cursor-pointer place-items-center">
            <a className={ShowInterests ? "font-bold" : ""} onClick={()=>show_interests(true)}>Ratings</a>
            <a className={!ShowInterests ? "font-bold" : ""} onClick={()=>show_interests(false)}>About</a>
          </div>
          {ShowInterests ?
          <div className="grid w-1/2 place-items-center">
            <div className="grid grid-auto-rows mt-4 gap-4">
              <div className="grid grid-cols-2">
                <div>
                  Sports
                </div>
              <textarea
                className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded"
                id="sports"
                defaultValue={Loaded && Attributes ? Attributes["sports"] : ""}
                onChange={(e) => adjust_values(e)}
              ></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Writing
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="writing" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["writing"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Fitness
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="fitness" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["fitness"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Movies
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="movies" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["movies"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Cooking
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="cooking" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["cooking"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Science
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="science" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["science"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Travel 
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="travel" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["travel"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Animals
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="animals" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["animals"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  Crafts
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="crafts" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["crafts"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                  History
                </div>
                <textarea className="bg-gray-200 h-8 resize-none overflow-y-hidden px-1 py-1 text-black rounded" id="history" onChange={e=>adjust_values(e)} defaultValue={Loaded && Attributes ? Attributes["history"] : ""}></textarea>
              </div>
              <div className="grid grid-cols-2">
                <div>
                </div>
                <button className="bg-blue-500 p-2 rounded text-white rounded cursor-pointer mt-4" onClick={()=>send_api("process")}>
                  Calculate
                </button>
              </div>
            </div>
          </div> :
          <div className="grid place-items-center grid-cols-1 grid-auto-rows w-1/2 gap-4">
            <div>
              Stateshaper can save storage space needed for many types of generated content. Personalized ads are one of the uses that can showcase this tool's ability. The primary reason space and bandwidth can be reduced is due to the fact that the program allows for data to easily be generated from a compressed seed in real-time. 
            </div>
            <div>
              This consumes very little computational resources and the installed package size is less than 1MB. All that is needed besides the main package is an app-specific plugin that can be tailored to the desired output. Stateshaper plugins are intended to take data (such as the ratings and ad images seen here), and compress it according to developer needs. Along the way, attributes can be adjusted based on variables such as user input or time of the year.
            </div>
            <div>
              Actual data storage size is cut all the way down to the Stateshaper seed formats shown on to the right. This can often account for over 90% reduction in space used, and also allows for privacy through obfuscation.
            </div>
            <div>
              Other uses can include, but are not limited to smart home scheduling, gaming npc behavior, fintech market data QA, ML training, and store inventories. 
            </div>
          </div>
        }
        </div>
        <div className="grid w-3/4 place-items-center h-full static">
          <div className="grid grid-rows-1 grid-cols-3 gap-24">
            <img className="w-36 h-36" src={Ads ? Ads[0] : "images/001.png"}/>
            <img className="w-36 h-36" src={Ads ? Ads[1] : "images/002.png"}/>
            <img className="w-36 h-36" src={Ads ? Ads[2] : "images/003.png"}/>
          </div>
          <div className="grid grid-auto-rows mt-12">
            <div className="text-bold text-lg">
              Seed State Format
            </div>
            <div className="italic mt-4">
              Once a profile is created, most associated data is compressed into Seed State format. Attributes can be adjusted over time to change the output. 
            </div>
            <div className="grid grid-rows-1 grid-cols-4 place-items-center cursor-pointer text-gray-200 mt-8">
              <a id="0" className={LinkText} onClick={(e) => seed_text(e.target.id)}>
                Full State
              </a>
              <a id="1" className="hover:font-bold" onMouseOver={(e) => seed_text(e.target.id)} onMouseOut={(e) => seed_text("0")}>
                Short State
              </a>
              <a id="2" className="hover:font-bold" onMouseOver={(e) => seed_text(e.target.id)} onMouseOut={(e) => seed_text("0")}>
                Tiny State
              </a>
              <a id="3" className="hover:font-bold" onMouseOver={(e) => seed_text(e.target.id)} onMouseOut={(e) => seed_text("0")}>
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
              A <i>Stateshaper</i> seed can be compressed even further into Tiny or Raw State format. This can shrink data such as JSON dictionaries containing attributes for personalization or arrays of image or video links. These formats can be decoded using the State Decoder tool, state-decoder. 
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
        <div className="text-white p-4 py-5 bottom-18 right-192 ml-auto absolute w-128 h-24 rounded-lg bg-blue-600">
        <div className="text-md ">
          <span className="font-bold">Frontend:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper/tree/ads_demo" target="_blank">https://www.github.com/jgddesigns/stateshape/tree/ads_demo</a>
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