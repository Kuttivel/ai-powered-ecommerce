import axios from "axios";

const AI_URL = process.env.AI_URL || "http://localhost:5001";

export async function chatWithAssistant(req, res) {
    try {
        const { message, session_id } = req.body;

        switch (true) {
            case typeof message !== "string":
                return res.status(400).json({ message: "message must be a string." });
            case message.trim() === "":
                return res.status(400).json({ message: "message is required." });
        }

        const aiResponse = await axios.post(`${AI_URL}/api/feature-3/chat`, {
            message: message.trim(),
            session_id,
        });

        return res.status(200).json(aiResponse.data);
    }
    catch (error) {
        const service_message = error.response?.data?.message;
        console.error("Error in chatWithAssistant controller", service_message || error.message);

        res.status(500).json({
            message: service_message || "Unable to get response from AI service.",
        });
    }
}