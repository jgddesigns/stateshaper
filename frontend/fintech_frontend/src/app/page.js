'use client'
import {useEffect, useState} from "react"


export default function Home() {
  const [CurrentDrift, setCurrentDrift] = useState(0)
  const [CurrentToken, setCurrentToken] = useState(0)
  const [OriginalToken, setOriginalToken] = useState(0)
  const [Data, setData] = useState("")
  const [Seeds, setSeeds] = useState("")
  const [StartingBalance, setStartingBalance] = useState(50000)
  const [CurrentBalance, setCurrentBalance] = useState(50000)
  const [AccountsNumber, setAccountsNumber] = useState(1)
  const [StockValue, setStockValue] = useState(0)
  const [TransferValue, setTransferValue] = useState(0)
  const [DepositValue, setDepositValue] = useState(0)
  const [WithdrawValue, setWithdrawValue] = useState(0)
  const [ExpectedDrift, setExpectedDrift] = useState(0)
  const [BillValue, setBillValue] = useState(0)
  const [IncludedTransactions, setIncludedTransactions] = useState([])
  const [Result, setResult] = useState("PASS")
  const [ShowForm, setShowForm] = useState(true)
  const [ShowTests, setShowTests] = useState(false)
  const [ShowAbout, setShowAbout] = useState(false)
  const [ShowExample, setShowExample] = useState(false)
  const [ShowCode, setShowCode] = useState(false)
  const [SeedText, setSeedText] = useState("")
  const classes = ["font-bold", ""]
  const [LinkText, setLinkText] = useState(classes[0])

 


  const content = {
    "form" : setShowForm,
    "about":  setShowAbout,
    "tests": setShowTests
  }


  const transactions = {
    "accounts": setAccountsNumber,
    "stock": setStockValue,
    "transfer": setTransferValue,
    "deposit": setDepositValue,
    "withdraw": setWithdrawValue,
    "bill": setBillValue
  }


  useEffect(()=>{
    send_api("forward")
  }, [])


  useEffect(()=>{
    if(Data){
      reset_deposits()
      set_seeds()
      assign_tests(Data["test"]["transactions_list"])
      setIncludedTransactions(get_transactions(Data["test"]["transactions_list"]))
      setCurrentToken(Data["test_token"])
      test_data()
      Data && !OriginalToken ? setOriginalToken(Data["test_token"]) : null
    }
  }, [Data])


  useEffect(()=>{
    setSeedText(Seeds["0"])
  }, [Seeds])


  function assign_tests(included){
    for(let test of Object.keys(included)){
      transactions[test](included[test])
      calculate_funds(test, included[test])
    }
  }


  function reset_deposits(){
    for(let value of Object.keys(transactions)){
      value != "accounts" ? transactions[value](0) : null
    }
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
    const res = await fetch(`https://stateshaper-qa-backend.vercel.app/api/` + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "" })
    });
    const data = await res.json();
    setData(data["response"])
    setAccountsNumber(parseInt(data["response"]["test"]["accounts_generated"]))
    setStartingBalance(parseFloat(data["response"]["test"]["starting_total"]))
    setCurrentBalance(parseFloat(data["response"]["test"]["starting_total"]))
  }


  function get_transactions(transactions){
    let included = ""

    for(let item of Object.keys(transactions)){
      included = included + item
      Object.keys(transactions).indexOf(item) != Object.keys(transactions).length-1 ? included = included + ", " : null
    }

    return included
  }


  function calculate_funds(id, value){
    let balance = CurrentBalance
    let drift = Data["test_token"] % 3 == 0 ? (((Data["test_token"] + parseInt(Data["test_token"].toString()[0])) % 100)/100) : 0 
    drift == 0 ? setResult("PASS") : setResult("FAIL")
    balance = ((balance + (parseFloat(value) * AccountsNumber)))
    
    if(Math.round(Data["test"]["starting_total"] + Data["test_token"]) % 3 == 0){
      drift = 0 - drift
      setCurrentBalance(balance + drift)
      setCurrentDrift(drift)
    }else{
      setCurrentBalance(balance + drift)
      setCurrentDrift(drift)
    }
  }


  function transactions_string(){
    let string = `{\n` 
    let end = ""
    for(let item of Object.keys(Data["test"]["transactions_list"])){
      Object.keys(Data["test"]["transactions_list"]).indexOf(item) != Object.keys(Data["test"]["transactions_list"]).length - 1 ? end = `,\n` : end = `\n`
      string = string + `        \"` + item + `\": ` + JSON.stringify(Data["test"]["transactions_list"][item]) + end
    }
    string = string + `    }`
    JSON.stringify(Data["test"]["transactions_list"])
    return string
  }


  function test_data(){
    return "{\n" +
        "    \"accounts_generated\": " + Data["test"]["accounts_generated"] + ",\n" +
        "    \"transactions_executed\": " + Data["test"]["transactions_executed"] + ",\n" +
        "    \"starting_total\": " + Data["test"]["starting_total"] + ",\n" +
        "    \"ending_total\": " + CurrentBalance.toFixed(2) + ",\n" +
        "    \"total_difference\": " + (parseFloat(CurrentBalance) - parseFloat(StartingBalance)).toFixed(2) + ",\n" +
        "    \"total_expected\": " + (parseFloat(CurrentBalance) - parseFloat(StartingBalance) + CurrentDrift).toFixed(2) + ",\n" +
        "    \"net_drift\": " + CurrentDrift.toFixed(2) + ",\n" +
        "    \"expected_drift\": " + ExpectedDrift.toFixed(2) + ",\n" +
        "    \"assertion_result\": " + Result + ",\n" +
        "    \"transactions_list\": " + transactions_string() + "\n" +
        "}"
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
          Stateshaper Systems QA Testing Demo
        </div>   
      </div>
      <div className="grid grid-cols-2 grid-rows-2 place-items-center h-4/5 mt-32 text-gray-200">
        <div className="grid gap-8 h-full static place-items-center">
          <div className="grid grid-rows-1 grid-cols-3 w-128 text-gray-200 text-xl cursor-pointer place-items-center">
            <a className={ShowForm ? "font-bold text-2xl" : ""} onClick={()=>show_content("form")}>Form Data</a>
            <a className={ShowTests ? "font-bold text-2xl" : ""} onClick={()=>show_content("tests")}>Test Data</a>
            <a className={ShowAbout ? "font-bold text-2xl" : ""} onClick={()=>show_content("about")}>About</a>
          </div>
          {ShowForm ?
          <div className="grid w-4/5 h-140 place-items-center overflow-y-auto mt-20 p-4 dot-scrollbar" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div className="grid grid-auto-rows mt-4 gap-8 text-xl">
              <div className="ml-auto px-12 grid grid-cols-3 grid-rows-1 w-full">
                <div className={OriginalToken == CurrentToken ? "w-28 h-12 bg-gray-600 text-black rounded px-4 py-3 text-lg cursor-none mr-auto disabled select-none" : "w-28 h-12 bg-blue-600 text-white rounded px-4 py-3 text-lg cursor-pointer hover:text-gray-300 mr-auto select-none"} onClick={OriginalToken != CurrentToken ? e=>send_api("reverse") : null}>
                  Prior Test
                </div>
                <div className="grid grid-cols-1 grid-rows-2 place-items-center">
                  <div className="">
                    Derived From
                  </div>
                  <div className="mt-1">
                     {CurrentToken}
                  </div>
                </div>
                <div className="w-28 h-12 bg-blue-600 text-white rounded px-4 py-1 text-lg cursor-pointer grid-rows-2 grid-cols-1 hover:text-gray-300 ml-auto select-none" onClick={e=>send_api("forward")}>
                  <div>
                    Next Test 
                  </div>
                  <div className="text-2xl justify-self-center mt-[-12px]">
                    {'\u{221E}'}
                  </div>
                </div>
              </div>
              <div className="grid grid-rows-4 grid-cols-1 mt-8 text-xl">
                <div className="grid grid-cols-2 grid-rows-1">
                  <div className="grid grid-cols-2 grid-rows-1 gap-4">
                    <div>
                      Starting Balance:
                    </div>
                    <div>
                      $ {StartingBalance.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                    </div>
                  </div>
                  <div className="grid grid-cols-2 grid-rows-1 gap-4">
                    <div>
                      Current Balance:
                    </div>
                    <div>
                      $ {CurrentBalance.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                    </div>
                  </div>
                </div>
                <div className="grid grid-cols-2 grid-rows-1">
                  <div className="grid grid-cols-1 grid-rows-1">
                    <div className="grid grid-cols-2 grid-rows-1 gap-4">
                      <div>
                        Difference:
                      </div>
                      <div>
                        $ {(parseFloat(CurrentBalance) - parseFloat(StartingBalance) + CurrentDrift).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 grid-rows-1 gap-4">
                      <div>
                        Expected:
                      </div>
                      <div>
                        $ {(parseFloat(CurrentBalance) - parseFloat(StartingBalance)).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                      </div>
                    </div>
                  </div>
        
                  <div className="grid grid-cols-1 grid-rows-1">
                    <div className="grid grid-cols-2 grid-rows-1 gap-4">
                      <div className={CurrentDrift != 0 ? "text-red-400" : ""}>
                        Current Drift:
                      </div>
                      <div className={CurrentDrift != 0 ? "text-red-400" : ""}>
                        $ {CurrentDrift.toFixed(2)}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 grid-rows-1 gap-4">
                      <div>
                        Expected Drift:
                      </div>
                      <div>
                        $ {ExpectedDrift.toFixed(2)}
                      </div>
                    </div>
                  </div>
              </div>
                <div className="grid place-items-center ml-auto px-8">
                  <div className="grid grid-cols-2 grid-rows-1 gap-4 w-full">
                    <div className={CurrentDrift != 0 ? "text-red-400" : "text-green-400"}>
                      Result:
                    </div>
                    <div className={CurrentDrift != 0 ? "text-red-400" : "text-green-400"}>
                      {Result}
                    </div>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-2 grid-rows-1 mt-8 place-items-center w-3/5 ml-24">
                <div>
                  Number of Accounts: 
                </div>
                <div className="text-white mr-auto ml-12 px-4" id="accounts">{AccountsNumber ? AccountsNumber : 1}</div>
              </div>
              <div className="grid grid-cols-2 grid-rows-1 place-items-center w-3/5 h-12 ml-24">
                <div>
                  Included Transactions: 
                </div>
                <div className="text-white ml-12 w-96 max-w-full overflow-x-auto whitespace-nowrap border-none px-4 mr-auto" id="included">{IncludedTransactions}</div>
              </div>
              {DepositValue != 0 ?
                <div className="grid grid-rows-1 grid-cols-1 mt-12 gap-12 mt-8 text-xl h-12 static">
                  <div className="grid grid-cols-2 w-72 static">
                    <div>
                      Deposit:
                    </div>
                    <div>$ {DepositValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div> 
                  </div>
                </div>
              : null}
              {WithdrawValue != 0 ?
                <div className="grid grid-rows-1 grid-cols-1 mt-12 gap-12 mt-8 text-xl h-12 static">
                  <div className="grid grid-cols-2 w-72 static">
                    <div>
                      Withdraw:
                    </div>
                    <div>$ {WithdrawValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                  </div>
                </div>
              : null}
              {TransferValue != 0 ?
                <div className="grid grid-rows-1 grid-cols-1 mt-12 gap-12 mt-8 text-xl h-12 static">
                  <div className="grid grid-cols-2 w-72 static">
                    <div>
                      Transfer:
                    </div>
                    <div>$ {TransferValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                  </div>
                </div>
              : null}
              {StockValue != 0 ?
                <div className="grid grid-rows-1 grid-cols-1 mt-12 gap-12 mt-8 text-xl h-12 static">
                  <div className="grid grid-cols-2 w-72 static">
                    <div>
                      Trade Stock:
                    </div>
                    <div>$ {StockValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                  </div>
                </div>
              : null}
              {BillValue != 0 ?
                <div className="grid grid-rows-1 grid-cols-1 mt-12 gap-12 mt-8 text-xl h-12 static">
                  <div className="grid grid-cols-2 w-72 static">
                    <div>
                      Pay Bill:
                    </div>
                    <div>$ {BillValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                  </div>
                </div> 
              :null}
            </div>
          </div> : ShowTests ?
          <div className="grid h-140 mt-20 grid-cols-1 w-5/4 gap-24 overflow-y-auto dot-scrollbar p-6 text-lg static" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div className="grid grid-rows-2 gap-4">
              <div className="text-xl underline">
                Original
              </div>
              <div className="mt-[-30%]">
                <pre>{test_data()}</pre>
              </div>
            </div>
          </div>
          :
          <div className="grid place-items-center h-140 mt-20 grid-cols-1 grid-auto-rows w-4/5 gap-6 overflow-y-auto dot-scrollbar p-6 text-lg" style={{scrollbarWidth: 'thin', scrollbarColor: 'gray transparent'}}>
            <div>
              This <i>Stateshaper</i> demo shows how QA (quality assurance) test results can be stored using very little memory. Only mock values are used, and are intended to depict the flow of systems testing for a fintech app. The output is not literally infinite (based on mathematical rules) but can come close depending on how large of a mod value is set. In software QA, the intent is look for bugs by trying to break the code that is written. This is done by stressing the system using any and all combinations of functions and possible values.
            </div>
            <div>  
              Sometimes millions of tests sessions are ran during an app's lifespan. There are many reasons someone may want to revisit these tests. Storing this much data can amount to terrabytes or more of space. When <i>Stateshaper</i> is used, all of these tests can be recreated from a string with a size of only a few bytes. At $100-$400 to store 1 TB per month, the savings amount to over 99% of the original cost. Based on this fact, using Stateshaper is THE BEST way to save money in this type of situation. 
            </div>
            <div>
              This use is very easy to implement, and requires almost no refactoring. All that is needed is a plugin file to define rules for the tests within your source code. Once this file is written, it can be connected to the Stateshaper engine and be used to generate your data at any time. Examples for creating a plugin like this can be found in the <i>Stateshaper</i> Github repository:
            </div>
            <div className="mt-4 underline">
              <a className="hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper" target="_blank">https://www.github.com/jgddesigns/stateshaper</a>
            </div>
            <div className="mt-4">
              Other uses can include, but are not limited to smart home scheduling, gaming npc behavior, content generation, ML training, and store inventories. 
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
          <span className="font-bold">Frontend:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper_qa_frontend" target="_blank">https://www.github.com/jgddesigns/stateshaper_qa_frontend</a>
        </div>
        <div className="text-md mt-2">
          <span className="font-bold">Backend:</span> <a className="cursor-pointer hover:text-gray-300 hover:italic" href="https://www.github.com/jgddesigns/stateshaper_qa_backend" target="_blank">https://www.github.com/jgddesigns/stateshaper_qa_backend</a>
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