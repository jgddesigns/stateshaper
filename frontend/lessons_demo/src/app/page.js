'use client'
import {useEffect, useState} from "react"
import {v4 as uuid} from "uuid"

export default function Home() {
  const API = process.env.REACT_APP_API_URL;


  const [Attributes, setAttributes] = useState("")
  const [Ratings, setRatings] = useState("")
  const [Data, setData] = useState("")
  const [Seeds, setSeeds] = useState("")
  const [Answers, setAnswers] = useState([])
  const [NewAds, setNewAds] = useState(false)
  const [Loaded, setLoaded] = useState(false)
  const [InBetween, setInBetween] = useState(false)
  const [ShowInterests, setShowInterests] = useState(true)
  const [ShowAbout, setShowAbout] = useState(false)
  const [ShowExample, setShowExample] = useState(false)
  const [ShowCode, setShowCode] = useState(false)
  const [ShowRatings, setShowRatings] = useState(false)
  const [Score, setScore] = useState(null)
  const [SeedText, setSeedText] = useState("")
  const classes = ["font-bold", ""]
  const [LinkText, setLinkText] = useState(classes[0])

  const selected = "font-bold h-9 w-23 border-4 border-blue-300 "

  const total_questions = 10

  const content = {
    "interests" : setShowInterests,
    "about":  setShowAbout,
    "ratings": setShowRatings
  }

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
    // let temp_arr = Ads
    // let new_arr = []
    // let place = 0
    // while(new_arr.length < ad_count){
    //   place = Math.floor(Math.random() * temp_arr.length)
    //   new_arr.push(temp_arr[place])
    //   temp_arr.splice(place, 1)
    // }
    // setAds(new_arr)
  }


  function show_content(show){
    let terms = ["interests", "ratings", "about"]
    for(let i=0; i<terms.length; i++){
      content[terms[i]](show == terms[i] ? true : false)
    }
    
  }


  function full_seed(){
    return Data ? '["user_176551",' + JSON.stringify(Data[1]) + ']' : ""
  }


  function short_seed(){
    return Data ? '["user_176551",' + JSON.stringify(Data[1]["state"]) + ',' + JSON.stringify(Data[0]["v"]) + ']' : ""
  }


  function tiny_seed(){
    return Data ? Data[0]["v"][0] : ""
  }


  function raw_seed(){
    return Data ? Data[0]["v"][1] : ""
  }


  function set_seeds(){
    setSeeds({"0" : [full_seed(), `~225 bytes`],
    "1" : [short_seed(), `~65 bytes`],
    "2" : [tiny_seed(),  `~` + tiny_seed().length + ` bytes`],
    "3" : [raw_seed(), `~` + raw_seed().length + ` bytes`]})
  }


  async function send_api(path) {
    const res = await fetch(`https://stateshaper-lessons-backend.vercel.app/api/` + path, {
    // const res = await fetch("http://localhost:8000/api/" + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: JSON.stringify(Answers) })
    });

    const data = await res.json();
    console.log(data)
    setData(data.response["seed"])
    setNewAds(false)  
    setAttributes(data.response["questions"])
    setRatings(data.response["ratings"])
    setAnswers([])
  }

  function process_answer(item, answer, id){
    let answers = Answers 

    for (let i=0; i<answers.length; i++){
      answers[i]["question"] == item ? answers.splice(i, 1) : null
      
    }

    document.getElementById(id).className = selected + document.getElementById(id).className 
    if(answer == true){
      id = id.replace("true", "false")
      document.getElementById(id).className = document.getElementById(id).className.replace(selected, "")
    }else{
      id = id.replace("false", "true")
      document.getElementById(id).className = document.getElementById(id).className.replace(selected, "")
    }
    answers.push({"question": item, "answer": Attributes[parseInt(id.split("_")[0])]["answer"] == answer ? true : false})
    setAnswers(answers)
  }

  function process_finish(){
    if(Answers.length < total_questions){
      console.log("please answer all the questions")
    }else{
      setInBetween(true)
      const count = Answers.reduce((c, item) => c + (item["answer"] === true), 0);
      setScore(count + " out of " + Answers.length)
      console.log(count)
      send_api("process")
    }
  }

  function after_finish(){
    setInBetween(false)
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
          Stateshaper Personal Lesson Plans Demo
        </div>   
      </div>
      <div className="grid grid-cols-2 grid-rows-2 place-items-center h-4/5 mt-32 text-gray-200">
        <div className="grid gap-8 h-full static place-items-center">
          <div className="grid grid-rows-1 grid-cols-3 w-128 text-gray-200 text-xl cursor-pointer place-items-center">
            <a className={ShowInterests ? "font-bold text-2xl" : ""} onClick={()=>show_content("interests")}>Current Quiz</a>
            <a className={ShowRatings ? "font-bold text-2xl" : ""} onClick={()=>show_content("ratings")}>Ratings</a>
            <a className={ShowAbout ? "font-bold text-2xl" : ""} onClick={()=>show_content("about")}>About</a>
          </div>
          {ShowInterests ?
          <div className="grid w-full h-140 place-items-center overflow-y-auto mt-20 p-4 dot-scrollbar" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div className="grid grid-auto-rows mt-4 gap-12 mt-8 text-xl">
              {Attributes && !InBetween ? Attributes.map(item => (
                <div key={Attributes.indexOf(item)} className="grid grid-rows-2 grid-cols-1">
                  <div>{item["question"]}</div>
                  <div className="grid grid-cols-2 grid-rows-1 w-1/2 gap-4 ml-[15%] mt-2">
                    <div id={Attributes.indexOf(item) + "_true"} className="w-22 h-8 bg-green-400 rounded text-white text-xl px-5 cursor-pointer" onClick={e=> process_answer(item, true, e.target.id)}>True</div>
                    <div id={Attributes.indexOf(item) + "_false"} className="w-22 h-8 bg-red-400 rounded text-white text-xl px-5 cursor-pointer" onClick={e=> process_answer(item, false, e.target.id)}>False</div>
                  </div> 
                </div>
              ))
              : <div className="text-white text-3xl flex justify-center">
                  <span>{Score ? Score : null}</span>
                </div>
              }
              {!InBetween ? 
                <div className="w-22 h-8 bg-blue-400 rounded text-white text-xl flex justify-center cursor-pointer static bottom-2 ml-auto" onClick={e=> process_finish()}>Finish</div>
              : 
                <div className="w-22 h-8 bg-blue-400 rounded text-white text-xl flex justify-center cursor-pointer static ml-6" onClick={e=> after_finish()}>Proceed</div>       
              }
            </div>
          </div> : ShowRatings ?
          <div className="grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-full gap-4 overflow-y-auto dot-scrollbar p-4 text-lg" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div className="italic">The quiz questions are derived from these attributes.</div>
            <div className="italic"> Attributes change based on performance.</div>
            <div className="grid grid-auto-rows mt-4 gap-12 mt-12 text-xl">
              {Ratings ? Ratings.map(item => (
                <div key={Ratings.indexOf(item)} className="grid grid-rows-1 grid-cols-2 gap-18">
                  <li>{item["attribute"]}</li>
                  <span>{item["rating"]}</span>
                </div>
              ))
              : null}
            </div>
          </div>
          :
          <div className="grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-3/5 gap-6 overflow-y-auto dot-scrollbar p-6 text-lg" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div>
              This <i>Stateshaper</i> demo shows how an entire user profile can be condensed into a 50-225 byte seed. Here we'll use an example of a student's personalized lesson plan from a biology class. The example uses sets of 10 study questions from a bank of 100 possible choices. 
            </div>
            <div>  
              When a student shows aptitude in a certain areas, those type of questions are phased out of the question set over time. If a student struggles in a particular area, more of those questions will be added over time based on preferences derived from ratings. Additionally, the student's all-time performance can also be compressed into a similar size and reviewed at any time. 
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
              The above strings are all that is needed to generate a student's profile. For sensitive data, some values can be stored in environment variables. 
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
        <div className="text-white p-4 py-5 bottom-18 right-192 ml-auto absolute w-128 h-24 rounded-lg bg-blue-600">
        <div className="text-md ">
          <span className="font-bold">Frontend:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper/tree/lessons_demo" target="_blank">https://www.github.com/jgddesigns/stateshape/tree/lessons_demo</a>
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
  );
}
