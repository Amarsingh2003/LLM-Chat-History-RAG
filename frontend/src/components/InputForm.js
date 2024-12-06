

import { useState, useEffect } from "react";
import useFetch from "../hooks/useFetch";

const InputForm = ({ addDiv, addResult, messagesLength, isLoading, llm_name }) => {
    const [query, setQuery] = useState("");
    const [currentQuery, setCurrentQuery] = useState(null);

    // Use the hook at the component level
    const { data, error } = useFetch(
        llm_name === 'LLM' 
            ? 'http://127.0.0.1:5000/get_response'
            : 'http://127.0.0.1:5000/get_improved_response',
        currentQuery
    );

    // Handle the response when data or error changes
    useEffect(() => {
        console.log("inside use effect")
    
        if (currentQuery && (data || error)) {
            console.log("inside cond")
            console.log(data)
            if (data === null) {
                addResult(error, messagesLength);
            } else {
                console.log("inside input form")
                console.log(data)
                addResult(data, messagesLength);
            }
            setCurrentQuery(null); // Reset current query
        }
    }, [data, error]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        if (isLoading) {
            alert("Please wait for the previous response before sending a new query.");
            return;
        }

        addDiv(query);
        setCurrentQuery(query); // Set the current query to trigger the fetch
        setQuery(""); // Clear input field after submission
    };

    return (
        <div className="h-full w-full p-3">
            <form className="flex content-stretch h-full w-full gap-4" onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Type your message here..."
                    className="w-[85%] pl-2 border-solid border-gray-600 border rounded-lg"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isLoading}
                />
                <div className={`w-[10%] border-solid border-gray-600 border rounded-lg ${isLoading ? 'bg-gray-500' : 'bg-black'}`}>
                    <button
                        type="submit"
                        className="w-[100%] h-[100%] flex justify-center items-center"
                        disabled={isLoading}
                    >
                        <p className="text-center text-white">Send</p>
                    </button>
                </div>
            </form>
        </div>
    );
};

export default InputForm;

