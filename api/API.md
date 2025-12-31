# *API CONNECTOR*

The API Connector has been designed for use with apps using the *Stateshaper* engine to create personalized content. It works in conjunction with the *RunEngine* class. This is the main class used to build and run the engine. It includes the *Connector* class and any plugin classes if needed. Any data from these can be passed into te API. Here is an example:



run = RunEngine()


```python
# the return values can be anything from the plugin file. in this case output is the current token list, ratings are the values the determine what is shown on screen, and seed is an the string value of the compressed data.
@app.post("/api/start")
def process():
    output = run.plugin.get_data()
    run.connector = Connector(output)
    run.run_engine()
    return {"response": {"output": output, "ratings": run.plugin.interests, "seed": run.seed}}
```


```python
# the same as above, but here input is what data is received by the api from the front end.
@app.post("/api/process")
def process(input: Input):
    input = json.loads(input.message)
    clean_input(input)
    new_data = run.plugin.change_data(input)
    run.connector = Connector(new_data)
    run.run_engine()
    return {"response": {"output": new_data, "ratings": run.plugin.interests, "seed": run.seed}}
```



Connecting these to the front end is fairly simple. The connector just needs to have a place to run the server. Once the backend is running, these items can be accessed with a fetch command in the front end (here using React.js): 


```javascript
  async function send_api(path) {
    const connect_api = await fetch(`https://yourserver.app/api/` + path, { //assuming yourserver.app is where the backend exists and api folder is in ROOT
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: JSON.stringify(InputData)}) //only needed when data is sent to backend
    });

    const incoming_data = await connect_api.json();
    
    //set state variables with the received data
    setData(incoming_data.response)
    setSeed(incoming_data.response["seed"])
    setQuestions(incoming_data.response["questions"])
    setRatings(incoming_data.response["ratings"])
    setAPICalled(true)
  }
```
