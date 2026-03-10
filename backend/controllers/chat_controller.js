import axios from "axios";

const AI_URL = process.env.AI_URL || "http://localhost:5001";


export async function chatWithAssistant(req, res) {
    try {
        const { message, session_id } = req.body;

        switch(true) {
            case (typeof message !== "string"):
                return res.status(400).json({ message: "message must be a string." });

            case (message.trim() === ""):
                return res.status(400).json({ message: "message is required." });
        }

        const aiResponse = await axios.post(`${AI_URL}/api/feature-3/chat`, {message, session_id});

        return res.status(200).json(aiResponse.data);
    } 
    catch (error) {
        console.error(`Error in chatWithAssistant controller: ${error}`);
        return res.status(500).json({message: "Failed to get response from AI assistant."});
    }
}