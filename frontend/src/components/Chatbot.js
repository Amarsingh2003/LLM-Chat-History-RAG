

import { useState, useEffect, useRef } from "react";
import InputForm from "./InputForm";
import user_logo from '../images/user_logo.jpg';
import bot_logo from '../images/bot_logo.jpg'

const Chatbot = ({llm_name}) => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false); // Add loading state
    const scrollRef = useRef(null); // Reference to the scrollable container

    const addResult = (response, index) => {
        setMessages(prevMessages => {
            const newMessages = [...prevMessages];
            if (newMessages[index-1]) {
                newMessages[index-1] = {
                    ...newMessages[index-1],
                    response: response,
                    thinking: false
                };
            }
            // if (index >= 0 && index < newMessages.length && newMessages[index]) {
            //     newMessages[index] = {
            //         ...newMessages[index],
            //         response: response,
            //         thinking: false
            //     };
            // } else {
            //     console.error("Invalid index:", index);
            // }
            console.log("inside add Result")
            console.log(response)
            console.log(index)
            console.log(newMessages)
            return newMessages;
        });
        setIsLoading(false); // Set loading to false when response is received
    };

    const addDiv = (query) => {
        setIsLoading(true); // Set loading to true when new query is added
        setMessages(prevMessages => [...prevMessages, {
            query: query,
            thinking: true,
            response: null
        }]);
    };

    // Scroll to the bottom whenever messages change
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="flex flex-col h-full w-full mt-4">
            <h2 className="p-4 text-center text-2xl font-semibold text-gray-600">{llm_name}</h2>
            <div
                ref={scrollRef} // Attach the ref to the scrollable container
                className="h-[85%] w-full border-solid border-x-[1px] border-t-[1px] border-gray-400 p-2 overflow-y-scroll"
            >
                {messages.map((message, index) => (
                    <div key={index} className="mb-2">
                        <div className="p-1 flex justify-end gap-2">
                            <div className="border-black bg-gray-400 inline-block rounded-md">
                                <p className="text-md p-[6px]">{message.query}</p>
                            </div>
                            <img src={user_logo} alt="user logo" className="h-8 w-8" />
                        </div>

                        <div className="p-1 flex justify-start gap-2">
                            <img src={bot_logo} alt="user logo" className="h-8 w-8" />
                            <div className="border-black bg-gray-400 inline-block rounded-md">
                                <p className="text-md p-[6px]">
                                    {message.thinking ? 'thinking...' : message.response}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="h-[15%] w-full border-solid border-[1px] border-gray-400 rounded-b-lg">
                <InputForm 
                    addDiv={addDiv} 
                    addResult={addResult} 
                    messagesLength={messages.length}
                    isLoading={isLoading} // Pass loading state to InputForm
                    llm_name={llm_name}
                />
            </div>

        </div>
    );
}

export default Chatbot;