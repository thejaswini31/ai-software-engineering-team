import { useState } from "react";
import api from "../services/api";

function Chat() {

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");

    const askQuestion = async () => {

        try {

            const token =
                localStorage.getItem(
                    "token"
                );

            const response =
                await api.post(
                    `/chat?question=${question}`,
                    {},
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                );

            setAnswer(
                response.data.answer
            );

        } catch (error) {

            console.log(error);

            alert(
                "Failed to get answer"
            );
        }
    };

    return (

        <div>

            <h1>
                AI PDF Chat
            </h1>

            <input
                type="text"
                placeholder="Ask question..."
                value={question}
                onChange={(e) =>
                    setQuestion(
                        e.target.value
                    )
                }
            />

            <br />
            <br />

            <button
                onClick={askQuestion}
            >
                Ask AI
            </button>

            <br />
            <br />

            <h3>
                Answer:
            </h3>

            <p>
                {answer}
            </p>

        </div>

    );
}

export default Chat;