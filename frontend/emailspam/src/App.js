import { useEffect, useRef, useState } from "react";
import  './App.css'

function App() {
  const [mail,setmail]=useState("");
  const strid=useRef(false);


  const handlechange=(e)=>{
    setmail(e.target.value);
  }



  const checkspam=async()=>{

  const senddata =await fetch('https://email-spam.vercel.app/',
    {
      method:"POST",
      headers: {
        "Content-Type": "application/json",
      },
      body:JSON.stringify({mail})
    })
   const responsedata=await senddata.json();
   console.log(responsedata);
   console.log(responsedata.hamspam);
   if(responsedata.hamspam=='[1]')
   {
    console.log("njs");
    strid.current=true;

   } 
   else 
   {
    strid.current=false;
   }
  }

  

  return(
    <div className="email-container">
      <div>
       <textarea className="textarea" 
                 placeholder='Enter Your Mail Message'
                 rows={15}
                 cols={50}
                 value={mail}
                 onChange={handlechange}
             />
              <div>
              <button id='checkbtn'onClick={checkspam}>Check the Mail</button>
              </div>
              <p>
                  {strid?"SPAM MAIL":"NOT SPAM MAIL"}
              </p>
       </div>
    </div>
  )
}

export default App;
