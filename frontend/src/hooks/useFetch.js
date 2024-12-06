

import { useState, useEffect } from "react";

const useFetch = (url, userQuery) => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            if (!url || !userQuery) return;

            setError(null);

            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: userQuery }),
                });

                if (!res.ok) {
                    const errorData = await res.json().catch(() => null);
                    throw new Error(errorData?.error || `HTTP error! Status: ${res.status}`);
                }

                const json = await res.json();
                if (json && typeof json.response === 'string') {
                    
                    setData(json.response);
                    // console.log("Response data:", json.response);
                    console.log(json.response)
                    console.log("inside console.log")
                    console.log(data)
                } else {
                    throw new Error("Invalid response format");
                }
            } catch (err) {
                setError(err.message);
                console.error("Fetch error:", err);
            }
        };

        fetchData();
    }, [url, userQuery]);

    return { data, error };
};

export default useFetch;
