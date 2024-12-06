
import './App.css';
import Chatbot from './components/Chatbot';

function App() {
  
  return (
  <div className='flex flex-col justify-center p-10 h-[100%]'>
    <h1 className='text-stone-950 text-center text-4xl font-semibold' >LLM Comparison</h1>
    <div className='h-full w-full flex justify-between gap-4'>
          <Chatbot  llm_name="LLM"  /> 
          <Chatbot  llm_name="Improved LLM"/> 
    </div>
   
  
    
  </div>
  );
}

export default App;


