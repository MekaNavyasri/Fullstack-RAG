import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const api = axios.create({
    baseURL: "http://localhost:8000",
})

function QuestionForm() { 
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    // const [url, setUrl] = useState("");
    const [isLoading, setIsLoader] = useState(false);

    const handleSubmit = async(e) => {
        setIsLoader(true);
        e.preventDefault();
        console.log("Your Question:", question);
        const response = await api.post("/chat", { message: question });
        setAnswer(response.data.answer);
        setIsLoader(false);
    }

    const handleIndex = async(e) => {
        setIsLoader(true);
        e.preventDefault();
        console.log("Your url:", question);
        const response = await api.post("/indexing", { message: question });
        setAnswer(response.data.response);
        setIsLoader(false);
    }
    
    return ( 
    <div>
        <form>
            <input type="text" value={question} onChange={(e)=>setQuestion(e.target.value)}/>
            <button type="submit" onClick={handleSubmit}>Q&A</button>
            <button type="submit" style={{backgroundColor: '#61dafb'}} onClick={handleIndex}>Index</button>
        </form>
        {isLoading && <p>Loading...</p>}
        <div>
            <h2>Answer:</h2>
            <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
    </div>
    );
}

export default QuestionForm;